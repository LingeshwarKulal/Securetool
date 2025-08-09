# Secure File Encryption To3. **Run the application:**
```bash
python src/main.py
```
Or on Windows: double-click `launch.bat`
A desktop application for secure file and folder encryption using industry-standard AES encryption.

## Features

- **File & Folder Encryption**: Encrypt individual files or entire directories
- **AES-256 Encryption**: Military-grade security using the cryptography library
- **Password Protection**: Strong password requirements with visual strength indicators
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **User-Friendly Interface**: Simple browse-button GUI built with tkinter
- **Data Integrity**: SHA-256 checksums ensure file integrity
- **Batch Operations**: Process multiple files simultaneously

## Installation

1. Clone this repository:
```bash
git clone <repository-url>
cd securityapplication
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python src/main.py
```

## Usage

1. **Encryption**:
   - Launch the application
   - Use Browse Files/Browse Folder buttons to select files
   - Click "Encrypt"
   - Enter a strong password
   - Choose output location
   - Wait for completion

2. **Decryption**:
   - Select encrypted files (.enc extension)
   - Click "Decrypt"
   - Enter the correct password
   - Choose output location
   - Wait for completion

## Security Features

- **AES-256-GCM**: Authenticated encryption with associated data
- **PBKDF2**: Key derivation with 100,000+ iterations
- **Secure Random**: Cryptographically secure salt generation
- **Memory Protection**: Secure key cleanup after operations

## Project Structure

```
securityapplication/
├── src/
│   ├── main.py              # Application entry point
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py   # Main GUI window
│   │   └── dialogs.py       # Password and settings dialogs
│   ├── core/
│   │   ├── __init__.py
│   │   ├── encryption.py    # Encryption/decryption engine
│   │   ├── file_manager.py  # File operations
│   │   └── security.py      # Security utilities
│   └── utils/
│       ├── __init__.py
│       ├── config.py        # Configuration management
│       └── logger.py        # Logging utilities
├── tests/                   # Unit and integration tests
├── docs/                    # Documentation
├── assets/                  # Icons and resources
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── PRD.md                  # Product Requirements Document
```

## Testing

Run the test suite:
```bash
pytest tests/ -v --cov=src
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Security Notice

This tool is designed for legitimate file protection purposes. Users are responsible for:
- Remembering their encryption passwords (passwords cannot be recovered)
- Complying with local laws and regulations
- Using strong, unique passwords
- Keeping backup copies of important data

## Support

For issues, feature requests, or questions, please open an issue on the project repository.
