"""
Build Script for BSSOD Analyzer Parser Tool

This script creates a standalone executable using PyInstaller.
Run with: python build.py
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path


# Build configuration
APP_NAME = "BSSOD_Analyzer_Parser"
MAIN_SCRIPT = "gui_app.py"
ICON_FILE = None  # Set to path of .ico file if available
MANIFEST_FILE = "app.manifest"  # UAC elevation manifest
ONE_FILE = True   # Create single executable
CONSOLE = False   # Hide console window


def clean_build():
    """Clean previous build artifacts."""
    dirs_to_clean = ['build', 'dist', '__pycache__']
    files_to_clean = [f'{APP_NAME}.spec']
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            print(f"Removing {dir_name}/...")
            shutil.rmtree(dir_name)
    
    for file_name in files_to_clean:
        if os.path.exists(file_name):
            print(f"Removing {file_name}...")
            os.remove(file_name)


def build_executable():
    """Build the executable using PyInstaller."""
    print("=" * 60)
    print("Building BSSOD Analyzer Parser Tool")
    print("=" * 60)
    
    # Base PyInstaller command
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        '--name', APP_NAME,
        '--noconfirm',
        '--clean',
    ]
    
    # Add options
    if ONE_FILE:
        cmd.append('--onefile')
    
    if not CONSOLE:
        cmd.append('--windowed')
    
    if ICON_FILE and os.path.exists(ICON_FILE):
        cmd.extend(['--icon', ICON_FILE])
    
    # Add UAC manifest for admin elevation (required for C:\Windows access)
    if os.path.exists(MANIFEST_FILE):
        cmd.extend(['--manifest', MANIFEST_FILE])
        print(f"Using manifest: {MANIFEST_FILE} (requires Administrator)")
    
    # Add data files (include src directory)
    cmd.extend(['--add-data', 'src;src'])
    
    # Hidden imports
    cmd.extend(['--hidden-import', 'customtkinter'])
    cmd.extend(['--hidden-import', 'tkinter'])
    
    # Main script
    cmd.append(MAIN_SCRIPT)
    
    print(f"\nRunning: {' '.join(cmd)}\n")
    
    # Run PyInstaller
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode == 0:
        print("\n" + "=" * 60)
        print("BUILD SUCCESSFUL!")
        print("=" * 60)
        
        exe_path = Path('dist') / (APP_NAME + '.exe')
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"\nExecutable: {exe_path}")
            print(f"Size: {size_mb:.2f} MB")
        
        print("\nYou can distribute the executable to users.")
        print("No Python installation required on target machines.")
    else:
        print("\n" + "=" * 60)
        print("BUILD FAILED!")
        print("=" * 60)
        sys.exit(1)


def main():
    """Main entry point."""
    # Change to script directory
    script_dir = Path(__file__).parent.absolute()
    os.chdir(script_dir)
    
    print(f"Working directory: {script_dir}")
    
    # Parse arguments
    if '--clean' in sys.argv:
        clean_build()
        print("Clean complete.")
        return
    
    if '--clean-build' in sys.argv:
        clean_build()
    
    # Build
    build_executable()


if __name__ == "__main__":
    main()
