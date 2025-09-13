"""
Vercel-compatible entry point for the Streamlit app
"""
import sys
import os

# Add parent directory to path to import our modules
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Import and run the main app
from web_app import main

if __name__ == "__main__":
    main()