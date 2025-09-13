#!/usr/bin/env python3
"""
Web server to run the Financial Agent TUI using textual-web
"""

import os
import asyncio
from pathlib import Path
from financial_agent_textual import FinancialAgentTUI

async def main():
    """Run the textual app directly via textual-web"""
    try:
        # Import textual-web components
        from textual_web import run_async
        
        # Get port from environment or default
        port = int(os.environ.get("PORT", 8000))
        host = os.environ.get("HOST", "0.0.0.0")
        
        print(f"Starting Financial Agent TUI web server on {host}:{port}")
        
        # Create and run the app
        app = FinancialAgentTUI()
        
        # Run the app using textual-web
        await run_async(
            app,
            host=host,
            port=port,
            public_url=None,
        )
        
    except ImportError:
        print("textual-web not properly installed, trying alternative approach...")
        
        # Alternative: Run the app normally (will work locally but not for web deployment)
        app = FinancialAgentTUI()
        app.run()

if __name__ == "__main__":
    asyncio.run(main())