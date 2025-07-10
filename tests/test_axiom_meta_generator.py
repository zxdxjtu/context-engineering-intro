#!/usr/bin/env python3
"""
Test suite for axiom-meta-generator.py
Tests the core functionality of metadata generation and management.
"""

import os
import sys
import tempfile
import shutil
import yaml
import pytest
from pathlib import Path

# Add the scripts directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from axiom_meta_generator import AxiomMetaGenerator


class TestAxiomMetaGenerator:
    """Test suite for AxiomMetaGenerator class."""
    
    def setup_method(self):
        """Set up test environment with temporary directory."""
        self.test_dir = tempfile.mkdtemp()
        self.generator = AxiomMetaGenerator(self.test_dir)
        
    def teardown_method(self):
        """Clean up temporary directory."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def create_test_file(self, relative_path: str, content: str = "# Test file\nprint('hello')\n"):
        """Create a test file with given content."""
        file_path = Path(self.test_dir) / relative_path
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content)
        return file_path
    
    def test_init_axiom_structure(self):
        """Test initialization of .axiom directory structure."""
        self.generator.init_axiom_structure()
        
        # Check that directories were created
        assert (Path(self.test_dir) / ".axiom").exists()
        assert (Path(self.test_dir) / ".axiom" / "meta").exists()
        assert (Path(self.test_dir) / ".axiom" / "cache").exists()
        assert (Path(self.test_dir) / ".axiom" / "index.yml").exists()
        
        # Check index.yml content
        with open(Path(self.test_dir) / ".axiom" / "index.yml", 'r') as f:
            index = yaml.safe_load(f)
        
        assert index['version'] == '1.0'
        assert 'project_context' in index
        assert 'file_categories' in index
        assert 'meta_files' in index
    
    def test_should_track_file(self):
        """Test file tracking logic."""
        # Should track Python files
        py_file = self.create_test_file("test.py")
        assert self.generator.should_track_file(py_file)
        
        # Should track JavaScript files
        js_file = self.create_test_file("test.js")
        assert self.generator.should_track_file(js_file)
        
        # Should not track hidden files
        hidden_file = self.create_test_file(".hidden")
        assert not self.generator.should_track_file(hidden_file)
        
        # Should not track node_modules
        nm_file = self.create_test_file("node_modules/package.js")
        assert not self.generator.should_track_file(nm_file)
        
        # Should track important config files
        readme_file = self.create_test_file("README.md")
        assert self.generator.should_track_file(readme_file)
    
    def test_estimate_tokens(self):
        """Test token estimation for different file types."""
        # Test Python file
        py_file = self.create_test_file("test.py", "def hello():\n    print('world')\n")
        tokens = self.generator.estimate_tokens(py_file)
        assert tokens > 0
        
        # Test larger file should have more tokens
        large_py_file = self.create_test_file("large.py", "# Large file\n" * 100)
        large_tokens = self.generator.estimate_tokens(large_py_file)
        assert large_tokens > tokens
    
    def test_determine_file_type(self):
        """Test file type determination."""
        # Test module file
        py_file = self.create_test_file("module.py")
        assert self.generator.determine_file_type(py_file) == "module"
        
        # Test test file
        test_file = self.create_test_file("test_module.py")
        assert self.generator.determine_file_type(test_file) == "test"
        
        # Test config file
        config_file = self.create_test_file("config.py")
        assert self.generator.determine_file_type(config_file) == "config"
        
        # Test documentation file
        doc_file = self.create_test_file("README.md")
        assert self.generator.determine_file_type(doc_file) == "doc"
    
    def test_determine_importance(self):
        """Test importance level determination."""
        # Test core files
        main_file = self.create_test_file("main.py")
        assert self.generator.determine_importance(main_file) == "core"
        
        # Test test files
        test_file = self.create_test_file("test_something.py")
        assert self.generator.determine_importance(test_file) == "test"
        
        # Test regular feature files
        feature_file = self.create_test_file("feature.py")
        assert self.generator.determine_importance(feature_file) == "feature"
    
    def test_generate_file_meta(self):
        """Test metadata generation for a file."""
        # Create a test Python file
        py_file = self.create_test_file("src/utils.py", 
            "import os\nfrom pathlib import Path\n\ndef get_file_size(path):\n    return os.path.getsize(path)\n")
        
        meta = self.generator.generate_file_meta(py_file)
        
        # Check meta structure
        assert meta['version'] == '1.0'
        assert 'generated_at' in meta
        assert 'file_info' in meta
        assert 'ai_summary' in meta
        assert 'code_structure' in meta
        assert 'relationships' in meta
        
        # Check file info
        file_info = meta['file_info']
        assert file_info['path'] == 'src/utils.py'
        assert file_info['type'] == 'module'
        assert file_info['language'] == 'python'
        assert file_info['size_bytes'] > 0
        assert file_info['estimated_tokens'] > 0
        
        # Check AI summary
        ai_summary = meta['ai_summary']
        assert ai_summary['importance'] == 'feature'
        assert ai_summary['complexity'] == 'medium'
        assert isinstance(ai_summary['key_concepts'], list)
        
        # Check code structure
        code_structure = meta['code_structure']
        assert isinstance(code_structure['imports'], list)
        assert len(code_structure['imports']) >= 2  # os and pathlib
    
    def test_save_and_load_file_meta(self):
        """Test saving and loading metadata."""
        py_file = self.create_test_file("test.py")
        meta = self.generator.generate_file_meta(py_file)
        
        # Initialize structure first
        self.generator.init_axiom_structure()
        
        # Save meta
        self.generator.save_file_meta(py_file, meta)
        
        # Check that meta file was created
        meta_path = Path(self.test_dir) / ".axiom" / "meta" / "test.py.yml"
        assert meta_path.exists()
        
        # Load and verify meta
        with open(meta_path, 'r') as f:
            loaded_meta = yaml.safe_load(f)
        
        assert loaded_meta['file_info']['path'] == meta['file_info']['path']
        assert loaded_meta['file_info']['type'] == meta['file_info']['type']
    
    def test_scan_and_generate_meta(self):
        """Test scanning project and generating metadata."""
        # Create test files
        self.create_test_file("main.py", "print('main')")
        self.create_test_file("utils.py", "def helper(): pass")
        self.create_test_file("test_main.py", "def test_main(): pass")
        self.create_test_file("README.md", "# Test Project")
        
        # Initialize and scan
        self.generator.init_axiom_structure()
        stats = self.generator.scan_and_generate_meta()
        
        # Check stats
        assert stats['total_files'] == 4
        assert stats['total_tokens'] > 0
        assert 'module' in stats['files_by_type']
        assert 'test' in stats['files_by_type']
        assert 'doc' in stats['files_by_type']
        
        # Check that meta files were created
        meta_dir = Path(self.test_dir) / ".axiom" / "meta"
        assert (meta_dir / "main.py.yml").exists()
        assert (meta_dir / "utils.py.yml").exists()
        assert (meta_dir / "test_main.py.yml").exists()
        assert (meta_dir / "README.md.yml").exists()
    
    def test_generate_index(self):
        """Test index generation."""
        # Create test files and meta
        self.create_test_file("main.py", "print('main')")
        self.create_test_file("utils.py", "def helper(): pass")
        
        self.generator.init_axiom_structure()
        self.generator.scan_and_generate_meta()
        self.generator.generate_index()
        
        # Check index file
        index_path = Path(self.test_dir) / ".axiom" / "index.yml"
        assert index_path.exists()
        
        with open(index_path, 'r') as f:
            index = yaml.safe_load(f)
        
        # Check index structure
        assert index['version'] == '1.0'
        assert 'project_context' in index
        assert 'file_categories' in index
        assert 'meta_files' in index
        
        # Check that files were categorized
        file_categories = index['file_categories']
        assert len(file_categories['core_modules']['files']) > 0 or len(file_categories['feature_modules']['files']) > 0
        
        # Check meta files count
        assert index['meta_files']['total_count'] == 2
    
    def test_clean_orphaned_meta(self):
        """Test cleaning of orphaned metadata files."""
        # Create test files and generate meta
        py_file = self.create_test_file("temp.py")
        self.generator.init_axiom_structure()
        self.generator.scan_and_generate_meta()
        
        # Verify meta file exists
        meta_path = Path(self.test_dir) / ".axiom" / "meta" / "temp.py.yml"
        assert meta_path.exists()
        
        # Remove source file
        py_file.unlink()
        
        # Clean orphaned meta
        self.generator.clean_orphaned_meta()
        
        # Verify meta file was removed
        assert not meta_path.exists()
    
    def test_update_meta_for_file(self):
        """Test updating metadata for a specific file."""
        # Create file and generate initial meta
        py_file = self.create_test_file("update_test.py", "print('v1')")
        self.generator.init_axiom_structure()
        self.generator.scan_and_generate_meta()
        
        # Get initial timestamp
        meta_path = Path(self.test_dir) / ".axiom" / "meta" / "update_test.py.yml"
        with open(meta_path, 'r') as f:
            initial_meta = yaml.safe_load(f)
        initial_timestamp = initial_meta['last_updated']
        
        # Update file content
        py_file.write_text("print('v2')\ndef new_function(): pass")
        
        # Update meta
        self.generator.update_meta_for_file(str(py_file))
        
        # Check that meta was updated
        with open(meta_path, 'r') as f:
            updated_meta = yaml.safe_load(f)
        
        # Timestamp should be different
        assert updated_meta['last_updated'] != initial_timestamp
        
        # File size should be different
        assert updated_meta['file_info']['size_bytes'] != initial_meta['file_info']['size_bytes']


class TestAxiomIntegration:
    """Integration tests for the complete Axiom workflow."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        
    def teardown_method(self):
        """Clean up temporary directory."""
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_complete_workflow(self):
        """Test the complete axiom workflow from initialization to meta generation."""
        # Change to test directory
        original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        try:
            # Create some test files
            Path("src").mkdir(exist_ok=True)
            Path("tests").mkdir(exist_ok=True)
            
            with open("src/main.py", "w") as f:
                f.write("def main():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    main()")
            
            with open("src/utils.py", "w") as f:
                f.write("import os\nfrom pathlib import Path\n\ndef get_files(directory):\n    return list(Path(directory).glob('*'))")
            
            with open("tests/test_main.py", "w") as f:
                f.write("import pytest\nfrom src.main import main\n\ndef test_main():\n    assert main() is None")
            
            with open("README.md", "w") as f:
                f.write("# Test Project\n\nThis is a test project for axiom protocol.")
            
            # Initialize generator
            generator = AxiomMetaGenerator(".")
            
            # Run complete workflow
            generator.init_axiom_structure()
            stats = generator.scan_and_generate_meta()
            generator.generate_index()
            
            # Verify results
            assert stats['total_files'] == 4
            assert stats['total_tokens'] > 0
            
            # Check that all expected files exist
            assert Path(".axiom").exists()
            assert Path(".axiom/meta").exists()
            assert Path(".axiom/cache").exists()
            assert Path(".axiom/index.yml").exists()
            
            # Check meta files
            assert Path(".axiom/meta/src/main.py.yml").exists()
            assert Path(".axiom/meta/src/utils.py.yml").exists()
            assert Path(".axiom/meta/tests/test_main.py.yml").exists()
            assert Path(".axiom/meta/README.md.yml").exists()
            
            # Check index content
            with open(".axiom/index.yml", 'r') as f:
                index = yaml.safe_load(f)
            
            assert index['meta_files']['total_count'] == 4
            assert index['meta_files']['sync_status'] == 'clean'
            
        finally:
            os.chdir(original_cwd)


def test_axiom_meta_generator_cli():
    """Test the CLI interface of axiom-meta-generator."""
    # This test would require subprocess calls to test the CLI
    # For now, we'll just verify the main function exists
    from axiom_meta_generator import main
    assert callable(main)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])