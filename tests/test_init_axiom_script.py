#!/usr/bin/env python3
"""
Test suite for init-axiom.sh script
Tests the initialization script functionality end-to-end.
"""

import os
import tempfile
import shutil
import subprocess
import pytest
from pathlib import Path


class TestInitAxiomScript:
    """Test suite for init-axiom.sh script."""
    
    def setup_method(self):
        """Set up test environment with temporary directory."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        
        # Get the path to the init script
        self.script_path = Path(__file__).parent.parent / "init-axiom.sh"
        assert self.script_path.exists(), f"Script not found at {self.script_path}"
        
    def teardown_method(self):
        """Clean up temporary directory."""
        os.chdir(self.original_cwd)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def run_init_script(self):
        """Run the init-axiom.sh script in the test directory."""
        os.chdir(self.test_dir)
        
        # Run the script
        result = subprocess.run(
            [str(self.script_path)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        return result
    
    def test_successful_initialization(self):
        """Test successful initialization of axiom protocol."""
        # Create a basic project structure
        os.chdir(self.test_dir)
        
        # Create some initial files
        with open("README.md", "w") as f:
            f.write("# Test Project")
        
        with open(".gitignore", "w") as f:
            f.write("node_modules/\n")
            
        # Create a simple Python file to test metadata generation
        Path("src").mkdir(exist_ok=True)
        with open("src/main.py", "w") as f:
            f.write("def main():\n    print('Hello, World!')")
        
        # Run the init script
        result = self.run_init_script()
        
        # Check that script succeeded
        assert result.returncode == 0, f"Script failed with: {result.stderr}"
        
        # Check that expected files were created
        assert Path(".axiom-manifest.yml").exists()
        assert Path(".claude/commands").exists()
        assert Path(".claude/commands/generate-prp.md").exists()
        assert Path(".claude/commands/generate-prp-pro.md").exists()
        assert Path(".claude/commands/execute-prp.md").exists()
        assert Path("CLAUDE.md").exists()
        assert Path("scripts/axiom-meta-generator.py").exists()
        
        # Check .axiom directory structure
        assert Path(".axiom").exists()
        assert Path(".axiom/meta").exists()
        assert Path(".axiom/cache").exists()
        assert Path(".axiom/index.yml").exists()
        
        # Check that .gitignore was updated
        with open(".gitignore", "r") as f:
            gitignore_content = f.read()
        
        assert ".axiom-manifest.yml" in gitignore_content
        assert "*.contract.yml" in gitignore_content
        assert ".axiom/" in gitignore_content
        
        # Check that initial metadata scan was performed
        assert Path(".axiom/meta/src/main.py.yml").exists()
        assert Path(".axiom/meta/README.md.yml").exists()
        
        # Verify script permissions
        script_copy = Path("scripts/axiom-meta-generator.py")
        assert os.access(script_copy, os.X_OK), "Script should be executable"
    
    def test_already_initialized_project(self):
        """Test behavior when project is already initialized."""
        os.chdir(self.test_dir)
        
        # Create manifest file to simulate already initialized project
        with open(".axiom-manifest.yml", "w") as f:
            f.write("version: '1.0'\n")
        
        # Run the init script
        result = self.run_init_script()
        
        # Check that script failed with appropriate error
        assert result.returncode == 1
        assert "already exists" in result.stderr
    
    def test_no_gitignore_file(self):
        """Test initialization when no .gitignore file exists."""
        os.chdir(self.test_dir)
        
        # Create basic files but no .gitignore
        with open("README.md", "w") as f:
            f.write("# Test Project")
        
        # Run the init script
        result = self.run_init_script()
        
        # Check that script succeeded
        assert result.returncode == 0
        
        # Check that expected files were created
        assert Path(".axiom-manifest.yml").exists()
        assert Path(".axiom").exists()
        
        # .gitignore should not exist (script shouldn't create it)
        assert not Path(".gitignore").exists()
    
    def test_no_python_available(self):
        """Test initialization when Python is not available."""
        os.chdir(self.test_dir)
        
        # Create basic files
        with open("README.md", "w") as f:
            f.write("# Test Project")
        
        # Mock environment without Python
        env = os.environ.copy()
        env['PATH'] = '/usr/bin:/bin'  # Minimal PATH without Python
        
        # Run the init script with limited PATH
        result = subprocess.run(
            [str(self.script_path)],
            capture_output=True,
            text=True,
            timeout=30,
            env=env
        )
        
        # Script should still succeed but skip metadata scan
        assert result.returncode == 0
        assert "Python3 not found" in result.stderr or "Skipping initial scan" in result.stderr
        
        # Basic structure should still be created
        assert Path(".axiom-manifest.yml").exists()
        assert Path(".axiom").exists()
        assert Path("scripts/axiom-meta-generator.py").exists()
    
    def test_manifest_template_content(self):
        """Test that manifest template is properly customized."""
        os.chdir(self.test_dir)
        
        # Run the init script
        result = self.run_init_script()
        assert result.returncode == 0
        
        # Check manifest content
        with open(".axiom-manifest.yml", "r") as f:
            manifest_content = f.read()
        
        # Should contain template structure
        assert "version: \"1.0\"" in manifest_content
        assert "project:" in manifest_content
        assert "commands:" in manifest_content
        assert "architecture:" in manifest_content
        assert "policies:" in manifest_content
    
    def test_claude_commands_copied(self):
        """Test that Claude commands are properly copied."""
        os.chdir(self.test_dir)
        
        # Run the init script
        result = self.run_init_script()
        assert result.returncode == 0
        
        # Check that all command files exist
        commands_dir = Path(".claude/commands")
        assert commands_dir.exists()
        
        expected_commands = [
            "generate-prp.md",
            "generate-prp-pro.md", 
            "execute-prp.md"
        ]
        
        for command in expected_commands:
            command_file = commands_dir / command
            assert command_file.exists(), f"Command file {command} not found"
            
            # Check that files have content
            assert command_file.stat().st_size > 0, f"Command file {command} is empty"
    
    def test_claude_md_template_copied(self):
        """Test that CLAUDE.md template is properly copied."""
        os.chdir(self.test_dir)
        
        # Run the init script
        result = self.run_init_script()
        assert result.returncode == 0
        
        # Check that CLAUDE.md exists
        claude_md = Path("CLAUDE.md")
        assert claude_md.exists()
        
        # Check content
        with open(claude_md, "r") as f:
            content = f.read()
        
        assert "AI-Native Development Guidelines" in content
        assert "Axiom Protocol" in content
        assert "meta information" in content
    
    def test_script_output_messages(self):
        """Test that script provides informative output messages."""
        os.chdir(self.test_dir)
        
        # Run the init script
        result = self.run_init_script()
        assert result.returncode == 0
        
        # Check for expected output messages
        combined_output = result.stdout + result.stderr
        
        assert "Initializing Axiom Protocol" in combined_output
        assert "Axiom Protocol initialized successfully!" in combined_output
        assert "Next steps:" in combined_output
        assert "Directory structure created:" in combined_output
    
    def test_file_permissions(self):
        """Test that created files have appropriate permissions."""
        os.chdir(self.test_dir)
        
        # Run the init script
        result = self.run_init_script()
        assert result.returncode == 0
        
        # Check script permissions
        script_file = Path("scripts/axiom-meta-generator.py")
        assert script_file.exists()
        assert os.access(script_file, os.X_OK), "Meta generator should be executable"
        
        # Check that other files are readable
        assert os.access(".axiom-manifest.yml", os.R_OK)
        assert os.access("CLAUDE.md", os.R_OK)
        assert os.access(".axiom/index.yml", os.R_OK)


class TestInitAxiomScriptIntegration:
    """Integration tests for init-axiom.sh script with real projects."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        self.script_path = Path(__file__).parent.parent / "init-axiom.sh"
        
    def teardown_method(self):
        """Clean up temporary directory."""
        os.chdir(self.original_cwd)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_python_project_initialization(self):
        """Test initialization of a Python project."""
        os.chdir(self.test_dir)
        
        # Create a realistic Python project structure
        directories = ["src", "tests", "docs"]
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
        
        # Create Python files
        python_files = {
            "src/__init__.py": "",
            "src/main.py": "def main():\n    print('Hello, World!')\n\nif __name__ == '__main__':\n    main()",
            "src/utils.py": "import os\nfrom pathlib import Path\n\ndef get_project_root():\n    return Path(__file__).parent.parent",
            "tests/__init__.py": "",
            "tests/test_main.py": "import pytest\nfrom src.main import main\n\ndef test_main():\n    assert main() is None",
            "tests/test_utils.py": "from src.utils import get_project_root\n\ndef test_get_project_root():\n    assert get_project_root().exists()"
        }
        
        for file_path, content in python_files.items():
            file_obj = Path(file_path)
            file_obj.parent.mkdir(parents=True, exist_ok=True)
            file_obj.write_text(content)
        
        # Create config files
        with open("requirements.txt", "w") as f:
            f.write("pytest>=6.0.0\npytest-cov>=2.0.0\n")
        
        with open("setup.py", "w") as f:
            f.write("from setuptools import setup, find_packages\n\nsetup(\n    name='test-project',\n    version='0.1.0',\n    packages=find_packages(),\n)")
        
        with open("README.md", "w") as f:
            f.write("# Test Python Project\n\nThis is a test project for axiom protocol integration.")
        
        with open(".gitignore", "w") as f:
            f.write("__pycache__/\n*.pyc\n.pytest_cache/\nvenv/\n.env\n")
        
        # Run the init script
        result = subprocess.run(
            [str(self.script_path)],
            capture_output=True,
            text=True,
            timeout=60  # Longer timeout for real project
        )
        
        # Check success
        assert result.returncode == 0, f"Script failed with: {result.stderr}"
        
        # Verify all expected files were created
        expected_files = [
            ".axiom-manifest.yml",
            "CLAUDE.md",
            "scripts/axiom-meta-generator.py",
            ".axiom/index.yml"
        ]
        
        for file_path in expected_files:
            assert Path(file_path).exists(), f"Expected file {file_path} not found"
        
        # Verify metadata was generated for Python files
        expected_meta_files = [
            ".axiom/meta/src/main.py.yml",
            ".axiom/meta/src/utils.py.yml", 
            ".axiom/meta/tests/test_main.py.yml",
            ".axiom/meta/tests/test_utils.py.yml",
            ".axiom/meta/README.md.yml"
        ]
        
        for meta_file in expected_meta_files:
            assert Path(meta_file).exists(), f"Expected meta file {meta_file} not found"
        
        # Check .gitignore was updated
        with open(".gitignore", "r") as f:
            gitignore_content = f.read()
        
        assert ".axiom/" in gitignore_content
        assert "*.contract.yml" in gitignore_content
    
    def test_javascript_project_initialization(self):
        """Test initialization of a JavaScript project."""
        os.chdir(self.test_dir)
        
        # Create JavaScript project structure
        directories = ["src", "tests", "public"]
        for directory in directories:
            Path(directory).mkdir(exist_ok=True)
        
        # Create JavaScript files
        js_files = {
            "src/index.js": "console.log('Hello, World!');\n\nfunction main() {\n    console.log('Application started');\n}\n\nmain();",
            "src/utils.js": "export function formatDate(date) {\n    return date.toISOString();\n}\n\nexport function validateEmail(email) {\n    return email.includes('@');\n}",
            "tests/index.test.js": "import { formatDate, validateEmail } from '../src/utils.js';\n\ntest('formatDate works', () => {\n    expect(formatDate(new Date())).toBeDefined();\n});",
            "public/index.html": "<!DOCTYPE html>\n<html>\n<head>\n    <title>Test App</title>\n</head>\n<body>\n    <h1>Test Application</h1>\n</body>\n</html>"
        }
        
        for file_path, content in js_files.items():
            file_obj = Path(file_path)
            file_obj.parent.mkdir(parents=True, exist_ok=True)
            file_obj.write_text(content)
        
        # Create package.json
        with open("package.json", "w") as f:
            f.write('''{
  "name": "test-project",
  "version": "1.0.0",
  "description": "Test project for axiom protocol",
  "main": "src/index.js",
  "scripts": {
    "test": "jest",
    "start": "node src/index.js"
  },
  "dependencies": {},
  "devDependencies": {
    "jest": "^27.0.0"
  }
}''')
        
        with open("README.md", "w") as f:
            f.write("# Test JavaScript Project\n\nThis is a test JavaScript project for axiom protocol integration.")
        
        with open(".gitignore", "w") as f:
            f.write("node_modules/\n*.log\n.env\n")
        
        # Run the init script
        result = subprocess.run(
            [str(self.script_path)],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Check success
        assert result.returncode == 0, f"Script failed with: {result.stderr}"
        
        # Verify metadata was generated for JavaScript files
        expected_meta_files = [
            ".axiom/meta/src/index.js.yml",
            ".axiom/meta/src/utils.js.yml",
            ".axiom/meta/tests/index.test.js.yml",
            ".axiom/meta/package.json.yml",
            ".axiom/meta/README.md.yml"
        ]
        
        for meta_file in expected_meta_files:
            assert Path(meta_file).exists(), f"Expected meta file {meta_file} not found"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])