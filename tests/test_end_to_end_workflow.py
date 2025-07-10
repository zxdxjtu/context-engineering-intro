#!/usr/bin/env python3
"""
End-to-end integration tests for the complete Axiom Protocol workflow.
Tests the full user journey from initialization to PRP execution.
"""

import os
import sys
import tempfile
import shutil
import subprocess
import pytest
import yaml
from pathlib import Path

# Add scripts to path for testing
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))


class TestCompleteWorkflow:
    """Test the complete end-to-end workflow."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        
        # Get paths to key scripts and files
        self.project_root = Path(__file__).parent.parent
        self.init_script = self.project_root / "init-axiom.sh"
        
        assert self.init_script.exists(), f"Init script not found at {self.init_script}"
        
    def teardown_method(self):
        """Clean up."""
        os.chdir(self.original_cwd)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def create_sample_project(self):
        """Create a realistic sample project for testing."""
        os.chdir(self.test_dir)
        
        # Create project structure
        directories = [
            "src", "src/components", "src/utils", 
            "tests", "tests/unit", "tests/integration",
            "docs", "config"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
        
        # Create Python files with realistic content
        files = {
            "src/__init__.py": "",
            "src/main.py": '''#!/usr/bin/env python3
"""Main application entry point."""

import sys
from pathlib import Path
from src.components.app import Application
from src.utils.config import load_config

def main():
    """Run the main application."""
    config = load_config()
    app = Application(config)
    return app.run()

if __name__ == "__main__":
    sys.exit(main())
''',
            "src/components/__init__.py": "",
            "src/components/app.py": '''"""Application main class."""

import logging
from typing import Dict, Any

class Application:
    """Main application class."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize application with config."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        
    def run(self) -> int:
        """Run the application."""
        self.logger.info("Starting application")
        # Main application logic would go here
        return 0
''',
            "src/utils/__init__.py": "",
            "src/utils/config.py": '''"""Configuration utilities."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any

def load_config(config_path: str = None) -> Dict[str, Any]:
    """Load configuration from file."""
    if config_path is None:
        config_path = Path(__file__).parent.parent.parent / "config" / "config.yml"
    
    if not Path(config_path).exists():
        return get_default_config()
    
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def get_default_config() -> Dict[str, Any]:
    """Get default configuration."""
    return {
        "app_name": "sample-app",
        "version": "1.0.0",
        "debug": False,
        "log_level": "INFO"
    }
''',
            "tests/__init__.py": "",
            "tests/unit/__init__.py": "",
            "tests/unit/test_app.py": '''"""Tests for Application class."""

import pytest
from src.components.app import Application

def test_application_init():
    """Test application initialization."""
    config = {"test": True}
    app = Application(config)
    assert app.config == config

def test_application_run():
    """Test application run method."""
    config = {"test": True}
    app = Application(config)
    result = app.run()
    assert result == 0
''',
            "tests/unit/test_config.py": '''"""Tests for config utilities."""

import pytest
from src.utils.config import get_default_config, load_config

def test_get_default_config():
    """Test default config generation."""
    config = get_default_config()
    assert "app_name" in config
    assert "version" in config
    assert config["app_name"] == "sample-app"

def test_load_config_default():
    """Test loading config with defaults."""
    config = load_config("nonexistent.yml")
    assert config == get_default_config()
''',
            "config/config.yml": '''app_name: "sample-app"
version: "1.0.0"
debug: false
log_level: "INFO"
database:
  host: "localhost"
  port: 5432
  name: "sampledb"
''',
            "requirements.txt": '''pytest>=6.0.0
pytest-cov>=2.0.0
pyyaml>=5.4.0
''',
            "setup.py": '''from setuptools import setup, find_packages

setup(
    name="sample-app",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "pyyaml>=5.4.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "pytest-cov>=2.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "sample-app=src.main:main",
        ],
    },
)
''',
            "README.md": '''# Sample Application

This is a sample application created to test the Axiom Protocol framework.

## Features

- Modular architecture
- Configuration management
- Comprehensive testing
- AI-optimized development workflow

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m src.main
```

## Testing

```bash
pytest tests/
```
''',
            ".gitignore": '''__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

.pytest_cache/
.coverage
htmlcov/

.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

.vscode/
.idea/
*.swp
*.swo
*~
'''
        }
        
        for file_path, content in files.items():
            file_obj = Path(file_path)
            file_obj.parent.mkdir(parents=True, exist_ok=True)
            file_obj.write_text(content)
    
    def test_complete_initialization_workflow(self):
        """Test the complete initialization workflow."""
        # Create sample project
        self.create_sample_project()
        
        # Run initialization
        result = subprocess.run(
            [str(self.init_script)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Check that initialization succeeded
        assert result.returncode == 0, f"Initialization failed: {result.stderr}"
        
        # Verify all expected files and directories exist
        expected_paths = [
            ".axiom-manifest.yml",
            ".axiom/",
            ".axiom/meta/",
            ".axiom/cache/",
            ".axiom/index.yml",
            ".claude/commands/",
            "CLAUDE.md",
            "scripts/axiom-meta-generator.py"
        ]
        
        for path in expected_paths:
            assert Path(path).exists(), f"Expected path {path} not found after initialization"
        
        # Check that metadata was generated for all relevant files
        expected_meta_files = [
            ".axiom/meta/src/main.py.yml",
            ".axiom/meta/src/components/app.py.yml",
            ".axiom/meta/src/utils/config.py.yml",
            ".axiom/meta/tests/unit/test_app.py.yml",
            ".axiom/meta/tests/unit/test_config.py.yml",
            ".axiom/meta/README.md.yml",
            ".axiom/meta/requirements.txt.yml"
        ]
        
        for meta_file in expected_meta_files:
            assert Path(meta_file).exists(), f"Expected meta file {meta_file} not found"
        
        # Verify index.yml content
        with open(".axiom/index.yml", 'r') as f:
            index = yaml.safe_load(f)
        
        assert index['version'] == '1.0'
        assert index['meta_files']['total_count'] > 0
        assert index['meta_files']['sync_status'] == 'clean'
        assert index['project_context']['token_budget_per_session'] > 0
        
        # Check that files were properly categorized
        file_categories = index['file_categories']
        assert file_categories['core_modules']['estimated_tokens'] > 0 or file_categories['feature_modules']['estimated_tokens'] > 0
        assert file_categories['test_files']['estimated_tokens'] > 0
        
        # Verify .gitignore was updated
        with open(".gitignore", 'r') as f:
            gitignore_content = f.read()
        
        assert ".axiom/" in gitignore_content
        assert "*.contract.yml" in gitignore_content
        assert ".axiom-manifest.yml" in gitignore_content
    
    def test_meta_file_content_quality(self):
        """Test that generated meta files have high-quality content."""
        # Create and initialize project
        self.create_sample_project()
        
        result = subprocess.run([str(self.init_script)], capture_output=True, timeout=60)
        assert result.returncode == 0
        
        # Check specific meta file content
        meta_file = Path(".axiom/meta/src/components/app.py.yml")
        assert meta_file.exists()
        
        with open(meta_file, 'r') as f:
            meta = yaml.safe_load(f)
        
        # Verify meta structure
        assert meta['version'] == '1.0'
        assert 'file_info' in meta
        assert 'ai_summary' in meta
        assert 'code_structure' in meta
        assert 'relationships' in meta
        
        # Check file info
        file_info = meta['file_info']
        assert file_info['path'] == 'src/components/app.py'
        assert file_info['type'] == 'module'
        assert file_info['language'] == 'python'
        assert file_info['size_bytes'] > 0
        assert file_info['estimated_tokens'] > 0
        
        # Check AI summary
        ai_summary = meta['ai_summary']
        assert ai_summary['purpose']  # Should have a purpose
        assert ai_summary['importance'] in ['core', 'feature', 'test']
        assert ai_summary['complexity'] in ['low', 'medium', 'high']
        
        # Check code structure
        code_structure = meta['code_structure']
        assert isinstance(code_structure['imports'], list)
        assert isinstance(code_structure['main_functions'], list)
        
        # Check that imports were detected
        # The app.py file imports logging and typing
        imports = code_structure['imports']
        assert len(imports) > 0  # Should detect some imports
    
    def test_token_estimation_accuracy(self):
        """Test that token estimations are reasonable."""
        self.create_sample_project()
        
        result = subprocess.run([str(self.init_script)], capture_output=True, timeout=60)
        assert result.returncode == 0
        
        with open(".axiom/index.yml", 'r') as f:
            index = yaml.safe_load(f)
        
        # Check total token estimation
        total_tokens = 0
        for category in index['file_categories'].values():
            total_tokens += category['estimated_tokens']
        
        # Should be reasonable for our sample project
        assert 1000 < total_tokens < 50000, f"Token estimation seems unreasonable: {total_tokens}"
        
        # Check individual file estimations
        meta_file = Path(".axiom/meta/src/main.py.yml")
        with open(meta_file, 'r') as f:
            meta = yaml.safe_load(f)
        
        tokens = meta['file_info']['estimated_tokens']
        size_bytes = meta['file_info']['size_bytes']
        
        # Token estimate should be reasonable relative to file size
        assert 0 < tokens < size_bytes * 2, f"Token estimation unreasonable: {tokens} for {size_bytes} bytes"
    
    def test_file_categorization(self):
        """Test that files are properly categorized."""
        self.create_sample_project()
        
        result = subprocess.run([str(self.init_script)], capture_output=True, timeout=60)
        assert result.returncode == 0
        
        with open(".axiom/index.yml", 'r') as f:
            index = yaml.safe_load(f)
        
        file_categories = index['file_categories']
        
        # Check that we have files in appropriate categories
        assert len(file_categories['feature_modules']['files']) > 0 or len(file_categories['core_modules']['files']) > 0
        assert len(file_categories['test_files']['files']) > 0
        assert len(file_categories['config_files']['files']) > 0
        
        # Main.py should be categorized as core
        core_files = file_categories['core_modules']['files']
        feature_files = file_categories['feature_modules']['files']
        assert 'src/main.py' in core_files or 'src/main.py' in feature_files
        
        # Test files should be in test category
        test_files = file_categories['test_files']['files']
        assert any('test_' in f for f in test_files)
        
        # Config files should be in config category
        config_files = file_categories['config_files']['files']
        assert any('config' in f.lower() or f.endswith('.yml') or f.endswith('.txt') for f in config_files)
    
    def test_contract_creation_workflow(self):
        """Test creating contract files for modules."""
        self.create_sample_project()
        
        # Initialize project
        result = subprocess.run([str(self.init_script)], capture_output=True, timeout=60)
        assert result.returncode == 0
        
        # Create a contract file for the app module
        contract_content = '''# Contract for Application class
summary: "Main application class that handles initialization and execution"
component: "components"

preconditions:
  - name: "config"
    type: "Dict[str, Any]"
    description: "Configuration dictionary"

postconditions:
  - name: "return_code"
    type: "int"
    description: "Application exit code (0 for success)"

invariants:
  - "Application maintains config state throughout execution"
  - "Logger is properly configured"

dependencies:
  internal: ["src/utils/config.py"]
  external: ["logging", "typing"]
'''
        
        with open("src/components/app.contract.yml", 'w') as f:
            f.write(contract_content)
        
        # Update metadata to reflect contract
        from axiom_meta_generator import AxiomMetaGenerator
        
        generator = AxiomMetaGenerator(".")
        generator.update_meta_for_file("src/components/app.py")
        generator.generate_index()
        
        # Check that contract is referenced in meta
        with open(".axiom/meta/src/components/app.py.yml", 'r') as f:
            meta = yaml.safe_load(f)
        
        assert meta['contract_file'] == "src/components/app.contract.yml"
        
        # Verify contract file exists and is valid
        assert Path("src/components/app.contract.yml").exists()
        
        with open("src/components/app.contract.yml", 'r') as f:
            contract = yaml.safe_load(f)
        
        assert contract['summary']
        assert 'preconditions' in contract
        assert 'postconditions' in contract
        assert 'dependencies' in contract
    
    def test_meta_synchronization(self):
        """Test that meta files stay synchronized with source files."""
        self.create_sample_project()
        
        # Initialize project
        result = subprocess.run([str(self.init_script)], capture_output=True, timeout=60)
        assert result.returncode == 0
        
        # Get initial meta timestamp
        meta_file = Path(".axiom/meta/src/main.py.yml")
        with open(meta_file, 'r') as f:
            initial_meta = yaml.safe_load(f)
        initial_timestamp = initial_meta['last_updated']
        
        # Modify source file
        with open("src/main.py", 'a') as f:
            f.write("\n# Added comment for testing\n")
        
        # Update meta
        from axiom_meta_generator import AxiomMetaGenerator
        generator = AxiomMetaGenerator(".")
        generator.update_meta_for_file("src/main.py")
        
        # Check that meta was updated
        with open(meta_file, 'r') as f:
            updated_meta = yaml.safe_load(f)
        
        assert updated_meta['last_updated'] != initial_timestamp
        assert updated_meta['file_info']['size_bytes'] > initial_meta['file_info']['size_bytes']
    
    def test_project_scaling(self):
        """Test that the system handles larger projects reasonably."""
        # Create a larger project structure
        os.chdir(self.test_dir)
        
        # Create many files to test scaling
        for i in range(20):
            module_dir = Path(f"module_{i}")
            module_dir.mkdir()
            
            # Create main module file
            with open(module_dir / f"module_{i}.py", 'w') as f:
                f.write(f'''"""Module {i} implementation."""

def function_{i}():
    """Function for module {i}."""
    return "module_{i}_result"

class Class{i}:
    """Class for module {i}."""
    
    def __init__(self):
        self.value = {i}
    
    def method_{i}(self):
        """Method for module {i}."""
        return self.value * 2
''')
            
            # Create test file
            with open(module_dir / f"test_module_{i}.py", 'w') as f:
                f.write(f'''"""Tests for module {i}."""

import pytest
from .module_{i} import function_{i}, Class{i}

def test_function_{i}():
    """Test function_{i}."""
    result = function_{i}()
    assert result == "module_{i}_result"

def test_class_{i}():
    """Test Class{i}."""
    obj = Class{i}()
    assert obj.value == {i}
    assert obj.method_{i}() == {i * 2}
''')
        
        # Create main README
        with open("README.md", 'w') as f:
            f.write("# Large Test Project\n\nThis project tests scaling with many modules.")
        
        # Initialize
        result = subprocess.run([str(self.init_script)], capture_output=True, timeout=120)
        assert result.returncode == 0
        
        # Check that all files were processed
        with open(".axiom/index.yml", 'r') as f:
            index = yaml.safe_load(f)
        
        # Should have processed 40+ files (20 modules + 20 tests + README)
        assert index['meta_files']['total_count'] >= 40
        
        # Token budget should be reasonable
        total_tokens = sum(cat['estimated_tokens'] for cat in index['file_categories'].values())
        assert total_tokens > 5000  # Should be substantial
        assert total_tokens < 200000  # But not excessive
        
        # Should complete in reasonable time (already tested by timeout)
        assert index['meta_files']['sync_status'] == 'clean'


class TestErrorHandling:
    """Test error handling in the workflow."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        
        self.project_root = Path(__file__).parent.parent
        self.init_script = self.project_root / "init-axiom.sh"
        
    def teardown_method(self):
        """Clean up."""
        os.chdir(self.original_cwd)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_corrupted_meta_file_recovery(self):
        """Test recovery from corrupted meta files."""
        os.chdir(self.test_dir)
        
        # Create simple project
        with open("test.py", 'w') as f:
            f.write("print('test')")
        
        # Initialize
        result = subprocess.run([str(self.init_script)], capture_output=True, timeout=60)
        assert result.returncode == 0
        
        # Corrupt meta file
        meta_file = Path(".axiom/meta/test.py.yml")
        with open(meta_file, 'w') as f:
            f.write("invalid: yaml: content: [")
        
        # Try to regenerate
        from axiom_meta_generator import AxiomMetaGenerator
        generator = AxiomMetaGenerator(".")
        
        # Should handle gracefully and regenerate
        generator.scan_and_generate_meta()
        
        # Meta file should be fixed
        with open(meta_file, 'r') as f:
            meta = yaml.safe_load(f)
        
        assert meta['version'] == '1.0'
        assert meta['file_info']['path'] == 'test.py'
    
    def test_missing_source_file_cleanup(self):
        """Test cleanup of orphaned meta files."""
        os.chdir(self.test_dir)
        
        # Create and initialize
        with open("temp.py", 'w') as f:
            f.write("print('temp')")
        
        result = subprocess.run([str(self.init_script)], capture_output=True, timeout=60)
        assert result.returncode == 0
        
        # Verify meta file exists
        meta_file = Path(".axiom/meta/temp.py.yml")
        assert meta_file.exists()
        
        # Remove source file
        Path("temp.py").unlink()
        
        # Clean orphaned meta
        from axiom_meta_generator import AxiomMetaGenerator
        generator = AxiomMetaGenerator(".")
        generator.clean_orphaned_meta()
        
        # Meta file should be removed
        assert not meta_file.exists()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])