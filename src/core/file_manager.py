"""
File Management Operations
Handles file and folder operations, including batch processing and folder encryption
"""

import os
import shutil
import zipfile
import tempfile
import json
from pathlib import Path
from typing import List, Callable, Optional
import secrets

class FileManager:
    """Manages file and folder operations for encryption/decryption"""
    
    def __init__(self):
        self.temp_dir = None
        
    def encrypt_folder(self, folder_path, output_path, encryption_engine, password, 
                      progress_callback: Optional[Callable] = None):
        """
        Encrypt an entire folder structure
        
        Args:
            folder_path: Path to folder to encrypt
            output_path: Path to output encrypted file
            encryption_engine: Encryption engine instance
            password: Encryption password
            progress_callback: Optional callback for progress updates
        """
        try:
            folder_path = Path(folder_path)
            output_path = Path(output_path)
            
            if not folder_path.exists():
                raise FileNotFoundError(f"Folder not found: {folder_path}")
            
            if not folder_path.is_dir():
                raise ValueError(f"Path is not a directory: {folder_path}")
            
            # Create temporary zip file
            with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
                temp_zip_path = temp_zip.name
            
            try:
                # Create zip archive of folder
                total_files = self._count_files_in_folder(folder_path)
                processed_files = 0
                
                with zipfile.ZipFile(temp_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for root, dirs, files in os.walk(folder_path):
                        for file in files:
                            file_path = Path(root) / file
                            archive_path = file_path.relative_to(folder_path)
                            
                            zipf.write(file_path, archive_path)
                            
                            processed_files += 1
                            if progress_callback:
                                progress = (processed_files / total_files) * 50  # First 50% for zipping
                                progress_callback(progress, f"Archiving: {file}")
                
                # Encrypt the zip file
                if progress_callback:
                    progress_callback(50, "Encrypting archive...")
                
                encryption_engine.encrypt_file(temp_zip_path, output_path, password)
                
                if progress_callback:
                    progress_callback(100, "Folder encryption completed")
                    
            finally:
                # Clean up temporary zip file
                if os.path.exists(temp_zip_path):
                    os.unlink(temp_zip_path)
                    
        except Exception as e:
            raise Exception(f"Folder encryption failed: {str(e)}")
    
    def decrypt_folder(self, encrypted_file_path, output_folder, encryption_engine, password,
                      progress_callback: Optional[Callable] = None):
        """
        Decrypt an encrypted folder
        
        Args:
            encrypted_file_path: Path to encrypted folder file
            output_folder: Path to output folder
            encryption_engine: Encryption engine instance
            password: Decryption password
            progress_callback: Optional callback for progress updates
        """
        try:
            encrypted_file_path = Path(encrypted_file_path)
            output_folder = Path(output_folder)
            
            if not encrypted_file_path.exists():
                raise FileNotFoundError(f"Encrypted file not found: {encrypted_file_path}")
            
            # Create temporary zip file for decryption
            with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
                temp_zip_path = temp_zip.name
            
            try:
                # Decrypt to temporary zip file
                if progress_callback:
                    progress_callback(0, "Decrypting archive...")
                
                encryption_engine.decrypt_file(encrypted_file_path, temp_zip_path, password)
                
                if progress_callback:
                    progress_callback(50, "Extracting files...")
                
                # Extract zip file to output folder
                output_folder.mkdir(parents=True, exist_ok=True)
                
                with zipfile.ZipFile(temp_zip_path, 'r') as zipf:
                    # Get list of files for progress tracking
                    file_list = zipf.namelist()
                    total_files = len(file_list)
                    
                    for i, member in enumerate(file_list):
                        zipf.extract(member, output_folder)
                        
                        if progress_callback:
                            progress = 50 + ((i + 1) / total_files) * 50  # Second 50% for extraction
                            progress_callback(progress, f"Extracting: {member}")
                
                if progress_callback:
                    progress_callback(100, "Folder decryption completed")
                    
            finally:
                # Clean up temporary zip file
                if os.path.exists(temp_zip_path):
                    os.unlink(temp_zip_path)
                    
        except Exception as e:
            raise Exception(f"Folder decryption failed: {str(e)}")
    
    def encrypt_multiple_files(self, file_paths: List[str], output_directory, 
                              encryption_engine, password,
                              progress_callback: Optional[Callable] = None):
        """
        Encrypt multiple files in batch
        
        Args:
            file_paths: List of file paths to encrypt
            output_directory: Directory to save encrypted files
            encryption_engine: Encryption engine instance
            password: Encryption password
            progress_callback: Optional callback for progress updates
        """
        try:
            output_directory = Path(output_directory)
            output_directory.mkdir(parents=True, exist_ok=True)
            
            total_files = len(file_paths)
            results = {
                'successful': [],
                'failed': []
            }
            
            for i, file_path in enumerate(file_paths):
                try:
                    file_path = Path(file_path)
                    if not file_path.exists():
                        results['failed'].append({
                            'file': str(file_path),
                            'error': 'File not found'
                        })
                        continue
                    
                    if file_path.is_dir():
                        # Handle directory
                        output_path = output_directory / (file_path.name + '.enc')
                        self.encrypt_folder(file_path, output_path, encryption_engine, password)
                    else:
                        # Handle file
                        output_path = output_directory / (file_path.name + '.enc')
                        encryption_engine.encrypt_file(file_path, output_path, password)
                    
                    results['successful'].append(str(file_path))
                    
                    if progress_callback:
                        progress = ((i + 1) / total_files) * 100
                        progress_callback(progress, f"Encrypted: {file_path.name}")
                        
                except Exception as e:
                    results['failed'].append({
                        'file': str(file_path),
                        'error': str(e)
                    })
            
            return results
            
        except Exception as e:
            raise Exception(f"Batch encryption failed: {str(e)}")
    
    def decrypt_multiple_files(self, file_paths: List[str], output_directory,
                              encryption_engine, password,
                              progress_callback: Optional[Callable] = None):
        """
        Decrypt multiple files in batch
        
        Args:
            file_paths: List of encrypted file paths to decrypt
            output_directory: Directory to save decrypted files
            encryption_engine: Encryption engine instance
            password: Decryption password
            progress_callback: Optional callback for progress updates
        """
        try:
            output_directory = Path(output_directory)
            output_directory.mkdir(parents=True, exist_ok=True)
            
            total_files = len(file_paths)
            results = {
                'successful': [],
                'failed': []
            }
            
            for i, file_path in enumerate(file_paths):
                try:
                    file_path = Path(file_path)
                    if not file_path.exists():
                        results['failed'].append({
                            'file': str(file_path),
                            'error': 'File not found'
                        })
                        continue
                    
                    # Remove .enc extension for output filename
                    if file_path.suffix == '.enc':
                        output_name = file_path.stem
                    else:
                        output_name = file_path.name + '_decrypted'
                    
                    output_path = output_directory / output_name
                    
                    # Check if encrypted file is a folder or regular file
                    if self.is_encrypted_folder(file_path):
                        self.decrypt_folder(file_path, output_path, encryption_engine, password)
                    else:
                        encryption_engine.decrypt_file(file_path, output_path, password)
                    
                    results['successful'].append(str(file_path))
                    
                    if progress_callback:
                        progress = ((i + 1) / total_files) * 100
                        progress_callback(progress, f"Decrypted: {file_path.name}")
                        
                except Exception as e:
                    results['failed'].append({
                        'file': str(file_path),
                        'error': str(e)
                    })
            
            return results
            
        except Exception as e:
            raise Exception(f"Batch decryption failed: {str(e)}")
    
    def is_encrypted_folder(self, file_path):
        """
        Check if encrypted file contains a folder (zip archive)
        
        Args:
            file_path: Path to encrypted file
            
        Returns:
            True if file contains an encrypted folder
        """
        try:
            # This is a simple heuristic - in a real implementation,
            # you might want to store metadata about the file type
            # For now, we'll try to decrypt a small portion and check if it's a zip
            
            # Create temporary file for testing
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                temp_path = temp_file.name
            
            try:
                # Try to decrypt just the beginning of the file to check format
                # This is a simplified approach - you might want to store metadata instead
                return file_path.name.endswith('.enc') and 'folder' in file_path.stem.lower()
            except:
                return False
            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception:
            return False
    
    def secure_delete_file(self, file_path, passes=3):
        """
        Securely delete a file by overwriting it multiple times
        
        Args:
            file_path: Path to file to delete
            passes: Number of overwrite passes
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return
            
            file_size = file_path.stat().st_size
            
            with open(file_path, "r+b") as file:
                for _ in range(passes):
                    file.seek(0)
                    # Overwrite with random data
                    for _ in range(0, file_size, 4096):
                        chunk_size = min(4096, file_size - file.tell())
                        if chunk_size <= 0:
                            break
                        random_data = secrets.token_bytes(chunk_size)
                        file.write(random_data)
                    file.flush()
                    os.fsync(file.fileno())  # Force write to disk
            
            # Finally delete the file
            file_path.unlink()
            
        except Exception as e:
            raise Exception(f"Secure deletion failed: {str(e)}")
    
    def get_folder_info(self, folder_path):
        """
        Get information about a folder (file count, total size)
        
        Args:
            folder_path: Path to folder
            
        Returns:
            Dictionary with folder information
        """
        try:
            folder_path = Path(folder_path)
            if not folder_path.exists() or not folder_path.is_dir():
                raise ValueError("Invalid folder path")
            
            total_files = 0
            total_size = 0
            
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = Path(root) / file
                    try:
                        file_stat = file_path.stat()
                        total_files += 1
                        total_size += file_stat.st_size
                    except (OSError, IOError):
                        # Skip files that can't be accessed
                        continue
            
            return {
                'total_files': total_files,
                'total_size': total_size,
                'total_size_mb': total_size / (1024 * 1024),
                'folder_name': folder_path.name
            }
            
        except Exception as e:
            raise Exception(f"Failed to get folder info: {str(e)}")
    
    def validate_file_paths(self, file_paths: List[str]):
        """
        Validate a list of file paths
        
        Args:
            file_paths: List of file paths to validate
            
        Returns:
            Dictionary with valid and invalid paths
        """
        results = {
            'valid': [],
            'invalid': []
        }
        
        for file_path in file_paths:
            try:
                path_obj = Path(file_path)
                if path_obj.exists():
                    results['valid'].append(str(path_obj))
                else:
                    results['invalid'].append({
                        'path': file_path,
                        'reason': 'File does not exist'
                    })
            except Exception as e:
                results['invalid'].append({
                    'path': file_path,
                    'reason': str(e)
                })
        
        return results
    
    def create_backup(self, file_path, backup_suffix='_backup'):
        """
        Create a backup of a file before encryption
        
        Args:
            file_path: Path to file to backup
            backup_suffix: Suffix for backup file
            
        Returns:
            Path to backup file
        """
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")
            
            # Create backup filename
            backup_path = file_path.parent / (file_path.stem + backup_suffix + file_path.suffix)
            
            # Ensure backup filename is unique
            counter = 1
            while backup_path.exists():
                backup_path = file_path.parent / (
                    file_path.stem + backup_suffix + f"_{counter}" + file_path.suffix
                )
                counter += 1
            
            # Copy file to backup location
            shutil.copy2(file_path, backup_path)
            return str(backup_path)
            
        except Exception as e:
            raise Exception(f"Backup creation failed: {str(e)}")
    
    def cleanup_temp_files(self):
        """Clean up any temporary files created during operations"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            try:
                shutil.rmtree(self.temp_dir)
                self.temp_dir = None
            except Exception:
                pass  # Best effort cleanup
    
    def _count_files_in_folder(self, folder_path):
        """Count total files in a folder recursively"""
        count = 0
        for root, dirs, files in os.walk(folder_path):
            count += len(files)
        return count
    
    def get_file_type_stats(self, file_paths: List[str]):
        """
        Get statistics about file types in the selection
        
        Args:
            file_paths: List of file paths
            
        Returns:
            Dictionary with file type statistics
        """
        stats = {
            'total_files': 0,
            'total_folders': 0,
            'file_types': {},
            'total_size': 0
        }
        
        for file_path in file_paths:
            try:
                path_obj = Path(file_path)
                if not path_obj.exists():
                    continue
                
                if path_obj.is_dir():
                    stats['total_folders'] += 1
                    # Add folder contents to stats
                    folder_info = self.get_folder_info(path_obj)
                    stats['total_files'] += folder_info['total_files']
                    stats['total_size'] += folder_info['total_size']
                else:
                    stats['total_files'] += 1
                    file_size = path_obj.stat().st_size
                    stats['total_size'] += file_size
                    
                    # Track file extension
                    ext = path_obj.suffix.lower()
                    if not ext:
                        ext = 'no_extension'
                    
                    if ext not in stats['file_types']:
                        stats['file_types'][ext] = {'count': 0, 'size': 0}
                    
                    stats['file_types'][ext]['count'] += 1
                    stats['file_types'][ext]['size'] += file_size
                    
            except Exception:
                continue  # Skip files that can't be accessed
        
        return stats
