"""
Core financial analysis engine - shared between Textual and Rich agents
"""
import yfinance as yf
import pandas as pd
import numpy as np
import requests
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import json


@dataclass
class StockData:
    """Core stock data structure"""
    symbol: str
    name: str
    current_price: float
    change_percent: float
    market_cap: Optional[float] = None
    volume: Optional[int] = None


@dataclass
class FundamentalMetrics:
    """Fundamental analysis metrics"""
    pe_ratio: Optional[float] = None
    peg_ratio: Optional[float] = None
    pb_ratio: Optional[float] = None
    ps_ratio: Optional[float] = None
    ev_ebitda: Optional[float] = None
    roe: Optional[float] = None
    roa: Optional[float] = None
    profit_margin: Optional[float] = None
    debt_to_equity: Optional[float] = None
    current_ratio: Optional[float] = None
    revenue_growth: Optional[float] = None
    earnings_growth: Optional[float] = None
    score: float = 0.0


@dataclass
class TechnicalMetrics:
    """Technical analysis metrics"""
    rsi: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    sma_20: Optional[float] = None
    sma_50: Optional[float] = None
    sma_200: Optional[float] = None
    bollinger_upper: Optional[float] = None
    bollinger_lower: Optional[float] = None
    support_level: Optional[float] = None
    resistance_level: Optional[float] = None
    trend: str = "NEUTRAL"
    score: float = 0.0


@dataclass
class SentimentMetrics:
    """Sentiment analysis metrics"""
    news_sentiment: Optional[float] = None
    social_sentiment: Optional[float] = None
    analyst_rating: Optional[str] = None
    analyst_count: Optional[int] = None
    analyst_score: Optional[float] = None
    news_article_count: int = 0
    social_post_count: int = 0
    sentiment_summary: str = ""
    confidence: float = 0.0
    score: float = 0.0


@dataclass
class Recommendation:
    """Final recommendation with confidence"""
    action: str  # BUY, SELL, HOLD, STRONG_BUY, STRONG_SELL
    confidence: float  # 0-100
    price_target: Optional[float] = None
    risk_level: str = "MEDIUM"  # LOW, MEDIUM, HIGH
    reasoning: List[str] = None
    overall_score: float = 0.0


class FinancialAnalyzer:
    """Core financial analysis engine"""
    
    def __init__(self):
        self.fundamental_weights = {
            'pe_ratio': 0.15,
            'roe': 0.20,
            'debt_to_equity': 0.15,
            'revenue_growth': 0.15,
            'profit_margin': 0.15,
            'current_ratio': 0.10,
            'pb_ratio': 0.10
        }
        
        self.technical_weights = {
            'trend': 0.30,
            'rsi': 0.20,
            'macd': 0.25,
            'moving_averages': 0.25
        }
    
    def get_stock_data(self, symbol: str) -> StockData:
        """Fetch basic stock data"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1d")
            
            if hist.empty:
                raise ValueError(f"No data found for symbol {symbol}")
            
            current_price = hist['Close'].iloc[-1]
            prev_close = info.get('previousClose', current_price)
            change_percent = ((current_price - prev_close) / prev_close) * 100
            
            return StockData(
                symbol=symbol.upper(),
                name=info.get('longName', symbol),
                current_price=round(current_price, 2),
                change_percent=round(change_percent, 2),
                market_cap=info.get('marketCap'),
                volume=info.get('volume')
            )
        except Exception as e:
            raise ValueError(f"Error fetching data for {symbol}: {str(e)}")
    
    def get_historical_data(self, symbol: str, period: str = "1mo") -> pd.DataFrame:
        """Fetch historical stock price data
        
        Args:
            symbol: Stock symbol
            period: Time period (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
        
        Returns:
            DataFrame with Date, Open, High, Low, Close, Volume columns
        """
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period)
            
            if hist.empty:
                raise ValueError(f"No historical data found for symbol {symbol}")
            
            # Reset index to make Date a column
            hist = hist.reset_index()
            
            return hist[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
        except Exception as e:
            raise ValueError(f"Error fetching historical data for {symbol}: {str(e)}")
    
    def analyze_fundamentals(self, symbol: str) -> FundamentalMetrics:
        """Perform fundamental analysis"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Get financial ratios
            pe_ratio = info.get('trailingPE')
            peg_ratio = info.get('pegRatio')
            pb_ratio = info.get('priceToBook')
            ps_ratio = info.get('priceToSalesTrailing12Months')
            ev_ebitda = info.get('enterpriseToEbitda')
            
            # Profitability metrics
            roe = info.get('returnOnEquity')
            if roe:
                roe = roe * 100  # Convert to percentage
            
            roa = info.get('returnOnAssets')
            if roa:
                roa = roa * 100
                
            profit_margin = info.get('profitMargins')
            if profit_margin:
                profit_margin = profit_margin * 100
            
            # Financial health
            debt_to_equity = info.get('debtToEquity')
            current_ratio = info.get('currentRatio')
            
            # Growth metrics
            revenue_growth = info.get('revenueGrowth')
            if revenue_growth:
                revenue_growth = revenue_growth * 100
                
            earnings_growth = info.get('earningsGrowth')
            if earnings_growth:
                earnings_growth = earnings_growth * 100
            
            fundamentals = FundamentalMetrics(
                pe_ratio=pe_ratio,
                peg_ratio=peg_ratio,
                pb_ratio=pb_ratio,
                ps_ratio=ps_ratio,
                ev_ebitda=ev_ebitda,
                roe=roe,
                roa=roa,
                profit_margin=profit_margin,
                debt_to_equity=debt_to_equity,
                current_ratio=current_ratio,
                revenue_growth=revenue_growth,
                earnings_growth=earnings_growth
            )
            
            # Calculate fundamental score
            fundamentals.score = self._calculate_fundamental_score(fundamentals)
            
            return fundamentals
            
        except Exception as e:
            print(f"Error in fundamental analysis: {str(e)}")
            return FundamentalMetrics()
    
    def analyze_technicals(self, symbol: str) -> TechnicalMetrics:
        """Perform technical analysis"""
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="6mo")
            
            if len(hist) < 50:
                raise ValueError("Insufficient historical data for technical analysis")
            
            # Calculate technical indicators
            close = hist['Close']
            
            # Moving averages
            sma_20 = close.rolling(window=20).mean().iloc[-1]
            sma_50 = close.rolling(window=50).mean().iloc[-1]
            sma_200 = close.rolling(window=200).mean().iloc[-1] if len(close) >= 200 else None
            
            # RSI calculation
            rsi = self._calculate_rsi(close)
            
            # MACD calculation
            macd, macd_signal = self._calculate_macd(close)
            
            # Bollinger Bands
            bb_upper, bb_lower = self._calculate_bollinger_bands(close)
            
            # Support and Resistance (simplified)
            current_price = close.iloc[-1]
            recent_high = close.tail(20).max()
            recent_low = close.tail(20).min()
            
            # Trend determination
            trend = self._determine_trend(current_price, sma_20, sma_50, sma_200)
            
            technicals = TechnicalMetrics(
                rsi=round(rsi, 2) if rsi else None,
                macd=round(macd, 4) if macd else None,
                macd_signal=round(macd_signal, 4) if macd_signal else None,
                sma_20=round(sma_20, 2),
                sma_50=round(sma_50, 2),
                sma_200=round(sma_200, 2) if sma_200 else None,
                bollinger_upper=round(bb_upper, 2) if bb_upper else None,
                bollinger_lower=round(bb_lower, 2) if bb_lower else None,
                support_level=round(recent_low, 2),
                resistance_level=round(recent_high, 2),
                trend=trend
            )
            
            # Calculate technical score
            technicals.score = self._calculate_technical_score(technicals, current_price)
            
            return technicals
            
        except Exception as e:
            print(f"Error in technical analysis: {str(e)}")
            return TechnicalMetrics()
    
    def analyze_sentiment(self, symbol: str) -> SentimentMetrics:
        """Perform comprehensive sentiment analysis"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            company_name = info.get('longName', symbol)
            
            # Get analyst recommendations (baseline)
            analyst_rating = info.get('recommendationKey', 'none')
            analyst_count = info.get('numberOfAnalystOpinions', 0)
            
            # Convert recommendation to score
            rating_scores = {
                'strong_buy': 90,
                'buy': 75,
                'hold': 50,
                'sell': 25,
                'strong_sell': 10
            }
            
            analyst_score = rating_scores.get(analyst_rating, 50)
            
            # Initialize sentiment metrics with analyst data
            sentiment = SentimentMetrics(
                analyst_rating=analyst_rating.replace('_', ' ').title(),
                analyst_count=analyst_count,
                analyst_score=analyst_score
            )
            
            # Try to get advanced sentiment analysis
            try:
                from sentiment_analyzer import SentimentAnalyzer
                sentiment_analyzer = SentimentAnalyzer()
                
                # Only perform advanced analysis if API keys are available
                if sentiment_analyzer.news_api_key or sentiment_analyzer.reddit_client:
                    analysis = sentiment_analyzer.analyze_stock_sentiment(symbol, company_name)
                    
                    # Update sentiment metrics with real data
                    sentiment.news_sentiment = analysis.news_sentiment * 100 if analysis.news_sentiment else None
                    sentiment.social_sentiment = analysis.social_sentiment * 100 if analysis.social_sentiment else None
                    sentiment.news_article_count = len(analysis.news_articles)
                    sentiment.social_post_count = len(analysis.social_posts)
                    sentiment.sentiment_summary = analysis.summary
                    sentiment.confidence = analysis.confidence * 100
                    
                    # Calculate enhanced sentiment score
                    if analysis.overall_score:
                        # Combine advanced sentiment (70%) with analyst rating (30%)
                        advanced_score = analysis.overall_score * 100
                        sentiment.score = advanced_score * 0.7 + analyst_score * 0.3
                    else:
                        sentiment.score = analyst_score
                else:
                    # Fallback to analyst-only scoring
                    sentiment.score = analyst_score
                    sentiment.sentiment_summary = f"Based on {analyst_count} analyst recommendations"
                    sentiment.confidence = min(80, analyst_count * 10) if analyst_count > 0 else 30
                    
            except ImportError:
                # Sentiment analyzer not available, use analyst data only
                sentiment.score = analyst_score
                sentiment.sentiment_summary = f"Based on {analyst_count} analyst recommendations only"
                sentiment.confidence = min(80, analyst_count * 10) if analyst_count > 0 else 30
            except Exception as e:
                print(f"Warning: Advanced sentiment analysis failed: {e}")
                sentiment.score = analyst_score
                sentiment.sentiment_summary = f"Fallback to analyst data due to API error"
                sentiment.confidence = min(80, analyst_count * 10) if analyst_count > 0 else 30
            
            return sentiment
            
        except Exception as e:
            print(f"Error in sentiment analysis: {str(e)}")
            return SentimentMetrics()
    
    def generate_recommendation(self, symbol: str, fundamentals: FundamentalMetrics, 
                              technicals: TechnicalMetrics, sentiment: SentimentMetrics) -> Recommendation:
        """Generate final recommendation"""
        
        # Calculate overall score
        fundamental_weight = 0.5
        technical_weight = 0.3
        sentiment_weight = 0.2
        
        overall_score = (
            fundamentals.score * fundamental_weight +
            technicals.score * technical_weight +
            sentiment.score * sentiment_weight
        )
        
        # Determine action
        if overall_score >= 80:
            action = "STRONG_BUY"
        elif overall_score >= 65:
            action = "BUY"
        elif overall_score >= 35:
            action = "HOLD"
        elif overall_score >= 20:
            action = "SELL"
        else:
            action = "STRONG_SELL"
        
        # Calculate confidence based on consensus
        scores = [fundamentals.score, technicals.score, sentiment.score]
        confidence = 100 - (np.std(scores) * 2)  # Lower std = higher confidence
        confidence = max(20, min(95, confidence))  # Clamp between 20-95
        
        # Generate reasoning
        reasoning = []
        if fundamentals.score >= 70:
            reasoning.append("Strong fundamentals")
        elif fundamentals.score <= 30:
            reasoning.append("Weak fundamentals")
            
        if technicals.trend in ["BULLISH", "STRONG_BULLISH"]:
            reasoning.append("Bullish technical trend")
        elif technicals.trend in ["BEARISH", "STRONG_BEARISH"]:
            reasoning.append("Bearish technical trend")
            
        if sentiment.score >= 70:
            reasoning.append("Positive market sentiment")
        elif sentiment.score <= 30:
            reasoning.append("Negative market sentiment")
        
        # Simple price target calculation
        current_price = yf.Ticker(symbol).history(period="1d")['Close'].iloc[-1]
        price_target = None
        if action in ["BUY", "STRONG_BUY"]:
            price_target = current_price * (1 + (overall_score - 50) / 500)
        elif action in ["SELL", "STRONG_SELL"]:
            price_target = current_price * (1 - (50 - overall_score) / 500)
        
        # Risk level
        risk_level = "LOW" if confidence > 80 else "MEDIUM" if confidence > 60 else "HIGH"
        
        return Recommendation(
            action=action,
            confidence=round(confidence, 1),
            price_target=round(price_target, 2) if price_target else None,
            risk_level=risk_level,
            reasoning=reasoning,
            overall_score=round(overall_score, 1)
        )
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> Optional[float]:
        """Calculate RSI indicator"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.iloc[-1]
        except:
            return None
    
    def _calculate_macd(self, prices: pd.Series) -> Tuple[Optional[float], Optional[float]]:
        """Calculate MACD indicator"""
        try:
            ema_12 = prices.ewm(span=12).mean()
            ema_26 = prices.ewm(span=26).mean()
            macd = ema_12 - ema_26
            signal = macd.ewm(span=9).mean()
            return macd.iloc[-1], signal.iloc[-1]
        except:
            return None, None
    
    def _calculate_bollinger_bands(self, prices: pd.Series, period: int = 20) -> Tuple[Optional[float], Optional[float]]:
        """Calculate Bollinger Bands"""
        try:
            sma = prices.rolling(window=period).mean()
            std = prices.rolling(window=period).std()
            upper = sma + (std * 2)
            lower = sma - (std * 2)
            return upper.iloc[-1], lower.iloc[-1]
        except:
            return None, None
    
    def _determine_trend(self, current: float, sma_20: float, sma_50: float, sma_200: Optional[float]) -> str:
        """Determine price trend"""
        if sma_200 is None:
            if current > sma_20 > sma_50:
                return "BULLISH"
            elif current < sma_20 < sma_50:
                return "BEARISH"
            else:
                return "NEUTRAL"
        
        if current > sma_20 > sma_50 > sma_200:
            return "STRONG_BULLISH"
        elif current > sma_20 > sma_50:
            return "BULLISH"
        elif current < sma_20 < sma_50 < sma_200:
            return "STRONG_BEARISH"
        elif current < sma_20 < sma_50:
            return "BEARISH"
        else:
            return "NEUTRAL"
    
    def _calculate_fundamental_score(self, fundamentals: FundamentalMetrics) -> float:
        """Calculate fundamental analysis score (0-100)"""
        score = 50  # Base score
        
        # P/E ratio scoring
        if fundamentals.pe_ratio:
            if fundamentals.pe_ratio < 15:
                score += 10
            elif fundamentals.pe_ratio < 25:
                score += 5
            elif fundamentals.pe_ratio > 40:
                score -= 10
        
        # ROE scoring
        if fundamentals.roe:
            if fundamentals.roe > 20:
                score += 15
            elif fundamentals.roe > 15:
                score += 10
            elif fundamentals.roe > 10:
                score += 5
            elif fundamentals.roe < 5:
                score -= 10
        
        # Debt-to-equity scoring
        if fundamentals.debt_to_equity:
            if fundamentals.debt_to_equity < 0.3:
                score += 10
            elif fundamentals.debt_to_equity < 0.6:
                score += 5
            elif fundamentals.debt_to_equity > 1.0:
                score -= 10
        
        # Revenue growth scoring
        if fundamentals.revenue_growth:
            if fundamentals.revenue_growth > 20:
                score += 15
            elif fundamentals.revenue_growth > 10:
                score += 10
            elif fundamentals.revenue_growth > 5:
                score += 5
            elif fundamentals.revenue_growth < 0:
                score -= 10
        
        return max(0, min(100, score))
    
    def _calculate_technical_score(self, technicals: TechnicalMetrics, current_price: float) -> float:
        """Calculate technical analysis score (0-100)"""
        score = 50  # Base score
        
        # RSI scoring
        if technicals.rsi:
            if 40 <= technicals.rsi <= 60:
                score += 10  # Neutral zone
            elif 30 <= technicals.rsi <= 40:
                score += 5   # Slightly oversold
            elif technicals.rsi < 30:
                score += 15  # Oversold (buy signal)
            elif 60 <= technicals.rsi <= 70:
                score += 5   # Slightly overbought
            elif technicals.rsi > 70:
                score -= 10  # Overbought (sell signal)
        
        # Trend scoring
        trend_scores = {
            "STRONG_BULLISH": 20,
            "BULLISH": 15,
            "NEUTRAL": 0,
            "BEARISH": -15,
            "STRONG_BEARISH": -20
        }
        score += trend_scores.get(technicals.trend, 0)
        
        # MACD scoring
        if technicals.macd and technicals.macd_signal:
            if technicals.macd > technicals.macd_signal:
                score += 10  # Bullish crossover
            else:
                score -= 5   # Bearish crossover
        
        # Moving average scoring
        if technicals.sma_20 and technicals.sma_50:
            if current_price > technicals.sma_20 > technicals.sma_50:
                score += 10
            elif current_price < technicals.sma_20 < technicals.sma_50:
                score -= 10
        
        return max(0, min(100, score))


# Example usage and testing
if __name__ == "__main__":
    analyzer = FinancialAnalyzer()
    
    # Test with a sample stock
    try:
        symbol = "AAPL"
        print(f"Analyzing {symbol}...")
        
        stock_data = analyzer.get_stock_data(symbol)
        fundamentals = analyzer.analyze_fundamentals(symbol)
        technicals = analyzer.analyze_technicals(symbol)
        sentiment = analyzer.analyze_sentiment(symbol)
        recommendation = analyzer.generate_recommendation(symbol, fundamentals, technicals, sentiment)
        
        print(f"Stock: {stock_data.name} ({stock_data.symbol})")
        print(f"Price: ${stock_data.current_price} ({stock_data.change_percent:+.2f}%)")
        print(f"Recommendation: {recommendation.action} (Confidence: {recommendation.confidence}%)")
        print(f"Price Target: ${recommendation.price_target}")
        print(f"Overall Score: {recommendation.overall_score}/100")
        
    except Exception as e:
        print(f"Error: {e}")