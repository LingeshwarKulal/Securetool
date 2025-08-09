#!/usr/bin/env python3
"""
Local Verification Script
Tests that the app works correctly before Vercel deployment
"""

import sys
import os
import tempfile
import base64

def test_requirements():
    """Test that all required packages can be imported"""
    print("🔍 Testing package imports...")
    
    try:
        import flask
        print(f"  ✅ Flask {flask.__version__}")
    except ImportError as e:
        print(f"  ❌ Flask: {e}")
        return False
    
    try:
        import cryptography
        print(f"  ✅ Cryptography")
    except ImportError as e:
        print(f"  ❌ Cryptography: {e}")
        return False
    
    try:
        from cryptography.fernet import Fernet
        print(f"  ✅ Fernet encryption")
    except ImportError as e:
        print(f"  ❌ Fernet: {e}")
        return False
    
    return True

def test_app_import():
    """Test that our app can be imported"""
    print("\n🔍 Testing app import...")
    
    try:
        import app
        print("  ✅ app.py imports successfully")
        return True
    except ImportError as e:
        print(f"  ❌ app.py import failed: {e}")
        return False

def test_encryption():
    """Test the encryption functionality"""
    print("\n🔍 Testing encryption functionality...")
    
    try:
        from app import SimpleEncryption
        
        # Create test data
        test_data = b"Hello, this is a test file for encryption!"
        password = "test_password_123"
        
        # Create temporary files
        with tempfile.NamedTemporaryFile(delete=False) as input_file:
            input_file.write(test_data)
            input_path = input_file.name
        
        with tempfile.NamedTemporaryFile(delete=False) as output_file:
            output_path = output_file.name
        
        # Test encryption
        encryption = SimpleEncryption()
        success, message = encryption.encrypt_file(input_path, output_path, password)
        
        if success:
            print("  ✅ Encryption successful")
            
            # Test decryption
            with tempfile.NamedTemporaryFile(delete=False) as decrypt_file:
                decrypt_path = decrypt_file.name
            
            success, message = encryption.decrypt_file(output_path, decrypt_path, password)
            
            if success:
                with open(decrypt_path, 'rb') as f:
                    decrypted_data = f.read()
                
                if decrypted_data == test_data:
                    print("  ✅ Decryption successful - data integrity verified")
                    return True
                else:
                    print("  ❌ Decryption failed - data mismatch")
                    return False
            else:
                print(f"  ❌ Decryption failed: {message}")
                return False
        else:
            print(f"  ❌ Encryption failed: {message}")
            return False
            
        # Cleanup
        os.unlink(input_path)
        os.unlink(output_path)
        os.unlink(decrypt_path)
        
    except Exception as e:
        print(f"  ❌ Encryption test failed: {e}")
        return False

def main():
    """Run all verification tests"""
    print("🚀 Vercel Deployment Verification Script")
    print("=" * 50)
    
    all_passed = True
    
    # Test 1: Package imports
    if not test_requirements():
        all_passed = False
    
    # Test 2: App import
    if not test_app_import():
        all_passed = False
    
    # Test 3: Encryption functionality
    if not test_encryption():
        all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Your app is ready for Vercel deployment")
        print("✅ No dependency issues detected")
        print("✅ Encryption functionality works correctly")
    else:
        print("❌ SOME TESTS FAILED")
        print("⚠️  Fix the issues above before deploying")
    
    print("\n📋 Next Steps:")
    print("1. Check your Vercel dashboard for latest deployment")
    print("2. Look for commit f74fa94 in deployments")
    print("3. Verify the build succeeds without tkinter-dev errors")

if __name__ == "__main__":
    main()
