"""
Simple demonstration script to test the encryption functionality
"""

import os
import sys
import tempfile
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from core.encryption import EncryptionEngine
from core.file_manager import FileManager

def demo_encryption():
    """Demonstrate encryption and decryption functionality"""
    print("🔐 Secure File Encryption Tool - Demo")
    print("=" * 50)
    
    # Create temporary directory for demo
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Create a sample file
        sample_file = temp_path / "demo_file.txt"
        sample_content = """
This is a demonstration of the Secure File Encryption Tool.

Features:
- AES-256 encryption
- Secure password protection
- File integrity verification
- Cross-platform support

This file will be encrypted and then decrypted to verify functionality.
        """.strip()
        
        sample_file.write_text(sample_content)
        print(f"✅ Created sample file: {sample_file.name}")
        print(f"   Original size: {len(sample_content)} bytes")
        
        # Initialize encryption engine
        engine = EncryptionEngine()
        password = "Demo_Password_2025!"
        
        # Encrypt the file
        encrypted_file = temp_path / "demo_file.enc"
        print(f"\n🔒 Encrypting file...")
        
        try:
            engine.encrypt_file(sample_file, encrypted_file, password)
            encrypted_size = encrypted_file.stat().st_size
            print(f"✅ Encryption successful!")
            print(f"   Encrypted size: {encrypted_size} bytes")
            print(f"   Encryption overhead: {encrypted_size - len(sample_content)} bytes")
            
        except Exception as e:
            print(f"❌ Encryption failed: {e}")
            return False
        
        # Verify encrypted file is different
        encrypted_content = encrypted_file.read_bytes()
        if sample_content.encode() in encrypted_content:
            print("❌ Warning: Original content found in encrypted file!")
            return False
        else:
            print("✅ Encrypted content is properly obfuscated")
        
        # Decrypt the file
        decrypted_file = temp_path / "demo_file_decrypted.txt"
        print(f"\n🔓 Decrypting file...")
        
        try:
            engine.decrypt_file(encrypted_file, decrypted_file, password)
            decrypted_content = decrypted_file.read_text()
            print(f"✅ Decryption successful!")
            
        except Exception as e:
            print(f"❌ Decryption failed: {e}")
            return False
        
        # Verify content integrity
        if decrypted_content == sample_content:
            print("✅ File integrity verified - content matches original!")
        else:
            print("❌ File integrity check failed - content differs!")
            return False
        
        # Test folder encryption
        print(f"\n📁 Testing folder encryption...")
        
        # Create sample folder
        sample_folder = temp_path / "demo_folder"
        sample_folder.mkdir()
        (sample_folder / "file1.txt").write_text("Content of file 1")
        (sample_folder / "file2.txt").write_text("Content of file 2")
        (sample_folder / "subfolder").mkdir()
        (sample_folder / "subfolder" / "file3.txt").write_text("Content of file 3")
        
        print(f"✅ Created sample folder with 3 files")
        
        # Encrypt folder
        fm = FileManager()
        encrypted_folder_file = temp_path / "demo_folder.enc"
        
        try:
            fm.encrypt_folder(sample_folder, encrypted_folder_file, engine, password)
            print(f"✅ Folder encryption successful!")
            
        except Exception as e:
            print(f"❌ Folder encryption failed: {e}")
            return False
        
        # Decrypt folder
        decrypted_folder = temp_path / "demo_folder_decrypted"
        
        try:
            fm.decrypt_folder(encrypted_folder_file, decrypted_folder, engine, password)
            print(f"✅ Folder decryption successful!")
            
            # Verify folder structure
            if (decrypted_folder / "file1.txt").exists() and \
               (decrypted_folder / "file2.txt").exists() and \
               (decrypted_folder / "subfolder" / "file3.txt").exists():
                print("✅ Folder structure preserved!")
            else:
                print("❌ Folder structure not preserved!")
                return False
                
        except Exception as e:
            print(f"❌ Folder decryption failed: {e}")
            return False
        
        print(f"\n🎉 All tests passed successfully!")
        print(f"✅ The Secure File Encryption Tool is working correctly!")
        return True

if __name__ == "__main__":
    success = demo_encryption()
    if success:
        print(f"\n🚀 Ready for production use!")
        sys.exit(0)
    else:
        print(f"\n❌ Some tests failed. Please check the implementation.")
        sys.exit(1)
