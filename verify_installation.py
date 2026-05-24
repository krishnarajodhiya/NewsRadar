#!/usr/bin/env python3
"""
NewsVerify AI - Installation & Verification Script
Verifies that all required files have been created correctly
"""

import os
import sys
from pathlib import Path

# ANSI Colors
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_header():
    print(f"""
{BOLD}{BLUE}
╔══════════════════════════════════════════════════════════════╗
║           NewsVerify AI - Installation Verification          ║
║                  Fake News Detection System                  ║
╚══════════════════════════════════════════════════════════════╝
{RESET}
""")

def verify_file(path, file_type="FILE"):
    """Verify if a file exists"""
    if os.path.exists(path):
        size = os.path.getsize(path) if os.path.isfile(path) else 0
        size_str = f" ({size} bytes)" if size > 0 else ""
        print(f"{GREEN}✓{RESET} {path}{size_str}")
        return True
    else:
        print(f"{RED}✗{RESET} {path} - NOT FOUND")
        return False

def main():
    print_header()
    
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Verification sections
    sections = {
        "📄 Documentation Files": [
            "README.md",
            "QUICKSTART.md",
            "API_DOCS.md",
            "CONFIG.md",
            "SETUP_SUMMARY.md",
            "PROJECT_OVERVIEW.md",
        ],
        "⚙️ Configuration Files": [
            "requirements.txt",
            ".env.example",
            ".gitignore",
            "package.json",
        ],
        "🐍 Backend Files": [
            "backend/app.py",
            "backend/train_model.py",
            "backend/preprocessor.py",
            "backend/database.py",
        ],
        "🎨 Frontend Files": [
            "frontend/index.html",
            "frontend/style.css",
            "frontend/script.js",
        ],
        "🔧 Setup Scripts": [
            "setup.sh",
            "setup.bat",
            "run.sh",
            "run.bat",
        ],
        "📁 Directories": [
            "backend",
            "frontend",
            "models",
            "data",
        ],
    }
    
    total_files = 0
    verified_files = 0
    
    for section, files in sections.items():
        print(f"\n{BOLD}{section}{RESET}")
        print("-" * 60)
        
        for file_path in files:
            if verify_file(file_path):
                verified_files += 1
            total_files += 1
    
    # Summary
    print(f"\n{BOLD}{'='*60}{RESET}")
    print(f"{BOLD}Verification Summary:{RESET}")
    print(f"{'='*60}")
    
    if verified_files == total_files:
        print(f"{GREEN}{BOLD}✓ All {total_files} components verified!{RESET}")
        print(f"{GREEN}✓ Project structure is complete.{RESET}")
        return 0
    else:
        missing = total_files - verified_files
        print(f"{YELLOW}⚠ {missing} files missing out of {total_files}{RESET}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
