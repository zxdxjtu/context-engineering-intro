#!/usr/bin/env python3
"""
Axiom Meta Generator
Generates and maintains .axiom directory structure with AI-optimized metadata.
"""

import os
import sys
import yaml
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse

class AxiomMetaGenerator:
    """Generates and maintains axiom metadata for AI-optimized codebase understanding."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.axiom_dir = self.project_root / ".axiom"
        self.meta_dir = self.axiom_dir / "meta" 
        self.cache_dir = self.axiom_dir / "cache"
        
        # File type mappings
        self.file_types = {
            '.py': 'python',
            '.js': 'javascript', 
            '.ts': 'typescript',
            '.tsx': 'typescript',
            '.jsx': 'javascript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.md': 'markdown',
            '.yml': 'yaml',
            '.yaml': 'yaml',
            '.json': 'json',
            '.toml': 'toml',
            '.sh': 'shell',
            '.sql': 'sql'
        }
        
        # Token estimation (rough)
        self.token_multipliers = {
            'python': 0.4,
            'javascript': 0.3,
            'typescript': 0.35,
            'java': 0.45,
            'cpp': 0.5,
            'c': 0.5,
            'go': 0.4,
            'rust': 0.45,
            'markdown': 0.25,
            'yaml': 0.2,
            'json': 0.15,
            'shell': 0.3,
            'sql': 0.35
        }
        
    def init_axiom_structure(self) -> None:
        """Initialize .axiom directory structure."""
        self.axiom_dir.mkdir(exist_ok=True)
        self.meta_dir.mkdir(exist_ok=True)
        self.cache_dir.mkdir(exist_ok=True)
        
        # Create initial index if it doesn't exist
        index_path = self.axiom_dir / "index.yml"
        if not index_path.exists():
            self.generate_index()
            
    def should_track_file(self, file_path: Path) -> bool:
        """Determine if a file should be tracked in axiom metadata."""
        # Skip hidden files, cache, build artifacts
        if file_path.name.startswith('.'):
            return False
            
        # Skip common build/cache directories
        skip_dirs = {
            'node_modules', '__pycache__', '.git', 'build', 'dist', 
            'target', '.pytest_cache', '.axiom', 'venv', 'env'
        }
        
        if any(part in skip_dirs for part in file_path.parts):
            return False
            
        # Only track files with known extensions or important config files
        important_files = {'Dockerfile', 'Makefile', 'README.md', 'LICENSE'}
        if file_path.name in important_files:
            return True
            
        return file_path.suffix in self.file_types
        
    def estimate_tokens(self, file_path: Path) -> int:
        """Estimate token count for a file."""
        try:
            size_bytes = file_path.stat().st_size
            language = self.file_types.get(file_path.suffix, 'text')
            multiplier = self.token_multipliers.get(language, 0.3)
            return int(size_bytes * multiplier)
        except:
            return 0
            
    def determine_file_type(self, file_path: Path) -> str:
        """Determine the type/category of a file."""
        name = file_path.name.lower()
        
        if 'test' in name or file_path.parent.name == 'tests':
            return 'test'
        elif name in ['config.py', 'settings.py', 'package.json', 'requirements.txt']:
            return 'config'
        elif file_path.suffix in ['.py', '.js', '.ts', '.tsx', '.jsx']:
            return 'module'
        elif file_path.suffix == '.md':
            return 'doc'
        else:
            return 'script'
            
    def determine_importance(self, file_path: Path) -> str:
        """Determine the importance level of a file."""
        name = file_path.name.lower()
        
        # Core files
        if name in ['main.py', 'index.js', 'app.py', '__init__.py']:
            return 'core'
        
        # Test files
        if 'test' in name:
            return 'test'
            
        # Configuration
        if name in ['config.py', 'settings.py', 'package.json']:
            return 'core'
            
        # Regular feature files
        return 'feature'
        
    def analyze_file_relationships(self, file_path: Path) -> Dict[str, List[str]]:
        """Analyze imports and dependencies for a file."""
        relationships = {
            'imports': [],
            'imported_by': [],
            'depends_on': [],
            'similar_files': []
        }
        
        try:
            content = file_path.read_text(encoding='utf-8')
            
            # Simple import detection (can be enhanced)
            if file_path.suffix == '.py':
                import re
                imports = re.findall(r'from\s+(\S+)\s+import|import\s+(\S+)', content)
                for imp in imports:
                    module = imp[0] if imp[0] else imp[1]
                    if not module.startswith('.'):  # Skip relative imports for now
                        relationships['imports'].append(module)
                        
        except Exception:
            pass
            
        return relationships
        
    def generate_file_meta(self, file_path: Path) -> Dict[str, Any]:
        """Generate metadata for a single file."""
        relative_path = file_path.relative_to(self.project_root)
        
        # Basic file info
        stat = file_path.stat()
        file_type = self.determine_file_type(file_path)
        language = self.file_types.get(file_path.suffix, 'text')
        estimated_tokens = self.estimate_tokens(file_path)
        importance = self.determine_importance(file_path)
        
        # Analyze relationships
        relationships = self.analyze_file_relationships(file_path)
        
        # Generate purpose (simple heuristic, can be enhanced with AI)
        purpose = f"Handles {file_path.stem} functionality"
        if file_type == 'test':
            purpose = f"Tests for {file_path.stem} module"
        elif file_type == 'config':
            purpose = f"Configuration settings for the project"
            
        meta = {
            'version': '1.0',
            'generated_at': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat(),
            'file_info': {
                'path': str(relative_path),
                'type': file_type,
                'language': language,
                'size_bytes': stat.st_size,
                'estimated_tokens': estimated_tokens
            },
            'ai_summary': {
                'purpose': purpose,
                'complexity': 'medium',  # Can be enhanced with analysis
                'importance': importance,
                'key_concepts': [],
                'reading_priority': 'important' if importance == 'core' else 'optional',
                'context_dependencies': []
            },
            'code_structure': {
                'exports': [],
                'imports': relationships['imports'],
                'main_functions': [],
                'data_structures': []
            },
            'ai_hints': {
                'skippable_sections': [],
                'critical_lines': [],
                'patterns': []
            },
            'relationships': relationships,
            'change_tracking': {
                'last_significant_change': datetime.now().isoformat(),
                'change_frequency': 'medium',
                'stability': 'stable'
            },
            'contract_file': str(relative_path.with_suffix('.contract.yml')) if (self.project_root / str(relative_path.with_suffix('.contract.yml'))).exists() else None
        }
        
        return meta
        
    def save_file_meta(self, file_path: Path, meta: Dict[str, Any]) -> None:
        """Save metadata for a file."""
        relative_path = file_path.relative_to(self.project_root)
        meta_path = self.meta_dir / f"{relative_path}.yml"
        
        # Create directory structure
        meta_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save metadata
        with open(meta_path, 'w') as f:
            yaml.dump(meta, f, default_flow_style=False, sort_keys=False)
            
    def scan_and_generate_meta(self) -> Dict[str, Any]:
        """Scan project and generate metadata for all trackable files."""
        stats = {
            'total_files': 0,
            'total_tokens': 0,
            'files_by_type': {},
            'files_by_importance': {}
        }
        
        for root, dirs, files in os.walk(self.project_root):
            root_path = Path(root)
            
            # Skip axiom directory and other excluded directories
            if '.axiom' in root_path.parts:
                continue
                
            for file_name in files:
                file_path = root_path / file_name
                
                if self.should_track_file(file_path):
                    print(f"Processing: {file_path.relative_to(self.project_root)}")
                    
                    meta = self.generate_file_meta(file_path)
                    self.save_file_meta(file_path, meta)
                    
                    # Update stats
                    stats['total_files'] += 1
                    stats['total_tokens'] += meta['file_info']['estimated_tokens']
                    
                    file_type = meta['file_info']['type']
                    importance = meta['ai_summary']['importance']
                    
                    stats['files_by_type'][file_type] = stats['files_by_type'].get(file_type, 0) + 1
                    stats['files_by_importance'][importance] = stats['files_by_importance'].get(importance, 0) + 1
                    
        return stats
        
    def generate_index(self) -> None:
        """Generate or update the main index.yml file."""
        # Scan for all meta files
        meta_files = []
        file_categories = {
            'core_modules': {'files': [], 'estimated_tokens': 0},
            'feature_modules': {'files': [], 'estimated_tokens': 0},
            'config_files': {'files': [], 'estimated_tokens': 0},
            'test_files': {'files': [], 'estimated_tokens': 0}
        }
        
        if self.meta_dir.exists():
            for meta_file in self.meta_dir.rglob("*.yml"):
                try:
                    with open(meta_file, 'r') as f:
                        meta = yaml.safe_load(f)
                        
                    file_path = meta['file_info']['path']
                    importance = meta['ai_summary']['importance']
                    file_type = meta['file_info']['type']
                    tokens = meta['file_info']['estimated_tokens']
                    
                    meta_files.append(file_path)
                    
                    # Categorize files
                    if importance == 'core':
                        file_categories['core_modules']['files'].append(file_path)
                        file_categories['core_modules']['estimated_tokens'] += tokens
                    elif file_type == 'test':
                        file_categories['test_files']['files'].append(file_path)
                        file_categories['test_files']['estimated_tokens'] += tokens
                    elif file_type == 'config':
                        file_categories['config_files']['files'].append(file_path)
                        file_categories['config_files']['estimated_tokens'] += tokens
                    else:
                        file_categories['feature_modules']['files'].append(file_path)
                        file_categories['feature_modules']['estimated_tokens'] += tokens
                        
                except Exception as e:
                    print(f"Error reading {meta_file}: {e}")
                    
        index = {
            'version': '1.0',
            'generated_at': datetime.now().isoformat(),
            'project_root': '.',
            'project_context': {
                'name': self.project_root.name,
                'goal': 'AI-optimized project with comprehensive metadata',
                'ai_optimization_level': 'high',
                'token_budget_per_session': 100000
            },
            'file_categories': file_categories,
            'dependency_clusters': {},
            'ai_shortcuts': {
                'entry_points': [],
                'critical_interfaces': [],
                'data_models': [],
                'external_apis': []
            },
            'meta_files': {
                'total_count': len(meta_files),
                'last_updated': datetime.now().isoformat(),
                'sync_status': 'clean'
            }
        }
        
        # Save index
        index_path = self.axiom_dir / "index.yml"
        with open(index_path, 'w') as f:
            yaml.dump(index, f, default_flow_style=False, sort_keys=False)
            
    def update_meta_for_file(self, file_path: str) -> None:
        """Update metadata for a specific file."""
        file_path = Path(file_path)
        if self.should_track_file(file_path) and file_path.exists():
            meta = self.generate_file_meta(file_path)
            self.save_file_meta(file_path, meta)
            print(f"Updated meta for: {file_path}")
        else:
            print(f"Skipping: {file_path}")
            
    def clean_orphaned_meta(self) -> None:
        """Remove metadata files for which source files no longer exist."""
        if not self.meta_dir.exists():
            return
            
        for meta_file in self.meta_dir.rglob("*.yml"):
            # Extract original file path
            relative_meta = meta_file.relative_to(self.meta_dir)
            original_path = self.project_root / str(relative_meta)[:-4]  # Remove .yml
            
            if not original_path.exists():
                print(f"Removing orphaned meta: {meta_file}")
                meta_file.unlink()
                
                # Remove empty directories
                try:
                    meta_file.parent.rmdir()
                except:
                    pass

def main():
    parser = argparse.ArgumentParser(description='Axiom Meta Generator')
    parser.add_argument('--init', action='store_true', help='Initialize axiom structure')
    parser.add_argument('--scan', action='store_true', help='Scan and generate all metadata')
    parser.add_argument('--update', type=str, help='Update metadata for specific file')
    parser.add_argument('--clean', action='store_true', help='Clean orphaned metadata')
    parser.add_argument('--project-root', type=str, default='.', help='Project root directory')
    
    args = parser.parse_args()
    
    generator = AxiomMetaGenerator(args.project_root)
    
    if args.init:
        print("Initializing axiom structure...")
        generator.init_axiom_structure()
        print("Axiom structure initialized.")
        
    if args.scan:
        print("Scanning project and generating metadata...")
        generator.init_axiom_structure()
        stats = generator.scan_and_generate_meta()
        generator.generate_index()
        
        print(f"\nGeneration complete:")
        print(f"  Total files: {stats['total_files']}")
        print(f"  Total estimated tokens: {stats['total_tokens']:,}")
        print(f"  Files by type: {stats['files_by_type']}")
        print(f"  Files by importance: {stats['files_by_importance']}")
        
    if args.update:
        generator.update_meta_for_file(args.update)
        generator.generate_index()
        
    if args.clean:
        print("Cleaning orphaned metadata...")
        generator.clean_orphaned_meta()
        generator.generate_index()
        
    if not any([args.init, args.scan, args.update, args.clean]):
        parser.print_help()

if __name__ == "__main__":
    main()