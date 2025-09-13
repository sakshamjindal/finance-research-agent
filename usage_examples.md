# Financial Research Agent - Usage Examples

## 🚀 **Running the Applications**

### Rich CLI Interface

**Basic Usage:**
```bash
python financial_agent_rich.py
```
1. Enter stock ticker (e.g., AAPL)
2. Choose analysis mode:
   - [1] 📈 Standard Analysis - Basic fundamental, technical, sentiment
   - [2] 🔬 Comprehensive Analysis - Advanced metrics (Health, Risk, Valuation, Quality)

**Direct Analysis:**
```bash
# Standard analysis
python financial_agent_rich.py --symbol AAPL

# Comprehensive analysis 
python financial_agent_rich.py --symbol AAPL --comprehensive
```

### Textual TUI Interface

```bash
python financial_agent_textual.py
```
1. Enter stock ticker in the input field
2. Click either:
   - 📈 **Standard** - Traditional analysis
   - 🔬 **Comprehensive** - Advanced analysis with additional tabs

## 📊 **Analysis Modes Comparison**

### Standard Analysis
- **Fundamental Analysis**: PE ratio, ROE, debt metrics, growth rates
- **Technical Analysis**: RSI, MACD, moving averages, trend indicators  
- **Sentiment Analysis**: Analyst ratings, news sentiment (with API keys)
- **Recommendation**: Buy/sell/hold with confidence level

### Comprehensive Analysis
All Standard Analysis features **PLUS**:

#### 💊 Financial Health Analysis
- **Piotroski F-Score** (0-9): Fundamental strength assessment
- **Altman Z-Score**: Bankruptcy risk prediction (Safe > 3.0, Gray Zone 1.8-3.0, Distress < 1.8)
- **Working Capital**: Liquidity assessment
- **Debt Coverage Ratios**: Cash flow vs debt analysis

#### ⚠️ Risk Analysis  
- **Beta**: Market correlation and systematic risk
- **Sharpe Ratio**: Risk-adjusted returns (Excellent > 1.0, Good > 0.5)
- **Max Drawdown**: Historical volatility assessment
- **30D/90D Volatility**: Short-term risk metrics
- **Value at Risk (95%)**: Downside risk quantification

#### 💰 Valuation Analysis
- **DCF Model**: Discounted cash flow intrinsic value estimates
- **Graham Number**: Conservative value investing metric  
- **Price-to-Free Cash Flow**: Cash generation efficiency
- **EV Ratios**: Enterprise Value to Sales, EBIT analysis

#### 📊 Quality Analysis
- **Earnings Quality Score**: Overall earnings reliability (0-100)
- **Cash Flow vs Earnings**: Quality of reported earnings
- **Accruals Analysis**: Potential earnings manipulation detection
- **Accounting Red Flags**: Automated warning system

#### 🎯 Advanced Features
- **Key Insights**: Automated analysis takeaways
- **Warning System**: Risk alerts and red flags
- **Composite Scoring**: Weighted overall assessment
- **Confidence Levels**: Analysis reliability indicators

## 🔍 **Example Analysis Output**

### Standard Analysis Results:
- Stock overview with price and market cap
- 3 analysis tables (Fundamental, Technical, Sentiment)  
- Final recommendation with confidence

### Comprehensive Analysis Results:
- **Everything from Standard Analysis PLUS:**
- 4 additional analysis panels in a grid layout:
  - Financial Health (Piotroski, Altman Z-Score)
  - Risk Analysis (Beta, Sharpe, Max Drawdown)
  - Valuation (DCF, Graham Number, P/FCF)  
  - Quality (Earnings Quality, Cash Flow Analysis)
- Key Insights panel with automated takeaways
- Warnings panel with risk alerts
- Overall Assessment with composite score

## 🎨 **Visual Features**

- **Color-coded Ratings**: Green (Good), Yellow (Fair), Red (Poor)
- **Progress Indicators**: Real-time analysis progress
- **Rich Formatting**: Tables, panels, and structured layouts
- **Multi-panel Layout**: Comprehensive results in organized grid
- **Interactive Elements**: Mode selection, watchlist management

## 🧪 **Testing Different Stocks**

Try these examples to see different analysis scenarios:

```bash
# Large cap tech (typically high valuation)
python financial_agent_rich.py --symbol AAPL --comprehensive

# Growth stock (high volatility)  
python financial_agent_rich.py --symbol TSLA --comprehensive

# Value stock (lower P/E ratios)
python financial_agent_rich.py --symbol BRK-B --comprehensive

# Dividend stock (stable financials)
python financial_agent_rich.py --symbol JNJ --comprehensive
```

## ⚙️ **Configuration**

The system uses default analysis weights:
- Fundamental Analysis: 50%
- Technical Analysis: 30%  
- Sentiment Analysis: 20%

For comprehensive analysis composite scoring:
- Fundamental: 25%
- Financial Health: 20%
- Valuation: 15%
- Technical: 15%
- Quality: 10%
- Momentum: 10%
- Risk: 5%

## 🔑 **API Keys (Optional)**

For enhanced sentiment analysis, configure these environment variables:
- `NEWS_API_KEY` - NewsAPI.org for news sentiment
- `REDDIT_CLIENT_ID` - Reddit API for social sentiment  
- `REDDIT_CLIENT_SECRET` - Reddit API secret
- `REDDIT_USER_AGENT` - User agent string

Without API keys, the system uses analyst ratings for sentiment analysis.