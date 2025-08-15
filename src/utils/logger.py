"""
Logging utilities for the application
"""

import logging
import logging.handlers
import os
import sys
from pathlib import Path
from datetime import datetime

def setup_logging(log_level=logging.INFO, log_to_file=True, log_dir=None):
    """
    Setup application logging
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_to_file: Whether to log to file
        log_dir: Directory for log files (default: user config dir)
    """
    
    # Create logger
    logger = logging.getLogger('secure_file_encryption')
    logger.setLevel(log_level)
    
    # Clear any existing handlers
    logger.handlers.clear()
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_to_file:
        if log_dir is None:
            log_dir = Path.home() / '.secure_file_encryption' / 'logs'
        else:
            log_dir = Path(log_dir)
        
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create rotating file handler
        log_file = log_dir / 'application.log'
        file_handler = logging.handlers.RotatingFileHandler(
            log_file, maxBytes=10*1024*1024, backupCount=5  # 10MB files, keep 5 backups
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
        # Set secure permissions on log file
        try:
            os.chmod(log_file, 0o600)
        except OSError as e:
            # Best effort on Windows - log but don't fail
            print(f"Warning: Could not set secure log file permissions: {e}", file=sys.stderr)
    
    return logger

def get_logger(name=None):
    """
    Get logger instance
    
    Args:
        name: Logger name (default: secure_file_encryption)
        
    Returns:
        Logger instance
    """
    if name is None:
        name = 'secure_file_encryption'
    return logging.getLogger(name)

class SecurityLogger:
    """Specialized logger for security events"""
    
    def __init__(self, log_dir=None):
        """
        Initialize security logger
        
        Args:
            log_dir: Directory for security log files
        """
        if log_dir is None:
            log_dir = Path.home() / '.secure_file_encryption' / 'logs'
        else:
            log_dir = Path(log_dir)
        
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create security logger
        self.logger = logging.getLogger('security_audit')
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create security log file handler
        security_log_file = log_dir / 'security.log'
        handler = logging.handlers.RotatingFileHandler(
            security_log_file, maxBytes=50*1024*1024, backupCount=10  # 50MB files, keep 10
        )
        
        # Security log format includes more details
        formatter = logging.Formatter(
            '%(asctime)s - SECURITY - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S UTC'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        # Set restrictive permissions
        try:
            os.chmod(security_log_file, 0o600)
        except OSError as e:
            print(f"Warning: Could not set secure permissions on security log: {e}", file=sys.stderr)
    
    def log_encryption_start(self, file_path, algorithm):
        """Log encryption operation start"""
        self.logger.info(f"ENCRYPTION_START: {file_path} using {algorithm}")
    
    def log_encryption_success(self, file_path, algorithm, file_size):
        """Log successful encryption"""
        self.logger.info(f"ENCRYPTION_SUCCESS: {file_path} ({file_size} bytes) using {algorithm}")
    
    def log_encryption_failure(self, file_path, algorithm, error):
        """Log encryption failure"""
        self.logger.error(f"ENCRYPTION_FAILURE: {file_path} using {algorithm} - {error}")
    
    def log_decryption_start(self, file_path):
        """Log decryption operation start"""
        self.logger.info(f"DECRYPTION_START: {file_path}")
    
    def log_decryption_success(self, file_path, file_size):
        """Log successful decryption"""
        self.logger.info(f"DECRYPTION_SUCCESS: {file_path} ({file_size} bytes)")
    
    def log_decryption_failure(self, file_path, error):
        """Log decryption failure"""
        self.logger.error(f"DECRYPTION_FAILURE: {file_path} - {error}")
    
    def log_authentication_failure(self, context=""):
        """Log authentication failure"""
        self.logger.warning(f"AUTH_FAILURE: {context}")
    
    def log_file_access(self, file_path, operation, success=True):
        """Log file access attempt"""
        status = "SUCCESS" if success else "FAILURE"
        self.logger.info(f"FILE_ACCESS_{status}: {operation} on {file_path}")
    
    def log_security_violation(self, violation_type, details):
        """Log security violation"""
        self.logger.critical(f"SECURITY_VIOLATION: {violation_type} - {details}")
    
    def log_application_start(self):
        """Log application startup"""
        self.logger.info("APPLICATION_START: Secure File Encryption Tool started")
    
    def log_application_stop(self):
        """Log application shutdown"""
        self.logger.info("APPLICATION_STOP: Secure File Encryption Tool stopped")

class PerformanceLogger:
    """Logger for performance monitoring"""
    
    def __init__(self, log_dir=None):
        """
        Initialize performance logger
        
        Args:
            log_dir: Directory for performance log files
        """
        if log_dir is None:
            log_dir = Path.home() / '.secure_file_encryption' / 'logs'
        else:
            log_dir = Path(log_dir)
        
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create performance logger
        self.logger = logging.getLogger('performance')
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Create performance log file handler
        perf_log_file = log_dir / 'performance.log'
        handler = logging.handlers.RotatingFileHandler(
            perf_log_file, maxBytes=20*1024*1024, backupCount=5  # 20MB files, keep 5
        )
        
        formatter = logging.Formatter(
            '%(asctime)s - PERF - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def log_operation_time(self, operation, duration, file_size=None):
        """
        Log operation timing
        
        Args:
            operation: Operation name
            duration: Duration in seconds
            file_size: Optional file size in bytes
        """
        if file_size:
            throughput = file_size / duration if duration > 0 else 0
            self.logger.info(f"{operation}: {duration:.2f}s, {file_size} bytes, {throughput:.0f} bytes/s")
        else:
            self.logger.info(f"{operation}: {duration:.2f}s")
    
    def log_memory_usage(self, operation, memory_mb):
        """Log memory usage"""
        self.logger.info(f"MEMORY_{operation}: {memory_mb:.1f} MB")
    
    def log_startup_time(self, duration):
        """Log application startup time"""
        self.logger.info(f"STARTUP_TIME: {duration:.2f}s")

class LogAnalyzer:
    """Analyzer for log files"""
    
    def __init__(self, log_dir=None):
        """
        Initialize log analyzer
        
        Args:
            log_dir: Directory containing log files
        """
        if log_dir is None:
            log_dir = Path.home() / '.secure_file_encryption' / 'logs'
        else:
            log_dir = Path(log_dir)
        
        self.log_dir = log_dir
    
    def get_security_events(self, start_date=None, end_date=None):
        """
        Get security events from security log
        
        Args:
            start_date: Start date filter (datetime)
            end_date: End date filter (datetime)
            
        Returns:
            List of security events
        """
        events = []
        security_log = self.log_dir / 'security.log'
        
        if not security_log.exists():
            return events
        
        try:
            with open(security_log, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or not line.startswith('20'):  # Skip non-log lines
                        continue
                    
                    # Parse log line
                    parts = line.split(' - ', 3)
                    if len(parts) >= 4:
                        timestamp_str = parts[0]
                        level = parts[2]
                        message = parts[3]
                        
                        try:
                            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
                            
                            # Apply date filters
                            if start_date and timestamp < start_date:
                                continue
                            if end_date and timestamp > end_date:
                                continue
                            
                            events.append({
                                'timestamp': timestamp,
                                'level': level,
                                'message': message
                            })
                        except ValueError:
                            continue  # Skip malformed timestamp
        except (IOError, OSError) as e:
            print(f"Warning: Could not read security log file: {e}", file=sys.stderr)
        
        return events
    
    def get_performance_stats(self, operation_type=None):
        """
        Get performance statistics
        
        Args:
            operation_type: Filter by operation type
            
        Returns:
            Dictionary with performance statistics
        """
        stats = {
            'total_operations': 0,
            'avg_duration': 0,
            'max_duration': 0,
            'min_duration': float('inf'),
            'avg_throughput': 0,
            'operations': []
        }
        
        perf_log = self.log_dir / 'performance.log'
        
        if not perf_log.exists():
            return stats
        
        durations = []
        throughputs = []
        
        try:
            with open(perf_log, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line or 'PERF' not in line:
                        continue
                    
                    # Parse performance log line
                    if operation_type and operation_type not in line:
                        continue
                    
                    # Extract duration and throughput
                    if ': ' in line and 's' in line:
                        try:
                            parts = line.split(': ', 1)[1]
                            if 'bytes/s' in parts:
                                # Has throughput info
                                metrics = parts.split(', ')
                                duration = float(metrics[0].replace('s', ''))
                                throughput = float(metrics[2].split()[0])
                                
                                durations.append(duration)
                                throughputs.append(throughput)
                            else:
                                # Duration only
                                duration = float(parts.replace('s', ''))
                                durations.append(duration)
                        except (ValueError, IndexError):
                            continue
        except (IOError, OSError) as e:
            print(f"Warning: Could not read performance log: {e}", file=sys.stderr)
        
        if durations:
            stats['total_operations'] = len(durations)
            stats['avg_duration'] = sum(durations) / len(durations)
            stats['max_duration'] = max(durations)
            stats['min_duration'] = min(durations)
        
        if throughputs:
            stats['avg_throughput'] = sum(throughputs) / len(throughputs)
        
        return stats
    
    def cleanup_old_logs(self, days_to_keep=30):
        """
        Clean up log files older than specified days
        
        Args:
            days_to_keep: Number of days to keep logs
        """
        if not self.log_dir.exists():
            return
        
        cutoff_time = datetime.now().timestamp() - (days_to_keep * 24 * 3600)
        
        for log_file in self.log_dir.glob('*.log*'):
            try:
                if log_file.stat().st_mtime < cutoff_time:
                    log_file.unlink()
            except (OSError, IOError) as e:
                print(f"Warning: Could not delete old log file {log_file}: {e}", file=sys.stderr)
                continue  # Skip files that can't be deleted
