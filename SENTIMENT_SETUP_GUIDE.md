# Sentiment Analysis Setup Guide

## 🎯 Overview

The Financial Research Agent now supports **real-time sentiment analysis** from news sources and social media! This guide will help you set up the required API keys.

## 🚀 Quick Start (Recommended)

### 1. **Get NewsAPI Key (Easiest)**
- Visit: https://newsapi.org/register
- Sign up with email
- Free tier: **1,000 requests/day**
- Copy your API key

### 2. **Get Reddit API Keys (Free)**
- Visit: https://www.reddit.com/prefs/apps
- Click "Create App" or "Create Another App"
- Choose "script" type
- Note down:
  - **Client ID** (under the app name)
  - **Client Secret**

### 3. **Set Up Environment**

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` and add your keys:
```bash
NEWS_API_KEY=your_news_api_key_here
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
REDDIT_USER_AGENT=FinancialAgent/1.0
```

### 4. **Install Additional Packages**
```bash
pip install praw textblob python-dotenv
```

### 5. **Test Setup**
```bash
python setup_environment.py --status
```

## 📊 What You Get

### **With API Keys:**
- **News Sentiment**: Real-time analysis of financial news
- **Social Sentiment**: Reddit discussions from r/investing, r/stocks, etc.
- **Enhanced Confidence**: Higher accuracy recommendations
- **Detailed Insights**: Article counts, post analysis, trending topics

### **Without API Keys:**
- **Basic Analysis**: Still works with analyst ratings only
- **Reduced Features**: "No API key" shown for news/social sentiment
- **Lower Confidence**: Recommendations based only on fundamentals + technicals

## 🔧 Advanced Setup (Optional)

### **Enhanced News Coverage**

**Finnhub (Financial Focus)**
```bash
FINNHUB_API_KEY=your_key_here
```
- Free: 60 calls/minute
- Financial news, earnings, SEC filings
- Sign up: https://finnhub.io/register

**Alpha Vantage**
```bash
ALPHA_VANTAGE_API_KEY=your_key_here  
```
- Free: 25 requests/day
- Market data + news sentiment
- Sign up: https://www.alphavantage.co/support/#api-key

### **Social Media Expansion**

**Twitter/X (Premium)**
```bash
TWITTER_BEARER_TOKEN=your_token_here
```
- Cost: $100+/month
- Real-time social sentiment
- Sign up: https://developer.twitter.com/

**StockTwits (Free)**
```bash
STOCKTWITS_ACCESS_TOKEN=your_token_here
```
- Free tier available
- Financial-focused social media
- Sign up: https://api.stocktwits.com/

## 🧪 Testing Your Setup

### **1. Check Installation**
```bash
python setup_environment.py
```

### **2. Test Sentiment Analysis**
```bash
python sentiment_analyzer.py
```

### **3. Run Full Agent Test**
```bash
# Rich version (recommended for testing)
python financial_agent_rich.py --symbol AAPL

# Textual version (full TUI)
python financial_agent_textual.py
```

## 📈 Example Output Comparison

### **Without API Keys:**
```
┌─ Sentiment Analysis ────────┐
│ Analyst Rating │ Buy       │ 75/100    │
│ News Sentiment │ No API key│ N/A       │
│ Social Media   │ No API key│ N/A       │
│ Overall Score  │ Fair      │ 65/100    │
└─────────────────────────────┘
```

### **With API Keys:**
```
┌─ Sentiment Analysis ────────────────────────┐
│ Analyst Rating │ Buy           │ 75/100      │
│ News Sentiment │ 78.5/100      │ 12 articles │
│ Social Media   │ 65.2/100      │ 8 posts     │
│ Overall Score  │ Good          │ 74/100 (85%)│
│ Summary        │ Positive sentiment based   │
│                │ on 12 articles, 8 posts    │
└─────────────────────────────────────────────┘
```

## ⚠️ Important Notes

### **Rate Limits**
- **NewsAPI**: 1,000 requests/day (sufficient for ~100 stock analyses)
- **Reddit**: 1,000 requests/minute (very generous)
- Built-in rate limiting prevents API abuse

### **Data Quality**
- **Recency**: News from last 7 days, weighted by freshness
- **Relevance**: Only articles/posts mentioning the stock
- **Accuracy**: Combines multiple sentiment sources for reliability

### **Privacy**
- **No Personal Data**: Only fetches public financial discussions
- **Local Storage**: All analysis cached locally
- **API Keys**: Stored only in your local .env file

## 🔧 Troubleshooting

### **"No module named 'praw'" Error**
```bash
pip install praw
```

### **"No module named 'textblob'" Error** 
```bash
pip install textblob
```

### **API Key Not Working**
1. Check `.env` file exists in the project root
2. Verify no extra spaces around `=` in `.env`
3. Restart the application after adding keys
4. Test with `python setup_environment.py --status`

### **Reddit API Issues**
1. Ensure app type is "script", not "web app"
2. Use the Client ID from under the app name
3. Include a user agent like "FinancialAgent/1.0"

### **Low Confidence Scores**
- Normal with limited API keys
- More data sources = higher confidence
- Conflicting signals also reduce confidence

## 🎉 Success!

Once set up, your financial agent will provide:
- **Real-time sentiment** from news and social media
- **Higher accuracy** recommendations
- **Detailed insights** into market perception
- **Professional-grade** analysis comparable to Bloomberg Terminal

## 💡 Next Steps

After basic setup, consider:
1. **Adding more API keys** for comprehensive coverage
2. **Running batch analysis** on your watchlist
3. **Setting up alerts** for sentiment changes
4. **Exploring historical comparisons**

The sentiment analysis significantly improves recommendation accuracy and provides invaluable market insights!