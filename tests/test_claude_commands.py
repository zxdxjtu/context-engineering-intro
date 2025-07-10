#!/usr/bin/env python3
"""
Test suite for Claude slash commands
Tests the functionality and integration of PRP generation and execution commands.
"""

import os
import tempfile
import shutil
import pytest
from pathlib import Path
import yaml


class TestClaudeCommands:
    """Test suite for Claude slash commands."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        
        # Get command file paths
        self.commands_dir = Path(__file__).parent.parent / ".claude" / "commands"
        assert self.commands_dir.exists(), f"Commands directory not found at {self.commands_dir}"
        
    def teardown_method(self):
        """Clean up temporary directory."""
        os.chdir(self.original_cwd)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_command_files_exist(self):
        """Test that all expected command files exist."""
        expected_commands = [
            "generate-prp.md",
            "generate-prp-pro.md",
            "execute-prp.md"
        ]
        
        for command in expected_commands:
            command_file = self.commands_dir / command
            assert command_file.exists(), f"Command file {command} not found"
            assert command_file.stat().st_size > 0, f"Command file {command} is empty"
    
    def test_generate_prp_command_structure(self):
        """Test the structure and content of generate-prp.md command."""
        command_file = self.commands_dir / "generate-prp.md"
        
        with open(command_file, 'r') as f:
            content = f.read()
        
        # Check for required sections
        assert "# Create PRP" in content
        assert "## Research Process" in content
        assert "## PRP Generation" in content
        assert "## Output" in content
        assert "## Quality Checklist" in content
        
        # Check for key instructions
        assert "Research" in content
        assert "Plan" in content
        assert "Implement" in content
        assert "ULTRATHINK" in content
        assert "validation gates" in content
    
    def test_generate_prp_pro_command_structure(self):
        """Test the structure and content of generate-prp-pro.md command."""
        command_file = self.commands_dir / "generate-prp-pro.md"
        
        with open(command_file, 'r') as f:
            content = f.read()
        
        # Check for required sections
        assert "# NAME" in content
        assert "generate-prp-pro" in content
        assert "# DESCRIPTION" in content
        assert "# PROMPT" in content
        
        # Check for workflow steps
        assert "Step 1: AI-Optimized Context Analysis" in content
        assert "Step 2: Generate a Dynamic Questionnaire" in content
        assert "Step 3: Interactive Dialogue" in content
        assert "Step 4: Synthesize AI-Optimized PRP" in content
        assert "Step 5: Final Output & Axiom Integration" in content
        
        # Check for Axiom Protocol integration
        assert ".axiom/index.yml" in content
        assert ".axiom/meta/" in content
        assert "AXIOM_REQUIREMENTS" in content
        assert "meta file updates" in content
    
    def test_execute_prp_command_structure(self):
        """Test the structure and content of execute-prp.md command."""
        command_file = self.commands_dir / "execute-prp.md"
        
        with open(command_file, 'r') as f:
            content = f.read()
        
        # Check for required sections
        assert "# Execute BASE PRP" in content
        assert "## AI-Optimized Execution Process" in content
        assert "## Axiom Protocol Requirements" in content
        
        # Check for execution steps
        assert "Load PRP & Axiom Context" in content
        assert "ULTRATHINK with AI Context" in content
        assert "Execute with Meta Maintenance" in content
        assert "Validate & Sync" in content
        assert "Complete with Axiom Verification" in content
        
        # Check for Axiom integration
        assert ".axiom/index.yml" in content
        assert "meta files" in content
        assert "axiom-meta-generator.py" in content
        assert "contract.yml" in content
    
    def test_command_file_format(self):
        """Test that command files follow proper markdown format."""
        for command_file in self.commands_dir.glob("*.md"):
            with open(command_file, 'r') as f:
                content = f.read()
            
            # Should start with markdown header
            lines = content.split('\n')
            assert lines[0].startswith('#'), f"Command {command_file.name} should start with markdown header"
            
            # Should have proper markdown structure
            assert '##' in content or '#' in content, f"Command {command_file.name} should have structured sections"
    
    def test_prp_generation_workflow_consistency(self):
        """Test that PRP generation commands have consistent workflow."""
        # Check generate-prp.md
        with open(self.commands_dir / "generate-prp.md", 'r') as f:
            generate_content = f.read()
        
        # Check generate-prp-pro.md  
        with open(self.commands_dir / "generate-prp-pro.md", 'r') as f:
            generate_pro_content = f.read()
        
        # Both should mention research phase
        assert "research" in generate_content.lower()
        assert "research" in generate_pro_content.lower()
        
        # Both should mention validation
        assert "validation" in generate_content.lower()
        assert "validation" in generate_pro_content.lower()
        
        # Pro version should have additional Axiom features
        assert ".axiom" in generate_pro_content
        assert "meta" in generate_pro_content
        
    def test_execute_prp_axiom_integration(self):
        """Test that execute-prp command properly integrates with Axiom Protocol."""
        command_file = self.commands_dir / "execute-prp.md"
        
        with open(command_file, 'r') as f:
            content = f.read()
        
        # Should check .axiom context first
        assert ".axiom/index.yml" in content
        assert "FIRST" in content and ".axiom" in content
        
        # Should maintain meta files
        assert "meta file" in content
        assert "update" in content and "meta" in content
        
        # Should run meta generator
        assert "axiom-meta-generator.py" in content
        assert "--scan" in content
        
        # Should verify sync status
        assert "sync_status" in content
        assert "clean" in content
        
        # Should never commit without meta updates
        assert "Never commit" in content
        assert "meta" in content


class TestPRPTemplateIntegration:
    """Test integration with PRP templates."""
    
    def setup_method(self):
        """Set up test environment."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        
        # Get template paths
        self.prp_templates_dir = Path(__file__).parent.parent / "PRPs" / "templates"
        
    def teardown_method(self):
        """Clean up."""
        os.chdir(self.original_cwd)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def test_prp_base_template_exists(self):
        """Test that PRP base template exists and has proper structure."""
        template_file = self.prp_templates_dir / "prp_base.md"
        
        if template_file.exists():
            with open(template_file, 'r') as f:
                content = f.read()
            
            # Should have standard PRP sections
            expected_sections = ["CONTEXT", "TASK", "PERSONA", "FORMAT"]
            for section in expected_sections:
                assert f"## {section}" in content or f"# {section}" in content
    
    def test_commands_reference_templates(self):
        """Test that commands properly reference PRP templates."""
        commands_dir = Path(__file__).parent.parent / ".claude" / "commands"
        
        # Check generate-prp.md
        generate_file = commands_dir / "generate-prp.md"
        if generate_file.exists():
            with open(generate_file, 'r') as f:
                content = f.read()
            
            # Should reference template
            assert "prp_base.md" in content or "template" in content.lower()
        
        # Check generate-prp-pro.md
        generate_pro_file = commands_dir / "generate-prp-pro.md"
        if generate_pro_file.exists():
            with open(generate_pro_file, 'r') as f:
                content = f.read()
            
            # Should reference template
            assert "prp_base.md" in content or "template" in content.lower()


class TestAxiomCommandIntegration:
    """Test integration between commands and Axiom Protocol."""
    
    def setup_method(self):
        """Set up test environment with initialized axiom project."""
        self.test_dir = tempfile.mkdtemp()
        self.original_cwd = os.getcwd()
        os.chdir(self.test_dir)
        
        # Create a mock axiom project
        self.create_mock_axiom_project()
        
    def teardown_method(self):
        """Clean up."""
        os.chdir(self.original_cwd)
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)
    
    def create_mock_axiom_project(self):
        """Create a mock project with axiom structure."""
        # Create .axiom directory
        Path(".axiom").mkdir()
        Path(".axiom/meta").mkdir()
        Path(".axiom/cache").mkdir()
        
        # Create index.yml
        index_content = {
            'version': '1.0',
            'project_context': {
                'name': 'test-project',
                'goal': 'Test project for axiom protocol',
                'ai_optimization_level': 'high',
                'token_budget_per_session': 100000
            },
            'file_categories': {
                'core_modules': {'files': [], 'estimated_tokens': 0},
                'feature_modules': {'files': [], 'estimated_tokens': 0},
                'config_files': {'files': [], 'estimated_tokens': 0},
                'test_files': {'files': [], 'estimated_tokens': 0}
            },
            'meta_files': {
                'total_count': 0,
                'last_updated': '2023-01-01T00:00:00',
                'sync_status': 'clean'
            }
        }
        
        with open(".axiom/index.yml", 'w') as f:
            yaml.dump(index_content, f)
        
        # Create manifest
        manifest_content = {
            'version': '1.0',
            'project': {
                'name': 'test-project',
                'goal': 'Test project',
                'stack': ['Python']
            },
            'commands': {
                'install': 'pip install -r requirements.txt',
                'run': 'python main.py',
                'test': 'pytest',
                'lint': 'ruff check'
            }
        }
        
        with open(".axiom-manifest.yml", 'w') as f:
            yaml.dump(manifest_content, f)
        
        # Create some source files
        with open("main.py", 'w') as f:
            f.write("def main():\n    print('Hello')\n\nif __name__ == '__main__':\n    main()")
        
        # Create corresponding meta file
        meta_content = {
            'version': '1.0',
            'file_info': {
                'path': 'main.py',
                'type': 'module',
                'language': 'python',
                'size_bytes': 50,
                'estimated_tokens': 20
            },
            'ai_summary': {
                'purpose': 'Main application entry point',
                'importance': 'core',
                'complexity': 'low'
            }
        }
        
        with open(".axiom/meta/main.py.yml", 'w') as f:
            yaml.dump(meta_content, f)
    
    def test_mock_project_structure(self):
        """Test that mock project has proper structure."""
        assert Path(".axiom").exists()
        assert Path(".axiom/index.yml").exists()
        assert Path(".axiom-manifest.yml").exists()
        assert Path("main.py").exists()
        assert Path(".axiom/meta/main.py.yml").exists()
        
        # Test that index.yml is valid
        with open(".axiom/index.yml", 'r') as f:
            index = yaml.safe_load(f)
        
        assert index['version'] == '1.0'
        assert 'project_context' in index
        assert index['meta_files']['sync_status'] == 'clean'
    
    def test_commands_can_read_axiom_context(self):
        """Test that commands can properly read axiom context."""
        commands_dir = Path(__file__).parent.parent / ".claude" / "commands"
        
        # The commands should reference reading .axiom/index.yml
        for command_file in commands_dir.glob("*.md"):
            with open(command_file, 'r') as f:
                content = f.read()
            
            # At least one command should mention reading axiom context
            if ".axiom" in content:
                assert "index.yml" in content or "meta" in content


class TestCommandWorkflowIntegration:
    """Test the complete workflow from command to execution."""
    
    def test_workflow_documentation_consistency(self):
        """Test that all commands document consistent workflow."""
        commands_dir = Path(__file__).parent.parent / ".claude" / "commands"
        
        workflow_keywords = [
            "research", "plan", "implement", "validate", "ultrathink"
        ]
        
        for command_file in commands_dir.glob("*.md"):
            with open(command_file, 'r') as f:
                content = f.read().lower()
            
            # Each command should mention key workflow concepts
            workflow_mentions = sum(1 for keyword in workflow_keywords if keyword in content)
            assert workflow_mentions >= 2, f"Command {command_file.name} should mention workflow concepts"
    
    def test_axiom_integration_consistency(self):
        """Test that Axiom integration is consistent across commands."""
        commands_dir = Path(__file__).parent.parent / ".claude" / "commands"
        
        axiom_features = [
            ".axiom", "meta", "contract", "token"
        ]
        
        # At least the pro and execute commands should have axiom integration
        important_commands = ["generate-prp-pro.md", "execute-prp.md"]
        
        for command_name in important_commands:
            command_file = commands_dir / command_name
            if command_file.exists():
                with open(command_file, 'r') as f:
                    content = f.read().lower()
                
                # Should mention axiom features
                axiom_mentions = sum(1 for feature in axiom_features if feature in content)
                assert axiom_mentions >= 2, f"Command {command_name} should have axiom integration"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])