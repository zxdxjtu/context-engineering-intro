#!/usr/bin/env python3
"""
Test runner script for the Axiom Protocol framework.
Provides convenient test execution with different options.
"""

import os
import sys
import argparse
import subprocess
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and return success status."""
    if description:
        print(f"\n{'='*60}")
        print(f"Running: {description}")
        print(f"Command: {' '.join(cmd)}")
        print(f"{'='*60}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        print(f"✅ SUCCESS: {description}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ FAILED: {description}")
        print(f"Exit code: {e.returncode}")
        return False
    except FileNotFoundError:
        print(f"❌ COMMAND NOT FOUND: {cmd[0]}")
        return False


def check_dependencies():
    """Check that required dependencies are available."""
    print("Checking dependencies...")
    
    dependencies = [
        ("python3", "Python 3"),
        ("pytest", "Pytest testing framework")
    ]
    
    missing = []
    for cmd, name in dependencies:
        try:
            subprocess.run([cmd, "--version"], capture_output=True, check=True)
            print(f"✅ {name} is available")
        except (subprocess.CalledProcessError, FileNotFoundError):
            print(f"❌ {name} is missing")
            missing.append(name)
    
    if missing:
        print(f"\nMissing dependencies: {', '.join(missing)}")
        print("Please install missing dependencies before running tests.")
        return False
    
    return True


def install_test_dependencies():
    """Install test dependencies."""
    print("Installing test dependencies...")
    
    # Install pytest and other test dependencies
    cmd = [sys.executable, "-m", "pip", "install", "pytest", "pyyaml"]
    return run_command(cmd, "Installing pytest and dependencies")


def run_unit_tests():
    """Run unit tests."""
    cmd = [
        "python3", "-m", "pytest", 
        "tests/test_axiom_meta_generator.py",
        "-v", "--tb=short"
    ]
    return run_command(cmd, "Unit tests for axiom meta generator")


def run_script_tests():
    """Run script integration tests."""
    cmd = [
        "python3", "-m", "pytest",
        "tests/test_init_axiom_script.py",
        "-v", "--tb=short"
    ]
    return run_command(cmd, "Integration tests for init script")


def run_command_tests():
    """Run Claude command tests."""
    cmd = [
        "python3", "-m", "pytest",
        "tests/test_claude_commands.py", 
        "-v", "--tb=short"
    ]
    return run_command(cmd, "Tests for Claude slash commands")


def run_e2e_tests():
    """Run end-to-end tests."""
    cmd = [
        "python3", "-m", "pytest",
        "tests/test_end_to_end_workflow.py",
        "-v", "--tb=short", "--maxfail=3"
    ]
    return run_command(cmd, "End-to-end workflow tests")


def run_all_tests():
    """Run all tests."""
    cmd = [
        "python3", "-m", "pytest",
        "tests/",
        "-v", "--tb=short"
    ]
    return run_command(cmd, "All tests")


def run_fast_tests():
    """Run only fast tests (excluding slow/e2e tests)."""
    cmd = [
        "python3", "-m", "pytest", 
        "tests/",
        "-v", "--tb=short",
        "-m", "not slow and not e2e"
    ]
    return run_command(cmd, "Fast tests only")


def run_coverage_tests():
    """Run tests with coverage reporting."""
    # Install coverage if needed
    subprocess.run([sys.executable, "-m", "pip", "install", "pytest-cov"], 
                  capture_output=True)
    
    cmd = [
        "python3", "-m", "pytest",
        "tests/",
        "--cov=scripts",
        "--cov-report=html",
        "--cov-report=term",
        "-v"
    ]
    return run_command(cmd, "Tests with coverage reporting")


def validate_init_script():
    """Validate the init-axiom.sh script by running it in a test environment."""
    print("\nValidating init-axiom.sh script...")
    
    # Create temporary test directory
    import tempfile
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            
            # Create a minimal test project
            with open("README.md", "w") as f:
                f.write("# Test Project\n")
            
            with open("test.py", "w") as f:
                f.write("print('hello world')\n")
            
            with open(".gitignore", "w") as f:
                f.write("__pycache__/\n")
            
            # Run the init script
            script_path = Path(original_cwd) / "init-axiom.sh"
            cmd = [str(script_path)]
            
            success = run_command(cmd, "Running init-axiom.sh in test environment")
            
            if success:
                # Check that expected files were created
                expected_files = [
                    ".axiom-manifest.yml",
                    ".axiom/index.yml",
                    ".claude/commands/generate-prp.md",
                    "CLAUDE.md",
                    "scripts/axiom-meta-generator.py"
                ]
                
                missing_files = []
                for file_path in expected_files:
                    if not Path(file_path).exists():
                        missing_files.append(file_path)
                
                if missing_files:
                    print(f"❌ Missing expected files: {missing_files}")
                    success = False
                else:
                    print("✅ All expected files created successfully")
            
            return success
            
        finally:
            os.chdir(original_cwd)


def validate_meta_generator():
    """Validate the meta generator by running it on the project itself."""
    print("\nValidating axiom-meta-generator.py...")
    
    # Run meta generator on current project
    cmd = ["python3", "scripts/axiom-meta-generator.py", "--help"]
    if not run_command(cmd, "Checking meta generator help"):
        return False
    
    # Test initialization
    import tempfile
    with tempfile.TemporaryDirectory() as temp_dir:
        original_cwd = os.getcwd()
        try:
            os.chdir(temp_dir)
            
            # Create test file
            with open("test.py", "w") as f:
                f.write("def test(): pass\n")
            
            # Test init
            cmd = ["python3", str(Path(original_cwd) / "scripts" / "axiom-meta-generator.py"), "--init"]
            if not run_command(cmd, "Testing meta generator init"):
                return False
            
            # Test scan
            cmd = ["python3", str(Path(original_cwd) / "scripts" / "axiom-meta-generator.py"), "--scan"]
            success = run_command(cmd, "Testing meta generator scan")
            
            # Check results
            if success and Path(".axiom/index.yml").exists():
                print("✅ Meta generator validation successful")
                return True
            else:
                print("❌ Meta generator validation failed")
                return False
                
        finally:
            os.chdir(original_cwd)


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="Test runner for Axiom Protocol framework")
    parser.add_argument("--check-deps", action="store_true", 
                       help="Check dependencies only")
    parser.add_argument("--install-deps", action="store_true",
                       help="Install test dependencies")
    parser.add_argument("--unit", action="store_true",
                       help="Run unit tests only")
    parser.add_argument("--script", action="store_true", 
                       help="Run script integration tests only")
    parser.add_argument("--commands", action="store_true",
                       help="Run Claude command tests only")
    parser.add_argument("--e2e", action="store_true",
                       help="Run end-to-end tests only")
    parser.add_argument("--fast", action="store_true",
                       help="Run fast tests only (exclude slow/e2e)")
    parser.add_argument("--coverage", action="store_true",
                       help="Run tests with coverage reporting")
    parser.add_argument("--validate", action="store_true",
                       help="Validate scripts by running them")
    parser.add_argument("--all", action="store_true", 
                       help="Run all tests (default)")
    
    args = parser.parse_args()
    
    # Change to project root directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    print(f"Running tests from: {project_root}")
    
    # Check dependencies first
    if args.check_deps or not check_dependencies():
        return 1 if args.check_deps else 1
    
    if args.install_deps:
        if not install_test_dependencies():
            return 1
        print("✅ Dependencies installed successfully")
        return 0
    
    # Determine which tests to run
    success = True
    
    if args.validate:
        print("\n🔧 VALIDATION PHASE")
        success &= validate_init_script()
        success &= validate_meta_generator()
    
    if args.unit:
        print("\n🧪 UNIT TESTS")
        success &= run_unit_tests()
    elif args.script:
        print("\n📜 SCRIPT TESTS")
        success &= run_script_tests()
    elif args.commands:
        print("\n⚡ COMMAND TESTS")
        success &= run_command_tests()
    elif args.e2e:
        print("\n🔄 END-TO-END TESTS")
        success &= run_e2e_tests()
    elif args.fast:
        print("\n⚡ FAST TESTS")
        success &= run_fast_tests()
    elif args.coverage:
        print("\n📊 COVERAGE TESTS")
        success &= run_coverage_tests()
    else:
        # Run all tests by default
        print("\n🚀 RUNNING ALL TESTS")
        print("\n🔧 Validation Phase")
        success &= validate_init_script()
        success &= validate_meta_generator()
        
        print("\n🧪 Unit Tests")
        success &= run_unit_tests()
        
        print("\n📜 Script Integration Tests")
        success &= run_script_tests()
        
        print("\n⚡ Command Tests")
        success &= run_command_tests()
        
        print("\n🔄 End-to-End Tests")
        success &= run_e2e_tests()
    
    # Final result
    print(f"\n{'='*60}")
    if success:
        print("🎉 ALL TESTS PASSED!")
        print("The Axiom Protocol framework is working correctly.")
        return 0
    else:
        print("❌ SOME TESTS FAILED!")
        print("Please check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())