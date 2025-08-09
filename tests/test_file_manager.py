"""
Tests for the file manager
"""

import pytest
import shutil
from pathlib import Path

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from core.file_manager import FileManager
from core.encryption import EncryptionEngine

class TestFileManager:
    """Test cases for FileManager"""
    
    def test_init(self):
        """Test file manager initialization"""
        fm = FileManager()
        assert fm.temp_dir is None
    
    def test_folder_encryption_decryption(self, sample_folder, temp_dir):
        """Test folder encryption and decryption"""
        fm = FileManager()
        engine = EncryptionEngine()
        password = "folder_test_password"
        
        encrypted_file = temp_dir / "encrypted_folder.enc"
        decrypted_folder = temp_dir / "decrypted_folder"
        
        # Encrypt folder
        fm.encrypt_folder(sample_folder, encrypted_file, engine, password)
        assert encrypted_file.exists()
        assert encrypted_file.stat().st_size > 0
        
        # Decrypt folder
        fm.decrypt_folder(encrypted_file, decrypted_folder, engine, password)
        assert decrypted_folder.exists()
        assert decrypted_folder.is_dir()
        
        # Verify folder structure is preserved
        assert (decrypted_folder / "file1.txt").exists()
        assert (decrypted_folder / "file2.txt").exists()
        assert (decrypted_folder / "subfolder").exists()
        assert (decrypted_folder / "subfolder" / "file3.txt").exists()
        
        # Verify file contents
        assert (decrypted_folder / "file1.txt").read_text() == "Content of file 1"
        assert (decrypted_folder / "file2.txt").read_text() == "Content of file 2"
        assert (decrypted_folder / "subfolder" / "file3.txt").read_text() == "Content of file 3"
    
    def test_multiple_files_encryption(self, sample_text_file, sample_binary_file, temp_dir):
        """Test batch encryption of multiple files"""
        fm = FileManager()
        engine = EncryptionEngine()
        password = "batch_test_password"
        
        output_dir = temp_dir / "encrypted_output"
        file_paths = [str(sample_text_file), str(sample_binary_file)]
        
        # Encrypt multiple files
        results = fm.encrypt_multiple_files(file_paths, output_dir, engine, password)
        
        assert len(results['successful']) == 2
        assert len(results['failed']) == 0
        assert str(sample_text_file) in results['successful']
        assert str(sample_binary_file) in results['successful']
        
        # Verify encrypted files exist
        assert (output_dir / (sample_text_file.name + '.enc')).exists()
        assert (output_dir / (sample_binary_file.name + '.enc')).exists()
    
    def test_multiple_files_decryption(self, sample_text_file, temp_dir):
        """Test batch decryption of multiple files"""
        fm = FileManager()
        engine = EncryptionEngine()
        password = "batch_decrypt_password"
        
        # First encrypt some files
        encrypted_dir = temp_dir / "encrypted"
        encrypted_dir.mkdir()
        
        encrypted_file1 = encrypted_dir / "file1.enc"
        encrypted_file2 = encrypted_dir / "file2.enc"
        
        engine.encrypt_file(sample_text_file, encrypted_file1, password)
        engine.encrypt_file(sample_text_file, encrypted_file2, password)
        
        # Now decrypt them
        output_dir = temp_dir / "decrypted_output"
        file_paths = [str(encrypted_file1), str(encrypted_file2)]
        
        results = fm.decrypt_multiple_files(file_paths, output_dir, engine, password)
        
        assert len(results['successful']) == 2
        assert len(results['failed']) == 0
        
        # Verify decrypted files exist
        assert (output_dir / "file1").exists()
        assert (output_dir / "file2").exists()
    
    def test_get_folder_info(self, sample_folder):
        """Test getting folder information"""
        fm = FileManager()
        
        info = fm.get_folder_info(sample_folder)
        
        assert info['total_files'] == 3  # file1.txt, file2.txt, subfolder/file3.txt
        assert info['total_size'] > 0
        assert info['total_size_mb'] > 0
        assert info['folder_name'] == sample_folder.name
    
    def test_validate_file_paths(self, sample_text_file, temp_dir):
        """Test file path validation"""
        fm = FileManager()
        
        nonexistent_file = temp_dir / "nonexistent.txt"
        file_paths = [str(sample_text_file), str(nonexistent_file)]
        
        results = fm.validate_file_paths(file_paths)
        
        assert len(results['valid']) == 1
        assert len(results['invalid']) == 1
        assert str(sample_text_file) in results['valid']
        assert results['invalid'][0]['path'] == str(nonexistent_file)
        assert 'does not exist' in results['invalid'][0]['reason']
    
    def test_create_backup(self, sample_text_file, temp_dir):
        """Test file backup creation"""
        fm = FileManager()
        
        backup_path = fm.create_backup(sample_text_file)
        backup_file = Path(backup_path)
        
        assert backup_file.exists()
        assert backup_file.name.endswith('_backup.txt')
        assert backup_file.read_text() == sample_text_file.read_text()
    
    def test_secure_delete_file(self, temp_dir):
        """Test secure file deletion"""
        fm = FileManager()
        
        # Create a test file
        test_file = temp_dir / "to_delete.txt"
        test_file.write_text("This file will be securely deleted")
        
        assert test_file.exists()
        
        # Securely delete it
        fm.secure_delete_file(test_file)
        
        assert not test_file.exists()
    
    def test_get_file_type_stats(self, sample_text_file, sample_binary_file, sample_folder):
        """Test file type statistics"""
        fm = FileManager()
        
        file_paths = [str(sample_text_file), str(sample_binary_file), str(sample_folder)]
        stats = fm.get_file_type_stats(file_paths)
        
        assert stats['total_files'] >= 2  # At least the two direct files
        assert stats['total_folders'] == 1
        assert stats['total_size'] > 0
        assert '.txt' in stats['file_types']
        assert '.bin' in stats['file_types']
    
    def test_is_encrypted_folder(self, temp_dir):
        """Test encrypted folder detection"""
        fm = FileManager()
        
        # This is a simple heuristic test
        folder_file = temp_dir / "my_folder.enc"
        folder_file.touch()
        
        regular_file = temp_dir / "regular_file.enc"
        regular_file.touch()
        
        # Based on current implementation (filename heuristic)
        assert fm.is_encrypted_folder(folder_file)
        assert not fm.is_encrypted_folder(regular_file)
    
    def test_nonexistent_file_encryption(self, temp_dir):
        """Test handling of nonexistent files in batch operations"""
        fm = FileManager()
        engine = EncryptionEngine()
        password = "test_password"
        
        nonexistent_file = temp_dir / "does_not_exist.txt"
        output_dir = temp_dir / "output"
        
        results = fm.encrypt_multiple_files([str(nonexistent_file)], output_dir, engine, password)
        
        assert len(results['successful']) == 0
        assert len(results['failed']) == 1
        assert results['failed'][0]['file'] == str(nonexistent_file)
        assert 'not found' in results['failed'][0]['error'].lower()
    
    def test_empty_folder_encryption(self, temp_dir):
        """Test encryption of empty folder"""
        fm = FileManager()
        engine = EncryptionEngine()
        password = "empty_folder_password"
        
        # Create empty folder
        empty_folder = temp_dir / "empty_folder"
        empty_folder.mkdir()
        
        encrypted_file = temp_dir / "empty_encrypted.enc"
        decrypted_folder = temp_dir / "empty_decrypted"
        
        # Encrypt and decrypt empty folder
        fm.encrypt_folder(empty_folder, encrypted_file, engine, password)
        fm.decrypt_folder(encrypted_file, decrypted_folder, engine, password)
        
        assert decrypted_folder.exists()
        assert decrypted_folder.is_dir()
        # Should be empty
        assert len(list(decrypted_folder.iterdir())) == 0
    
    def test_folder_with_special_characters(self, temp_dir):
        """Test folder encryption with files containing special characters"""
        fm = FileManager()
        engine = EncryptionEngine()
        password = "special_chars_password"
        
        # Create folder with special character filenames
        test_folder = temp_dir / "special_folder"
        test_folder.mkdir()
        
        # Create files with various special characters
        (test_folder / "file with spaces.txt").write_text("Content 1")
        (test_folder / "file-with-dashes.txt").write_text("Content 2")
        (test_folder / "file_with_underscores.txt").write_text("Content 3")
        
        encrypted_file = temp_dir / "special_encrypted.enc"
        decrypted_folder = temp_dir / "special_decrypted"
        
        # Encrypt and decrypt
        fm.encrypt_folder(test_folder, encrypted_file, engine, password)
        fm.decrypt_folder(encrypted_file, decrypted_folder, engine, password)
        
        # Verify all files are preserved
        assert (decrypted_folder / "file with spaces.txt").exists()
        assert (decrypted_folder / "file-with-dashes.txt").exists()
        assert (decrypted_folder / "file_with_underscores.txt").exists()
        
        # Verify contents
        assert (decrypted_folder / "file with spaces.txt").read_text() == "Content 1"
        assert (decrypted_folder / "file-with-dashes.txt").read_text() == "Content 2"
        assert (decrypted_folder / "file_with_underscores.txt").read_text() == "Content 3"
