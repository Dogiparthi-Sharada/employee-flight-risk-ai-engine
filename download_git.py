#!/usr/bin/env python3
"""
Download and install portable Git
"""

import urllib.request
import subprocess
import os
from pathlib import Path
import sys

def download_and_extract_git():
    """Download portable Git and set up PATH"""
    
    git_dir = Path("C:/git-portable/bin")
    git_exe = git_dir / "git.exe"
    
    # If git already exists, just add to PATH
    if git_exe.exists():
        print(f"✅ Git found at {git_exe}")
        add_to_path(str(git_dir))
        return True
    
    print("Downloading portable Git...")
    
    # Download portable git 7z.exe
    url = "https://github.com/git-for-windows/git/releases/download/v2.45.0.windows.1/PortableGit-2.45.0-64-bit.7z.exe"
    target = Path("C:/git-installer.exe")
    
    try:
        urllib.request.urlretrieve(url, target)
        print(f"✅ Downloaded to {target}")
        
        # Extract
        print("Extracting...")
        extract_dir = Path("C:/git-portable")
        extract_dir.mkdir(parents=True, exist_ok=True)
        
        # Run 7z exe
        subprocess.run([str(target), "-o" + str(extract_dir), "-y"], 
                      check=False, capture_output=True)
        
        print(f"✅ Extracted to {extract_dir}")
        
        # Clean up
        target.unlink()
        
        # Add to PATH
        add_to_path(str(git_dir))
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def add_to_path(git_bin_path):
    """Add git to system PATH"""
    try:
        result = subprocess.run(
            ["powershell", "-Command", 
             f'$env:PATH += ";{git_bin_path}"; [Environment]::SetEnvironmentVariable("PATH", $env:PATH, "User")'],
            capture_output=True, text=True, check=False
        )
        print(f"✅ Added to PATH: {git_bin_path}")
    except Exception as e:
        print(f"Note: Could not add to PATH automatically: {e}")
        print(f"Please add manually: {git_bin_path}")

if __name__ == "__main__":
    success = download_and_extract_git()
    
    if success:
        print("\n" + "="*60)
        print("✅ Git Setup Complete!")
        print("="*60)
        print("\nNow run: python setup_git.py")
    else:
        print("\n⚠️  Automatic installation failed")
        print("Please manually download from: https://git-scm.com/download/win")
