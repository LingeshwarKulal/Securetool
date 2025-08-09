"""
Encryption and Decryption Engine
Handles all cryptographic operations using industry-standard algorithms
"""

import os
import hashlib
import struct
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import secrets

class EncryptionEngine:
    """Main encryption/decryption engine"""
    
    # File format constants
    MAGIC_HEADER = b'SEFT'  # Secure File Encryption Tool
    VERSION = 1
    CHUNK_SIZE = 64 * 1024  # 64KB chunks for streaming
    
    def __init__(self, algorithm='AES-256-GCM', pbkdf2_iterations=100000):
        """
        Initialize encryption engine
        
        Args:
            algorithm: Encryption algorithm to use
            pbkdf2_iterations: Number of PBKDF2 iterations for key derivation
        """
        self.algorithm = algorithm
        self.pbkdf2_iterations = pbkdf2_iterations
        self.backend = default_backend()
        
    def encrypt_file(self, input_path, output_path, password):
        """
        Encrypt a file
        
        Args:
            input_path: Path to input file
            output_path: Path to output encrypted file
            password: Encryption password
        """
        try:
            input_path = Path(input_path)
            output_path = Path(output_path)
            
            if not input_path.exists():
                raise FileNotFoundError(f"Input file not found: {input_path}")
                
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Generate salt and derive key
            salt = secrets.token_bytes(32)
            key = self._derive_key(password, salt)
            
            # Generate IV/nonce
            if self.algorithm == 'AES-256-GCM':
                iv = secrets.token_bytes(12)  # 96-bit nonce for GCM
            else:
                iv = secrets.token_bytes(16)  # 128-bit IV for CBC
            
            # Calculate file hash for integrity
            file_hash = self._calculate_file_hash(input_path)
            
            with open(input_path, 'rb') as infile, open(output_path, 'wb') as outfile:
                # Write header
                self._write_header(outfile, salt, iv, file_hash)
                
                # Initialize cipher
                cipher = self._create_cipher(key, iv)
                encryptor = cipher.encryptor()
                
                # Initialize padding for CBC mode
                if self.algorithm == 'AES-256-CBC':
                    padder = padding.PKCS7(128).padder()  # AES block size is 128 bits
                
                # Encrypt file in chunks
                while True:
                    chunk = infile.read(self.CHUNK_SIZE)
                    if not chunk:
                        break
                    
                    if self.algorithm == 'AES-256-CBC':
                        # Apply padding to chunk
                        padded_chunk = padder.update(chunk)
                        encrypted_chunk = encryptor.update(padded_chunk)
                    else:
                        encrypted_chunk = encryptor.update(chunk)
                    
                    outfile.write(encrypted_chunk)
                
                # Finalize encryption
                if self.algorithm == 'AES-256-CBC':
                    # Finalize padding
                    final_padded_chunk = padder.finalize()
                    if final_padded_chunk:
                        final_encrypted_chunk = encryptor.update(final_padded_chunk)
                        outfile.write(final_encrypted_chunk)
                
                final_chunk = encryptor.finalize()
                if final_chunk:
                    outfile.write(final_chunk)
                
                # Write authentication tag for GCM mode
                if self.algorithm == 'AES-256-GCM':
                    outfile.write(encryptor.tag)
                    
        except Exception as e:
            # Clean up incomplete output file
            if output_path.exists():
                output_path.unlink()
            raise Exception(f"Encryption failed: {str(e)}")
            
    def decrypt_file(self, input_path, output_path, password):
        """
        Decrypt a file
        
        Args:
            input_path: Path to encrypted file
            output_path: Path to output decrypted file
            password: Decryption password
        """
        try:
            input_path = Path(input_path)
            output_path = Path(output_path)
            
            if not input_path.exists():
                raise FileNotFoundError(f"Encrypted file not found: {input_path}")
                
            # Ensure output directory exists
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(input_path, 'rb') as infile:
                # Read and validate header
                header_info = self._read_header(infile)
                salt = header_info['salt']
                iv = header_info['iv']
                original_hash = header_info['file_hash']
                
                # Derive key
                key = self._derive_key(password, salt)
                
                # Read encrypted data
                encrypted_data = infile.read()
                
                # Extract authentication tag for GCM mode
                if self.algorithm == 'AES-256-GCM':
                    if len(encrypted_data) < 16:
                        raise ValueError("Invalid encrypted file format")
                    tag = encrypted_data[-16:]
                    encrypted_data = encrypted_data[:-16]
                else:
                    tag = None
                
                # Initialize cipher for decryption
                cipher = self._create_cipher(key, iv, tag)
                decryptor = cipher.decryptor()
                
                # Decrypt data
                decrypted_data = decryptor.update(encrypted_data)
                decrypted_data += decryptor.finalize()
                
                # Remove padding for CBC mode
                if self.algorithm == 'AES-256-CBC':
                    unpadder = padding.PKCS7(128).unpadder()
                    decrypted_data = unpadder.update(decrypted_data)
                    decrypted_data += unpadder.finalize()
                
            # Write decrypted data to output file
            with open(output_path, 'wb') as outfile:
                outfile.write(decrypted_data)
            
            # Verify file integrity
            if not self._verify_file_integrity(output_path, original_hash):
                output_path.unlink()  # Remove corrupted file
                raise ValueError("File integrity check failed - file may be corrupted")
                
        except Exception as e:
            # Clean up incomplete output file
            if output_path.exists():
                output_path.unlink()
            raise Exception(f"Decryption failed: {str(e)}")
            
    def encrypt_data(self, data, password):
        """
        Encrypt raw data
        
        Args:
            data: Bytes to encrypt
            password: Encryption password
            
        Returns:
            Encrypted data with header
        """
        try:
            # Generate salt and derive key
            salt = secrets.token_bytes(32)
            key = self._derive_key(password, salt)
            
            # Generate IV/nonce
            if self.algorithm == 'AES-256-GCM':
                iv = secrets.token_bytes(12)
            else:
                iv = secrets.token_bytes(16)
            
            # Calculate data hash
            data_hash = hashlib.sha256(data).digest()
            
            # Create cipher
            cipher = self._create_cipher(key, iv)
            encryptor = cipher.encryptor()
            
            # Apply padding for CBC mode
            if self.algorithm == 'AES-256-CBC':
                padder = padding.PKCS7(128).padder()
                padded_data = padder.update(data)
                padded_data += padder.finalize()
                data_to_encrypt = padded_data
            else:
                data_to_encrypt = data
            
            # Encrypt data
            encrypted_data = encryptor.update(data_to_encrypt)
            encrypted_data += encryptor.finalize()
            
            # Build result with header
            result = bytearray()
            result.extend(self.MAGIC_HEADER)
            result.extend(struct.pack('<I', self.VERSION))
            result.extend(struct.pack('<I', len(salt)))
            result.extend(salt)
            result.extend(struct.pack('<I', len(iv)))
            result.extend(iv)
            result.extend(struct.pack('<I', len(data_hash)))
            result.extend(data_hash)
            result.extend(encrypted_data)
            
            # Add authentication tag for GCM
            if self.algorithm == 'AES-256-GCM':
                result.extend(encryptor.tag)
                
            return bytes(result)
            
        except Exception as e:
            raise Exception(f"Data encryption failed: {str(e)}")
            
    def decrypt_data(self, encrypted_data, password):
        """
        Decrypt raw data
        
        Args:
            encrypted_data: Encrypted bytes with header
            password: Decryption password
            
        Returns:
            Decrypted data
        """
        try:
            # Parse header
            offset = 0
            
            # Check magic header
            magic = encrypted_data[offset:offset+4]
            if magic != self.MAGIC_HEADER:
                raise ValueError("Invalid file format")
            offset += 4
            
            # Check version
            version = struct.unpack('<I', encrypted_data[offset:offset+4])[0]
            if version != self.VERSION:
                raise ValueError(f"Unsupported file version: {version}")
            offset += 4
            
            # Read salt
            salt_len = struct.unpack('<I', encrypted_data[offset:offset+4])[0]
            offset += 4
            salt = encrypted_data[offset:offset+salt_len]
            offset += salt_len
            
            # Read IV
            iv_len = struct.unpack('<I', encrypted_data[offset:offset+4])[0]
            offset += 4
            iv = encrypted_data[offset:offset+iv_len]
            offset += iv_len
            
            # Read original hash
            hash_len = struct.unpack('<I', encrypted_data[offset:offset+4])[0]
            offset += 4
            original_hash = encrypted_data[offset:offset+hash_len]
            offset += hash_len
            
            # Get encrypted payload
            payload = encrypted_data[offset:]
            
            # Extract authentication tag for GCM
            if self.algorithm == 'AES-256-GCM':
                if len(payload) < 16:
                    raise ValueError("Invalid encrypted data format")
                tag = payload[-16:]
                payload = payload[:-16]
            else:
                tag = None
            
            # Derive key and create cipher
            key = self._derive_key(password, salt)
            cipher = self._create_cipher(key, iv, tag)
            decryptor = cipher.decryptor()
            
            # Decrypt
            decrypted_data = decryptor.update(payload)
            decrypted_data += decryptor.finalize()
            
            # Remove padding for CBC mode
            if self.algorithm == 'AES-256-CBC':
                unpadder = padding.PKCS7(128).unpadder()
                decrypted_data = unpadder.update(decrypted_data)
                decrypted_data += unpadder.finalize()
            
            # Verify integrity
            data_hash = hashlib.sha256(decrypted_data).digest()
            if data_hash != original_hash:
                raise ValueError("Data integrity check failed")
                
            return decrypted_data
            
        except Exception as e:
            raise Exception(f"Data decryption failed: {str(e)}")
    
    def _derive_key(self, password, salt):
        """Derive encryption key from password using PBKDF2"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,  # 256-bit key
            salt=salt,
            iterations=self.pbkdf2_iterations,
            backend=self.backend
        )
        return kdf.derive(password.encode('utf-8'))
    
    def _create_cipher(self, key, iv, tag=None):
        """Create cipher object based on algorithm"""
        if self.algorithm == 'AES-256-GCM':
            cipher = Cipher(
                algorithms.AES(key),
                modes.GCM(iv, tag),
                backend=self.backend
            )
        elif self.algorithm == 'AES-256-CBC':
            cipher = Cipher(
                algorithms.AES(key),
                modes.CBC(iv),
                backend=self.backend
            )
        else:
            raise ValueError(f"Unsupported algorithm: {self.algorithm}")
            
        return cipher
    
    def _write_header(self, outfile, salt, iv, file_hash):
        """Write encrypted file header"""
        # Magic header
        outfile.write(self.MAGIC_HEADER)
        
        # Version
        outfile.write(struct.pack('<I', self.VERSION))
        
        # Salt
        outfile.write(struct.pack('<I', len(salt)))
        outfile.write(salt)
        
        # IV/Nonce
        outfile.write(struct.pack('<I', len(iv)))
        outfile.write(iv)
        
        # Original file hash
        outfile.write(struct.pack('<I', len(file_hash)))
        outfile.write(file_hash)
    
    def _read_header(self, infile):
        """Read and validate encrypted file header"""
        # Check magic header
        magic = infile.read(4)
        if magic != self.MAGIC_HEADER:
            raise ValueError("Invalid file format - not an encrypted file")
        
        # Check version
        version_data = infile.read(4)
        if len(version_data) != 4:
            raise ValueError("Invalid file format - corrupted header")
        version = struct.unpack('<I', version_data)[0]
        if version != self.VERSION:
            raise ValueError(f"Unsupported file version: {version}")
        
        # Read salt
        salt_len_data = infile.read(4)
        if len(salt_len_data) != 4:
            raise ValueError("Invalid file format - corrupted salt length")
        salt_len = struct.unpack('<I', salt_len_data)[0]
        salt = infile.read(salt_len)
        if len(salt) != salt_len:
            raise ValueError("Invalid file format - corrupted salt")
        
        # Read IV
        iv_len_data = infile.read(4)
        if len(iv_len_data) != 4:
            raise ValueError("Invalid file format - corrupted IV length")
        iv_len = struct.unpack('<I', iv_len_data)[0]
        iv = infile.read(iv_len)
        if len(iv) != iv_len:
            raise ValueError("Invalid file format - corrupted IV")
        
        # Read original file hash
        hash_len_data = infile.read(4)
        if len(hash_len_data) != 4:
            raise ValueError("Invalid file format - corrupted hash length")
        hash_len = struct.unpack('<I', hash_len_data)[0]
        file_hash = infile.read(hash_len)
        if len(file_hash) != hash_len:
            raise ValueError("Invalid file format - corrupted hash")
        
        return {
            'salt': salt,
            'iv': iv,
            'file_hash': file_hash
        }
    
    def _calculate_file_hash(self, file_path):
        """Calculate SHA-256 hash of file"""
        hash_sha256 = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(self.CHUNK_SIZE), b""):
                hash_sha256.update(chunk)
        return hash_sha256.digest()
    
    def _verify_file_integrity(self, file_path, expected_hash):
        """Verify file integrity using hash"""
        actual_hash = self._calculate_file_hash(file_path)
        return actual_hash == expected_hash
    
    def is_encrypted_file(self, file_path):
        """Check if file is encrypted by this tool"""
        try:
            with open(file_path, 'rb') as f:
                magic = f.read(4)
                return magic == self.MAGIC_HEADER
        except Exception:
            return False
    
    def get_file_info(self, encrypted_file_path):
        """Get information about encrypted file"""
        try:
            with open(encrypted_file_path, 'rb') as f:
                header_info = self._read_header(f)
                
                # Get file size
                f.seek(0, 2)  # Seek to end
                total_size = f.tell()
                
                # Calculate header size
                f.seek(0)
                self._read_header(f)
                header_size = f.tell()
                
                # Calculate encrypted data size
                encrypted_size = total_size - header_size
                if self.algorithm == 'AES-256-GCM':
                    encrypted_size -= 16  # Subtract tag size
                
                return {
                    'algorithm': self.algorithm,
                    'header_size': header_size,
                    'encrypted_size': encrypted_size,
                    'total_size': total_size,
                    'salt_length': len(header_info['salt']),
                    'iv_length': len(header_info['iv'])
                }
        except Exception as e:
            raise Exception(f"Failed to read file info: {str(e)}")


class FernetEngine:
    """Alternative encryption engine using Fernet (simpler but less flexible)"""
    
    def __init__(self):
        self.pbkdf2_iterations = 100000
    
    def encrypt_file(self, input_path, output_path, password):
        """Encrypt file using Fernet"""
        try:
            # Generate salt and derive key
            salt = secrets.token_bytes(32)
            key = self._derive_key(password, salt)
            fernet = Fernet(key)
            
            # Read and encrypt file
            with open(input_path, 'rb') as infile:
                plaintext = infile.read()
            
            encrypted_data = fernet.encrypt(plaintext)
            
            # Write salt + encrypted data
            with open(output_path, 'wb') as outfile:
                outfile.write(salt)
                outfile.write(encrypted_data)
                
        except Exception as e:
            if os.path.exists(output_path):
                os.unlink(output_path)
            raise Exception(f"Fernet encryption failed: {str(e)}")
    
    def decrypt_file(self, input_path, output_path, password):
        """Decrypt file using Fernet"""
        try:
            with open(input_path, 'rb') as infile:
                # Read salt and encrypted data
                salt = infile.read(32)
                encrypted_data = infile.read()
            
            # Derive key and decrypt
            key = self._derive_key(password, salt)
            fernet = Fernet(key)
            plaintext = fernet.decrypt(encrypted_data)
            
            # Write decrypted data
            with open(output_path, 'wb') as outfile:
                outfile.write(plaintext)
                
        except Exception as e:
            if os.path.exists(output_path):
                os.unlink(output_path)
            raise Exception(f"Fernet decryption failed: {str(e)}")
    
    def _derive_key(self, password, salt):
        """Derive Fernet key from password"""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=self.pbkdf2_iterations,
            backend=default_backend()
        )
        key = kdf.derive(password.encode('utf-8'))
        return Fernet.generate_key()
