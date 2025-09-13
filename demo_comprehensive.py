#!/usr/bin/env python3
"""
Demo script showing comprehensive analysis features
"""
import sys
from financial_agent_rich import FinancialAgentRich


def demo_comprehensive_analysis():
    """Demonstrate the comprehensive analysis features"""
    print("🚀 Financial Research Agent - Comprehensive Analysis Demo")
    print("=" * 60)
    
    agent = FinancialAgentRich()
    
    # Test symbols for different scenarios
    test_symbols = ["AAPL", "TSLA", "MSFT"]
    
    print("\n📊 Available Analysis Types:")
    print("1. 📈 Standard Analysis - Basic fundamental, technical, sentiment")
    print("2. 🔬 Comprehensive Analysis - Advanced metrics including:")
    print("   • Financial Health (Piotroski Score, Altman Z-Score)")
    print("   • Risk Analysis (Beta, Sharpe Ratio, Max Drawdown)")
    print("   • Valuation Models (DCF, Graham Number, Price/FCF)")
    print("   • Quality Analysis (Earnings Quality, Cash Flow Analysis)")
    print("   • Momentum Analysis (Multi-timeframe momentum)")
    print("   • Sector Context & Market Correlation")
    
    print("\n🎯 Key Features Added:")
    print("   ✅ Piotroski F-Score (0-9) for financial health")
    print("   ✅ Altman Z-Score for bankruptcy risk assessment")
    print("   ✅ DCF valuation model with growth assumptions") 
    print("   ✅ Advanced risk metrics (Sharpe, Sortino, VaR)")
    print("   ✅ Earnings quality assessment")
    print("   ✅ Cash flow vs earnings analysis")
    print("   ✅ Multi-timeframe momentum analysis")
    print("   ✅ Comprehensive composite scoring")
    
    print("\n💡 Usage:")
    print("   • Run: python financial_agent_rich.py")
    print("   • Type 'comprehensive' at the prompt")
    print("   • Enter any stock ticker (e.g., AAPL, TSLA, MSFT)")
    print("   • View detailed multi-panel analysis")
    
    print("\n🔥 What's New vs Basic Analysis:")
    print("   • 4 additional analysis panels (Health, Risk, Valuation, Quality)")
    print("   • 15+ new financial metrics and ratios")
    print("   • Advanced scoring algorithms")
    print("   • Visual panels with color-coded ratings")
    print("   • Key insights and warnings system")
    print("   • Composite score combining all factors")
    
    print("\n" + "=" * 60)
    print("🎉 Your financial analysis is now significantly more comprehensive!")
    print("Try it out: python financial_agent_rich.py")


if __name__ == "__main__":
    demo_comprehensive_analysis()