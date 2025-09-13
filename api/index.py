"""
FastAPI web application for Vercel deployment
Provides the same functionality as the Textual TUI in a web interface
"""
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import json
import sys
import os
from typing import Optional

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from finance_core import FinancialAnalyzer
from comprehensive_analyzer import ComprehensiveAnalyzer

app = FastAPI(title="Financial Research Agent", description="Professional Stock Analysis Platform")

# Templates
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))

# Initialize analyzers
analyzer = FinancialAnalyzer()
comprehensive_analyzer = ComprehensiveAnalyzer()

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_stock(
    request: Request,
    symbol: str = Form(...),
    analysis_mode: str = Form(...)
):
    """Analyze a stock symbol"""
    try:
        symbol = symbol.upper().strip()
        
        if not symbol or len(symbol) > 10:
            raise HTTPException(status_code=400, detail="Invalid ticker symbol")
        
        # Basic analysis
        stock_data = analyzer.get_stock_data(symbol)
        fundamentals = analyzer.analyze_fundamentals(symbol)
        technicals = analyzer.analyze_technicals(symbol)
        sentiment = analyzer.analyze_sentiment(symbol)
        recommendation = analyzer.generate_recommendation(symbol, fundamentals, technicals, sentiment)
        
        # Comprehensive analysis if requested
        comprehensive = None
        if analysis_mode == "comprehensive":
            comprehensive = comprehensive_analyzer.perform_comprehensive_analysis(symbol)
        
        results = {
            "stock_data": stock_data,
            "fundamentals": fundamentals,
            "technicals": technicals,
            "sentiment": sentiment,
            "recommendation": recommendation,
            "comprehensive": comprehensive,
            "symbol": symbol,
            "analysis_mode": analysis_mode
        }
        
        return templates.TemplateResponse("results.html", {
            "request": request,
            "results": results,
            "json_results": json.dumps(results, default=str)
        })
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/analyze/{symbol}")
async def api_analyze(symbol: str, mode: str = "standard"):
    """API endpoint for stock analysis"""
    try:
        symbol = symbol.upper().strip()
        
        # Basic analysis
        stock_data = analyzer.get_stock_data(symbol)
        fundamentals = analyzer.analyze_fundamentals(symbol)
        technicals = analyzer.analyze_technicals(symbol)
        sentiment = analyzer.analyze_sentiment(symbol)
        recommendation = analyzer.generate_recommendation(symbol, fundamentals, technicals, sentiment)
        
        results = {
            "symbol": symbol,
            "stock_data": {
                "name": stock_data.name,
                "current_price": stock_data.current_price,
                "change_percent": stock_data.change_percent,
                "market_cap": stock_data.market_cap,
                "volume": stock_data.volume
            },
            "recommendation": {
                "action": recommendation.action,
                "confidence": recommendation.confidence,
                "overall_score": recommendation.overall_score,
                "risk_level": recommendation.risk_level,
                "reasoning": recommendation.reasoning
            },
            "fundamentals": {
                "pe_ratio": fundamentals.pe_ratio,
                "roe": fundamentals.roe,
                "debt_to_equity": fundamentals.debt_to_equity,
                "revenue_growth": fundamentals.revenue_growth,
                "score": fundamentals.score
            },
            "technicals": {
                "rsi": technicals.rsi,
                "trend": technicals.trend,
                "score": technicals.score
            },
            "sentiment": {
                "score": sentiment.score,
                "analyst_rating": sentiment.analyst_rating,
                "analyst_count": sentiment.analyst_count
            }
        }
        
        # Add comprehensive analysis if requested
        if mode == "comprehensive":
            comprehensive = comprehensive_analyzer.perform_comprehensive_analysis(symbol)
            results["comprehensive"] = {
                "composite_score": comprehensive.composite_score,
                "confidence_level": comprehensive.confidence_level,
                "financial_health": {
                    "piotroski_score": comprehensive.financial_health.piotroski_score,
                    "altman_z_score": comprehensive.financial_health.altman_z_score,
                    "score": comprehensive.financial_health.score
                },
                "risk_metrics": {
                    "beta": comprehensive.risk_metrics.beta,
                    "sharpe_ratio": comprehensive.risk_metrics.sharpe_ratio,
                    "max_drawdown": comprehensive.risk_metrics.max_drawdown,
                    "risk_score": comprehensive.risk_metrics.risk_score
                },
                "valuation_metrics": {
                    "dcf_estimate": comprehensive.valuation_metrics.dcf_estimate,
                    "graham_number": comprehensive.valuation_metrics.graham_number,
                    "valuation_score": comprehensive.valuation_metrics.valuation_score
                },
                "key_insights": comprehensive.key_insights,
                "warnings": comprehensive.warnings
            }
        
        return results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Financial Research Agent"}

# For Vercel
handler = app