# Railway Deployment Guide

Your Financial Research Agent is now ready for deployment on Railway! Here's how to deploy it:

## 🚀 Quick Deployment Steps

### Option 1: Deploy via Railway CLI (Recommended)

1. **Install Railway CLI**:
   ```bash
   npm install -g @railway/cli
   ```

2. **Login to Railway**:
   ```bash
   railway login
   ```

3. **Initialize and Deploy**:
   ```bash
   railway init
   railway up
   ```

### Option 2: Deploy via GitHub Integration

1. **Push your code to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit - Financial Research Agent"
   git remote add origin <your-github-repo-url>
   git push -u origin main
   ```

2. **Connect to Railway**:
   - Go to [railway.app](https://railway.app)
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

## 📋 Deployment Configuration

The following files are configured for Railway deployment:

- **`Dockerfile`**: Containerizes the FastAPI application
- **`railway.toml`**: Railway deployment configuration
- **`requirements.txt`**: Python dependencies
- **`fastapi_web.py`**: Web application entry point
- **`.dockerignore`**: Docker ignore patterns

## 🌐 What You'll Get

Once deployed, you'll have:

- **Web Interface**: Beautiful, responsive web UI for stock analysis
- **API Endpoints**: 
  - `GET /` - Main web interface
  - `POST /analyze` - Stock analysis API
  - `GET /health` - Health check endpoint
- **Automatic HTTPS**: Railway provides SSL certificates
- **Custom Domain**: Option to add your own domain

## 🔧 Environment Variables (Optional)

For full functionality, you can set these environment variables in Railway:

```bash
# Required for sentiment analysis
NEWS_API_KEY=your_news_api_key
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret

# Optional for additional data sources
FINNHUB_API_KEY=your_finnhub_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
```

## 🎯 Features Available on Web

- **Stock Analysis**: Standard and comprehensive analysis modes
- **Real-time Data**: Current stock prices and metrics
- **Fundamental Analysis**: P/E ratio, ROE, profit margins, etc.
- **Technical Analysis**: RSI, MACD, moving averages, trends
- **Sentiment Analysis**: News and social media sentiment
- **Investment Recommendations**: Buy/sell/hold with confidence levels
- **Responsive Design**: Works on desktop and mobile

## 📊 Analysis Modes

### Standard Analysis
- Basic fundamental metrics
- Technical indicators
- Sentiment analysis
- Investment recommendation

### Comprehensive Analysis
- All standard analysis features
- Piotroski F-Score
- Altman Z-Score
- Advanced risk metrics
- DCF valuation model
- Quality assessment

## 🔍 Usage

Once deployed, users can:

1. Enter a stock ticker symbol (e.g., AAPL, MSFT, TSLA)
2. Choose between Standard or Comprehensive analysis
3. View detailed results in an intuitive web interface
4. Get actionable investment recommendations

## 🛠️ Local Development

To run locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run FastAPI server
python fastapi_web.py

# Access at http://localhost:8000
```

## 🔄 Alternative: Textual TUI

If you prefer the original terminal-based interface:

```bash
# Run Rich CLI interface
python financial_agent_rich.py

# Run Textual TUI interface  
python financial_agent_textual.py
```

## 📈 Scaling

Railway automatically handles:
- **Auto-scaling**: Scales based on demand
- **Load balancing**: Distributes traffic
- **Health monitoring**: Automatically restarts if needed
- **Resource optimization**: Efficient resource usage

Your Financial Research Agent is production-ready and will provide professional-grade stock analysis to users worldwide! 🌍