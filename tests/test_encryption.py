"""
Tests for the encryption engine
"""

import pytest
import os
from pathlib import Path
import tempfile

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from core.encryption import EncryptionEngine

class TestEncryptionEngine:
    """Test cases for EncryptionEngine"""
    
    def test_init_default(self):
        """Test engine initialization with defaults"""
        engine = EncryptionEngine()
        assert engine.algorithm == 'AES-256-GCM'
        assert engine.pbkdf2_iterations == 100000
    
    def test_init_custom(self):
        """Test engine initialization with custom parameters"""
        engine = EncryptionEngine(algorithm='AES-256-CBC', pbkdf2_iterations=150000)
        assert engine.algorithm == 'AES-256-CBC'
        assert engine.pbkdf2_iterations == 150000
    
    def test_key_derivation(self):
        """Test key derivation from password"""
        engine = EncryptionEngine()
        password = "test_password_123"
        salt = b'test_salt_16_bytes'
        
        key1 = engine._derive_key(password, salt)
        key2 = engine._derive_key(password, salt)
        
        # Same password and salt should produce same key
        assert key1 == key2
        assert len(key1) == 32  # 256-bit key
        
        # Different salt should produce different key
        different_salt = b'different_salt16'
        key3 = engine._derive_key(password, different_salt)
        assert key1 != key3
    
    def test_file_encryption_decryption(self, sample_text_file, temp_dir):
        """Test file encryption and decryption"""
        engine = EncryptionEngine()
        password = "secure_password_123!"
        
        encrypted_file = temp_dir / "encrypted.enc"
        decrypted_file = temp_dir / "decrypted.txt"
        
        # Read original content
        original_content = sample_text_file.read_text()
        
        # Encrypt file
        engine.encrypt_file(sample_text_file, encrypted_file, password)
        assert encrypted_file.exists()
        assert encrypted_file.stat().st_size > 0
        
        # Verify encrypted file is different from original
        with open(encrypted_file, 'rb') as f:
            encrypted_content = f.read()
        assert original_content.encode() not in encrypted_content
        
        # Decrypt file
        engine.decrypt_file(encrypted_file, decrypted_file, password)
        assert decrypted_file.exists()
        
        # Verify decrypted content matches original
        decrypted_content = decrypted_file.read_text()
        assert decrypted_content == original_content
    
    def test_binary_file_encryption(self, sample_binary_file, temp_dir):
        """Test encryption of binary files"""
        engine = EncryptionEngine()
        password = "binary_test_password"
        
        encrypted_file = temp_dir / "binary_encrypted.enc"
        decrypted_file = temp_dir / "binary_decrypted.bin"
        
        # Read original binary content
        original_content = sample_binary_file.read_bytes()
        
        # Encrypt and decrypt
        engine.encrypt_file(sample_binary_file, encrypted_file, password)
        engine.decrypt_file(encrypted_file, decrypted_file, password)
        
        # Verify binary content is preserved
        decrypted_content = decrypted_file.read_bytes()
        assert decrypted_content == original_content
    
    def test_wrong_password(self, sample_text_file, temp_dir):
        """Test decryption with wrong password fails"""
        engine = EncryptionEngine()
        correct_password = "correct_password"
        wrong_password = "wrong_password"
        
        encrypted_file = temp_dir / "encrypted.enc"
        decrypted_file = temp_dir / "decrypted.txt"
        
        # Encrypt with correct password
        engine.encrypt_file(sample_text_file, encrypted_file, correct_password)
        
        # Try to decrypt with wrong password
        with pytest.raises(Exception):
            engine.decrypt_file(encrypted_file, decrypted_file, wrong_password)
    
    def test_data_encryption_decryption(self):
        """Test data encryption and decryption"""
        engine = EncryptionEngine()
        password = "data_test_password"
        original_data = b"This is test data for encryption"
        
        # Encrypt data
        encrypted_data = engine.encrypt_data(original_data, password)
        assert isinstance(encrypted_data, bytes)
        assert len(encrypted_data) > len(original_data)
        assert original_data not in encrypted_data
        
        # Decrypt data
        decrypted_data = engine.decrypt_data(encrypted_data, password)
        assert decrypted_data == original_data
    
    def test_corrupted_file(self, sample_text_file, temp_dir):
        """Test handling of corrupted encrypted files"""
        engine = EncryptionEngine()
        password = "test_password"
        
        encrypted_file = temp_dir / "encrypted.enc"
        decrypted_file = temp_dir / "decrypted.txt"
        
        # Encrypt file normally
        engine.encrypt_file(sample_text_file, encrypted_file, password)
        
        # Corrupt the encrypted file
        with open(encrypted_file, 'r+b') as f:
            f.seek(50)  # Go to middle of file
            f.write(b'\xFF\xFF\xFF\xFF')  # Write some garbage
        
        # Try to decrypt corrupted file
        with pytest.raises(Exception):
            engine.decrypt_file(encrypted_file, decrypted_file, password)
    
    def test_is_encrypted_file(self, sample_text_file, temp_dir):
        """Test encrypted file detection"""
        engine = EncryptionEngine()
        password = "test_password"
        
        encrypted_file = temp_dir / "encrypted.enc"
        
        # Plain file should not be detected as encrypted
        assert not engine.is_encrypted_file(sample_text_file)
        
        # Encrypt file
        engine.encrypt_file(sample_text_file, encrypted_file, password)
        
        # Encrypted file should be detected
        assert engine.is_encrypted_file(encrypted_file)
    
    def test_get_file_info(self, sample_text_file, temp_dir):
        """Test getting encrypted file information"""
        engine = EncryptionEngine()
        password = "test_password"
        
        encrypted_file = temp_dir / "encrypted.enc"
        engine.encrypt_file(sample_text_file, encrypted_file, password)
        
        file_info = engine.get_file_info(encrypted_file)
        
        assert 'algorithm' in file_info
        assert 'header_size' in file_info
        assert 'encrypted_size' in file_info
        assert 'total_size' in file_info
        assert file_info['algorithm'] == engine.algorithm
        assert file_info['total_size'] > 0
    
    def test_empty_file(self, temp_dir):
        """Test encryption of empty file"""
        engine = EncryptionEngine()
        password = "test_password"
        
        # Create empty file
        empty_file = temp_dir / "empty.txt"
        empty_file.touch()
        
        encrypted_file = temp_dir / "empty_encrypted.enc"
        decrypted_file = temp_dir / "empty_decrypted.txt"
        
        # Encrypt and decrypt empty file
        engine.encrypt_file(empty_file, encrypted_file, password)
        engine.decrypt_file(encrypted_file, decrypted_file, password)
        
        # Verify empty file is preserved
        assert decrypted_file.stat().st_size == 0
    
    def test_large_file_chunks(self, temp_dir):
        """Test encryption of file larger than chunk size"""
        engine = EncryptionEngine()
        password = "test_password"
        
        # Create file larger than chunk size
        large_file = temp_dir / "large.txt"
        chunk_size = engine.CHUNK_SIZE
        content = "A" * (chunk_size * 2 + 1000)  # More than 2 chunks
        large_file.write_text(content)
        
        encrypted_file = temp_dir / "large_encrypted.enc"
        decrypted_file = temp_dir / "large_decrypted.txt"
        
        # Encrypt and decrypt
        engine.encrypt_file(large_file, encrypted_file, password)
        engine.decrypt_file(encrypted_file, decrypted_file, password)
        
        # Verify content is preserved
        decrypted_content = decrypted_file.read_text()
        assert decrypted_content == content
    
    def test_different_algorithms(self, sample_text_file, temp_dir):
        """Test different encryption algorithms"""
        algorithms = ['AES-256-GCM', 'AES-256-CBC']
        password = "test_password"
        original_content = sample_text_file.read_text()
        
        for algorithm in algorithms:
            engine = EncryptionEngine(algorithm=algorithm)
            
            encrypted_file = temp_dir / f"encrypted_{algorithm.replace('-', '_')}.enc"
            decrypted_file = temp_dir / f"decrypted_{algorithm.replace('-', '_')}.txt"
            
            # Encrypt and decrypt with this algorithm
            engine.encrypt_file(sample_text_file, encrypted_file, password)
            engine.decrypt_file(encrypted_file, decrypted_file, password)
            
            # Verify content is preserved
            decrypted_content = decrypted_file.read_text()
            assert decrypted_content == original_content
    
    def test_password_with_special_characters(self, sample_text_file, temp_dir):
        """Test encryption with password containing special characters"""
        engine = EncryptionEngine()
        special_password = "pásswörd_with_spëcial_chärs!@#$%^&*()"
        
        encrypted_file = temp_dir / "encrypted.enc"
        decrypted_file = temp_dir / "decrypted.txt"
        original_content = sample_text_file.read_text()
        
        # Encrypt and decrypt with special character password
        engine.encrypt_file(sample_text_file, encrypted_file, special_password)
        engine.decrypt_file(encrypted_file, decrypted_file, special_password)
        
        # Verify content is preserved
        decrypted_content = decrypted_file.read_text()
        assert decrypted_content == original_content
