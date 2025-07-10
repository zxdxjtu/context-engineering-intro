#!/usr/bin/env python3
"""
Pytest configuration and shared fixtures for the test suite.
"""

import os
import sys
import tempfile
import shutil
import pytest
from pathlib import Path

# Add the scripts directory to Python path
TEST_DIR = Path(__file__).parent
PROJECT_ROOT = TEST_DIR.parent
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

sys.path.insert(0, str(SCRIPTS_DIR))


@pytest.fixture
def temp_project_dir():
    """Create a temporary directory for testing projects."""
    temp_dir = tempfile.mkdtemp()
    original_cwd = os.getcwd()
    
    yield temp_dir
    
    # Cleanup
    os.chdir(original_cwd)
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)


@pytest.fixture
def project_root():
    """Path to the project root directory."""
    return PROJECT_ROOT


@pytest.fixture
def init_script_path(project_root):
    """Path to the init-axiom.sh script."""
    script_path = project_root / "init-axiom.sh"
    assert script_path.exists(), f"Init script not found at {script_path}"
    return script_path


@pytest.fixture
def commands_dir(project_root):
    """Path to the .claude/commands directory."""
    commands_path = project_root / ".claude" / "commands"
    assert commands_path.exists(), f"Commands directory not found at {commands_path}"
    return commands_path


@pytest.fixture
def templates_dir(project_root):
    """Path to the templates directory."""
    templates_path = project_root / "templates"
    assert templates_path.exists(), f"Templates directory not found at {templates_path}"
    return templates_path


@pytest.fixture
def sample_python_project(temp_project_dir):
    """Create a sample Python project for testing."""
    os.chdir(temp_project_dir)
    
    # Create directory structure
    directories = ["src", "tests", "docs"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    # Create Python files
    files = {
        "src/__init__.py": "",
        "src/main.py": '''def main():
    """Main function."""
    print("Hello, World!")
    return 0

if __name__ == "__main__":
    main()
''',
        "src/utils.py": '''"""Utility functions."""

def helper_function(x):
    """Helper function."""
    return x * 2

class UtilityClass:
    """Utility class."""
    
    def __init__(self, value):
        self.value = value
    
    def process(self):
        """Process the value."""
        return self.value + 1
''',
        "tests/__init__.py": "",
        "tests/test_main.py": '''import pytest
from src.main import main

def test_main():
    """Test main function."""
    result = main()
    assert result == 0
''',
        "tests/test_utils.py": '''import pytest
from src.utils import helper_function, UtilityClass

def test_helper_function():
    """Test helper function."""
    assert helper_function(5) == 10

def test_utility_class():
    """Test utility class."""
    util = UtilityClass(10)
    assert util.process() == 11
''',
        "README.md": '''# Sample Project

This is a sample project for testing.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python -m src.main
```
''',
        "requirements.txt": '''pytest>=6.0.0
''',
        ".gitignore": '''__pycache__/
*.pyc
.pytest_cache/
'''
    }
    
    for file_path, content in files.items():
        file_obj = Path(file_path)
        file_obj.parent.mkdir(parents=True, exist_ok=True)
        file_obj.write_text(content)
    
    return temp_project_dir


@pytest.fixture
def sample_javascript_project(temp_project_dir):
    """Create a sample JavaScript project for testing."""
    os.chdir(temp_project_dir)
    
    # Create directory structure
    directories = ["src", "tests", "public"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    # Create JavaScript files
    files = {
        "src/index.js": '''console.log("Hello, World!");

function main() {
    console.log("Application started");
    return 0;
}

module.exports = { main };
''',
        "src/utils.js": '''/**
 * Utility functions
 */

function helperFunction(x) {
    return x * 2;
}

class UtilityClass {
    constructor(value) {
        this.value = value;
    }
    
    process() {
        return this.value + 1;
    }
}

module.exports = { helperFunction, UtilityClass };
''',
        "tests/index.test.js": '''const { main } = require('../src/index');

test('main function', () => {
    expect(main()).toBe(0);
});
''',
        "tests/utils.test.js": '''const { helperFunction, UtilityClass } = require('../src/utils');

test('helper function', () => {
    expect(helperFunction(5)).toBe(10);
});

test('utility class', () => {
    const util = new UtilityClass(10);
    expect(util.process()).toBe(11);
});
''',
        "package.json": '''{
  "name": "sample-project",
  "version": "1.0.0",
  "description": "Sample project for testing",
  "main": "src/index.js",
  "scripts": {
    "test": "jest",
    "start": "node src/index.js"
  },
  "devDependencies": {
    "jest": "^27.0.0"
  }
}
''',
        "README.md": '''# Sample JavaScript Project

This is a sample JavaScript project for testing.

## Installation

```bash
npm install
```

## Usage

```bash
npm start
```

## Testing

```bash
npm test
```
''',
        ".gitignore": '''node_modules/
*.log
.env
'''
    }
    
    for file_path, content in files.items():
        file_obj = Path(file_path)
        file_obj.parent.mkdir(parents=True, exist_ok=True)
        file_obj.write_text(content)
    
    return temp_project_dir


@pytest.fixture
def axiom_meta_generator():
    """Import and return AxiomMetaGenerator class."""
    from axiom_meta_generator import AxiomMetaGenerator
    return AxiomMetaGenerator


def pytest_configure(config):
    """Configure pytest with custom markers."""
    config.addinivalue_line(
        "markers", "slow: marks tests as slow (deselect with '-m \"not slow\"')"
    )
    config.addinivalue_line(
        "markers", "integration: marks tests as integration tests"
    )
    config.addinivalue_line(
        "markers", "e2e: marks tests as end-to-end tests"
    )


def pytest_collection_modifyitems(config, items):
    """Modify test collection to add markers automatically."""
    for item in items:
        # Mark integration tests
        if "integration" in item.nodeid or "test_integration" in item.nodeid:
            item.add_marker(pytest.mark.integration)
        
        # Mark end-to-end tests
        if "e2e" in item.nodeid or "end_to_end" in item.nodeid:
            item.add_marker(pytest.mark.e2e)
            item.add_marker(pytest.mark.slow)
        
        # Mark slow tests
        if "test_complete_workflow" in item.nodeid or "test_project_scaling" in item.nodeid:
            item.add_marker(pytest.mark.slow)


# Test data constants
SAMPLE_PYTHON_FILE_CONTENT = '''#!/usr/bin/env python3
"""Sample Python module for testing."""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional


def sample_function(param1: str, param2: int = 10) -> str:
    """Sample function with type hints.
    
    Args:
        param1: First parameter
        param2: Second parameter with default
        
    Returns:
        Processed string result
    """
    result = f"{param1}_{param2}"
    return result.upper()


class SampleClass:
    """Sample class for testing."""
    
    def __init__(self, name: str, values: List[int]):
        """Initialize the sample class."""
        self.name = name
        self.values = values
        self._private_attr = "private"
    
    def public_method(self) -> Dict[str, int]:
        """Public method that returns a dictionary."""
        return {
            "count": len(self.values),
            "sum": sum(self.values),
            "max": max(self.values) if self.values else 0
        }
    
    def _private_method(self) -> None:
        """Private method."""
        pass


if __name__ == "__main__":
    # Example usage
    result = sample_function("test", 42)
    print(result)
    
    obj = SampleClass("example", [1, 2, 3, 4, 5])
    stats = obj.public_method()
    print(stats)
'''

SAMPLE_CONTRACT_CONTENT = '''# Sample contract file
summary: "Sample module contract for testing"
component: "core"

preconditions:
  - name: "param1"
    type: "str"
    description: "Input string parameter"
  - name: "param2"
    type: "int"
    description: "Input integer parameter"

postconditions:
  - name: "result"
    type: "str"
    description: "Processed uppercase string"

invariants:
  - "Function is pure and has no side effects"
  - "Result is always uppercase"

dependencies:
  internal: []
  external: ["os", "sys", "pathlib", "typing"]
'''