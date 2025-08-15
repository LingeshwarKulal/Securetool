"""
Simplified Web-based Secure File Encryption Tool
Flask application optimized for Vercel deployment
"""

from flask import Flask, render_template, request, jsonify
import os
import tempfile
import base64
import hashlib
import secrets
from werkzeug.utils import secure_filename
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

class SimpleEncryption:
    """Simplified encryption for web deployment"""
    
    def __init__(self):
        self.backend = default_backend()
    
    def _derive_key(self, password, salt):
        """Derive encryption key from password and salt"""
        password_bytes = password.encode('utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=self.backend
        )
        return base64.urlsafe_b64encode(kdf.derive(password_bytes))
    
    def encrypt_file(self, input_path, output_path, password):
        """Encrypt a file"""
        try:
            # Generate random salt
            salt = secrets.token_bytes(16)
            
            # Derive key
            key = self._derive_key(password, salt)
            fernet = Fernet(key)
            
            # Read and encrypt file
            with open(input_path, 'rb') as infile:
                file_data = infile.read()
            
            encrypted_data = fernet.encrypt(file_data)
            
            # Write salt + encrypted data
            with open(output_path, 'wb') as outfile:
                outfile.write(salt)
                outfile.write(encrypted_data)
            
            return True, "File encrypted successfully"
            
        except Exception as e:
            return False, f"Encryption failed: {str(e)}"
    
    def decrypt_file(self, input_path, output_path, password):
        """Decrypt a file"""
        try:
            # Read encrypted file
            with open(input_path, 'rb') as infile:
                salt = infile.read(16)  # First 16 bytes are salt
                encrypted_data = infile.read()
            
            # Derive key
            key = self._derive_key(password, salt)
            fernet = Fernet(key)
            
            # Decrypt data
            decrypted_data = fernet.decrypt(encrypted_data)
            
            # Write decrypted file
            with open(output_path, 'wb') as outfile:
                outfile.write(decrypted_data)
            
            return True, "File decrypted successfully"
            
        except Exception as e:
            return False, f"Decryption failed: {str(e)}"

# Initialize encryption
encryption = SimpleEncryption()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
def encrypt_file():
    """Encrypt uploaded file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        password = request.form.get('password')
        
        if not file or not password:
            return jsonify({'error': 'File and password required'}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_input = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp_input.name)
        
        # Create output file
        temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.enc')
        
        # Encrypt file
        success, message = encryption.encrypt_file(temp_input.name, temp_output.name, password)
        
        if success:
            # Read encrypted file and encode as base64
            with open(temp_output.name, 'rb') as f:
                encrypted_data = base64.b64encode(f.read()).decode()
            
            # Cleanup
            os.unlink(temp_input.name)
            os.unlink(temp_output.name)
            
            return jsonify({
                'success': True,
                'filename': f"{filename}.enc",
                'data': encrypted_data
            })
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/decrypt', methods=['POST'])
def decrypt_file():
    """Decrypt uploaded file"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        password = request.form.get('password')
        
        if not file or not password:
            return jsonify({'error': 'File and password required'}), 400
        
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_input = tempfile.NamedTemporaryFile(delete=False)
        file.save(temp_input.name)
        
        # Create output file
        original_name = filename.replace('.enc', '') if filename.endswith('.enc') else filename + '.dec'
        temp_output = tempfile.NamedTemporaryFile(delete=False)
        
        # Decrypt file
        success, message = encryption.decrypt_file(temp_input.name, temp_output.name, password)
        
        if success:
            # Read decrypted file and encode as base64
            with open(temp_output.name, 'rb') as f:
                decrypted_data = base64.b64encode(f.read()).decode()
            
            # Cleanup
            os.unlink(temp_input.name)
            os.unlink(temp_output.name)
            
            return jsonify({
                'success': True,
                'filename': original_name,
                'data': decrypted_data
            })
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# For Vercel
app = app

if __name__ == '__main__':
    # Never use debug=True in production!
    # Use environment variable to control debug mode
    import os
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='127.0.0.1')
