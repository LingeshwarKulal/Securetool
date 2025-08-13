"""
Web-based Secure File Encryption Tool
Flask application for Vercel deployment
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import tempfile
import base64
from werkzeug.utils import secure_filename

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from core.encryption import EncryptionEngine
except ImportError:
    # Fallback for deployment environments
    sys.path.insert(0, os.path.dirname(__file__))
    from src.core.encryption import EncryptionEngine

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize encryption
encryption = EncryptionEngine()

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
        temp_input.close()  # Close the file handle
        file.save(temp_input.name)
        
        # Create output file
        temp_output = tempfile.NamedTemporaryFile(delete=False, suffix='.enc')
        temp_output.close()  # Close the file handle
        
        # Encrypt file
        try:
            encryption.encrypt_file(temp_input.name, temp_output.name, password)
            success = True
            message = "Encryption successful"
        except Exception as e:
            success = False
            message = str(e)
        
        if success:
            # Read encrypted file and encode as base64
            with open(temp_output.name, 'rb') as f:
                encrypted_data = base64.b64encode(f.read()).decode()
            
            # Cleanup
            try:
                os.unlink(temp_input.name)
            except OSError:
                pass  # File might already be deleted
            try:
                os.unlink(temp_output.name)
            except OSError:
                pass  # File might already be deleted
            
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
        temp_input.close()  # Close the file handle
        file.save(temp_input.name)
        
        # Create output file
        original_name = filename.replace('.enc', '') if filename.endswith('.enc') else filename + '.dec'
        temp_output = tempfile.NamedTemporaryFile(delete=False)
        temp_output.close()  # Close the file handle
        
        # Decrypt file
        try:
            encryption.decrypt_file(temp_input.name, temp_output.name, password)
            success = True
            message = "Decryption successful"
        except Exception as e:
            success = False
            message = str(e)
        
        if success:
            # Read decrypted file and encode as base64
            with open(temp_output.name, 'rb') as f:
                decrypted_data = base64.b64encode(f.read()).decode()
            
            # Cleanup
            try:
                os.unlink(temp_input.name)
            except OSError:
                pass  # File might already be deleted
            try:
                os.unlink(temp_output.name)
            except OSError:
                pass  # File might already be deleted
            
            return jsonify({
                'success': True,
                'filename': original_name,
                'data': decrypted_data
            })
        else:
            return jsonify({'error': message}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
