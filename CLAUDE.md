# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based financial research agent that provides comprehensive stock analysis through fundamental, technical, and sentiment analysis. The system consists of two CLI interfaces (rich and textual) sharing a common analysis engine.

## Key Components

### Core Architecture
- **`finance_core.py`**: Central analysis engine containing `FinancialAnalyzer` class with fundamental, technical, and sentiment analysis methods
- **`comprehensive_analyzer.py`**: Advanced analysis engine with sophisticated financial metrics including Piotroski F-Score, Altman Z-Score, DCF valuation, risk analysis, and quality assessment
- **`financial_agent_rich.py`**: Rich CLI interface with beautiful formatting and progress bars, includes comprehensive analysis mode
- **`financial_agent_textual.py`**: Full TUI interface with tabbed layout and keyboard navigation
- **`sentiment_analyzer.py`**: Dedicated sentiment analysis from news and social media sources
- **`config.py`**: Configuration management with weights and thresholds for analysis components
- **`cache_manager.py`**: Local data caching system for API responses and analysis results
- **`setup_environment.py`**: Environment setup and API key validation utility

### Data Flow
1. User input (stock ticker) → Agent interface
2. Agent calls `FinancialAnalyzer` from `finance_core.py`
3. Analyzer fetches data from APIs (Yahoo Finance, NewsAPI, Reddit, etc.)
4. Results cached via `cache_manager.py`
5. Analysis scores combined using weights from `config.py`
6. Recommendation generated with confidence score
7. Results displayed in chosen interface format

## Common Development Commands

### Running the Applications
```bash
# Rich CLI interface (recommended for testing)
python financial_agent_rich.py

# Rich interface with direct symbol analysis
python financial_agent_rich.py --symbol AAPL

# Comprehensive analysis mode (Rich interface)
python financial_agent_rich.py --symbol AAPL --comprehensive

# Interactive mode - choose analysis mode after entering ticker
python financial_agent_rich.py
# 1. Enter ticker (e.g., AAPL)
# 2. Choose: [1] Standard or [2] Comprehensive

# Textual TUI interface (full interactive)
python financial_agent_textual.py

# Test sentiment analysis directly
python sentiment_analyzer.py

# Setup and validate environment
python setup_environment.py
```

### Dependencies Installation
```bash
pip install yfinance textual rich click pandas numpy praw textblob python-dotenv
```

### Testing Setup
```bash
# Check environment and API keys
python setup_environment.py --status

# Test core analysis engine
python -c "from finance_core import FinancialAnalyzer; analyzer = FinancialAnalyzer(); print(analyzer.analyze_stock('AAPL'))"
```

## Configuration

### Environment Setup
- Copy `.env.example` to `.env` and configure API keys
- Required for full sentiment analysis: `NEWS_API_KEY`, `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET`
- Optional APIs: `FINNHUB_API_KEY`, `ALPHA_VANTAGE_API_KEY`

### Analysis Weights
Modify `config.py` to adjust:
- Overall score: Fundamental (50%) + Technical (30%) + Sentiment (20%)
- Fundamental weights: PE ratio, ROE, debt-to-equity, etc.
- Technical weights: trend, RSI, MACD, moving averages
- Recommendation thresholds: Strong Buy (80+), Buy (65-79), Hold (35-64), Sell (20-34)

## Key Classes and Methods

### FinancialAnalyzer (finance_core.py)
- `analyze_stock(symbol)`: Main analysis method returning comprehensive results
- `get_fundamental_analysis(ticker)`: Financial metrics and ratios
- `get_technical_analysis(ticker)`: Technical indicators and signals
- `get_sentiment_analysis(symbol)`: News and social media sentiment
- `calculate_recommendation(scores)`: Buy/sell/hold logic with confidence

### ComprehensiveAnalyzer (comprehensive_analyzer.py)
- `perform_comprehensive_analysis(symbol)`: Complete advanced analysis suite
- `_analyze_financial_health(ticker, symbol)`: Piotroski F-Score, Altman Z-Score calculations
- `_analyze_risk(ticker, symbol)`: Beta, Sharpe ratio, max drawdown, volatility analysis
- `_analyze_valuation(ticker, symbol)`: DCF model, Graham number, P/FCF ratios
- `_analyze_quality(ticker, symbol)`: Earnings quality, cash flow analysis, red flags
- `_analyze_momentum(ticker, symbol)`: Multi-timeframe momentum analysis
- `_calculate_composite_score()`: Weighted composite scoring across all factors

### Data Structures
- `StockData`: Basic stock information (price, change, volume)
- `FundamentalMetrics`: PE ratio, ROE, debt metrics, growth rates
- `TechnicalMetrics`: RSI, MACD, moving averages, trend indicators
- `SentimentMetrics`: News sentiment, social sentiment, analyst ratings
- `FinancialHealthMetrics`: Piotroski score, Altman Z-score, working capital, debt coverage
- `RiskMetrics`: Beta, Sharpe ratio, max drawdown, volatility measures, VaR
- `ValuationMetrics`: DCF estimates, Graham number, P/FCF, EV ratios
- `QualityMetrics`: Earnings quality, accruals ratio, accounting red flags
- `ComprehensiveAnalysis`: Complete analysis results with composite scoring and insights

## Common Modifications

### Adding New Analysis Metrics
1. Update relevant `@dataclass` in `finance_core.py` (e.g., `FundamentalMetrics`)
2. Add calculation logic in corresponding analysis method
3. Update scoring logic in `calculate_*_score()` methods
4. Adjust weights in `config.py` if needed
5. Update display methods in both agent interfaces

### Modifying Recommendation Logic
- Update thresholds in `RecommendationThresholds` class in `config.py`
- Modify `calculate_recommendation()` method in `FinancialAnalyzer`
- Adjust confidence calculation logic based on score consensus

### Adding New Data Sources
1. Add API configuration to `.env.example` and config classes
2. Implement data fetching methods in `sentiment_analyzer.py` or `finance_core.py`
3. Update caching logic in `cache_manager.py`
4. Add appropriate error handling and rate limiting

## Architecture Principles

- **Separation of Concerns**: Analysis engine separate from UI interfaces
- **Shared Core**: Both agents use the same `FinancialAnalyzer` for consistency
- **Configurable Weights**: Analysis components and thresholds easily adjustable
- **Caching Strategy**: API responses cached locally to reduce API calls and improve performance
- **Error Handling**: Graceful degradation when APIs unavailable or data missing
- **Rate Limiting**: Built-in delays and request management for API compliance