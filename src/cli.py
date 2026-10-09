#!/usr/bin/env python3
"""Stale Scan - Find outdated content in documentation."""

import argparse
import json
import re
import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List


def scan_file(filepath: Path, threshold_days: int = 90) -> dict:
    """Scan a file for stale content."""
    findings = []
    content = filepath.read_text(encoding='utf-8', errors='ignore')
    lines = content.split('\n')
    
    now = datetime.now()
    threshold = timedelta(days=threshold_days)
    
    # Patterns to check
    date_pattern = re.compile(r'(?:dated|updated|last modified|published)\s*:?\s*(\d{4}-\d{2}-\d{2})', re.IGNORECASE)
    todo_pattern = re.compile(r'(TODO|FIXME|HACK|XXX):\s*(.+)', re.IGNORECASE)
    year_pattern = re.compile(r'\b(20\d{2})\b')
    
    for i, line in enumerate(lines, 1):
        # Check for old dates
        for match in date_pattern.finditer(line):
            try:
                date = datetime.strptime(match.group(1), '%Y-%m-%d')
                age = now - date
                if age > threshold:
                    findings.append({
                        "type": "old_date",
                        "line": i,
                        "content": line.strip(),
                        "date": match.group(1),
                        "age_days": age.days
                    })
            except ValueError:
                pass
        
        # Check for aged TODOs
        for match in todo_pattern.finditer(line):
            findings.append({
                "type": "todo",
                "line": i,
                "content": line.strip(),
                "tag": match.group(1).upper()
            })
    
    return {
        "file": str(filepath),
        "findings": findings,
        "finding_count": len(findings)
    }


def scan_directory(dirpath: Path, threshold_days: int = 90, 
                   extensions: List[str] = None) -> List[dict]:
    """Scan all files in a directory."""
    if extensions is None:
        extensions = ['.md', '.txt', '.rst', '.py', '.js', '.ts']
    
    results = []
    for ext in extensions:
        for filepath in dirpath.rglob(f'*{ext}'):
            if filepath.is_file():
                result = scan_file(filepath, threshold_days)
                if result['finding_count'] > 0:
                    results.append(result)
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Scan for stale content in files")
    parser.add_argument("path", help="Directory or file to scan")
    parser.add_argument("-d", "--days", type=int, default=90, help="Stale threshold in days")
    parser.add_argument("-j", "--json", action="store_true", help="JSON output")
    
    args = parser.parse_args()
    
    path = Path(args.path)
    
    if path.is_file():
        results = [scan_file(path, args.days)]
    elif path.is_dir():
        results = scan_directory(path, args.days)
    else:
        print(f"Error: {path} not found", file=sys.stderr)
        sys.exit(1)
    
    if args.json:
        print(json.dumps(results, indent=2))
    else:
        total = sum(r['finding_count'] for r in results)
        print(f"Stale Scan Results: {total} findings in {len(results)} files")
        for result in results:
            print(f"\n{result['file']}:")
            for f in result['findings'][:5]:
                print(f"  [{f['type']}] Line {f['line']}: {f['content'][:60]}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
