#!/usr/bin/env python3
"""
Axiom Sync - Automatic meta information synchronization mechanism
Monitors file changes and automatically updates meta information.
"""

import os
import sys
import time
import hashlib
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Set, Optional
import yaml

# Import the meta generator
from axiom_meta_generator import AxiomMetaGenerator


class AxiomSync:
    """Automatic synchronization system for Axiom meta information."""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.generator = AxiomMetaGenerator(str(self.project_root))
        self.cache_file = self.project_root / ".axiom" / "cache" / "sync_cache.yml"
        self.file_hashes: Dict[str, str] = {}
        self.last_sync_time = datetime.now()
        
        # Load cached hashes
        self.load_cache()
        
    def load_cache(self) -> None:
        """Load cached file hashes from previous runs."""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r') as f:
                    cache_data = yaml.safe_load(f) or {}
                self.file_hashes = cache_data.get('file_hashes', {})
                last_sync = cache_data.get('last_sync_time')
                if last_sync:
                    self.last_sync_time = datetime.fromisoformat(last_sync)
            except Exception as e:
                print(f"Warning: Could not load sync cache: {e}")
                self.file_hashes = {}
    
    def save_cache(self) -> None:
        """Save current file hashes to cache."""
        try:
            self.cache_file.parent.mkdir(parents=True, exist_ok=True)
            
            cache_data = {
                'file_hashes': self.file_hashes,
                'last_sync_time': self.last_sync_time.isoformat(),
                'generated_at': datetime.now().isoformat()
            }
            
            with open(self.cache_file, 'w') as f:
                yaml.dump(cache_data, f, default_flow_style=False)
                
        except Exception as e:
            print(f"Warning: Could not save sync cache: {e}")
    
    def calculate_file_hash(self, file_path: Path) -> str:
        """Calculate SHA256 hash of a file."""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            return hashlib.sha256(content).hexdigest()
        except Exception:
            return ""
    
    def scan_for_changes(self) -> Set[str]:
        """Scan for changed files since last sync."""
        changed_files = set()
        
        # Scan all trackable files
        for root, dirs, files in os.walk(self.project_root):
            root_path = Path(root)
            
            # Skip .axiom directory and other excluded directories
            if '.axiom' in root_path.parts:
                continue
                
            for file_name in files:
                file_path = root_path / file_name
                
                if self.generator.should_track_file(file_path):
                    relative_path = str(file_path.relative_to(self.project_root))
                    current_hash = self.calculate_file_hash(file_path)
                    
                    # Check if file is new or changed
                    if relative_path not in self.file_hashes or self.file_hashes[relative_path] != current_hash:
                        changed_files.add(relative_path)
                        self.file_hashes[relative_path] = current_hash
        
        # Check for deleted files
        existing_files = set()
        for root, dirs, files in os.walk(self.project_root):
            root_path = Path(root)
            if '.axiom' in root_path.parts:
                continue
            for file_name in files:
                file_path = root_path / file_name
                if self.generator.should_track_file(file_path):
                    existing_files.add(str(file_path.relative_to(self.project_root)))
        
        deleted_files = set(self.file_hashes.keys()) - existing_files
        for deleted_file in deleted_files:
            del self.file_hashes[deleted_file]
            print(f"File deleted: {deleted_file}")
        
        return changed_files
    
    def sync_meta_for_file(self, relative_path: str) -> bool:
        """Sync meta information for a specific file."""
        file_path = self.project_root / relative_path
        
        if not file_path.exists():
            print(f"File not found: {relative_path}")
            return False
        
        try:
            print(f"Syncing meta for: {relative_path}")
            self.generator.update_meta_for_file(str(file_path))
            return True
        except Exception as e:
            print(f"Error syncing {relative_path}: {e}")
            return False
    
    def update_sync_status(self, status: str = "clean") -> None:
        """Update sync status in index.yml."""
        index_path = self.project_root / ".axiom" / "index.yml"
        
        if not index_path.exists():
            return
        
        try:
            with open(index_path, 'r') as f:
                index = yaml.safe_load(f) or {}
            
            if 'meta_files' not in index:
                index['meta_files'] = {}
            
            index['meta_files']['sync_status'] = status
            index['meta_files']['last_updated'] = datetime.now().isoformat()
            
            with open(index_path, 'w') as f:
                yaml.dump(index, f, default_flow_style=False, sort_keys=False)
                
        except Exception as e:
            print(f"Error updating sync status: {e}")
    
    def full_sync(self) -> None:
        """Perform a full synchronization of all files."""
        print("Performing full sync...")
        
        # Initialize axiom structure if needed
        self.generator.init_axiom_structure()
        
        # Mark as syncing
        self.update_sync_status("syncing")
        
        try:
            # Scan for all changes
            changed_files = self.scan_for_changes()
            
            if not changed_files:
                print("No changes detected.")
            else:
                print(f"Found {len(changed_files)} changed files")
                
                # Update meta for each changed file
                success_count = 0
                for file_path in changed_files:
                    if self.sync_meta_for_file(file_path):
                        success_count += 1
                
                print(f"Successfully synced {success_count}/{len(changed_files)} files")
            
            # Clean orphaned meta files
            self.generator.clean_orphaned_meta()
            
            # Regenerate index
            self.generator.generate_index()
            
            # Update timestamps
            self.last_sync_time = datetime.now()
            
            # Mark as clean
            self.update_sync_status("clean")
            
            # Save cache
            self.save_cache()
            
            print("Full sync completed successfully")
            
        except Exception as e:
            print(f"Full sync failed: {e}")
            self.update_sync_status("error")
            raise
    
    def incremental_sync(self) -> None:
        """Perform incremental sync of only changed files."""
        print("Performing incremental sync...")
        
        # Mark as syncing
        self.update_sync_status("syncing")
        
        try:
            changed_files = self.scan_for_changes()
            
            if not changed_files:
                print("No changes detected.")
                self.update_sync_status("clean")
                return
            
            print(f"Syncing {len(changed_files)} changed files...")
            
            success_count = 0
            for file_path in changed_files:
                if self.sync_meta_for_file(file_path):
                    success_count += 1
            
            # Update index only if we had changes
            if success_count > 0:
                self.generator.generate_index()
            
            self.last_sync_time = datetime.now()
            self.update_sync_status("clean")
            self.save_cache()
            
            print(f"Incremental sync completed: {success_count}/{len(changed_files)} files synced")
            
        except Exception as e:
            print(f"Incremental sync failed: {e}")
            self.update_sync_status("error")
            raise
    
    def watch_mode(self, interval: int = 30) -> None:
        """Watch for file changes and auto-sync."""
        print(f"Starting watch mode with {interval}s interval...")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                try:
                    self.incremental_sync()
                    time.sleep(interval)
                except KeyboardInterrupt:
                    print("\nStopping watch mode...")
                    break
                except Exception as e:
                    print(f"Error in watch mode: {e}")
                    time.sleep(interval)
                    
        except KeyboardInterrupt:
            print("\nWatch mode stopped")
    
    def check_sync_status(self) -> str:
        """Check current sync status."""
        index_path = self.project_root / ".axiom" / "index.yml"
        
        if not index_path.exists():
            return "not_initialized"
        
        try:
            with open(index_path, 'r') as f:
                index = yaml.safe_load(f) or {}
            
            status = index.get('meta_files', {}).get('sync_status', 'unknown')
            return status
            
        except Exception:
            return "error"
    
    def force_file_sync(self, file_path: str) -> None:
        """Force sync a specific file regardless of hash."""
        print(f"Force syncing: {file_path}")
        
        full_path = self.project_root / file_path
        if not full_path.exists():
            print(f"File not found: {file_path}")
            return
        
        # Update hash and sync
        current_hash = self.calculate_file_hash(full_path)
        self.file_hashes[file_path] = current_hash
        
        if self.sync_meta_for_file(file_path):
            self.generator.generate_index()
            self.save_cache()
            print(f"Successfully force synced: {file_path}")
        else:
            print(f"Failed to sync: {file_path}")


def main():
    """Main CLI interface for axiom-sync."""
    parser = argparse.ArgumentParser(description='Axiom automatic synchronization tool')
    parser.add_argument('--project-root', type=str, default='.', 
                       help='Project root directory')
    parser.add_argument('--full-sync', action='store_true',
                       help='Perform full synchronization')
    parser.add_argument('--incremental', action='store_true',
                       help='Perform incremental sync')
    parser.add_argument('--watch', action='store_true',
                       help='Watch for changes and auto-sync')
    parser.add_argument('--interval', type=int, default=30,
                       help='Watch interval in seconds (default: 30)')
    parser.add_argument('--status', action='store_true',
                       help='Check sync status')
    parser.add_argument('--force-file', type=str,
                       help='Force sync specific file')
    
    args = parser.parse_args()
    
    # Create sync instance
    sync = AxiomSync(args.project_root)
    
    try:
        if args.status:
            status = sync.check_sync_status()
            print(f"Sync status: {status}")
            
            if status == "clean":
                print("✅ All meta files are synchronized")
            elif status == "syncing":
                print("🔄 Synchronization in progress")
            elif status == "error":
                print("❌ Synchronization error detected")
            elif status == "not_initialized":
                print("⚠️  Axiom not initialized")
            else:
                print(f"⚠️  Unknown status: {status}")
                
        elif args.force_file:
            sync.force_file_sync(args.force_file)
            
        elif args.watch:
            sync.watch_mode(args.interval)
            
        elif args.incremental:
            sync.incremental_sync()
            
        elif args.full_sync:
            sync.full_sync()
            
        else:
            # Default to incremental sync
            sync.incremental_sync()
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()