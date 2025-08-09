"""
Configuration Management
Handles application settings and preferences
"""

import os
import json
import configparser
from pathlib import Path
from typing import Any, Dict, Optional

class Config:
    """Application configuration manager"""
    
    def __init__(self, config_dir=None):
        """
        Initialize configuration manager
        
        Args:
            config_dir: Directory to store config files (default: user home)
        """
        if config_dir is None:
            # Use user's home directory for config
            self.config_dir = Path.home() / '.secure_file_encryption'
        else:
            self.config_dir = Path(config_dir)
        
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / 'config.json'
        
        # Default configuration values
        self.defaults = {
            'encryption_algorithm': 'AES-256-GCM',
            'pbkdf2_iterations': 100000,
            'secure_deletion_passes': 3,
            'default_output_dir': '',
            'auto_clear_selection': True,
            'show_notifications': True,
            'remember_last_directory': True,
            'confirm_deletions': True,
            'show_password_strength': True,
            'max_password_attempts': 3,
            'session_timeout': 1800,  # 30 minutes
            'backup_before_encryption': False,
            'compress_before_encryption': True,
            'verify_after_encryption': True,
            'log_security_events': True,
            'theme': 'default',
            'language': 'en',
            'window_geometry': '800x600',
            'recent_directories': []
        }
        
        self.config = self.defaults.copy()
        self.load()
    
    def load(self):
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    file_config = json.load(f)
                
                # Merge with defaults (in case new settings were added)
                self.config.update(file_config)
                
                # Validate loaded config
                self._validate_config()
                
        except Exception as e:
            print(f"Warning: Failed to load config file: {e}")
            # Use defaults if config file is corrupted
            self.config = self.defaults.copy()
    
    def save(self):
        """Save configuration to file"""
        try:
            # Ensure config directory exists
            self.config_dir.mkdir(exist_ok=True)
            
            # Write config file with proper formatting
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            raise Exception(f"Failed to save configuration: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            key: Configuration key
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """
        Set configuration value
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self.config[key] = value
    
    def reset_to_defaults(self):
        """Reset configuration to default values"""
        self.config = self.defaults.copy()
    
    def get_recent_directories(self, max_count=10):
        """
        Get list of recent directories
        
        Args:
            max_count: Maximum number of directories to return
            
        Returns:
            List of recent directory paths
        """
        recent = self.get('recent_directories', [])
        return recent[:max_count]
    
    def add_recent_directory(self, directory: str, max_count=10):
        """
        Add directory to recent list
        
        Args:
            directory: Directory path to add
            max_count: Maximum number of directories to keep
        """
        recent = self.get('recent_directories', [])
        
        # Remove if already exists
        if directory in recent:
            recent.remove(directory)
        
        # Add to beginning
        recent.insert(0, directory)
        
        # Limit list size
        recent = recent[:max_count]
        
        self.set('recent_directories', recent)
    
    def get_theme_settings(self):
        """Get theme-related settings"""
        return {
            'theme': self.get('theme', 'default'),
            'window_geometry': self.get('window_geometry', '800x600')
        }
    
    def get_security_settings(self):
        """Get security-related settings"""
        return {
            'encryption_algorithm': self.get('encryption_algorithm', 'AES-256-GCM'),
            'pbkdf2_iterations': self.get('pbkdf2_iterations', 100000),
            'max_password_attempts': self.get('max_password_attempts', 3),
            'session_timeout': self.get('session_timeout', 1800),
            'log_security_events': self.get('log_security_events', True)
        }
    
    def get_file_operation_settings(self):
        """Get file operation-related settings"""
        return {
            'backup_before_encryption': self.get('backup_before_encryption', False),
            'compress_before_encryption': self.get('compress_before_encryption', True),
            'verify_after_encryption': self.get('verify_after_encryption', True),
            'secure_deletion_passes': self.get('secure_deletion_passes', 3),
            'auto_clear_selection': self.get('auto_clear_selection', True)
        }
    
    def export_config(self, export_path: str):
        """
        Export configuration to file
        
        Args:
            export_path: Path to export file
        """
        try:
            export_data = {
                'version': '1.0',
                'export_timestamp': str(Path().ctime()),
                'config': self.config
            }
            
            with open(export_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=4, ensure_ascii=False)
                
        except Exception as e:
            raise Exception(f"Failed to export configuration: {e}")
    
    def import_config(self, import_path: str):
        """
        Import configuration from file
        
        Args:
            import_path: Path to import file
        """
        try:
            with open(import_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            if 'config' in import_data:
                # Merge imported config with defaults
                imported_config = import_data['config']
                new_config = self.defaults.copy()
                new_config.update(imported_config)
                
                # Validate imported config
                old_config = self.config.copy()
                self.config = new_config
                
                try:
                    self._validate_config()
                except Exception as e:
                    # Restore old config if validation fails
                    self.config = old_config
                    raise Exception(f"Invalid configuration file: {e}")
            else:
                raise Exception("Invalid configuration file format")
                
        except Exception as e:
            raise Exception(f"Failed to import configuration: {e}")
    
    def _validate_config(self):
        """Validate configuration values"""
        # Validate encryption algorithm
        valid_algorithms = ['AES-256-GCM', 'AES-256-CBC', 'Fernet']
        if self.config.get('encryption_algorithm') not in valid_algorithms:
            self.config['encryption_algorithm'] = self.defaults['encryption_algorithm']
        
        # Validate PBKDF2 iterations
        iterations = self.config.get('pbkdf2_iterations', 100000)
        if not isinstance(iterations, int) or iterations < 10000:
            self.config['pbkdf2_iterations'] = self.defaults['pbkdf2_iterations']
        
        # Validate secure deletion passes
        passes = self.config.get('secure_deletion_passes', 3)
        if not isinstance(passes, int) or passes < 1 or passes > 10:
            self.config['secure_deletion_passes'] = self.defaults['secure_deletion_passes']
        
        # Validate boolean settings
        bool_settings = [
            'auto_clear_selection', 'show_notifications', 'remember_last_directory',
            'confirm_deletions', 'show_password_strength', 'backup_before_encryption',
            'compress_before_encryption', 'verify_after_encryption', 'log_security_events'
        ]
        
        for setting in bool_settings:
            if not isinstance(self.config.get(setting), bool):
                self.config[setting] = self.defaults[setting]
        
        # Validate numeric settings
        numeric_settings = {
            'max_password_attempts': (1, 10),
            'session_timeout': (60, 3600)  # 1 minute to 1 hour
        }
        
        for setting, (min_val, max_val) in numeric_settings.items():
            value = self.config.get(setting)
            if not isinstance(value, int) or value < min_val or value > max_val:
                self.config[setting] = self.defaults[setting]
        
        # Validate recent directories list
        recent = self.config.get('recent_directories', [])
        if not isinstance(recent, list):
            self.config['recent_directories'] = []
        else:
            # Filter out non-existent directories
            valid_dirs = [d for d in recent if isinstance(d, str) and os.path.exists(d)]
            self.config['recent_directories'] = valid_dirs[:10]  # Keep max 10


class LegacyConfigMigrator:
    """Migrates configuration from older versions"""
    
    @staticmethod
    def migrate_from_ini(ini_path: str, config: Config):
        """
        Migrate configuration from INI format
        
        Args:
            ini_path: Path to INI config file
            config: Config instance to update
        """
        try:
            if not os.path.exists(ini_path):
                return
            
            parser = configparser.ConfigParser()
            parser.read(ini_path)
            
            # Mapping from INI sections/keys to JSON keys
            mappings = {
                ('security', 'algorithm'): 'encryption_algorithm',
                ('security', 'iterations'): 'pbkdf2_iterations',
                ('security', 'deletion_passes'): 'secure_deletion_passes',
                ('ui', 'auto_clear'): 'auto_clear_selection',
                ('ui', 'show_notifications'): 'show_notifications',
                ('ui', 'theme'): 'theme',
                ('ui', 'geometry'): 'window_geometry'
            }
            
            for (section, key), json_key in mappings.items():
                if parser.has_section(section) and parser.has_option(section, key):
                    value = parser.get(section, key)
                    
                    # Convert value to appropriate type
                    if json_key in ['pbkdf2_iterations', 'secure_deletion_passes']:
                        value = int(value)
                    elif json_key in ['auto_clear_selection', 'show_notifications']:
                        value = parser.getboolean(section, key)
                    
                    config.set(json_key, value)
            
            # Save migrated config
            config.save()
            
            # Optionally backup old config file
            backup_path = ini_path + '.bak'
            if not os.path.exists(backup_path):
                os.rename(ini_path, backup_path)
                
        except Exception as e:
            print(f"Warning: Failed to migrate legacy config: {e}")


class ConfigValidator:
    """Configuration validation utilities"""
    
    @staticmethod
    def validate_file_path(path: str, must_exist=False, must_be_dir=False):
        """
        Validate file path
        
        Args:
            path: Path to validate
            must_exist: Whether path must exist
            must_be_dir: Whether path must be a directory
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not path:
            return False, "Path cannot be empty"
        
        try:
            path_obj = Path(path)
            
            if must_exist and not path_obj.exists():
                return False, f"Path does not exist: {path}"
            
            if must_be_dir and path_obj.exists() and not path_obj.is_dir():
                return False, f"Path is not a directory: {path}"
            
            return True, ""
            
        except Exception as e:
            return False, f"Invalid path: {e}"
    
    @staticmethod
    def validate_algorithm(algorithm: str):
        """Validate encryption algorithm"""
        valid_algorithms = ['AES-256-GCM', 'AES-256-CBC', 'Fernet']
        if algorithm not in valid_algorithms:
            return False, f"Invalid algorithm. Must be one of: {', '.join(valid_algorithms)}"
        return True, ""
    
    @staticmethod
    def validate_iterations(iterations: int):
        """Validate PBKDF2 iterations"""
        if not isinstance(iterations, int):
            return False, "Iterations must be an integer"
        if iterations < 10000:
            return False, "Iterations must be at least 10,000"
        if iterations > 1000000:
            return False, "Iterations must not exceed 1,000,000"
        return True, ""
