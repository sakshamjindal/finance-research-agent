"""
Advanced Sentiment Analysis for Financial Research Agent
Integrates NewsAPI, Reddit, and other sources for comprehensive sentiment scoring
"""
import os
import re
import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import json
from collections import Counter

# For Reddit API
try:
    import praw
    PRAW_AVAILABLE = True
except ImportError:
    PRAW_AVAILABLE = False
    print("Warning: praw not installed. Reddit sentiment will be unavailable.")
    print("Install with: pip install praw")

# Simple sentiment analysis (can be enhanced with TextBlob or VADER)
try:
    from textblob import TextBlob
    TEXTBLOB_AVAILABLE = True
except ImportError:
    TEXTBLOB_AVAILABLE = False
    print("Warning: textblob not installed. Using basic sentiment analysis.")
    print("Install with: pip install textblob")


@dataclass
class NewsArticle:
    """News article data structure"""
    title: str
    description: str
    source: str
    published_at: datetime
    url: str
    sentiment_score: float = 0.0
    relevance_score: float = 0.0


@dataclass
class SocialPost:
    """Social media post data structure"""
    text: str
    source: str
    timestamp: datetime
    author: str
    sentiment_score: float = 0.0
    upvotes: int = 0
    relevance_score: float = 0.0


@dataclass
class SentimentAnalysis:
    """Complete sentiment analysis results"""
    overall_score: float
    news_sentiment: float
    social_sentiment: float
    news_articles: List[NewsArticle]
    social_posts: List[SocialPost]
    confidence: float
    summary: str


class SentimentAnalyzer:
    """Advanced sentiment analysis for stocks"""
    
    def __init__(self):
        # API keys from environment variables
        self.news_api_key = os.getenv('NEWS_API_KEY')
        self.reddit_client_id = os.getenv('REDDIT_CLIENT_ID')
        self.reddit_client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.reddit_user_agent = os.getenv('REDDIT_USER_AGENT', 'FinancialAgent/1.0')
        
        # Initialize Reddit client
        self.reddit_client = None
        if PRAW_AVAILABLE and all([self.reddit_client_id, self.reddit_client_secret]):
            try:
                self.reddit_client = praw.Reddit(
                    client_id=self.reddit_client_id,
                    client_secret=self.reddit_client_secret,
                    user_agent=self.reddit_user_agent
                )
            except Exception as e:
                print(f"Warning: Could not initialize Reddit client: {e}")
        
        # Financial keywords for relevance scoring
        self.financial_keywords = {
            'positive': ['buy', 'bullish', 'growth', 'profit', 'revenue', 'beat', 'strong', 'outperform', 'upgrade', 'rally'],
            'negative': ['sell', 'bearish', 'loss', 'decline', 'miss', 'weak', 'underperform', 'downgrade', 'crash', 'drop'],
            'neutral': ['hold', 'maintain', 'stable', 'flat', 'sideways', 'consolidation']
        }
        
        # Subreddits to monitor
        self.financial_subreddits = [
            'investing', 'stocks', 'SecurityAnalysis', 'ValueInvesting', 
            'financialindependence', 'StockMarket', 'wallstreetbets'
        ]
    
    def analyze_stock_sentiment(self, symbol: str, company_name: str = None) -> SentimentAnalysis:
        """Perform comprehensive sentiment analysis for a stock"""
        # Fetch news sentiment
        news_articles = self.get_news_sentiment(symbol, company_name)
        news_sentiment = self.calculate_news_sentiment(news_articles)
        
        # Fetch social sentiment
        social_posts = self.get_social_sentiment(symbol, company_name)
        social_sentiment = self.calculate_social_sentiment(social_posts)
        
        # Calculate overall sentiment
        overall_sentiment = self.calculate_overall_sentiment(news_sentiment, social_sentiment)
        
        # Generate summary
        summary = self.generate_sentiment_summary(news_articles, social_posts, overall_sentiment)
        
        # Calculate confidence based on data quantity and consistency
        confidence = self.calculate_confidence(news_articles, social_posts, news_sentiment, social_sentiment)
        
        return SentimentAnalysis(
            overall_score=overall_sentiment,
            news_sentiment=news_sentiment,
            social_sentiment=social_sentiment,
            news_articles=news_articles,
            social_posts=social_posts,
            confidence=confidence,
            summary=summary
        )
    
    def get_news_sentiment(self, symbol: str, company_name: str = None) -> List[NewsArticle]:
        """Fetch and analyze news articles"""
        articles = []
        
        if not self.news_api_key:
            return articles
        
        # Search queries
        queries = [symbol]
        if company_name:
            queries.append(company_name)
        
        for query in queries:
            try:
                # NewsAPI endpoint
                url = 'https://newsapi.org/v2/everything'
                params = {
                    'q': f'"{query}" AND (stock OR market OR financial OR earnings OR revenue)',
                    'apiKey': self.news_api_key,
                    'language': 'en',
                    'sortBy': 'relevancy',
                    'pageSize': 20,
                    'from': (datetime.now() - timedelta(days=7)).isoformat()
                }
                
                response = requests.get(url, params=params, timeout=10)
                response.raise_for_status()
                
                data = response.json()
                
                for article_data in data.get('articles', []):
                    if not article_data.get('title') or article_data.get('title') == '[Removed]':
                        continue
                    
                    article = NewsArticle(
                        title=article_data['title'],
                        description=article_data.get('description', ''),
                        source=article_data['source']['name'],
                        published_at=datetime.fromisoformat(article_data['publishedAt'].replace('Z', '+00:00')),
                        url=article_data['url']
                    )
                    
                    # Analyze sentiment
                    article.sentiment_score = self.analyze_text_sentiment(
                        f"{article.title} {article.description}"
                    )
                    
                    # Calculate relevance
                    article.relevance_score = self.calculate_relevance(
                        f"{article.title} {article.description}", symbol, company_name
                    )
                    
                    if article.relevance_score > 0.3:  # Only include relevant articles
                        articles.append(article)
                
                # Rate limiting
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Warning: Error fetching news for {query}: {e}")
        
        # Remove duplicates and sort by relevance
        seen_titles = set()
        unique_articles = []
        for article in sorted(articles, key=lambda x: x.relevance_score, reverse=True):
            if article.title not in seen_titles:
                seen_titles.add(article.title)
                unique_articles.append(article)
        
        return unique_articles[:15]  # Return top 15 most relevant articles
    
    def get_social_sentiment(self, symbol: str, company_name: str = None) -> List[SocialPost]:
        """Fetch and analyze social media posts"""
        posts = []
        
        if not self.reddit_client:
            return posts
        
        try:
            # Search across financial subreddits
            for subreddit_name in self.financial_subreddits:
                try:
                    subreddit = self.reddit_client.subreddit(subreddit_name)
                    
                    # Search for posts mentioning the symbol
                    search_queries = [f"${symbol}", symbol]
                    if company_name:
                        search_queries.append(company_name)
                    
                    for query in search_queries:
                        for submission in subreddit.search(query, sort='relevance', time_filter='week', limit=10):
                            post_text = f"{submission.title} {submission.selftext}"
                            
                            post = SocialPost(
                                text=post_text[:500],  # Limit text length
                                source=f"r/{subreddit_name}",
                                timestamp=datetime.fromtimestamp(submission.created_utc),
                                author=str(submission.author) if submission.author else 'deleted',
                                upvotes=submission.score
                            )
                            
                            # Analyze sentiment
                            post.sentiment_score = self.analyze_text_sentiment(post_text)
                            
                            # Calculate relevance
                            post.relevance_score = self.calculate_relevance(post_text, symbol, company_name)
                            
                            if post.relevance_score > 0.4:  # Only include relevant posts
                                posts.append(post)
                        
                        # Rate limiting
                        time.sleep(0.2)
                
                except Exception as e:
                    print(f"Warning: Error accessing r/{subreddit_name}: {e}")
                    continue
        
        except Exception as e:
            print(f"Warning: Error with Reddit API: {e}")
        
        # Remove duplicates and sort by relevance and upvotes
        unique_posts = list({post.text: post for post in posts}.values())
        return sorted(unique_posts, key=lambda x: (x.relevance_score, x.upvotes), reverse=True)[:20]
    
    def analyze_text_sentiment(self, text: str) -> float:
        """Analyze sentiment of text (-1 to 1)"""
        if not text:
            return 0.0
        
        text = text.lower()
        
        if TEXTBLOB_AVAILABLE:
            try:
                blob = TextBlob(text)
                return blob.sentiment.polarity
            except:
                pass
        
        # Fallback: Simple keyword-based sentiment analysis
        positive_count = sum(1 for word in self.financial_keywords['positive'] if word in text)
        negative_count = sum(1 for word in self.financial_keywords['negative'] if word in text)
        
        if positive_count == 0 and negative_count == 0:
            return 0.0
        
        total = positive_count + negative_count
        return (positive_count - negative_count) / total if total > 0 else 0.0
    
    def calculate_relevance(self, text: str, symbol: str, company_name: str = None) -> float:
        """Calculate how relevant text is to the stock (0 to 1)"""
        if not text:
            return 0.0
        
        text = text.lower()
        relevance_score = 0.0
        
        # Direct symbol mentions
        if f"${symbol.lower()}" in text:
            relevance_score += 0.4
        if symbol.lower() in text:
            relevance_score += 0.3
        
        # Company name mentions
        if company_name and company_name.lower() in text:
            relevance_score += 0.3
        
        # Financial keyword presence
        financial_word_count = 0
        all_keywords = sum(self.financial_keywords.values(), [])
        for keyword in all_keywords:
            if keyword in text:
                financial_word_count += 1
        
        if financial_word_count > 0:
            relevance_score += min(0.3, financial_word_count * 0.1)
        
        return min(1.0, relevance_score)
    
    def calculate_news_sentiment(self, articles: List[NewsArticle]) -> float:
        """Calculate weighted news sentiment"""
        if not articles:
            return 0.5  # Neutral
        
        total_weighted_sentiment = 0.0
        total_weight = 0.0
        
        for article in articles:
            # Weight by relevance and recency
            days_old = (datetime.now() - article.published_at.replace(tzinfo=None)).days
            recency_weight = max(0.1, 1.0 - (days_old / 7.0))  # Decay over 7 days
            
            weight = article.relevance_score * recency_weight
            total_weighted_sentiment += (article.sentiment_score + 1) / 2 * weight  # Convert to 0-1 scale
            total_weight += weight
        
        if total_weight == 0:
            return 0.5
        
        return total_weighted_sentiment / total_weight
    
    def calculate_social_sentiment(self, posts: List[SocialPost]) -> float:
        """Calculate weighted social sentiment"""
        if not posts:
            return 0.5  # Neutral
        
        total_weighted_sentiment = 0.0
        total_weight = 0.0
        
        for post in posts:
            # Weight by relevance, upvotes, and recency
            days_old = (datetime.now() - post.timestamp).days
            recency_weight = max(0.1, 1.0 - (days_old / 7.0))
            upvote_weight = min(2.0, 1.0 + (post.upvotes / 100.0))  # Max 2x weight for upvotes
            
            weight = post.relevance_score * recency_weight * upvote_weight
            total_weighted_sentiment += (post.sentiment_score + 1) / 2 * weight  # Convert to 0-1 scale
            total_weight += weight
        
        if total_weight == 0:
            return 0.5
        
        return total_weighted_sentiment / total_weight
    
    def calculate_overall_sentiment(self, news_sentiment: float, social_sentiment: float) -> float:
        """Calculate overall sentiment score"""
        # Weight news more heavily than social media
        news_weight = 0.7
        social_weight = 0.3
        
        overall = news_sentiment * news_weight + social_sentiment * social_weight
        return overall
    
    def calculate_confidence(self, news_articles: List[NewsArticle], social_posts: List[SocialPost],
                           news_sentiment: float, social_sentiment: float) -> float:
        """Calculate confidence in sentiment analysis"""
        confidence = 0.5  # Base confidence
        
        # Data quantity factor
        data_points = len(news_articles) + len(social_posts)
        quantity_factor = min(0.3, data_points / 20.0)  # Up to 0.3 bonus for quantity
        confidence += quantity_factor
        
        # Consistency factor (how aligned news and social sentiment are)
        sentiment_diff = abs(news_sentiment - social_sentiment)
        consistency_factor = 0.2 * (1 - sentiment_diff)  # Up to 0.2 bonus for consistency
        confidence += consistency_factor
        
        return min(0.95, confidence)
    
    def generate_sentiment_summary(self, news_articles: List[NewsArticle], 
                                 social_posts: List[SocialPost], overall_sentiment: float) -> str:
        """Generate human-readable sentiment summary"""
        if overall_sentiment > 0.65:
            sentiment_label = "Very Positive"
        elif overall_sentiment > 0.55:
            sentiment_label = "Positive"
        elif overall_sentiment > 0.45:
            sentiment_label = "Neutral"
        elif overall_sentiment > 0.35:
            sentiment_label = "Negative"
        else:
            sentiment_label = "Very Negative"
        
        news_count = len(news_articles)
        social_count = len(social_posts)
        
        summary = f"{sentiment_label} sentiment based on {news_count} news articles"
        if social_count > 0:
            summary += f" and {social_count} social media posts"
        summary += f" from the past week."
        
        return summary


# Utility functions for testing
def test_sentiment_analysis(symbol: str):
    """Test sentiment analysis for a symbol"""
    analyzer = SentimentAnalyzer()
    
    print(f"\nTesting sentiment analysis for {symbol}...")
    
    # Check API keys
    if not analyzer.news_api_key:
        print("❌ NEWS_API_KEY not found in environment variables")
    else:
        print("✅ NewsAPI configured")
    
    if not analyzer.reddit_client:
        print("❌ Reddit API not configured")
    else:
        print("✅ Reddit API configured")
    
    # Perform analysis
    try:
        analysis = analyzer.analyze_stock_sentiment(symbol)
        
        print(f"\nResults for {symbol}:")
        print(f"Overall Sentiment: {analysis.overall_score:.3f} ({analysis.summary})")
        print(f"News Sentiment: {analysis.news_sentiment:.3f} ({len(analysis.news_articles)} articles)")
        print(f"Social Sentiment: {analysis.social_sentiment:.3f} ({len(analysis.social_posts)} posts)")
        print(f"Confidence: {analysis.confidence:.1%}")
        
        if analysis.news_articles:
            print(f"\nTop news articles:")
            for i, article in enumerate(analysis.news_articles[:3]):
                print(f"{i+1}. {article.title} (Sentiment: {article.sentiment_score:.2f})")
        
        if analysis.social_posts:
            print(f"\nTop social posts:")
            for i, post in enumerate(analysis.social_posts[:3]):
                preview = post.text[:100] + "..." if len(post.text) > 100 else post.text
                print(f"{i+1}. {preview} (Sentiment: {post.sentiment_score:.2f})")
        
        return analysis
        
    except Exception as e:
        print(f"Error during analysis: {e}")
        return None


if __name__ == "__main__":
    # Test the sentiment analyzer
    test_symbol = "AAPL"
    
    print("Sentiment Analysis Test")
    print("=" * 50)
    print("Required environment variables:")
    print("- NEWS_API_KEY (from newsapi.org)")
    print("- REDDIT_CLIENT_ID (from reddit.com/prefs/apps)")
    print("- REDDIT_CLIENT_SECRET")
    print("- REDDIT_USER_AGENT (e.g., 'FinancialAgent/1.0')")
    
    result = test_sentiment_analysis(test_symbol)