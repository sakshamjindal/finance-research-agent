# Financial Research Agents

Two powerful CLI-based financial research tools that provide comprehensive stock analysis through fundamental, technical, and sentiment analysis.

## Features

### Core Analysis
- **Fundamental Analysis**: P/E ratios, ROE, debt metrics, growth rates
- **Technical Analysis**: RSI, MACD, moving averages, support/resistance
- **Sentiment Analysis**: Analyst ratings, market sentiment scoring
- **Smart Recommendations**: Buy/Sell/Hold with confidence levels
- **Price Targets**: AI-calculated target prices with upside/downside

### Key Metrics Analyzed
- **Valuation**: P/E, P/B, P/S, EV/EBITDA ratios
- **Profitability**: ROE, ROA, profit margins
- **Financial Health**: Debt/equity, current ratio, cash flow
- **Growth**: Revenue and earnings growth rates
- **Technical Indicators**: 14+ technical indicators
- **Risk Assessment**: Volatility, beta, sector risk

## Two Versions Available

### 1. Textual Agent (Interactive TUI)
**File**: `financial_agent_textual.py`

**Features**:
- Full interactive terminal user interface
- Tabbed interface with Overview, Fundamentals, Technical, Sentiment, Recommendation
- Real-time progress tracking
- Data tables with sortable columns
- Sidebar with quick info and analysis progress
- Keyboard shortcuts (Ctrl+Q to quit, Ctrl+R to refresh)

**Usage**:
```bash
python financial_agent_textual.py
```

**Interface Preview**:
```
┌─ FINANCIAL RESEARCH AGENT ─┐
│ [Overview] [Fundamentals] [Technical] [Sentiment] [Recommendation] │
│                                    │
│ APPLE INC (AAPL) - $150.25 (+2.5%) │
│ RECOMMENDATION: BUY (78% confidence) │
│ Price Target: $165 (9.8% upside)   │
└─────────────────────────────────────┘
```

### 2. Rich Agent (Beautiful CLI)
**File**: `financial_agent_rich.py`

**Features**:
- Beautiful formatted output with colors and styling
- Progress bars with spinners
- Interactive prompts and confirmations
- Watchlist management
- Direct analysis mode with command-line arguments
- Side-by-side comparison panels

**Usage**:
```bash
# Interactive mode
python financial_agent_rich.py

# Direct analysis mode
python financial_agent_rich.py --symbol AAPL
```

## Installation

### Prerequisites
```bash
pip install yfinance textual rich click pandas numpy
```

### All Dependencies
The agents require these Python packages:
- `yfinance` - Stock data API
- `textual` - TUI framework (for textual agent)
- `rich` - Beautiful terminal output (for rich agent)  
- `click` - CLI framework
- `pandas` - Data manipulation
- `numpy` - Numerical computations

## Quick Start

### Option 1: Textual Agent (Full TUI)
```bash
python financial_agent_textual.py
# Enter ticker when prompted (e.g., AAPL)
# Navigate with keyboard shortcuts
```

### Option 2: Rich Agent (Enhanced CLI)
```bash
python financial_agent_rich.py
# Follow interactive prompts
# Type 'watchlist' to manage saved stocks
# Type 'quit' to exit
```

## Example Analysis Output

### Stock Overview
```
┌─ Stock Information ─────────┐  ┌─ Recommendation Summary ─────┐
│ Company: Apple Inc          │  │ Recommendation: BUY          │
│ Symbol: AAPL                │  │ Confidence: 78%              │
│ Current Price: $150.25      │  │ Overall Score: 72/100        │
│ Change: +2.5%               │  │ Risk Level: MEDIUM           │
│ Market Cap: $2.85T          │  │ Price Target: $165           │
└─────────────────────────────┘  │ Upside: +9.8%               │
                                 └──────────────────────────────┘
```

### Detailed Analysis Tables
- **Fundamentals**: P/E ratios, ROE, debt metrics with ratings
- **Technical**: RSI, MACD, moving averages with signals  
- **Sentiment**: Analyst ratings, news sentiment scores

### Recommendation Engine
- **Buy/Sell/Hold** recommendations with confidence scores
- **Price targets** with upside/downside calculations
- **Risk assessment** (Low/Medium/High)
- **Key reasoning** points explaining the recommendation

## Advanced Features

### Watchlist Management (Rich Agent)
- Add stocks to personal watchlist
- Quick analysis from watchlist
- Persistent across sessions

### Progress Tracking
- Real-time analysis progress with visual indicators
- Step-by-step status updates
- Error handling with user-friendly messages

### Data Validation
- Input validation for stock tickers
- Error handling for invalid/delisted stocks
- Graceful handling of missing data points

## Scoring Algorithm

### Overall Score Calculation
```
Overall Score = (Fundamental × 50%) + (Technical × 30%) + (Sentiment × 20%)
```

### Recommendation Thresholds
- **Strong Buy**: 80-100 points
- **Buy**: 65-79 points  
- **Hold**: 35-64 points
- **Sell**: 20-34 points
- **Strong Sell**: 0-19 points

### Confidence Calculation
Based on consensus across all three analyses:
- High confidence when all analyses align
- Lower confidence when analyses conflict
- Range: 20-95%

## Customization

### Adding New Metrics
1. Update `finance_core.py` with new calculations
2. Modify display functions in respective agent files
3. Adjust scoring weights in `FinancialAnalyzer` class

### Styling (Rich Agent)
- Colors and styles defined in display functions
- Easy to customize themes and color schemes
- Rich markup support for advanced formatting

### Layout (Textual Agent)
- CSS styling in the `CSS` class variable
- Configurable layouts and responsive design
- Keyboard binding customization

## Data Sources

### Primary Data Source
- **Yahoo Finance API** via `yfinance` package
- Real-time and historical stock data
- Company fundamentals and financial statements
- Analyst recommendations

### Future Enhancements
- News sentiment analysis APIs
- Social media sentiment tracking
- Alternative data sources integration

## Error Handling

### Common Issues
- **Invalid ticker**: Clear error message with suggestions
- **Network issues**: Retry logic and offline mode
- **Missing data**: Graceful handling with N/A values
- **API rate limits**: Built-in delays and caching

### Debugging
- Verbose error messages in development mode
- Logging capabilities for troubleshooting
- Data validation at each analysis step

## Performance

### Analysis Speed
- Typical analysis: 5-10 seconds per stock
- Concurrent data fetching where possible
- Caching for repeated analyses

### Memory Usage
- Minimal memory footprint
- Efficient data structures
- Cleanup after each analysis

## Roadmap

### Planned Features
- [ ] News sentiment integration
- [ ] Social media sentiment analysis
- [ ] Portfolio analysis capabilities
- [ ] Historical backtesting
- [ ] Export to PDF/Excel
- [ ] Real-time alerts
- [ ] Peer comparison analysis
- [ ] Sector analysis
- [ ] Options analysis integration

### Version History
- **v1.0**: Initial release with core analysis
- **Future versions**: Enhanced features and data sources

## Contributing

The financial analysis engine (`finance_core.py`) is shared between both agents, making it easy to:
- Add new analysis metrics
- Improve calculation accuracy
- Integrate additional data sources
- Enhance recommendation algorithms

Both agents provide different user experiences while sharing the same powerful analysis engine, giving you flexibility to choose the interface that best fits your workflow.