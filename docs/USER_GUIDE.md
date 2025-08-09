# User Guide - Secure File Encryption Tool

## Table of Contents
1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Basic Operations](#basic-operations)
4. [Advanced Features](#advanced-features)
5. [Security Best Practices](#security-best-practices)
6. [Troubleshooting](#troubleshooting)
7. [Technical Specifications](#technical-specifications)

## Installation

### System Requirements
- Python 3.8 or higher
- Windows 10+, macOS 10.14+, or Linux (Ubuntu 18.04+)
- 4GB RAM minimum
- 100MB free disk space

### Installation Steps

1. **Download the application**
   ```bash
   git clone <repository-url>
   cd securityapplication
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python src/main.py
   ```

### Alternative Installation
For a system-wide installation:
```bash
pip install -e .
secure-encrypt-gui
```

## Getting Started

### First Launch
1. Double-click the application icon or run from command line
2. The main window will appear with the file selection interface
3. No initial setup is required - the application is ready to use

### Main Interface Overview
- **File Selection Area**: Drag and drop files/folders or use browse buttons
- **Operation Buttons**: Encrypt and Decrypt buttons
- **Progress Bar**: Shows operation progress
- **Status Bar**: Displays current operation status

## Basic Operations

### Encrypting Files

1. **Select Files/Folders**
   - Click "Browse Files" to select individual files
   - Click "Browse Folder" to select entire folders
   - Or drag and drop files/folders into the selection area

2. **Start Encryption**
   - Click the "🔒 Encrypt Files" button
   - Enter a strong password when prompted
   - Choose output directory for encrypted files

3. **Monitor Progress**
   - Watch the progress bar for completion status
   - View status messages in the status bar

4. **Completion**
   - Encrypted files will have the `.enc` extension
   - Original files remain unchanged (unless you choose to delete them)

### Decrypting Files

1. **Select Encrypted Files**
   - Choose files with `.enc` extension
   - Use browse button or drag and drop

2. **Start Decryption**
   - Click the "🔓 Decrypt Files" button
   - Enter the correct password
   - Choose output directory for decrypted files

3. **Verification**
   - Decrypted files will be restored to their original format
   - File integrity is automatically verified

### Password Guidelines

**Strong Password Requirements:**
- At least 12 characters long
- Contains uppercase letters (A-Z)
- Contains lowercase letters (a-z)
- Contains numbers (0-9)
- Contains special characters (!@#$%^&*)

**Password Security Tips:**
- Use unique passwords for each encryption session
- Consider using a password manager
- Never share passwords via unsecured channels
- Remember: passwords cannot be recovered if forgotten

## Advanced Features

### Batch Operations
- Select multiple files and folders simultaneously
- Process hundreds of files in a single operation
- Automatic progress tracking and error handling

### Folder Encryption
- Encrypts entire directory structures
- Preserves file organization and hierarchy
- Compresses folders before encryption for efficiency

### Settings Configuration
Access via **Tools > Settings**:

- **Encryption Algorithm**: Choose between AES-256-GCM, AES-256-CBC
- **Key Derivation Iterations**: Adjust security vs. speed trade-off
- **Secure Deletion**: Configure overwrite passes for deleted files
- **Default Directories**: Set preferred input/output locations

### File Types Supported
- **Documents**: PDF, DOC, DOCX, TXT, RTF
- **Images**: JPG, PNG, GIF, BMP, TIFF
- **Videos**: MP4, AVI, MOV, WMV
- **Archives**: ZIP, RAR, 7Z
- **Any file type**: No restrictions on file formats

## Security Best Practices

### Password Security
1. **Use Strong Passwords**
   - Minimum 12 characters
   - Mix of character types
   - Avoid common words or patterns

2. **Password Storage**
   - Never store passwords in plain text
   - Use dedicated password managers
   - Don't write passwords on paper

3. **Password Sharing**
   - Share passwords only through secure channels
   - Use separate communication method from file transfer
   - Consider using temporary, one-time passwords

### File Handling
1. **Backup Strategy**
   - Keep encrypted backups in multiple locations
   - Test backup integrity regularly
   - Store backups separately from originals

2. **Original File Management**
   - Securely delete originals after encryption (if desired)
   - Use secure deletion feature for sensitive files
   - Verify encryption success before deleting originals

3. **Storage Locations**
   - Store encrypted files in secure locations
   - Avoid public cloud storage for highly sensitive data
   - Use encrypted storage devices when possible

### Environmental Security
1. **Physical Security**
   - Lock workstation when away
   - Ensure privacy during password entry
   - Secure physical access to devices

2. **Network Security**
   - Use secure networks for file transfers
   - Avoid public Wi-Fi for sensitive operations
   - Keep software updated

## Troubleshooting

### Common Issues

**Application Won't Start**
- Verify Python 3.8+ is installed
- Check all dependencies are installed
- Run with `python -m pip install -r requirements.txt`

**Encryption Fails**
- Ensure sufficient disk space
- Check file permissions
- Verify files are not in use by other applications

**Decryption Fails**
- Verify password is correct (case-sensitive)
- Ensure encrypted file is not corrupted
- Check file was encrypted with this tool

**Performance Issues**
- Close other applications to free memory
- Use smaller batch sizes for large operations
- Check available disk space

### Error Messages

**"Invalid file format"**
- File was not encrypted with this tool
- File may be corrupted
- Try with a different file

**"Authentication failed"**
- Incorrect password
- File may be corrupted
- Verify you're using the right password

**"Insufficient permissions"**
- Run application as administrator (Windows)
- Check file/folder permissions
- Ensure output directory is writable

### Getting Help

1. **Built-in Help**
   - Use Help > User Guide menu
   - Check tooltips on interface elements

2. **Log Files**
   - Check application logs in user config directory
   - Enable debug logging in settings

3. **Community Support**
   - Check project documentation
   - Report issues on project repository
   - Contact support team

## Technical Specifications

### Encryption Details
- **Algorithm**: AES-256 in GCM or CBC mode
- **Key Derivation**: PBKDF2 with SHA-256
- **Iterations**: 100,000+ (configurable)
- **Salt**: 32-byte cryptographically secure random
- **IV/Nonce**: 12-byte (GCM) or 16-byte (CBC) random

### File Format
```
[Magic Header: 4 bytes]
[Version: 4 bytes]
[Salt Length: 4 bytes][Salt: variable]
[IV Length: 4 bytes][IV: variable]
[Hash Length: 4 bytes][Original Hash: variable]
[Encrypted Data: variable]
[Authentication Tag: 16 bytes] (GCM only)
```

### Performance Characteristics
- **Encryption Speed**: ~50-200 MB/s (hardware dependent)
- **Memory Usage**: <1GB for most operations
- **File Size Overhead**: ~100 bytes + algorithm overhead
- **Supported File Size**: Up to available disk space

### Compatibility
- **Cross-Platform**: Windows, macOS, Linux
- **Python Versions**: 3.8, 3.9, 3.10, 3.11+
- **File Systems**: NTFS, HFS+, ext4, and others
- **Archive Formats**: Standard ZIP compression for folders

### Security Certifications
- Implements NIST recommended encryption standards
- Uses well-tested cryptographic libraries
- Regular security audits and updates
- Follows cryptographic best practices

---

For additional support or questions, please refer to the project documentation or contact the development team.
