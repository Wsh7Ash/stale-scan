#!/usr/bin/env python3
"""Tests for stale-scan."""

import sys
sys.path.insert(0, 'src')
from pathlib import Path
import tempfile
import os

from cli import scan_file


def test_date_finding():
    """Test detection of old dates."""
    content = "Last updated: 2020-01-01\nSome content here"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write(content)
        temp_path = Path(f.name)
    
    try:
        result = scan_file(temp_path, threshold_days=30)
        assert result['finding_count'] >= 1
        assert any(f['type'] == 'old_date' for f in result['findings'])
    finally:
        os.unlink(temp_path)
    
    print("[PASS] Old date detection works")


def test_todo_finding():
    """Test detection of TODOs."""
    content = "Normal line\nTODO: Fix this later\nMore content"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(content)
        temp_path = Path(f.name)
    
    try:
        result = scan_file(temp_path, threshold_days=30)
        assert result['finding_count'] >= 1
        assert any(f['type'] == 'todo' for f in result['findings'])
    finally:
        os.unlink(temp_path)
    
    print("[PASS] TODO detection works")


def test_no_findings():
    """Test file with no issues."""
    content = "Current content without issues\nNothing to find here"
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write(content)
        temp_path = Path(f.name)
    
    try:
        result = scan_file(temp_path, threshold_days=30)
        assert result['finding_count'] == 0
    finally:
        os.unlink(temp_path)
    
    print("[PASS] Clean file handling works")


def run_tests():
    print("Running stale-scan tests...")
    test_date_finding()
    test_todo_finding()
    test_no_findings()
    print("All tests passed!")


if __name__ == "__main__":
    run_tests()
