# 🔍 Stale Scan

A content-tool that scans documentation files for stale content - outdated dates, TODOs older than a threshold, references to deprecated features.

## Quick Start

```bash
python -m stale_scan.cli docs/
```

## Features

- Find files with old dates in headers
- Locate aged TODO/FIXME comments
- Detect references to removed features
- JSON/markdown report output

## License

MIT
