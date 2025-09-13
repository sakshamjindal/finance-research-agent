#!/usr/bin/env python3
"""
Web-based Terminal for Financial Research Agent using FastAPI + xterm.js
Serves the actual Textual TUI in a web browser terminal
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import asyncio
import os
import sys
import pty
import select
import termios
import struct
import fcntl
import signal
from pathlib import Path
from typing import Dict

app = FastAPI(title="Financial Research Agent Terminal", description="Web Terminal for Stock Analysis TUI")

# Store active terminals
terminals: Dict[str, dict] = {}

@app.get("/", response_class=HTMLResponse)
async def terminal_page():
    """Serve the web terminal interface"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Financial Research Agent - Rich CLI</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/xterm@5.3.0/css/xterm.css" />
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            html, body {
                margin: 0;
                padding: 0;
                background: #000;
                font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
                overflow: hidden;
                height: 100vh;
                width: 100vw;
                position: fixed;
                top: 0;
                left: 0;
            }
            
            .header {
                display: none;
            }
            
            .header h1 {
                margin: 0;
                font-size: 1.8rem;
                font-weight: bold;
            }
            
            .header p {
                margin: 5px 0 0 0;
                color: #b0b0b0;
                font-size: 0.9rem;
            }
            
            #terminal-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                background: #000;
                overflow: hidden;
                z-index: 1;
            }
            
            #terminal {
                width: 100%;
                height: 100%;
                padding: 0;
                margin: 0;
                display: block;
            }
            
            .xterm {
                padding: 0 !important;
                margin: 0 !important;
            }
            
            .xterm-screen {
                width: 100% !important;
                height: 100% !important;
            }
            
            .connection-status {
                position: fixed;
                top: 10px;
                right: 20px;
                padding: 5px 10px;
                border-radius: 15px;
                font-size: 0.8rem;
                font-weight: bold;
                z-index: 1000;
            }
            
            .connected {
                background: #4CAF50;
                color: white;
            }
            
            .connecting {
                background: #FF9800;
                color: white;
            }
            
            .disconnected {
                background: #f44336;
                color: white;
            }
            
            .instructions {
                display: none;
            }
            
            .loading {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                color: #4CAF50;
                font-size: 1.2rem;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            
            .spinner {
                width: 20px;
                height: 20px;
                border: 2px solid #333;
                border-top: 2px solid #4CAF50;
                border-radius: 50%;
                animation: spin 1s linear infinite;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            /* Fullscreen terminal - no responsive changes needed */
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🏦 Financial Research Agent</h1>
            <p>Advanced Stock Analysis Terminal - Enter stock ticker and choose analysis mode</p>
            <div id="status" class="connection-status connecting">Connecting...</div>
        </div>
        
        <div id="terminal-container">
            <div id="loading" class="loading">
                <div class="spinner"></div>
                <span>Starting Rich CLI Financial Agent...</span>
            </div>
            <div id="terminal" style="display: none;"></div>
        </div>
        
        <div class="instructions">
            <strong>Instructions:</strong> Type stock symbols (e.g., AAPL, MSFT, TSLA) and follow the prompts • Use Tab/Arrow keys for navigation • Ctrl+Q to quit
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/xterm@5.3.0/lib/xterm.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/xterm-addon-fit@0.8.0/lib/xterm-addon-fit.js"></script>
        <script src="https://cdn.jsdelivr.net/npm/xterm-addon-web-links@0.9.0/lib/xterm-addon-web-links.js"></script>
        
        <script>
            // Initialize terminal
            const terminal = new Terminal({
                cursorBlink: true,
                fontSize: 14,
                fontFamily: 'Monaco, Menlo, "Ubuntu Mono", monospace',
                theme: {
                    background: '#000000',
                    foreground: '#ffffff',
                    cursor: '#4CAF50',
                    selection: '#4CAF50',
                    black: '#000000',
                    red: '#e74c3c',
                    green: '#2ecc71',
                    yellow: '#f1c40f',
                    blue: '#3498db',
                    magenta: '#9b59b6',
                    cyan: '#1abc9c',
                    white: '#ecf0f1',
                    brightBlack: '#34495e',
                    brightRed: '#c0392b',
                    brightGreen: '#27ae60',
                    brightYellow: '#f39c12',
                    brightBlue: '#2980b9',
                    brightMagenta: '#8e44ad',
                    brightCyan: '#16a085',
                    brightWhite: '#bdc3c7'
                },
                allowProposedApi: true
            });
            
            // Add addons
            const fitAddon = new FitAddon.FitAddon();
            const webLinksAddon = new WebLinksAddon.WebLinksAddon();
            
            terminal.loadAddon(fitAddon);
            terminal.loadAddon(webLinksAddon);
            
            // WebSocket connection
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws`;
            let socket;
            let isConnected = false;
            
            function updateStatus(status, text) {
                const statusEl = document.getElementById('status');
                statusEl.className = `connection-status ${status}`;
                statusEl.textContent = text;
            }
            
            function showTerminal() {
                document.getElementById('loading').style.display = 'none';
                document.getElementById('terminal').style.display = 'block';
                terminal.open(document.getElementById('terminal'));
                
                // Fit terminal to container and send initial size
                setTimeout(() => {
                    fitAddon.fit();
                    terminal.focus();
                    
                    // Send initial terminal size to backend
                    if (isConnected) {
                        const cols = terminal.cols;
                        const rows = terminal.rows;
                        console.log(`Initial terminal size: ${cols}x${rows}`);
                        
                        socket.send(JSON.stringify({
                            type: 'resize',
                            cols: cols,
                            rows: rows
                        }));
                    }
                    
                    // Force another resize
                    forceInitialResize();
                }, 200);
            }
            
            function connectWebSocket() {
                updateStatus('connecting', 'Connecting...');
                
                socket = new WebSocket(wsUrl);
                
                socket.onopen = function() {
                    console.log('WebSocket connected');
                    isConnected = true;
                    updateStatus('connected', 'Connected');
                    showTerminal();
                    
                    // Start the financial agent Rich CLI
                    socket.send(JSON.stringify({
                        type: 'start',
                        command: 'python financial_agent_rich.py'
                    }));
                };
                
                socket.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    
                    if (data.type === 'output') {
                        terminal.write(data.data);
                    } else if (data.type === 'resize') {
                        terminal.resize(data.cols, data.rows);
                    }
                };
                
                socket.onclose = function() {
                    console.log('WebSocket disconnected');
                    isConnected = false;
                    updateStatus('disconnected', 'Disconnected');
                    
                    // Attempt to reconnect after 3 seconds
                    setTimeout(connectWebSocket, 3000);
                };
                
                socket.onerror = function(error) {
                    console.error('WebSocket error:', error);
                    updateStatus('disconnected', 'Connection Error');
                };
            }
            
            // Terminal event handlers
            terminal.onData(function(data) {
                if (isConnected) {
                    socket.send(JSON.stringify({
                        type: 'input',
                        data: data
                    }));
                }
            });
            
            terminal.onResize(function(size) {
                if (isConnected) {
                    socket.send(JSON.stringify({
                        type: 'resize',
                        cols: size.cols,
                        rows: size.rows
                    }));
                }
            });
            
            // Window resize handler - resize terminal to fit available space
            function resizeTerminal() {
                if (terminal && fitAddon) {
                    try {
                        // Force fit to container
                        fitAddon.fit();
                        
                        // Send resize to backend
                        if (isConnected) {
                            const cols = terminal.cols;
                            const rows = terminal.rows;
                            console.log(`Resizing terminal to ${cols}x${rows}`);
                            
                            socket.send(JSON.stringify({
                                type: 'resize',
                                cols: cols,
                                rows: rows
                            }));
                        }
                    } catch (error) {
                        console.error('Error resizing terminal:', error);
                    }
                }
            }
            
            // Multiple resize event handlers for better coverage
            window.addEventListener('resize', () => {
                clearTimeout(window.resizeTimeout);
                window.resizeTimeout = setTimeout(resizeTerminal, 100);
            });
            
            window.addEventListener('orientationchange', () => {
                setTimeout(resizeTerminal, 200);
            });
            
            // Force initial resize when terminal is ready
            function forceInitialResize() {
                setTimeout(() => {
                    if (terminal && fitAddon) {
                        fitAddon.fit();
                        resizeTerminal();
                    }
                }, 500);
            }
            
            // Start connection
            connectWebSocket();
            
            // Prevent page reload on Ctrl+R in terminal
            document.addEventListener('keydown', function(e) {
                if (e.ctrlKey && e.key === 'r') {
                    e.preventDefault();
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for terminal communication"""
    await websocket.accept()
    
    terminal_id = None
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data["type"] == "start":
                # Start the financial agent in a PTY
                terminal_id = await start_terminal(websocket, data.get("command", "python financial_agent_textual.py"))
                
            elif data["type"] == "input" and terminal_id:
                # Send input to terminal
                if terminal_id in terminals:
                    terminal_info = terminals[terminal_id]
                    try:
                        os.write(terminal_info["master"], data["data"].encode())
                    except OSError:
                        pass
                        
            elif data["type"] == "resize" and terminal_id:
                # Resize terminal
                if terminal_id in terminals:
                    terminal_info = terminals[terminal_id]
                    try:
                        fcntl.ioctl(terminal_info["master"], termios.TIOCSWINSZ, 
                                  struct.pack("HHHH", data["rows"], data["cols"], 0, 0))
                    except OSError:
                        pass
                        
    except WebSocketDisconnect:
        pass
    finally:
        # Cleanup terminal
        if terminal_id and terminal_id in terminals:
            cleanup_terminal(terminal_id)

async def start_terminal(websocket: WebSocket, command: str) -> str:
    """Start a new terminal session"""
    import uuid
    import subprocess
    
    terminal_id = str(uuid.uuid4())
    
    try:
        # Create PTY
        master, slave = pty.openpty()
        
        # Start the process
        env = os.environ.copy()
        env["TERM"] = "xterm-256color"
        env["COLUMNS"] = "120"
        env["LINES"] = "30"
        env["FORCE_COLOR"] = "1"
        env["PYTHONUNBUFFERED"] = "1"
        
        # Start the Rich CLI financial agent
        process = subprocess.Popen(
            command.split(),
            stdin=slave,
            stdout=slave,
            stderr=slave,
            env=env,
            preexec_fn=os.setsid,
            cwd=os.getcwd()
        )
        
        # Close slave fd in parent
        os.close(slave)
        
        # Store terminal info
        terminals[terminal_id] = {
            "master": master,
            "process": process,
            "websocket": websocket
        }
        
        # Start reading from terminal
        asyncio.create_task(read_terminal_output(terminal_id))
        
        return terminal_id
        
    except Exception as e:
        print(f"Error starting terminal: {e}")
        return None

async def read_terminal_output(terminal_id: str):
    """Read output from terminal and send to WebSocket"""
    if terminal_id not in terminals:
        return
        
    terminal_info = terminals[terminal_id]
    master = terminal_info["master"]
    websocket = terminal_info["websocket"]
    
    try:
        while terminal_id in terminals:
            # Use select to check for data availability
            ready, _, _ = select.select([master], [], [], 0.1)
            
            if master in ready:
                try:
                    data = os.read(master, 1024)
                    if data:
                        await websocket.send_json({
                            "type": "output",
                            "data": data.decode("utf-8", errors="ignore")
                        })
                    else:
                        break
                except OSError:
                    break
            
            await asyncio.sleep(0.01)
            
    except Exception as e:
        print(f"Error reading terminal output: {e}")
    finally:
        cleanup_terminal(terminal_id)

def cleanup_terminal(terminal_id: str):
    """Clean up terminal resources"""
    if terminal_id in terminals:
        terminal_info = terminals[terminal_id]
        
        try:
            # Kill process group
            os.killpg(os.getpgid(terminal_info["process"].pid), signal.SIGTERM)
        except:
            pass
            
        try:
            # Close master fd
            os.close(terminal_info["master"])
        except:
            pass
            
        # Remove from terminals dict
        del terminals[terminal_id]

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Financial Research Agent Terminal"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"Starting Financial Research Agent Terminal on {host}:{port}")
    uvicorn.run(app, host=host, port=port)