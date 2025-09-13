"""
Web-based Financial Research Agent using Streamlit
Mirrors the functionality of the Textual TUI for web deployment
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import asyncio
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from finance_core import FinancialAnalyzer, StockData, FundamentalMetrics, TechnicalMetrics, SentimentMetrics, Recommendation
from comprehensive_analyzer import ComprehensiveAnalyzer, ComprehensiveAnalysis

# Page configuration
st.set_page_config(
    page_title="Financial Research Agent",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .success-metric {
        border-left-color: #28a745;
    }
    .warning-metric {
        border-left-color: #ffc107;
    }
    .danger-metric {
        border-left-color: #dc3545;
    }
    .analysis-section {
        margin: 1rem 0;
        padding: 1rem;
        background-color: #fafafa;
        border-radius: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

class WebFinancialAgent:
    def __init__(self):
        self.analyzer = FinancialAnalyzer()
        self.comprehensive_analyzer = ComprehensiveAnalyzer()
    
    def get_rating_color(self, rating: str) -> str:
        """Get color class for rating"""
        rating_colors = {
            "Good": "success-metric",
            "Fair": "warning-metric", 
            "Poor": "danger-metric",
            "Excellent": "success-metric",
            "High": "danger-metric",
            "Medium": "warning-metric",
            "Low": "success-metric"
        }
        return rating_colors.get(rating, "metric-card")
    
    def format_number(self, num):
        """Format large numbers with appropriate suffixes"""
        if num is None:
            return "N/A"
        if num >= 1e12:
            return f"${num/1e12:.2f}T"
        elif num >= 1e9:
            return f"${num/1e9:.2f}B"
        elif num >= 1e6:
            return f"${num/1e6:.2f}M"
        else:
            return f"${num:,.0f}"
    
    def create_stock_overview(self, stock_data: StockData, recommendation: Recommendation):
        """Create stock overview section"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Current Price",
                value=f"${stock_data.current_price}",
                delta=f"{stock_data.change_percent:+.2f}%"
            )
        
        with col2:
            st.metric(
                label="Market Cap",
                value=self.format_number(stock_data.market_cap),
                delta=None
            )
        
        with col3:
            # Color code recommendation
            rec_color = {
                "STRONG_BUY": "🟢",
                "BUY": "🟢", 
                "HOLD": "🟡",
                "SELL": "🔴",
                "STRONG_SELL": "🔴"
            }.get(recommendation.action, "⚪")
            
            st.metric(
                label="Recommendation",
                value=f"{rec_color} {recommendation.action}",
                delta=f"{recommendation.confidence}% confidence"
            )
        
        with col4:
            st.metric(
                label="Overall Score",
                value=f"{recommendation.overall_score}/100",
                delta=f"{recommendation.risk_level} Risk"
            )
    
    def create_fundamentals_section(self, fundamentals: FundamentalMetrics):
        """Create fundamentals analysis section"""
        st.subheader("📊 Fundamental Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Valuation Metrics**")
            if fundamentals.pe_ratio:
                st.metric("P/E Ratio", f"{fundamentals.pe_ratio:.2f}")
            if fundamentals.pb_ratio:
                st.metric("P/B Ratio", f"{fundamentals.pb_ratio:.2f}")
            if fundamentals.ps_ratio:
                st.metric("P/S Ratio", f"{fundamentals.ps_ratio:.2f}")
        
        with col2:
            st.markdown("**Profitability Metrics**")
            if fundamentals.roe:
                st.metric("ROE", f"{fundamentals.roe:.1f}%")
            if fundamentals.roa:
                st.metric("ROA", f"{fundamentals.roa:.1f}%")
            if fundamentals.profit_margin:
                st.metric("Profit Margin", f"{fundamentals.profit_margin:.1f}%")
        
        with col3:
            st.markdown("**Growth & Health**")
            if fundamentals.revenue_growth:
                st.metric("Revenue Growth", f"{fundamentals.revenue_growth:.1f}%")
            if fundamentals.current_ratio:
                st.metric("Current Ratio", f"{fundamentals.current_ratio:.2f}")
            if fundamentals.debt_to_equity:
                st.metric("Debt/Equity", f"{fundamentals.debt_to_equity:.2f}")
        
        # Overall score
        score_color = "🟢" if fundamentals.score >= 70 else "🟡" if fundamentals.score >= 50 else "🔴"
        st.metric("Fundamental Score", f"{score_color} {fundamentals.score:.1f}/100")
    
    def create_technical_section(self, technicals: TechnicalMetrics):
        """Create technical analysis section"""
        st.subheader("📈 Technical Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**Momentum Indicators**")
            if technicals.rsi:
                rsi_color = "🟢" if 30 <= technicals.rsi <= 70 else "🔴"
                st.metric("RSI (14)", f"{rsi_color} {technicals.rsi:.1f}")
            
            if technicals.macd and technicals.macd_signal:
                macd_signal = "🟢 Bullish" if technicals.macd > technicals.macd_signal else "🔴 Bearish"
                st.metric("MACD Signal", macd_signal)
        
        with col2:
            st.markdown("**Moving Averages**")
            if technicals.sma_20:
                st.metric("SMA 20", f"${technicals.sma_20:.2f}")
            if technicals.sma_50:
                st.metric("SMA 50", f"${technicals.sma_50:.2f}")
            if technicals.sma_200:
                st.metric("SMA 200", f"${technicals.sma_200:.2f}")
        
        with col3:
            st.markdown("**Support & Resistance**")
            if technicals.support_level:
                st.metric("Support", f"${technicals.support_level:.2f}")
            if technicals.resistance_level:
                st.metric("Resistance", f"${technicals.resistance_level:.2f}")
            
            # Trend indicator
            trend_color = {
                "STRONG_BULLISH": "🟢",
                "BULLISH": "🟢",
                "NEUTRAL": "🟡", 
                "BEARISH": "🔴",
                "STRONG_BEARISH": "🔴"
            }.get(technicals.trend, "⚪")
            st.metric("Trend", f"{trend_color} {technicals.trend}")
        
        # Overall score
        score_color = "🟢" if technicals.score >= 70 else "🟡" if technicals.score >= 50 else "🔴"
        st.metric("Technical Score", f"{score_color} {technicals.score:.1f}/100")
    
    def create_sentiment_section(self, sentiment: SentimentMetrics):
        """Create sentiment analysis section"""
        st.subheader("🎭 Sentiment Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Analyst Coverage**")
            if sentiment.analyst_rating:
                st.metric("Analyst Rating", sentiment.analyst_rating)
            if sentiment.analyst_count:
                st.metric("Analyst Count", sentiment.analyst_count)
        
        with col2:
            st.markdown("**Sentiment Sources**")
            if sentiment.news_sentiment is not None:
                news_color = "🟢" if sentiment.news_sentiment > 60 else "🔴" if sentiment.news_sentiment < 40 else "🟡"
                st.metric("News Sentiment", f"{news_color} {sentiment.news_sentiment:.1f}/100")
            else:
                st.info("News sentiment requires API key")
                
            if sentiment.social_sentiment is not None:
                social_color = "🟢" if sentiment.social_sentiment > 60 else "🔴" if sentiment.social_sentiment < 40 else "🟡"
                st.metric("Social Sentiment", f"{social_color} {sentiment.social_sentiment:.1f}/100")
            else:
                st.info("Social sentiment requires API keys")
        
        # Overall sentiment
        score_color = "🟢" if sentiment.score >= 70 else "🟡" if sentiment.score >= 50 else "🔴"
        st.metric("Sentiment Score", f"{score_color} {sentiment.score:.1f}/100")
        
        if sentiment.sentiment_summary:
            st.info(f"**Summary:** {sentiment.sentiment_summary}")
    
    def create_comprehensive_section(self, analysis: ComprehensiveAnalysis):
        """Create comprehensive analysis section"""
        st.subheader("🔬 Comprehensive Analysis")
        
        # Composite Score
        score_color = "🟢" if analysis.composite_score >= 70 else "🟡" if analysis.composite_score >= 50 else "🔴"
        st.metric("Composite Score", f"{score_color} {analysis.composite_score:.1f}/100", 
                 delta=f"{analysis.confidence_level:.1%} confidence")
        
        # Create tabs for different analysis areas
        tab1, tab2, tab3, tab4 = st.tabs(["💊 Health", "⚠️ Risk", "💰 Valuation", "📊 Quality"])
        
        with tab1:
            self.create_health_section(analysis.financial_health)
        
        with tab2:
            self.create_risk_section(analysis.risk_metrics)
        
        with tab3:
            self.create_valuation_section(analysis.valuation_metrics)
        
        with tab4:
            self.create_quality_section(analysis.quality_metrics)
        
        # Key Insights and Warnings
        if analysis.key_insights:
            st.subheader("🎯 Key Insights")
            for insight in analysis.key_insights:
                st.success(f"• {insight}")
        
        if analysis.warnings:
            st.subheader("⚠️ Warnings")
            for warning in analysis.warnings:
                st.error(warning)
    
    def create_health_section(self, health):
        """Create financial health section"""
        col1, col2 = st.columns(2)
        
        with col1:
            if health.piotroski_score is not None:
                score_color = "🟢" if health.piotroski_score >= 7 else "🟡" if health.piotroski_score >= 4 else "🔴"
                st.metric("Piotroski F-Score", f"{score_color} {health.piotroski_score}/9")
            
            if health.working_capital is not None:
                wc_color = "🟢" if health.working_capital > 0 else "🔴"
                st.metric("Working Capital", f"{wc_color} {self.format_number(health.working_capital)}")
        
        with col2:
            if health.altman_z_score is not None:
                if health.altman_z_score > 3.0:
                    z_color, z_label = "🟢", "Safe"
                elif health.altman_z_score > 1.8:
                    z_color, z_label = "🟡", "Gray Zone"
                else:
                    z_color, z_label = "🔴", "Distress"
                st.metric("Altman Z-Score", f"{z_color} {health.altman_z_score:.2f}", delta=z_label)
            
            if health.debt_coverage_ratio is not None:
                coverage_color = "🟢" if health.debt_coverage_ratio > 0.2 else "🔴"
                st.metric("Debt Coverage", f"{coverage_color} {health.debt_coverage_ratio:.2f}")
    
    def create_risk_section(self, risk):
        """Create risk analysis section"""
        col1, col2 = st.columns(2)
        
        with col1:
            if risk.beta is not None:
                beta_color = "🟢" if risk.beta < 1.2 else "🟡" if risk.beta < 1.5 else "🔴"
                st.metric("Beta", f"{beta_color} {risk.beta:.2f}")
            
            if risk.sharpe_ratio is not None:
                sharpe_color = "🟢" if risk.sharpe_ratio > 1.0 else "🟡" if risk.sharpe_ratio > 0.5 else "🔴"
                st.metric("Sharpe Ratio", f"{sharpe_color} {risk.sharpe_ratio:.2f}")
        
        with col2:
            if risk.max_drawdown is not None:
                dd_color = "🟢" if risk.max_drawdown > -15 else "🟡" if risk.max_drawdown > -30 else "🔴"
                st.metric("Max Drawdown", f"{dd_color} {risk.max_drawdown:.1f}%")
            
            if risk.volatility_30d is not None:
                vol_color = "🟢" if risk.volatility_30d < 20 else "🟡" if risk.volatility_30d < 35 else "🔴"
                st.metric("30D Volatility", f"{vol_color} {risk.volatility_30d:.1f}%")
    
    def create_valuation_section(self, valuation):
        """Create valuation analysis section"""
        col1, col2 = st.columns(2)
        
        with col1:
            if valuation.dcf_estimate is not None:
                st.metric("DCF Estimate", f"${valuation.dcf_estimate:.2f}")
            
            if valuation.graham_number is not None:
                st.metric("Graham Number", f"${valuation.graham_number:.2f}")
        
        with col2:
            if valuation.price_to_fcf is not None:
                fcf_color = "🟢" if valuation.price_to_fcf < 15 else "🟡" if valuation.price_to_fcf < 25 else "🔴"
                st.metric("Price/FCF", f"{fcf_color} {valuation.price_to_fcf:.1f}")
            
            if valuation.ev_sales is not None:
                ev_color = "🟢" if valuation.ev_sales < 3 else "🟡" if valuation.ev_sales < 6 else "🔴"
                st.metric("EV/Sales", f"{ev_color} {valuation.ev_sales:.1f}")
    
    def create_quality_section(self, quality):
        """Create quality analysis section"""
        col1, col2 = st.columns(2)
        
        with col1:
            if quality.earnings_quality is not None:
                eq_color = "🟢" if quality.earnings_quality >= 75 else "🟡" if quality.earnings_quality >= 50 else "🔴"
                st.metric("Earnings Quality", f"{eq_color} {quality.earnings_quality:.1f}%")
        
        with col2:
            if quality.cash_flow_to_earnings is not None:
                cf_color = "🟢" if quality.cash_flow_to_earnings > 1.0 else "🟡" if quality.cash_flow_to_earnings > 0.8 else "🔴"
                st.metric("CF/Earnings Ratio", f"{cf_color} {quality.cash_flow_to_earnings:.2f}")
        
        if quality.accounting_red_flags:
            st.warning(f"**Accounting Red Flags:** {len(quality.accounting_red_flags)} detected")
            for flag in quality.accounting_red_flags:
                st.error(f"• {flag}")
    
    def create_price_chart(self, symbol: str, period: str = "1mo"):
        """Create interactive price chart"""
        try:
            historical_data = self.analyzer.get_historical_data(symbol, period)
            
            fig = go.Figure()
            
            fig.add_trace(go.Candlestick(
                x=historical_data['Date'],
                open=historical_data['Open'],
                high=historical_data['High'],
                low=historical_data['Low'],
                close=historical_data['Close'],
                name=symbol
            ))
            
            fig.update_layout(
                title=f"{symbol} Price Chart ({period})",
                yaxis_title="Price ($)",
                xaxis_title="Date",
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        except Exception as e:
            st.error(f"Could not load chart: {str(e)}")


def main():
    """Main Streamlit application"""
    
    # Initialize session state
    if 'agent' not in st.session_state:
        st.session_state.agent = WebFinancialAgent()
    
    if 'analysis_results' not in st.session_state:
        st.session_state.analysis_results = None
    
    # Header
    st.markdown('<h1 class="main-header">📈 Financial Research Agent</h1>', unsafe_allow_html=True)
    st.markdown("**Professional-grade stock analysis with comprehensive metrics**")
    
    # Sidebar
    with st.sidebar:
        st.header("🔧 Analysis Settings")
        
        # Stock symbol input
        symbol = st.text_input(
            "Stock Ticker",
            placeholder="e.g., AAPL, TSLA, MSFT",
            help="Enter a valid stock ticker symbol"
        ).upper().strip()
        
        # Analysis mode selection
        analysis_mode = st.radio(
            "Analysis Mode",
            ["📈 Standard Analysis", "🔬 Comprehensive Analysis"],
            help="Standard: Basic analysis\nComprehensive: Advanced metrics + health/risk/valuation"
        )
        
        # Chart period for comprehensive mode
        if "🔬 Comprehensive" in analysis_mode:
            chart_period = st.selectbox(
                "Chart Period",
                ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y"],
                index=2
            )
        else:
            chart_period = "1mo"
        
        # Analyze button
        analyze_button = st.button("🚀 Analyze Stock", type="primary", use_container_width=True)
        
        # Info section
        st.markdown("---")
        st.markdown("### 💡 Features")
        if "🔬 Comprehensive" in analysis_mode:
            st.success("✅ Piotroski F-Score")
            st.success("✅ Altman Z-Score")
            st.success("✅ DCF Valuation")
            st.success("✅ Risk Analysis")
            st.success("✅ Quality Assessment")
        st.info("✅ Technical Analysis")
        st.info("✅ Fundamental Analysis") 
        st.info("✅ Sentiment Analysis")
    
    # Main content area
    if analyze_button and symbol:
        if len(symbol) > 10:
            st.error("Please enter a valid ticker symbol (max 10 characters)")
            return
        
        with st.spinner(f"Analyzing {symbol}..."):
            try:
                # Perform analysis
                agent = st.session_state.agent
                
                # Basic analysis
                stock_data = agent.analyzer.get_stock_data(symbol)
                fundamentals = agent.analyzer.analyze_fundamentals(symbol)
                technicals = agent.analyzer.analyze_technicals(symbol)
                sentiment = agent.analyzer.analyze_sentiment(symbol)
                recommendation = agent.analyzer.generate_recommendation(
                    symbol, fundamentals, technicals, sentiment
                )
                
                # Comprehensive analysis if selected
                comprehensive_analysis = None
                if "🔬 Comprehensive" in analysis_mode:
                    comprehensive_analysis = agent.comprehensive_analyzer.perform_comprehensive_analysis(symbol)
                
                # Store results
                st.session_state.analysis_results = {
                    'stock_data': stock_data,
                    'fundamentals': fundamentals,
                    'technicals': technicals,
                    'sentiment': sentiment,
                    'recommendation': recommendation,
                    'comprehensive': comprehensive_analysis,
                    'symbol': symbol,
                    'mode': analysis_mode,
                    'chart_period': chart_period
                }
                
            except Exception as e:
                st.error(f"Error analyzing {symbol}: {str(e)}")
                return
    
    # Display results if available
    if st.session_state.analysis_results:
        results = st.session_state.analysis_results
        agent = st.session_state.agent
        
        # Stock Overview
        st.markdown("---")
        st.header(f"📊 {results['stock_data'].name} ({results['symbol']})")
        agent.create_stock_overview(results['stock_data'], results['recommendation'])
        
        # Analysis sections
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Main analysis tabs
            if results['comprehensive']:
                tab1, tab2, tab3, tab4, tab5 = st.tabs([
                    "📊 Fundamentals", "📈 Technical", "🎭 Sentiment", 
                    "🔬 Comprehensive", "📉 Chart"
                ])
            else:
                tab1, tab2, tab3, tab4 = st.tabs([
                    "📊 Fundamentals", "📈 Technical", "🎭 Sentiment", "📉 Chart"
                ])
            
            with tab1:
                agent.create_fundamentals_section(results['fundamentals'])
            
            with tab2:
                agent.create_technical_section(results['technicals'])
            
            with tab3:
                agent.create_sentiment_section(results['sentiment'])
            
            if results['comprehensive']:
                with tab4:
                    agent.create_comprehensive_section(results['comprehensive'])
                with tab5:
                    agent.create_price_chart(results['symbol'], results['chart_period'])
            else:
                with tab4:
                    agent.create_price_chart(results['symbol'], results['chart_period'])
        
        with col2:
            # Recommendation summary
            st.subheader("📋 Investment Summary")
            
            rec = results['recommendation']
            action_colors = {
                "STRONG_BUY": "success",
                "BUY": "success",
                "HOLD": "warning",
                "SELL": "error",
                "STRONG_SELL": "error"
            }
            
            action_color = action_colors.get(rec.action, "info")
            getattr(st, action_color)(f"**Recommendation:** {rec.action}")
            st.metric("Confidence", f"{rec.confidence}%")
            st.metric("Overall Score", f"{rec.overall_score}/100")
            st.metric("Risk Level", rec.risk_level)
            
            if rec.price_target:
                current_price = results['stock_data'].current_price
                upside = ((rec.price_target - current_price) / current_price) * 100
                st.metric("Price Target", f"${rec.price_target:.2f}", delta=f"{upside:+.1f}%")
            
            # Key reasoning
            if rec.reasoning:
                st.subheader("🎯 Key Points")
                for reason in rec.reasoning:
                    st.info(f"• {reason}")
    
    else:
        # Welcome message
        st.markdown("---")
        st.info("👈 Enter a stock ticker in the sidebar and click **Analyze Stock** to begin!")
        
        # Example stocks
        st.subheader("🌟 Try These Examples:")
        example_cols = st.columns(4)
        examples = ["AAPL", "TSLA", "MSFT", "GOOGL"]
        
        for col, example in zip(example_cols, examples):
            with col:
                if st.button(f"📈 {example}", use_container_width=True):
                    st.rerun()


if __name__ == "__main__":
    main()