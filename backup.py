#!/usr/bin/env python3
"""
Backup system for gnS (Genius) Member Directory
Automatically backs up member data and uploaded photos
"""

import os
import json
import shutil
import zipfile
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BackupManager:
    def __init__(self, data_file='members.json', uploads_dir='static/uploads', backup_dir='backups'):
        self.data_file = data_file
        self.uploads_dir = uploads_dir
        self.backup_dir = backup_dir
        self._ensure_backup_dir()
    
    def _ensure_backup_dir(self):
        """Ensure backup directory exists"""
        os.makedirs(self.backup_dir, exist_ok=True)
    
    def create_backup(self):
        """Create a complete backup of data and files"""
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"gns_backup_{timestamp}"
            backup_path = os.path.join(self.backup_dir, f"{backup_name}.zip")
            
            with zipfile.ZipFile(backup_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                # Backup data file
                if os.path.exists(self.data_file):
                    zipf.write(self.data_file, f"data/{self.data_file}")
                    logger.info(f"Backed up data file: {self.data_file}")
                
                # Backup uploaded photos
                if os.path.exists(self.uploads_dir):
                    for root, dirs, files in os.walk(self.uploads_dir):
                        for file in files:
                            if file != '.gitkeep':  # Skip .gitkeep file
                                file_path = os.path.join(root, file)
                                arc_path = os.path.join('uploads', os.path.relpath(file_path, self.uploads_dir))
                                zipf.write(file_path, arc_path)
                    logger.info(f"Backed up uploads directory: {self.uploads_dir}")
                
                # Add backup metadata
                metadata = {
                    'backup_date': datetime.now().isoformat(),
                    'backup_version': '1.0',
                    'app_version': 'gnS v1.0',
                    'files_count': len(zipf.namelist())
                }
                zipf.writestr('backup_metadata.json', json.dumps(metadata, indent=2))
            
            logger.info(f"Backup created successfully: {backup_path}")
            return backup_path
            
        except Exception as e:
            logger.error(f"Error creating backup: {str(e)}")
            raise e
    
    def restore_backup(self, backup_path):
        """Restore from a backup file"""
        try:
            if not os.path.exists(backup_path):
                raise FileNotFoundError(f"Backup file not found: {backup_path}")
            
            # Create restore directory
            restore_dir = f"restore_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(restore_dir, exist_ok=True)
            
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(restore_dir)
                
                # Restore data file
                data_backup_path = os.path.join(restore_dir, 'data', self.data_file)
                if os.path.exists(data_backup_path):
                    shutil.copy2(data_backup_path, self.data_file)
                    logger.info(f"Restored data file: {self.data_file}")
                
                # Restore uploads
                uploads_backup_path = os.path.join(restore_dir, 'uploads')
                if os.path.exists(uploads_backup_path):
                    if os.path.exists(self.uploads_dir):
                        shutil.rmtree(self.uploads_dir)
                    shutil.copytree(uploads_backup_path, self.uploads_dir)
                    logger.info(f"Restored uploads directory: {self.uploads_dir}")
            
            # Clean up restore directory
            shutil.rmtree(restore_dir)
            logger.info(f"Backup restored successfully from: {backup_path}")
            
        except Exception as e:
            logger.error(f"Error restoring backup: {str(e)}")
            raise e
    
    def list_backups(self):
        """List all available backups"""
        try:
            backups = []
            if os.path.exists(self.backup_dir):
                for file in os.listdir(self.backup_dir):
                    if file.endswith('.zip') and file.startswith('gns_backup_'):
                        file_path = os.path.join(self.backup_dir, file)
                        stat = os.stat(file_path)
                        backups.append({
                            'filename': file,
                            'path': file_path,
                            'size': stat.st_size,
                            'created': datetime.fromtimestamp(stat.st_ctime).isoformat(),
                            'modified': datetime.fromtimestamp(stat.st_mtime).isoformat()
                        })
            
            # Sort by creation date (newest first)
            backups.sort(key=lambda x: x['created'], reverse=True)
            return backups
            
        except Exception as e:
            logger.error(f"Error listing backups: {str(e)}")
            return []
    
    def cleanup_old_backups(self, keep_count=10):
        """Remove old backups, keeping only the specified number"""
        try:
            backups = self.list_backups()
            if len(backups) > keep_count:
                for backup in backups[keep_count:]:
                    os.remove(backup['path'])
                    logger.info(f"Removed old backup: {backup['filename']}")
                
                logger.info(f"Cleanup completed. Kept {keep_count} most recent backups.")
            
        except Exception as e:
            logger.error(f"Error during backup cleanup: {str(e)}")
    
    def get_backup_stats(self):
        """Get backup statistics"""
        try:
            backups = self.list_backups()
            total_size = sum(backup['size'] for backup in backups)
            
            stats = {
                'total_backups': len(backups),
                'total_size_bytes': total_size,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'latest_backup': backups[0] if backups else None,
                'oldest_backup': backups[-1] if backups else None
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting backup stats: {str(e)}")
            return {}

def main():
    """Command line interface for backup operations"""
    import sys
    
    backup_manager = BackupManager()
    
    if len(sys.argv) < 2:
        print("Usage: python backup.py [create|list|stats|cleanup]")
        return
    
    command = sys.argv[1].lower()
    
    if command == 'create':
        print("Creating backup...")
        backup_path = backup_manager.create_backup()
        print(f"Backup created: {backup_path}")
        
    elif command == 'list':
        print("Available backups:")
        backups = backup_manager.list_backups()
        for backup in backups:
            size_mb = round(backup['size'] / (1024 * 1024), 2)
            print(f"  {backup['filename']} ({size_mb} MB) - {backup['created']}")
        
    elif command == 'stats':
        print("Backup statistics:")
        stats = backup_manager.get_backup_stats()
        print(f"  Total backups: {stats.get('total_backups', 0)}")
        print(f"  Total size: {stats.get('total_size_mb', 0)} MB")
        if stats.get('latest_backup'):
            print(f"  Latest backup: {stats['latest_backup']['filename']}")
        
    elif command == 'cleanup':
        print("Cleaning up old backups...")
        backup_manager.cleanup_old_backups()
        print("Cleanup completed.")
        
    else:
        print(f"Unknown command: {command}")
        print("Available commands: create, list, stats, cleanup")

if __name__ == '__main__':
    main()
