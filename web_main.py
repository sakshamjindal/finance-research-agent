#!/usr/bin/env python3
"""
Web deployment entry point for Financial Agent TUI using textual-web
"""

import os
import sys
from pathlib import Path

def main():
    """Main entry point for web deployment"""
    # Set up environment
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    # Import and run the textual app via textual serve command
    import subprocess
    
    # Get the directory where this script is located
    script_dir = Path(__file__).parent
    textual_app_path = script_dir / "financial_agent_textual.py"
    
    # Run textual serve command
    cmd = [
        sys.executable, "-m", "textual", "serve",
        str(textual_app_path),
        "--host", host,
        "--port", str(port)
    ]
    
    print(f"Starting Financial Agent TUI on {host}:{port}")
    print(f"Command: {' '.join(cmd)}")
    
    # Execute the command
    os.execvp(sys.executable, cmd)

if __name__ == "__main__":
    main()