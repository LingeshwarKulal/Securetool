"""
Test Configuration
"""

import pytest
import tempfile
import shutil
from pathlib import Path

@pytest.fixture
def temp_dir():
    """Create a temporary directory for tests"""
    temp_path = Path(tempfile.mkdtemp())
    yield temp_path
    shutil.rmtree(temp_path, ignore_errors=True)

@pytest.fixture
def sample_text_file(temp_dir):
    """Create a sample text file for testing"""
    file_path = temp_dir / "test_file.txt"
    with open(file_path, 'w') as f:
        f.write("This is a test file for encryption testing.\n")
        f.write("It contains multiple lines of text.\n")
        f.write("Each line tests different scenarios.\n")
    return file_path

@pytest.fixture
def sample_binary_file(temp_dir):
    """Create a sample binary file for testing"""
    file_path = temp_dir / "test_binary.bin"
    with open(file_path, 'wb') as f:
        f.write(b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09')
        f.write(b'\xFF\xFE\xFD\xFC\xFB\xFA\xF9\xF8\xF7\xF6')
    return file_path

@pytest.fixture
def sample_folder(temp_dir):
    """Create a sample folder structure for testing"""
    folder_path = temp_dir / "test_folder"
    folder_path.mkdir()
    
    # Create some files in the folder
    (folder_path / "file1.txt").write_text("Content of file 1")
    (folder_path / "file2.txt").write_text("Content of file 2")
    
    # Create a subfolder
    subfolder = folder_path / "subfolder"
    subfolder.mkdir()
    (subfolder / "file3.txt").write_text("Content of file 3")
    
    return folder_path
