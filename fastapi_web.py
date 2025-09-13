#!/usr/bin/env python3
"""
Web-based Financial Research Agent using FastAPI
Alternative to textual-web that works with Railway deployment
"""

from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import asyncio
import json
import os
from pathlib import Path
from typing import Optional, Dict, Any

from finance_core import FinancialAnalyzer
from comprehensive_analyzer import ComprehensiveAnalyzer

# Initialize FastAPI app
app = FastAPI(title="Financial Research Agent", description="Advanced Stock Analysis Tool")

# Global analyzer instances
analyzer = FinancialAnalyzer()
comprehensive_analyzer = ComprehensiveAnalyzer()

class AnalysisRequest(BaseModel):
    symbol: str
    analysis_mode: str = "standard"  # "standard" or "comprehensive"

class AnalysisResponse(BaseModel):
    symbol: str
    status: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with analysis form"""
    html_content = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Financial Research Agent</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                margin: 0; 
                padding: 20px; 
                background: #1a1a1a; 
                color: #e0e0e0; 
            }
            .container { 
                max-width: 1200px; 
                margin: 0 auto; 
                background: #2d2d2d; 
                border-radius: 10px; 
                padding: 30px; 
                box-shadow: 0 4px 6px rgba(0,0,0,0.3); 
            }
            h1 { 
                text-align: center; 
                color: #4CAF50; 
                margin-bottom: 30px; 
                font-size: 2.5rem; 
            }
            .form-group { 
                margin-bottom: 20px; 
            }
            label { 
                display: block; 
                margin-bottom: 5px; 
                font-weight: bold; 
                color: #b0b0b0; 
            }
            input[type="text"] { 
                width: 100%; 
                padding: 12px; 
                border: 1px solid #555; 
                border-radius: 5px; 
                background: #3a3a3a; 
                color: #e0e0e0; 
                font-size: 16px; 
            }
            .button-group { 
                display: flex; 
                gap: 10px; 
                justify-content: center; 
                margin: 30px 0; 
            }
            button { 
                padding: 12px 24px; 
                border: none; 
                border-radius: 5px; 
                cursor: pointer; 
                font-size: 16px; 
                font-weight: bold; 
                transition: background-color 0.3s; 
            }
            .btn-standard { 
                background: #2196F3; 
                color: white; 
            }
            .btn-standard:hover { 
                background: #1976D2; 
            }
            .btn-comprehensive { 
                background: #9C27B0; 
                color: white; 
            }
            .btn-comprehensive:hover { 
                background: #7B1FA2; 
            }
            #loading { 
                display: none; 
                text-align: center; 
                margin: 20px; 
                color: #4CAF50; 
            }
            #results { 
                margin-top: 30px; 
                padding: 20px; 
                background: #3a3a3a; 
                border-radius: 5px; 
                border-left: 4px solid #4CAF50; 
            }
            .metric-group { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                gap: 20px; 
                margin: 20px 0; 
            }
            .metric-card { 
                background: #2d2d2d; 
                padding: 15px; 
                border-radius: 8px; 
                border: 1px solid #555; 
            }
            .metric-title { 
                color: #4CAF50; 
                font-weight: bold; 
                margin-bottom: 10px; 
                font-size: 1.1rem; 
            }
            .error { 
                color: #f44336; 
                background: #3a1a1a; 
                padding: 15px; 
                border-radius: 5px; 
                margin: 10px 0; 
                border: 1px solid #f44336; 
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🏦 Financial Research Agent</h1>
            <p style="text-align: center; color: #b0b0b0; margin-bottom: 30px;">
                Advanced Stock Analysis with Fundamental, Technical, and Sentiment Analysis
            </p>
            
            <form id="analysisForm">
                <div class="form-group">
                    <label for="symbol">Stock Ticker Symbol:</label>
                    <input type="text" id="symbol" name="symbol" placeholder="e.g., AAPL, MSFT, TSLA" required>
                </div>
                
                <div class="button-group">
                    <button type="button" class="btn-standard" onclick="analyzeStock('standard')">
                        📈 Standard Analysis
                    </button>
                    <button type="button" class="btn-comprehensive" onclick="analyzeStock('comprehensive')">
                        🔬 Comprehensive Analysis
                    </button>
                </div>
            </form>
            
            <div id="loading">
                <p>⏳ Analyzing stock... This may take a few moments.</p>
                <div style="margin: 20px;">
                    <div style="display: inline-block; width: 300px; height: 4px; background: #555; border-radius: 2px;">
                        <div style="width: 0%; height: 100%; background: #4CAF50; border-radius: 2px; animation: loading 3s ease-in-out infinite;" id="progressBar"></div>
                    </div>
                </div>
            </div>
            
            <div id="results" style="display: none;"></div>
        </div>
        
        <style>
            @keyframes loading {
                0% { width: 0%; }
                50% { width: 70%; }
                100% { width: 100%; }
            }
        </style>
        
        <script>
            async function analyzeStock(mode) {
                const symbol = document.getElementById('symbol').value.trim().toUpperCase();
                if (!symbol) {
                    alert('Please enter a stock ticker symbol');
                    return;
                }
                
                document.getElementById('loading').style.display = 'block';
                document.getElementById('results').style.display = 'none';
                
                try {
                    const response = await fetch('/analyze', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            symbol: symbol,
                            analysis_mode: mode
                        })
                    });
                    
                    const data = await response.json();
                    document.getElementById('loading').style.display = 'none';
                    displayResults(data);
                    
                } catch (error) {
                    document.getElementById('loading').style.display = 'none';
                    document.getElementById('results').innerHTML = 
                        `<div class="error">Error: ${error.message}</div>`;
                    document.getElementById('results').style.display = 'block';
                }
            }
            
            function displayResults(data) {
                const resultsDiv = document.getElementById('results');
                if (data.status === 'error') {
                    resultsDiv.innerHTML = `<div class="error">Error: ${data.error}</div>`;
                    resultsDiv.style.display = 'block';
                    return;
                }
                
                const result = data.data;
                let html = `
                    <h2>Analysis Results for ${result.symbol}</h2>
                    
                    <div class="metric-group">
                        <div class="metric-card">
                            <div class="metric-title">Stock Overview</div>
                            <p><strong>Company:</strong> ${result.name || 'N/A'}</p>
                            <p><strong>Current Price:</strong> $${result.current_price || 'N/A'}</p>
                            <p><strong>Change:</strong> ${result.change_percent ? (result.change_percent >= 0 ? '+' : '') + result.change_percent.toFixed(2) + '%' : 'N/A'}</p>
                        </div>
                        
                        <div class="metric-card">
                            <div class="metric-title">Recommendation</div>
                            <p><strong>Action:</strong> <span style="color: ${getRecommendationColor(result.recommendation?.action)}">${result.recommendation?.action || 'N/A'}</span></p>
                            <p><strong>Confidence:</strong> ${result.recommendation?.confidence || 'N/A'}%</p>
                            <p><strong>Risk Level:</strong> ${result.recommendation?.risk_level || 'N/A'}</p>
                            ${result.recommendation?.price_target ? `<p><strong>Price Target:</strong> $${result.recommendation.price_target}</p>` : ''}
                        </div>
                    </div>
                `;
                
                if (result.fundamentals) {
                    html += `
                        <div class="metric-card">
                            <div class="metric-title">Fundamental Analysis</div>
                            <p><strong>P/E Ratio:</strong> ${result.fundamentals.pe_ratio?.toFixed(2) || 'N/A'}</p>
                            <p><strong>ROE:</strong> ${result.fundamentals.roe?.toFixed(1) || 'N/A'}%</p>
                            <p><strong>Profit Margin:</strong> ${result.fundamentals.profit_margin?.toFixed(1) || 'N/A'}%</p>
                            <p><strong>Debt/Equity:</strong> ${result.fundamentals.debt_to_equity?.toFixed(2) || 'N/A'}</p>
                            <p><strong>Score:</strong> ${result.fundamentals.score?.toFixed(1) || 'N/A'}/100</p>
                        </div>
                    `;
                }
                
                if (result.technicals) {
                    html += `
                        <div class="metric-card">
                            <div class="metric-title">Technical Analysis</div>
                            <p><strong>RSI (14):</strong> ${result.technicals.rsi?.toFixed(1) || 'N/A'}</p>
                            <p><strong>MACD:</strong> ${result.technicals.macd?.toFixed(4) || 'N/A'}</p>
                            <p><strong>SMA 20:</strong> $${result.technicals.sma_20?.toFixed(2) || 'N/A'}</p>
                            <p><strong>Trend:</strong> ${result.technicals.trend || 'N/A'}</p>
                            <p><strong>Score:</strong> ${result.technicals.score?.toFixed(1) || 'N/A'}/100</p>
                        </div>
                    `;
                }
                
                if (result.sentiment) {
                    html += `
                        <div class="metric-card">
                            <div class="metric-title">Sentiment Analysis</div>
                            <p><strong>Analyst Rating:</strong> ${result.sentiment.analyst_rating || 'N/A'}</p>
                            <p><strong>News Sentiment:</strong> ${result.sentiment.news_sentiment?.toFixed(1) || 'N/A'}/100</p>
                            <p><strong>Social Sentiment:</strong> ${result.sentiment.social_sentiment?.toFixed(1) || 'N/A'}/100</p>
                            <p><strong>Score:</strong> ${result.sentiment.score?.toFixed(1) || 'N/A'}/100</p>
                        </div>
                    `;
                }
                
                if (result.comprehensive_analysis) {
                    html += `
                        <div class="metric-card">
                            <div class="metric-title">🔬 Comprehensive Analysis</div>
                            <p><strong>Composite Score:</strong> ${result.comprehensive_analysis.composite_score?.toFixed(1) || 'N/A'}/100</p>
                            <p><strong>Confidence Level:</strong> ${(result.comprehensive_analysis.confidence_level * 100)?.toFixed(1) || 'N/A'}%</p>
                            ${result.comprehensive_analysis.financial_health?.piotroski_score ? `<p><strong>Piotroski Score:</strong> ${result.comprehensive_analysis.financial_health.piotroski_score}/9</p>` : ''}
                            ${result.comprehensive_analysis.financial_health?.altman_z_score ? `<p><strong>Altman Z-Score:</strong> ${result.comprehensive_analysis.financial_health.altman_z_score.toFixed(2)}</p>` : ''}
                        </div>
                    `;
                }
                
                resultsDiv.innerHTML = html;
                resultsDiv.style.display = 'block';
            }
            
            function getRecommendationColor(action) {
                const colors = {
                    'STRONG_BUY': '#4CAF50',
                    'BUY': '#8BC34A',
                    'HOLD': '#FF9800',
                    'SELL': '#FF5722',
                    'STRONG_SELL': '#f44336'
                };
                return colors[action] || '#e0e0e0';
            }
            
            // Allow Enter key to submit
            document.getElementById('symbol').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    analyzeStock('standard');
                }
            });
        </script>
    </body>
    </html>
    """
    return HTMLResponse(content=html_content)

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_stock(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """Analyze a stock symbol"""
    try:
        symbol = request.symbol.upper().strip()
        
        # Perform analysis
        if request.analysis_mode == "comprehensive":
            # Comprehensive analysis
            stock_data = analyzer.get_stock_data(symbol)
            fundamentals = analyzer.analyze_fundamentals(symbol)
            technicals = analyzer.analyze_technicals(symbol)
            sentiment = analyzer.analyze_sentiment(symbol)
            comprehensive_analysis = comprehensive_analyzer.perform_comprehensive_analysis(symbol)
            recommendation = analyzer.generate_recommendation(symbol, fundamentals, technicals, sentiment)
            
            result = {
                "symbol": stock_data.symbol,
                "name": stock_data.name,
                "current_price": stock_data.current_price,
                "change_percent": stock_data.change_percent,
                "fundamentals": fundamentals.__dict__ if fundamentals else None,
                "technicals": technicals.__dict__ if technicals else None,
                "sentiment": sentiment.__dict__ if sentiment else None,
                "comprehensive_analysis": comprehensive_analysis.__dict__ if comprehensive_analysis else None,
                "recommendation": recommendation.__dict__ if recommendation else None
            }
        else:
            # Standard analysis
            stock_data = analyzer.get_stock_data(symbol)
            fundamentals = analyzer.analyze_fundamentals(symbol)
            technicals = analyzer.analyze_technicals(symbol)
            sentiment = analyzer.analyze_sentiment(symbol)
            recommendation = analyzer.generate_recommendation(symbol, fundamentals, technicals, sentiment)
            
            result = {
                "symbol": stock_data.symbol,
                "name": stock_data.name,
                "current_price": stock_data.current_price,
                "change_percent": stock_data.change_percent,
                "fundamentals": fundamentals.__dict__ if fundamentals else None,
                "technicals": technicals.__dict__ if technicals else None,
                "sentiment": sentiment.__dict__ if sentiment else None,
                "recommendation": recommendation.__dict__ if recommendation else None
            }
        
        return AnalysisResponse(
            symbol=symbol,
            status="success",
            data=result
        )
        
    except Exception as e:
        return AnalysisResponse(
            symbol=request.symbol,
            status="error",
            error=str(e)
        )

@app.get("/health")
async def health_check():
    """Health check endpoint for Railway"""
    return {"status": "healthy", "service": "Financial Research Agent"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    print(f"Starting Financial Research Agent web server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)