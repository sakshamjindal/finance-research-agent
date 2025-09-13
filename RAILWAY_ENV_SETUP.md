# 🔐 Railway Environment Variables Setup

## ✅ Code Successfully Pushed to GitHub!

Your financial research agent is now available at:
**https://github.com/sakshamjindal/finance-research-agent**

## 🚀 Deploy to Railway (Manual Steps):

### 1. Deploy via Railway Dashboard
1. Go to **[railway.app](https://railway.app)**
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose **`sakshamjindal/finance-research-agent`**
5. Railway will automatically deploy using the `Dockerfile` and `railway.toml`

### 2. Configure Environment Variables in Railway

Once deployed, set these environment variables in Railway dashboard:

#### **Go to: Project → Settings → Variables → Add Variables**

#### 🔑 **Required API Keys (Optional but Recommended):**

```bash
# News API (for news sentiment analysis)
NEWS_API_KEY=your_news_api_key_here

# Reddit API (for social sentiment)
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret

# Optional: Additional data sources
FINNHUB_API_KEY=your_finnhub_api_key
ALPHA_VANTAGE_API_KEY=your_alpha_vantage_api_key
```

#### 🌐 **How to Get API Keys:**

1. **News API** (Free):
   - Go to [newsapi.org](https://newsapi.org)
   - Sign up for free account
   - Get API key from dashboard

2. **Reddit API** (Free):
   - Go to [reddit.com/prefs/apps](https://reddit.com/prefs/apps)
   - Create new app (script type)
   - Use client ID and secret

3. **Finnhub** (Optional, Free tier available):
   - Go to [finnhub.io](https://finnhub.io)
   - Sign up and get API key

4. **Alpha Vantage** (Optional, Free tier available):
   - Go to [alphavantage.co](https://alphavantage.co)
   - Sign up and get API key

## 📊 **App Features:**

### ✅ **Works WITHOUT API Keys:**
- ✅ Stock price data (Yahoo Finance)
- ✅ Fundamental analysis (P/E, ROE, etc.)
- ✅ Technical analysis (RSI, MACD, etc.)
- ✅ Basic analyst ratings
- ✅ Investment recommendations

### 🚀 **Enhanced WITH API Keys:**
- 📰 News sentiment analysis
- 📱 Social media sentiment
- 📈 Additional financial metrics
- 🔍 More comprehensive analysis

## 🎯 **Expected Railway URL:**

After deployment, your app will be available at something like:
- `https://finance-research-agent-production.railway.app`
- Or a similar Railway-generated URL

## 📱 **Usage:**

1. Enter any stock ticker (e.g., AAPL, MSFT, TSLA)
2. Choose Standard or Comprehensive analysis
3. Get detailed investment recommendations!

## 🔧 **Railway Settings:**

The app is configured with:
- ✅ **Auto-deploy** from GitHub
- ✅ **Health check** endpoint
- ✅ **Automatic restarts**
- ✅ **HTTPS** enabled
- ✅ **Environment variables** ready

Your financial research agent will be live within 5-10 minutes! 🎉