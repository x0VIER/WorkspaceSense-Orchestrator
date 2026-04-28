import pytest
import os
import json
from pathlib import Path
import WorkspaceSense

def test_hash_calculation(tmp_path):
    """Test that file hashing works correctly."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("hello world")
    
    hash1 = WorkspaceSense.calculate_file_hash(test_file)
    assert hash1 is not None
    
    # Change content and check hash changes
    test_file.write_text("hello world changed")
    hash2 = WorkspaceSense.calculate_file_hash(test_file)
    assert hash1 != hash2

def test_scan_directory(tmp_path):
    """Test directory scanning logic."""
    (tmp_path / "subdir").mkdir()
    (tmp_path / "file1.txt").write_text("content1")
    (tmp_path / "subdir" / "file2.txt").write_text("content2")
    
    manifest = WorkspaceSense.scan_directory(tmp_path)
    
    assert "file1.txt" in manifest
    assert str(Path("subdir") / "file2.txt") in manifest
    assert len(manifest) == 2

def test_compare_states():
    """Test drift detection comparison."""
    old_state = {
        "keep.txt": {"hash": "abc"},
        "modify.txt": {"hash": "def"},
        "delete.txt": {"hash": "ghi"}
    }
    new_state = {
        "keep.txt": {"hash": "abc"},
        "modify.txt": {"hash": "xyz"}, # changed
        "add.txt": {"hash": "123"}     # new
    }
    
    drift = WorkspaceSense.compare_states(old_state, new_state)
    
    assert "add.txt" in drift["added"]
    assert "modify.txt" in drift["modified"]
    assert "delete.txt" in drift["deleted"]
    assert len(drift["added"]) == 1
    assert len(drift["modified"]) == 1
    assert len(drift["deleted"]) == 1
