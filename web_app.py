"""
Web-based Secure File Encryption Tool
Flask application for Vercel deployment
"""

from flask import Flask, render_template, request, jsonify, send_file
import os
import sys
import tempfile
import base64
import secrets
import time
import hashlib
from collections import defaultdict
from werkzeug.utils import secure_filename
from functools import wraps

# Load environment variables
from dotenv import load_dotenv
load_dotenv()  # Load .env file if present

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from core.encryption import EncryptionEngine
except ImportError:
    # Fallback for deployment environments
    sys.path.insert(0, os.path.dirname(__file__))
    from src.core.encryption import EncryptionEngine

app = Flask(__name__)

# Configuration from environment variables
app.config['MAX_CONTENT_LENGTH'] = int(os.environ.get('MAX_UPLOAD_SIZE_MB', '16')) * 1024 * 1024
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', secrets.token_hex(32))

# Rate limiting configuration
RATE_LIMIT = int(os.environ.get('RATE_LIMIT_PER_MINUTE', '10'))
RATE_LIMIT_WINDOW = 60  # seconds

# Security headers
@app.after_request
def set_security_headers(response):
    """Add security headers to all responses"""
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    response.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'"
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    response.headers['Permissions-Policy'] = 'camera=(), microphone=(), geolocation=(), payment=()'
    return response

# Initialize encryption
encryption = EncryptionEngine()

# Rate limiting
request_counts = defaultdict(list)

def rate_limit_decorator(f):
    """Rate limiting decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        client_ip = request.environ.get('HTTP_X_FORWARDED_FOR', request.remote_addr)
        if client_ip:
            client_ip = client_ip.split(',')[0].strip()
        
        current_time = time.time()
        
        # Clean old requests
        request_counts[client_ip] = [
            req_time for req_time in request_counts[client_ip]
            if current_time - req_time < RATE_LIMIT_WINDOW
        ]
        
        # Check rate limit
        if len(request_counts[client_ip]) >= RATE_LIMIT:
            return jsonify({'error': 'Rate limit exceeded. Try again later.'}), 429
        
        # Add current request
        request_counts[client_ip].append(current_time)
        
        return f(*args, **kwargs)
    return decorated_function

def validate_file_type(filename):
    """Validate file type to prevent malicious uploads"""
    # Allow common file types but block potentially dangerous ones
    dangerous_extensions = {
        '.exe', '.bat', '.cmd', '.com', '.pif', '.scr', '.vbs', '.js', 
        '.jar', '.ps1', '.sh', '.php', '.asp', '.jsp', '.pl', '.py'
    }
    
    file_ext = os.path.splitext(filename.lower())[1]
    if file_ext in dangerous_extensions:
        return False, f"File type {file_ext} not allowed for security reasons"
    
    return True, "Valid file type"

def validate_password_strength(password):
    """Basic password validation"""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if len(password) > 128:
        return False, "Password too long (max 128 characters)"
    
    return True, "Password valid"

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/encrypt', methods=['POST'])
@rate_limit_decorator
def encrypt_file():
    """Encrypt uploaded file"""
    try:
        # Validate request
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        password = request.form.get('password', '').strip()
        
        if not file or not file.filename:
            return jsonify({'error': 'Invalid file'}), 400
        
        if not password:
            return jsonify({'error': 'Password required'}), 400
        
        # Validate password strength
        password_valid, password_msg = validate_password_strength(password)
        if not password_valid:
            return jsonify({'error': password_msg}), 400
        
        # Validate file type
        file_valid, file_msg = validate_file_type(file.filename)
        if not file_valid:
            return jsonify({'error': file_msg}), 400
        
        # Check file size
        if len(file.read()) > app.config['MAX_CONTENT_LENGTH']:
            return jsonify({'error': 'File too large'}), 400
        
        # Reset file pointer after reading
        file.seek(0)
        
        # Generate secure filename
        original_filename = secure_filename(file.filename)
        if not original_filename:
            original_filename = 'unnamed_file'
        
        # Create secure temporary files
        temp_input = tempfile.NamedTemporaryFile(delete=False, prefix='enc_input_', suffix='.tmp')
        temp_output = tempfile.NamedTemporaryFile(delete=False, prefix='enc_output_', suffix='.tmp')
        
        try:
            # Save uploaded file
            file.save(temp_input.name)
            temp_input.close()
            temp_output.close()
            
            # Encrypt file
            encryption.encrypt_file(temp_input.name, temp_output.name, password)
            
            # Read encrypted file and encode as base64
            with open(temp_output.name, 'rb') as f:
                encrypted_data = base64.b64encode(f.read()).decode()
            
            # Generate secure output filename
            output_filename = f"{original_filename}.enc"
            
            response_data = {
                'success': True,
                'filename': output_filename,
                'data': encrypted_data,
                'original_size': os.path.getsize(temp_input.name),
                'encrypted_size': os.path.getsize(temp_output.name)
            }
            
            return jsonify(response_data)
            
        finally:
            # Secure cleanup - overwrite temp files before deletion
            for temp_file in [temp_input.name, temp_output.name]:
                try:
                    if os.path.exists(temp_file):
                        # Overwrite with random data
                        with open(temp_file, 'wb') as f:
                            f.write(secrets.token_bytes(1024))
                        os.unlink(temp_file)
                except OSError:
                    pass  # Best effort cleanup
            
    except Exception as e:
        # Log error without exposing sensitive information
        error_id = hashlib.sha256(str(e).encode()).hexdigest()[:8]
        return jsonify({'error': f'Encryption failed. Error ID: {error_id}'}), 500

@app.route('/decrypt', methods=['POST'])
@rate_limit_decorator
def decrypt_file():
    """Decrypt uploaded file"""
    try:
        # Validate request
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400
        
        file = request.files['file']
        password = request.form.get('password', '').strip()
        
        if not file or not file.filename:
            return jsonify({'error': 'Invalid file'}), 400
        
        if not password:
            return jsonify({'error': 'Password required'}), 400
        
        # Validate password length
        password_valid, password_msg = validate_password_strength(password)
        if not password_valid:
            return jsonify({'error': password_msg}), 400
        
        # Check file size
        if len(file.read()) > app.config['MAX_CONTENT_LENGTH']:
            return jsonify({'error': 'File too large'}), 400
        
        # Reset file pointer after reading
        file.seek(0)
        
        # Generate secure filename
        original_filename = secure_filename(file.filename)
        if not original_filename:
            original_filename = 'unnamed_file'
        
        # Determine output filename
        if original_filename.endswith('.enc'):
            output_filename = original_filename[:-4]  # Remove .enc extension
        else:
            output_filename = f"{original_filename}.dec"
        
        # Create secure temporary files
        temp_input = tempfile.NamedTemporaryFile(delete=False, prefix='dec_input_', suffix='.tmp')
        temp_output = tempfile.NamedTemporaryFile(delete=False, prefix='dec_output_', suffix='.tmp')
        
        try:
            # Save uploaded file
            file.save(temp_input.name)
            temp_input.close()
            temp_output.close()
            
            # Decrypt file
            encryption.decrypt_file(temp_input.name, temp_output.name, password)
            
            # Read decrypted file and encode as base64
            with open(temp_output.name, 'rb') as f:
                decrypted_data = base64.b64encode(f.read()).decode()
            
            response_data = {
                'success': True,
                'filename': output_filename,
                'data': decrypted_data,
                'decrypted_size': os.path.getsize(temp_output.name)
            }
            
            return jsonify(response_data)
            
        finally:
            # Secure cleanup - overwrite temp files before deletion
            for temp_file in [temp_input.name, temp_output.name]:
                try:
                    if os.path.exists(temp_file):
                        # Overwrite with random data
                        with open(temp_file, 'wb') as f:
                            f.write(secrets.token_bytes(1024))
                        os.unlink(temp_file)
                except OSError:
                    pass  # Best effort cleanup
            
    except Exception as e:
        # Log error without exposing sensitive information
        error_id = hashlib.sha256(str(e).encode()).hexdigest()[:8]
        return jsonify({'error': f'Decryption failed. Error ID: {error_id}'}), 500

if __name__ == '__main__':
    app.run(debug=True)
