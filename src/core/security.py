"""
Security utilities and helper functions
"""

import os
import secrets
import string
import hashlib
import hmac
import time
from typing import Optional

class SecurityUtils:
    """Security-related utility functions"""
    
    @staticmethod
    def generate_secure_password(length=16, include_symbols=True):
        """
        Generate a cryptographically secure random password
        
        Args:
            length: Password length
            include_symbols: Whether to include special symbols
            
        Returns:
            Generated password string
        """
        if length < 8:
            raise ValueError("Password length must be at least 8 characters")
        
        # Define character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?" if include_symbols else ""
        
        # Ensure at least one character from each required set
        password = [
            secrets.choice(lowercase),
            secrets.choice(uppercase),
            secrets.choice(digits)
        ]
        
        if include_symbols:
            password.append(secrets.choice(symbols))
        
        # Fill remaining length with random characters from all sets
        all_chars = lowercase + uppercase + digits + symbols
        for _ in range(length - len(password)):
            password.append(secrets.choice(all_chars))
        
        # Shuffle the password list
        for i in range(len(password)):
            j = secrets.randbelow(len(password))
            password[i], password[j] = password[j], password[i]
        
        return ''.join(password)
    
    @staticmethod
    def check_password_strength(password):
        """
        Check password strength and return score and recommendations
        
        Args:
            password: Password to check
            
        Returns:
            Dictionary with strength score and details
        """
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("Password should be at least 12 characters long")
        
        # Character variety checks
        has_lower = any(c.islower() for c in password)
        has_upper = any(c.isupper() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_symbol = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
        
        if has_lower:
            score += 1
        else:
            feedback.append("Add lowercase letters")
            
        if has_upper:
            score += 1
        else:
            feedback.append("Add uppercase letters")
            
        if has_digit:
            score += 1
        else:
            feedback.append("Add numbers")
            
        if has_symbol:
            score += 1
        else:
            feedback.append("Add special characters")
        
        # Complexity bonus
        if len(password) >= 16:
            score += 1
        
        # Penalty for common patterns
        if password.lower() in ['password', '12345678', 'qwerty123']:
            score -= 3
            feedback.append("Avoid common passwords")
        
        # Calculate strength level
        if score >= 7:
            strength = "Very Strong"
        elif score >= 5:
            strength = "Strong"
        elif score >= 3:
            strength = "Good"
        elif score >= 2:
            strength = "Fair"
        else:
            strength = "Weak"
        
        return {
            'score': max(0, score),
            'max_score': 8,
            'strength': strength,
            'feedback': feedback,
            'percentage': min(100, (max(0, score) / 8) * 100)
        }
    
    @staticmethod
    def secure_compare(a, b):
        """
        Perform timing-safe string comparison
        
        Args:
            a: First string
            b: Second string
            
        Returns:
            True if strings are equal
        """
        return hmac.compare_digest(a.encode('utf-8'), b.encode('utf-8'))
    
    @staticmethod
    def hash_password(password, salt=None):
        """
        Hash a password with salt using PBKDF2
        
        Args:
            password: Password to hash
            salt: Salt bytes (generated if None)
            
        Returns:
            Tuple of (hash, salt)
        """
        if salt is None:
            salt = secrets.token_bytes(32)
        
        # Use PBKDF2 with SHA-256
        iterations = 100000
        hash_value = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, iterations)
        
        return hash_value, salt
    
    @staticmethod
    def verify_password(password, hash_value, salt):
        """
        Verify a password against its hash
        
        Args:
            password: Password to verify
            hash_value: Stored hash
            salt: Salt used for hashing
            
        Returns:
            True if password is correct
        """
        computed_hash, _ = SecurityUtils.hash_password(password, salt)
        return hmac.compare_digest(computed_hash, hash_value)
    
    @staticmethod
    def secure_random_bytes(length):
        """
        Generate cryptographically secure random bytes
        
        Args:
            length: Number of bytes to generate
            
        Returns:
            Random bytes
        """
        return secrets.token_bytes(length)
    
    @staticmethod
    def secure_random_string(length, alphabet=None):
        """
        Generate cryptographically secure random string
        
        Args:
            length: String length
            alphabet: Character alphabet (default: alphanumeric)
            
        Returns:
            Random string
        """
        if alphabet is None:
            alphabet = string.ascii_letters + string.digits
        
        return ''.join(secrets.choice(alphabet) for _ in range(length))
    
    @staticmethod
    def memory_clear(data):
        """
        Attempt to clear sensitive data from memory
        Note: This is best effort in Python due to garbage collection
        
        Args:
            data: Data to clear (string or bytes)
        """
        if isinstance(data, str):
            # Convert to bytearray for modification
            data_bytes = bytearray(data.encode('utf-8'))
        elif isinstance(data, bytes):
            data_bytes = bytearray(data)
        else:
            return
        
        # Overwrite with zeros
        for i in range(len(data_bytes)):
            data_bytes[i] = 0
    
    @staticmethod
    def validate_file_permissions(file_path):
        """
        Check if file has secure permissions (not world-readable)
        
        Args:
            file_path: Path to file to check
            
        Returns:
            Dictionary with permission information
        """
        try:
            stat_info = os.stat(file_path)
            mode = stat_info.st_mode
            
            # Check permissions (Unix-style)
            owner_read = bool(mode & 0o400)
            owner_write = bool(mode & 0o200)
            owner_exec = bool(mode & 0o100)
            
            group_read = bool(mode & 0o040)
            group_write = bool(mode & 0o020)
            group_exec = bool(mode & 0o010)
            
            other_read = bool(mode & 0o004)
            other_write = bool(mode & 0o002)
            other_exec = bool(mode & 0o001)
            
            # Security warnings
            warnings = []
            if other_read or other_write:
                warnings.append("File is accessible by others")
            if group_write:
                warnings.append("File is writable by group")
            if other_exec:
                warnings.append("File is executable by others")
            
            return {
                'owner': {'read': owner_read, 'write': owner_write, 'exec': owner_exec},
                'group': {'read': group_read, 'write': group_write, 'exec': group_exec},
                'other': {'read': other_read, 'write': other_write, 'exec': other_exec},
                'warnings': warnings,
                'secure': len(warnings) == 0
            }
            
        except Exception as e:
            return {'error': str(e)}


class PasswordPolicy:
    """Password policy enforcement"""
    
    def __init__(self, min_length=12, require_upper=True, require_lower=True,
                 require_digits=True, require_symbols=True, max_attempts=3):
        self.min_length = min_length
        self.require_upper = require_upper
        self.require_lower = require_lower
        self.require_digits = require_digits
        self.require_symbols = require_symbols
        self.max_attempts = max_attempts
        self.failed_attempts = 0
        self.last_attempt_time = 0
        self.lockout_duration = 300  # 5 minutes
    
    def validate_password(self, password):
        """
        Validate password against policy
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple of (is_valid, error_messages)
        """
        errors = []
        
        # Length check
        if len(password) < self.min_length:
            errors.append(f"Password must be at least {self.min_length} characters long")
        
        # Character requirements
        if self.require_upper and not any(c.isupper() for c in password):
            errors.append("Password must contain uppercase letters")
        
        if self.require_lower and not any(c.islower() for c in password):
            errors.append("Password must contain lowercase letters")
        
        if self.require_digits and not any(c.isdigit() for c in password):
            errors.append("Password must contain numbers")
        
        if self.require_symbols and not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            errors.append("Password must contain special characters")
        
        # Common password check
        common_passwords = [
            'password', '123456', '123456789', 'qwerty', 'abc123',
            'password123', 'admin', 'letmein', 'welcome', 'monkey'
        ]
        
        if password.lower() in common_passwords:
            errors.append("Password is too common")
        
        return len(errors) == 0, errors
    
    def check_lockout(self):
        """
        Check if account is locked out due to failed attempts
        
        Returns:
            Tuple of (is_locked, remaining_time)
        """
        if self.failed_attempts >= self.max_attempts:
            elapsed = time.time() - self.last_attempt_time
            if elapsed < self.lockout_duration:
                remaining = self.lockout_duration - elapsed
                return True, remaining
            else:
                # Lockout period expired, reset attempts
                self.failed_attempts = 0
        
        return False, 0
    
    def record_failed_attempt(self):
        """Record a failed password attempt"""
        self.failed_attempts += 1
        self.last_attempt_time = time.time()
    
    def reset_attempts(self):
        """Reset failed attempt counter"""
        self.failed_attempts = 0
        self.last_attempt_time = 0


class AuditLogger:
    """Security audit logging"""
    
    def __init__(self, log_file=None):
        self.log_file = log_file
        if log_file:
            self.ensure_log_file_exists()
    
    def ensure_log_file_exists(self):
        """Ensure log file exists and has secure permissions"""
        if not os.path.exists(self.log_file):
            # Create log file with restrictive permissions
            with open(self.log_file, 'w') as f:
                f.write("# Security Audit Log\n")
            
            # Set secure permissions (owner read/write only)
            try:
                os.chmod(self.log_file, 0o600)
            except OSError as e:
                # Log the error but don't fail - best effort on Windows
                print(f"Warning: Could not set secure file permissions: {e}")
    
    def log_event(self, event_type, details, user_id=None):
        """
        Log a security event
        
        Args:
            event_type: Type of event (e.g., 'encryption', 'decryption', 'failed_auth')
            details: Event details
            user_id: Optional user identifier
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S UTC", time.gmtime())
        
        log_entry = {
            'timestamp': timestamp,
            'event_type': event_type,
            'details': details,
            'user_id': user_id or 'unknown'
        }
        
        if self.log_file:
            try:
                with open(self.log_file, 'a') as f:
                    f.write(f"{timestamp} | {event_type} | {user_id or 'unknown'} | {details}\n")
            except (IOError, OSError) as e:
                # Don't fail the operation if logging fails, but could log to stderr
                import sys
                print(f"Warning: Failed to write to audit log: {e}", file=sys.stderr)
        
        return log_entry
    
    def log_encryption(self, file_path, algorithm, success=True):
        """Log encryption event"""
        status = "SUCCESS" if success else "FAILED"
        details = f"File encryption {status}: {file_path} using {algorithm}"
        return self.log_event('encryption', details)
    
    def log_decryption(self, file_path, success=True):
        """Log decryption event"""
        status = "SUCCESS" if success else "FAILED"
        details = f"File decryption {status}: {file_path}"
        return self.log_event('decryption', details)
    
    def log_authentication_failure(self, context=""):
        """Log authentication failure"""
        details = f"Authentication failed: {context}"
        return self.log_event('auth_failure', details)
    
    def log_security_violation(self, violation_type, details):
        """Log security violation"""
        return self.log_event('security_violation', f"{violation_type}: {details}")
