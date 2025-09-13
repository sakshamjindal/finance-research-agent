"""
Rich-based Financial Research Agent - Enhanced CLI with beautiful output
"""
import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn
from rich.layout import Layout
from rich.align import Align
from rich.text import Text
from rich.prompt import Prompt, Confirm
from rich.columns import Columns
from rich.rule import Rule
import time
import sys

from finance_core import FinancialAnalyzer, StockData, FundamentalMetrics, TechnicalMetrics, SentimentMetrics, Recommendation
from comprehensive_analyzer import ComprehensiveAnalyzer, ComprehensiveAnalysis


class FinancialAgentRich:
    """Rich-based Financial Research Agent"""
    
    def __init__(self):
        self.console = Console()
        self.analyzer = FinancialAnalyzer()
        self.comprehensive_analyzer = ComprehensiveAnalyzer()
        self.watchlist = []
        
    def show_banner(self):
        """Display application banner"""
        banner_text = Text("Financial Research Agent", style="bold blue")
        banner_text.append("\n", style="")
        banner_text.append("Advanced Stock Analysis with Rich CLI", style="dim")
        
        banner = Panel(
            Align.center(banner_text),
            border_style="blue",
            padding=(1, 2),
        )
        self.console.print(banner)
        self.console.print()
        
    def show_stock_suggestions(self):
        """Display popular stock suggestions"""
        self.console.print("[bold green]💡 Popular Stocks to Analyze:[/bold green]\n")
        
        # Define stock categories
        stock_categories = {
            "🏛️ Large Cap Tech": ["AAPL", "MSFT", "GOOGL", "AMZN", "META"],
            "🚗 Growth & Innovation": ["TSLA", "NVDA", "NFLX", "UBER", "SHOP"],
            "💰 Financial Services": ["BRK-A", "JPM", "V", "MA", "BAC"],
            "🏥 Healthcare & Biotech": ["JNJ", "PFE", "UNH", "ABBV", "TMO"],
            "🏭 Industrial & Energy": ["CAT", "XOM", "CVX", "GE", "BA"],
            "🛒 Consumer & Retail": ["KO", "PEP", "WMT", "HD", "MCD"]
        }
        
        # Create columns for each category
        columns = []
        for category, stocks in stock_categories.items():
            stock_list = "\n".join([f"• [cyan]{stock}[/cyan]" for stock in stocks])
            panel = Panel(
                stock_list,
                title=category,
                title_align="left",
                border_style="dim",
                padding=(0, 1)
            )
            columns.append(panel)
        
        # Display in columns
        self.console.print(Columns(columns[:3], equal=True))
        self.console.print()
        self.console.print(Columns(columns[3:], equal=True))
        self.console.print()
        
        # Show quick example
        example_panel = Panel(
            "[bold yellow]💡 Quick Start Examples:[/bold yellow]\n"
            "• Type [bold cyan]AAPL[/bold cyan] for Apple stock analysis\n"
            "• Type [bold cyan]TSLA[/bold cyan] for Tesla comprehensive analysis\n"
            "• Type [bold cyan]MSFT[/bold cyan] for Microsoft analysis",
            title="🚀 Getting Started",
            border_style="yellow",
            padding=(0, 1)
        )
        self.console.print(example_panel)
        self.console.print()
    
    def get_stock_input(self) -> str:
        """Get stock ticker from user input"""
        while True:
            symbol = Prompt.ask(
                "\n[bold cyan]Enter stock ticker[/bold cyan] (or 'quit' to exit, 'watchlist' to view watchlist)",
                default=""
            ).strip().upper()
            
            if symbol in ['QUIT', 'EXIT', 'Q']:
                return None
            elif symbol == 'WATCHLIST':
                self.show_watchlist()
                continue
            elif symbol and len(symbol) <= 10:  # Basic validation
                return symbol
            elif not symbol:
                self.console.print("[red]Please enter a valid stock ticker[/red]")
            else:
                self.console.print("[red]Please enter a valid ticker (max 10 characters)[/red]")
    
    def get_analysis_mode(self, symbol: str) -> str:
        """Get analysis mode from user"""
        self.console.print(f"\n[bold green]Selected: {symbol}[/bold green]")
        self.console.print("\n[bold cyan]Choose Analysis Mode:[/bold cyan]")
        self.console.print("1. 📈 [bold]Standard Analysis[/bold] - Basic fundamental, technical, sentiment")
        self.console.print("2. 🔬 [bold]Comprehensive Analysis[/bold] - Advanced metrics (Health, Risk, Valuation, Quality)")
        
        while True:
            choice = Prompt.ask(
                "\nSelect mode [1/2]",
                choices=["1", "2"],
                default="1"
            )
            
            if choice == "1":
                return "standard"
            elif choice == "2":
                return "comprehensive"
    
    def analyze_stock(self, symbol: str) -> bool:
        """Analyze a stock and display results"""
        try:
            # Show analysis progress
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=self.console
            ) as progress:
                
                task = progress.add_task(f"Analyzing {symbol}...", total=100)
                
                # Fetch basic data
                progress.update(task, description=f"Fetching data for {symbol}...", advance=20)
                stock_data = self.analyzer.get_stock_data(symbol)
                time.sleep(0.5)  # Small delay for visual effect
                
                # Fundamental analysis
                progress.update(task, description="Performing fundamental analysis...", advance=25)
                fundamentals = self.analyzer.analyze_fundamentals(symbol)
                time.sleep(0.3)
                
                # Technical analysis  
                progress.update(task, description="Performing technical analysis...", advance=25)
                technicals = self.analyzer.analyze_technicals(symbol)
                time.sleep(0.3)
                
                # Sentiment analysis
                progress.update(task, description="Analyzing market sentiment...", advance=20)
                sentiment = self.analyzer.analyze_sentiment(symbol)
                time.sleep(0.3)
                
                # Generate recommendation
                progress.update(task, description="Generating recommendation...", advance=10)
                recommendation = self.analyzer.generate_recommendation(
                    symbol, fundamentals, technicals, sentiment
                )
                time.sleep(0.2)
            
            self.console.print()
            
            # Display results
            self.display_stock_overview(stock_data, recommendation)
            self.display_detailed_analysis(fundamentals, technicals, sentiment)
            self.display_recommendation(recommendation)
            
            # Ask if user wants to add to watchlist
            if symbol not in self.watchlist:
                add_to_watchlist = Confirm.ask(f"\nAdd {symbol} to your watchlist?", default=False)
                if add_to_watchlist:
                    self.watchlist.append(symbol)
                    self.console.print(f"[green]✓ Added {symbol} to watchlist[/green]")
            
            return True
            
        except Exception as e:
            self.console.print(f"\n[red]Error analyzing {symbol}: {str(e)}[/red]")
            return False
    
    def display_stock_overview(self, stock_data: StockData, recommendation: Recommendation):
        """Display stock overview panel"""
        # Create main info table
        info_table = Table.grid(padding=1)
        info_table.add_column(justify="left", style="cyan")
        info_table.add_column(justify="right")
        
        # Format change with color
        change_color = "green" if stock_data.change_percent >= 0 else "red"
        change_text = f"+{stock_data.change_percent:.2f}%" if stock_data.change_percent >= 0 else f"{stock_data.change_percent:.2f}%"
        
        info_table.add_row("Company:", stock_data.name)
        info_table.add_row("Symbol:", stock_data.symbol)
        info_table.add_row("Current Price:", f"${stock_data.current_price}")
        info_table.add_row("Change:", f"[{change_color}]{change_text}[/{change_color}]")
        
        if stock_data.market_cap:
            market_cap_formatted = self.format_number(stock_data.market_cap)
            info_table.add_row("Market Cap:", market_cap_formatted)
        
        # Create recommendation summary
        rec_table = Table.grid(padding=1)
        rec_table.add_column(justify="left", style="cyan")
        rec_table.add_column(justify="right")
        
        # Color code recommendation
        action_colors = {
            "STRONG_BUY": "bright_green",
            "BUY": "green", 
            "HOLD": "yellow",
            "SELL": "red",
            "STRONG_SELL": "bright_red"
        }
        action_color = action_colors.get(recommendation.action, "white")
        
        rec_table.add_row("Recommendation:", f"[{action_color}]{recommendation.action}[/{action_color}]")
        rec_table.add_row("Confidence:", f"{recommendation.confidence}%")
        rec_table.add_row("Overall Score:", f"{recommendation.overall_score}/100")
        rec_table.add_row("Risk Level:", recommendation.risk_level)
        
        if recommendation.price_target:
            rec_table.add_row("Price Target:", f"${recommendation.price_target}")
            upside = ((recommendation.price_target - stock_data.current_price) / stock_data.current_price) * 100
            upside_color = "green" if upside >= 0 else "red"
            rec_table.add_row("Upside/Downside:", f"[{upside_color}]{upside:+.1f}%[/{upside_color}]")
        
        # Create side-by-side layout
        columns = Columns([
            Panel(info_table, title="Stock Information", border_style="blue"),
            Panel(rec_table, title="Recommendation Summary", border_style=action_color)
        ], equal=True)
        
        self.console.print(columns)
    
    def display_detailed_analysis(self, fundamentals: FundamentalMetrics, 
                                technicals: TechnicalMetrics, sentiment: SentimentMetrics):
        """Display detailed analysis in tables"""
        
        # Fundamental Analysis Table
        fund_table = Table(title="Fundamental Analysis", border_style="green")
        fund_table.add_column("Metric", style="cyan")
        fund_table.add_column("Value", justify="right")
        fund_table.add_column("Rating", justify="center")
        
        def get_rating_color(rating):
            colors = {"Good": "green", "Fair": "yellow", "Poor": "red", "N/A": "dim"}
            return colors.get(rating, "white")
        
        def get_fundamental_rating(value, good_threshold, bad_threshold, higher_better=True):
            if value is None:
                return "N/A"
            if higher_better:
                if value >= good_threshold:
                    return "Good"
                elif value <= bad_threshold:
                    return "Poor"
                else:
                    return "Fair"
            else:
                if value <= good_threshold:
                    return "Good"
                elif value >= bad_threshold:
                    return "Poor"
                else:
                    return "Fair"
        
        fundamental_metrics = [
            ("P/E Ratio", f"{fundamentals.pe_ratio:.2f}" if fundamentals.pe_ratio else "N/A",
             get_fundamental_rating(fundamentals.pe_ratio, 25, 40, False)),
            ("P/B Ratio", f"{fundamentals.pb_ratio:.2f}" if fundamentals.pb_ratio else "N/A",
             get_fundamental_rating(fundamentals.pb_ratio, 3, 5, False)),
            ("ROE", f"{fundamentals.roe:.1f}%" if fundamentals.roe else "N/A",
             get_fundamental_rating(fundamentals.roe, 15, 5)),
            ("ROA", f"{fundamentals.roa:.1f}%" if fundamentals.roa else "N/A",
             get_fundamental_rating(fundamentals.roa, 10, 3)),
            ("Profit Margin", f"{fundamentals.profit_margin:.1f}%" if fundamentals.profit_margin else "N/A",
             get_fundamental_rating(fundamentals.profit_margin, 10, 2)),
            ("Debt/Equity", f"{fundamentals.debt_to_equity:.2f}" if fundamentals.debt_to_equity else "N/A",
             get_fundamental_rating(fundamentals.debt_to_equity, 0.5, 1.0, False)),
            ("Current Ratio", f"{fundamentals.current_ratio:.2f}" if fundamentals.current_ratio else "N/A",
             get_fundamental_rating(fundamentals.current_ratio, 1.5, 1.0)),
            ("Revenue Growth", f"{fundamentals.revenue_growth:.1f}%" if fundamentals.revenue_growth else "N/A",
             get_fundamental_rating(fundamentals.revenue_growth, 10, 0)),
        ]
        
        for metric, value, rating in fundamental_metrics:
            rating_color = get_rating_color(rating)
            fund_table.add_row(metric, value, f"[{rating_color}]{rating}[/{rating_color}]")
        
        fund_table.add_row("", "", "")
        overall_fund_rating = "Good" if fundamentals.score >= 70 else "Fair" if fundamentals.score >= 50 else "Poor"
        fund_rating_color = get_rating_color(overall_fund_rating)
        fund_table.add_row("Overall Score", f"{fundamentals.score:.1f}/100", 
                          f"[{fund_rating_color}]{overall_fund_rating}[/{fund_rating_color}]")
        
        # Technical Analysis Table
        tech_table = Table(title="Technical Analysis", border_style="blue")
        tech_table.add_column("Indicator", style="cyan")
        tech_table.add_column("Value", justify="right")
        tech_table.add_column("Signal", justify="center")
        
        def get_rsi_signal_color(rsi):
            if rsi is None:
                return "dim", "N/A"
            if rsi < 30:
                return "green", "Oversold (Buy)"
            elif rsi > 70:
                return "red", "Overbought (Sell)"
            else:
                return "yellow", "Neutral"
        
        def get_macd_signal_color(macd, signal):
            if macd is None or signal is None:
                return "dim", "N/A"
            if macd > signal:
                return "green", "Bullish"
            else:
                return "red", "Bearish"
        
        def get_trend_color(trend):
            colors = {
                "STRONG_BULLISH": "bright_green",
                "BULLISH": "green",
                "NEUTRAL": "yellow",
                "BEARISH": "red",
                "STRONG_BEARISH": "bright_red"
            }
            return colors.get(trend, "white")
        
        rsi_color, rsi_signal = get_rsi_signal_color(technicals.rsi)
        macd_color, macd_signal = get_macd_signal_color(technicals.macd, technicals.macd_signal)
        trend_color = get_trend_color(technicals.trend)
        
        tech_table.add_row("RSI (14)", f"{technicals.rsi:.1f}" if technicals.rsi else "N/A",
                          f"[{rsi_color}]{rsi_signal}[/{rsi_color}]")
        tech_table.add_row("MACD", f"{technicals.macd:.4f}" if technicals.macd else "N/A",
                          f"[{macd_color}]{macd_signal}[/{macd_color}]")
        tech_table.add_row("SMA 20", f"${technicals.sma_20:.2f}" if technicals.sma_20 else "N/A", "")
        tech_table.add_row("SMA 50", f"${technicals.sma_50:.2f}" if technicals.sma_50 else "N/A", "")
        tech_table.add_row("SMA 200", f"${technicals.sma_200:.2f}" if technicals.sma_200 else "N/A", "")
        tech_table.add_row("Trend", technicals.trend, f"[{trend_color}]{technicals.trend}[/{trend_color}]")
        tech_table.add_row("Support", f"${technicals.support_level:.2f}" if technicals.support_level else "N/A", "")
        tech_table.add_row("Resistance", f"${technicals.resistance_level:.2f}" if technicals.resistance_level else "N/A", "")
        tech_table.add_row("", "", "")
        
        overall_tech_rating = "Good" if technicals.score >= 70 else "Fair" if technicals.score >= 50 else "Poor"
        tech_rating_color = get_rating_color(overall_tech_rating)
        tech_table.add_row("Overall Score", f"{technicals.score:.1f}/100",
                          f"[{tech_rating_color}]{overall_tech_rating}[/{tech_rating_color}]")
        
        # Sentiment Analysis Table
        sent_table = Table(title="Sentiment Analysis", border_style="magenta")
        sent_table.add_column("Source", style="cyan")
        sent_table.add_column("Rating", justify="center")
        sent_table.add_column("Score", justify="right")
        
        sent_table.add_row("Analyst Rating", sentiment.analyst_rating or "N/A",
                          f"{sentiment.analyst_score}/100" if sentiment.analyst_score else "N/A")
        sent_table.add_row("Analyst Count", f"{sentiment.analyst_count}" if sentiment.analyst_count else "N/A", "")
        
        # News sentiment
        if sentiment.news_sentiment is not None:
            news_color = "green" if sentiment.news_sentiment > 60 else "red" if sentiment.news_sentiment < 40 else "yellow"
            sent_table.add_row("News Sentiment", f"[{news_color}]{sentiment.news_sentiment:.1f}/100[/{news_color}]",
                              f"{sentiment.news_article_count} articles")
        else:
            sent_table.add_row("News Sentiment", "[dim]No API key[/dim]", "[dim]N/A[/dim]")
        
        # Social sentiment
        if sentiment.social_sentiment is not None:
            social_color = "green" if sentiment.social_sentiment > 60 else "red" if sentiment.social_sentiment < 40 else "yellow"
            sent_table.add_row("Social Media", f"[{social_color}]{sentiment.social_sentiment:.1f}/100[/{social_color}]",
                              f"{sentiment.social_post_count} posts")
        else:
            sent_table.add_row("Social Media", "[dim]No API key[/dim]", "[dim]N/A[/dim]")
        
        sent_table.add_row("", "", "")
        
        # Overall sentiment with confidence
        overall_sent_rating = "Good" if sentiment.score >= 70 else "Fair" if sentiment.score >= 50 else "Poor"
        sent_rating_color = get_rating_color(overall_sent_rating)
        confidence_text = f" ({sentiment.confidence:.0f}% confidence)" if sentiment.confidence > 0 else ""
        sent_table.add_row("Overall Score", f"[{sent_rating_color}]{overall_sent_rating}[/{sent_rating_color}]",
                          f"{sentiment.score:.1f}/100{confidence_text}")
        
        # Add sentiment summary if available
        if sentiment.sentiment_summary:
            sent_table.add_row("Summary", sentiment.sentiment_summary, "")
        
        # Display tables
        self.console.print()
        self.console.print(fund_table)
        self.console.print()
        self.console.print(tech_table)
        self.console.print()
        self.console.print(sent_table)
    
    def display_recommendation(self, recommendation: Recommendation):
        """Display final recommendation"""
        self.console.print()
        
        # Create recommendation panel
        rec_text = Text()
        
        # Action with color
        action_colors = {
            "STRONG_BUY": "bright_green",
            "BUY": "green",
            "HOLD": "yellow", 
            "SELL": "red",
            "STRONG_SELL": "bright_red"
        }
        action_color = action_colors.get(recommendation.action, "white")
        
        rec_text.append("RECOMMENDATION: ", style="bold")
        rec_text.append(recommendation.action, style=f"bold {action_color}")
        rec_text.append(f" (Confidence: {recommendation.confidence}%)\n\n", style="")
        
        # Add key points
        if recommendation.reasoning:
            rec_text.append("Key Analysis Points:\n", style="bold cyan")
            for reason in recommendation.reasoning:
                rec_text.append(f"• {reason}\n", style="")
        
        rec_text.append(f"\nOverall Score: {recommendation.overall_score}/100\n", style="")
        rec_text.append(f"Risk Level: {recommendation.risk_level}", style="")
        
        panel = Panel(
            rec_text,
            title="Investment Recommendation",
            border_style=action_color,
            padding=(1, 2)
        )
        
        self.console.print(panel)
    
    
    def perform_comprehensive_analysis(self, symbol: str) -> bool:
        """Perform and display comprehensive analysis"""
        try:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                console=self.console
            ) as progress:
                
                task = progress.add_task(f"🔍 Comprehensive Analysis for {symbol}...", total=100)
                
                # Perform basic analysis first
                progress.update(task, description="📊 Basic financial analysis...", advance=20)
                stock_data = self.analyzer.get_stock_data(symbol)
                fundamentals = self.analyzer.analyze_fundamentals(symbol)
                technicals = self.analyzer.analyze_technicals(symbol)
                sentiment = self.analyzer.analyze_sentiment(symbol)
                recommendation = self.analyzer.generate_recommendation(symbol, fundamentals, technicals, sentiment)
                
                # Perform comprehensive analysis
                progress.update(task, description="🧠 Advanced analysis...", advance=80)
                comprehensive = self.comprehensive_analyzer.perform_comprehensive_analysis(symbol)
                
            # Display all results
            self.display_stock_overview(stock_data, recommendation)
            self.display_detailed_analysis(fundamentals, technicals, sentiment)
            self.display_comprehensive_results(comprehensive)
            self.display_recommendation(recommendation)
            
            # Ask to add to watchlist
            if Confirm.ask(f"\nAdd {symbol} to your watchlist?", default=False):
                if symbol not in self.watchlist:
                    self.watchlist.append(symbol)
                    self.console.print(f"[green]✓ Added {symbol} to watchlist[/green]")
                else:
                    self.console.print(f"[yellow]{symbol} is already in your watchlist[/yellow]")
            
            return True
            
        except Exception as e:
            self.console.print(f"\n[red]Error analyzing {symbol}: {str(e)}[/red]")
            return False
    
    def display_comprehensive_results(self, analysis: ComprehensiveAnalysis):
        """Display comprehensive analysis results"""
        
        # Financial Health Panel
        health_panel = self.create_financial_health_panel(analysis.financial_health)
        
        # Risk Analysis Panel  
        risk_panel = self.create_risk_analysis_panel(analysis.risk_metrics)
        
        # Valuation Analysis Panel
        valuation_panel = self.create_valuation_panel(analysis.valuation_metrics)
        
        # Quality Metrics Panel
        quality_panel = self.create_quality_panel(analysis.quality_metrics)
        
        # Display panels in a grid
        self.console.print("\n" + "="*80)
        self.console.print("[bold magenta]🔬 COMPREHENSIVE ANALYSIS RESULTS[/bold magenta]", justify="center")
        self.console.print("="*80)
        
        # Row 1: Health & Risk
        columns1 = Columns([health_panel, risk_panel], equal=True, expand=True)
        self.console.print(columns1)
        
        # Row 2: Valuation & Quality
        columns2 = Columns([valuation_panel, quality_panel], equal=True, expand=True)
        self.console.print(columns2)
        
        # Key Insights
        if analysis.key_insights:
            insights_text = Text()
            insights_text.append("🎯 Key Insights:\n", style="bold cyan")
            for insight in analysis.key_insights:
                insights_text.append(f"  • {insight}\n", style="")
                
            insights_panel = Panel(insights_text, title="Key Insights", border_style="cyan")
            self.console.print(insights_panel)
        
        # Warnings
        if analysis.warnings:
            warnings_text = Text()
            for warning in analysis.warnings:
                warnings_text.append(f"  {warning}\n", style="red")
                
            warnings_panel = Panel(warnings_text, title="⚠️ Warnings", border_style="red")
            self.console.print(warnings_panel)
        
        # Composite Score
        score_color = "green" if analysis.composite_score >= 70 else "yellow" if analysis.composite_score >= 50 else "red"
        composite_text = Text()
        composite_text.append(f"Composite Score: ", style="bold")
        composite_text.append(f"{analysis.composite_score:.1f}/100", style=f"bold {score_color}")
        composite_text.append(f"\nAnalysis Confidence: {analysis.confidence_level:.1%}", style="")
        
        composite_panel = Panel(
            Align.center(composite_text), 
            title="Overall Assessment", 
            border_style=score_color
        )
        self.console.print(composite_panel)
    
    def create_financial_health_panel(self, health) -> Panel:
        """Create financial health analysis panel"""
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Metric", style="cyan", width=18)
        table.add_column("Value", justify="right", width=12)
        table.add_column("Rating", justify="center", width=8)
        
        # Piotroski Score
        if health.piotroski_score is not None:
            score_rating = "Good" if health.piotroski_score >= 7 else "Fair" if health.piotroski_score >= 4 else "Poor"
            table.add_row("Piotroski Score", f"{health.piotroski_score}/9", score_rating)
        
        # Altman Z-Score
        if health.altman_z_score is not None:
            if health.altman_z_score > 3.0:
                z_rating, z_color = "Safe", "green"
            elif health.altman_z_score > 1.8:
                z_rating, z_color = "Gray Zone", "yellow"
            else:
                z_rating, z_color = "Distress", "red"
            table.add_row("Altman Z-Score", f"{health.altman_z_score:.2f}", f"[{z_color}]{z_rating}[/{z_color}]")
        
        # Working Capital
        if health.working_capital is not None:
            wc_formatted = self.format_number(health.working_capital)
            wc_rating = "Good" if health.working_capital > 0 else "Poor"
            table.add_row("Working Capital", wc_formatted, wc_rating)
        
        # Overall Health Score
        health_rating = "Good" if health.score >= 70 else "Fair" if health.score >= 50 else "Poor"
        health_color = "green" if health.score >= 70 else "yellow" if health.score >= 50 else "red"
        table.add_row("", "", "")
        table.add_row("Health Score", f"{health.score:.1f}/100", f"[{health_color}]{health_rating}[/{health_color}]")
        
        return Panel(table, title="💊 Financial Health", border_style="magenta")
    
    def create_risk_analysis_panel(self, risk) -> Panel:
        """Create risk analysis panel"""
        table = Table(show_header=True, header_style="bold red")
        table.add_column("Metric", style="cyan", width=18)
        table.add_column("Value", justify="right", width=12)
        table.add_column("Rating", justify="center", width=8)
        
        # Beta
        if risk.beta is not None:
            beta_rating = "Low" if risk.beta < 0.8 else "Medium" if risk.beta < 1.2 else "High"
            table.add_row("Beta", f"{risk.beta:.2f}", beta_rating)
        
        # Sharpe Ratio
        if risk.sharpe_ratio is not None:
            sharpe_rating = "Excellent" if risk.sharpe_ratio > 1.0 else "Good" if risk.sharpe_ratio > 0.5 else "Poor"
            table.add_row("Sharpe Ratio", f"{risk.sharpe_ratio:.2f}", sharpe_rating)
        
        # Max Drawdown
        if risk.max_drawdown is not None:
            dd_rating = "Low" if risk.max_drawdown > -15 else "Medium" if risk.max_drawdown > -30 else "High"
            dd_color = "green" if risk.max_drawdown > -15 else "yellow" if risk.max_drawdown > -30 else "red"
            table.add_row("Max Drawdown", f"{risk.max_drawdown:.1f}%", f"[{dd_color}]{dd_rating}[/{dd_color}]")
        
        # Volatility
        if risk.volatility_30d is not None:
            vol_rating = "Low" if risk.volatility_30d < 20 else "Medium" if risk.volatility_30d < 35 else "High"
            table.add_row("30D Volatility", f"{risk.volatility_30d:.1f}%", vol_rating)
        
        # Overall Risk Score
        risk_rating = "Low" if risk.risk_score >= 70 else "Medium" if risk.risk_score >= 50 else "High"
        risk_color = "green" if risk.risk_score >= 70 else "yellow" if risk.risk_score >= 50 else "red"
        table.add_row("", "", "")
        table.add_row("Risk Score", f"{risk.risk_score:.1f}/100", f"[{risk_color}]{risk_rating}[/{risk_color}]")
        
        return Panel(table, title="⚠️ Risk Analysis", border_style="red")
    
    def create_valuation_panel(self, valuation) -> Panel:
        """Create valuation analysis panel"""
        table = Table(show_header=True, header_style="bold green")
        table.add_column("Metric", style="cyan", width=18)
        table.add_column("Value", justify="right", width=12)
        table.add_column("Rating", justify="center", width=8)
        
        # DCF Estimate
        if valuation.dcf_estimate is not None:
            table.add_row("DCF Estimate", f"${valuation.dcf_estimate:.2f}", "Model")
        
        # Graham Number
        if valuation.graham_number is not None:
            table.add_row("Graham Number", f"${valuation.graham_number:.2f}", "Value")
        
        # Price to FCF
        if valuation.price_to_fcf is not None:
            fcf_rating = "Good" if valuation.price_to_fcf < 15 else "Fair" if valuation.price_to_fcf < 25 else "Poor"
            table.add_row("Price/FCF", f"{valuation.price_to_fcf:.1f}", fcf_rating)
        
        # EV/Sales
        if valuation.ev_sales is not None:
            ev_rating = "Good" if valuation.ev_sales < 3 else "Fair" if valuation.ev_sales < 6 else "Poor"
            table.add_row("EV/Sales", f"{valuation.ev_sales:.1f}", ev_rating)
        
        # Overall Valuation Score
        val_rating = "Undervalued" if valuation.valuation_score >= 70 else "Fair Value" if valuation.valuation_score >= 50 else "Overvalued"
        val_color = "green" if valuation.valuation_score >= 70 else "yellow" if valuation.valuation_score >= 50 else "red"
        table.add_row("", "", "")
        table.add_row("Valuation Score", f"{valuation.valuation_score:.1f}/100", f"[{val_color}]{val_rating}[/{val_color}]")
        
        return Panel(table, title="💰 Valuation Analysis", border_style="green")
    
    def create_quality_panel(self, quality) -> Panel:
        """Create quality analysis panel"""
        table = Table(show_header=True, header_style="bold blue")
        table.add_column("Metric", style="cyan", width=18)
        table.add_column("Value", justify="right", width=12)
        table.add_column("Rating", justify="center", width=8)
        
        # Earnings Quality
        if quality.earnings_quality is not None:
            eq_rating = "High" if quality.earnings_quality >= 75 else "Medium" if quality.earnings_quality >= 50 else "Low"
            eq_color = "green" if quality.earnings_quality >= 75 else "yellow" if quality.earnings_quality >= 50 else "red"
            table.add_row("Earnings Quality", f"{quality.earnings_quality:.1f}%", f"[{eq_color}]{eq_rating}[/{eq_color}]")
        
        # Cash Flow to Earnings
        if quality.cash_flow_to_earnings is not None:
            cf_rating = "Good" if quality.cash_flow_to_earnings > 1.0 else "Fair" if quality.cash_flow_to_earnings > 0.8 else "Poor"
            table.add_row("CF/Earnings", f"{quality.cash_flow_to_earnings:.2f}", cf_rating)
        
        # Accruals Ratio
        if quality.accruals_ratio is not None:
            acc_rating = "Low" if abs(quality.accruals_ratio) < 0.2 else "High"
            acc_color = "green" if abs(quality.accruals_ratio) < 0.2 else "red"
            table.add_row("Accruals Ratio", f"{quality.accruals_ratio:.2f}", f"[{acc_color}]{acc_rating}[/{acc_color}]")
        
        # Red Flags
        if quality.accounting_red_flags:
            table.add_row("Red Flags", f"{len(quality.accounting_red_flags)}", "⚠️")
        
        # Overall Quality Score
        qual_rating = "High" if quality.score >= 75 else "Medium" if quality.score >= 50 else "Low"
        qual_color = "green" if quality.score >= 75 else "yellow" if quality.score >= 50 else "red"
        table.add_row("", "", "")
        table.add_row("Quality Score", f"{quality.score:.1f}/100", f"[{qual_color}]{qual_rating}[/{qual_color}]")
        
        return Panel(table, title="📊 Quality Analysis", border_style="blue")
    
    def show_watchlist(self):
        """Display current watchlist"""
        if not self.watchlist:
            self.console.print("\n[yellow]Your watchlist is empty[/yellow]")
            return
        
        self.console.print(f"\n[bold cyan]Your Watchlist ({len(self.watchlist)} stocks):[/bold cyan]")
        for i, symbol in enumerate(self.watchlist, 1):
            self.console.print(f"  {i}. {symbol}")
        
        # Option to analyze from watchlist
        choice = Prompt.ask("\nEnter number to analyze, or press Enter to continue", default="")
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.watchlist):
                symbol = self.watchlist[idx]
                self.console.print(f"\nAnalyzing {symbol} from watchlist...")
                self.analyze_stock(symbol)
    
    def format_number(self, num):
        """Format large numbers with appropriate suffixes"""
        if num >= 1e12:
            return f"${num/1e12:.2f}T"
        elif num >= 1e9:
            return f"${num/1e9:.2f}B"
        elif num >= 1e6:
            return f"${num/1e6:.2f}M"
        else:
            return f"${num:,.0f}"
    
    def run(self):
        """Main application loop"""
        self.show_banner()
        self.show_stock_suggestions()
        
        while True:
            try:
                symbol = self.get_stock_input()
                
                if symbol is None:  # User wants to quit
                    self.console.print("\n[cyan]Thank you for using Financial Research Agent![/cyan]")
                    break
                
                # Get analysis mode
                mode = self.get_analysis_mode(symbol)
                
                # Perform analysis based on mode
                if mode == "comprehensive":
                    success = self.perform_comprehensive_analysis(symbol)
                else:
                    success = self.analyze_stock(symbol)
                
                if success:
                    # Ask if user wants to analyze another stock
                    self.console.print()
                    continue_analysis = Confirm.ask("Analyze another stock?", default=True)
                    if not continue_analysis:
                        self.console.print("\n[cyan]Thank you for using Financial Research Agent![/cyan]")
                        break
                else:
                    # On error, ask if they want to try again
                    retry = Confirm.ask("Try analyzing another stock?", default=True)
                    if not retry:
                        break
            
            except KeyboardInterrupt:
                self.console.print("\n\n[yellow]Exiting...[/yellow]")
                break
            except Exception as e:
                self.console.print(f"\n[red]Unexpected error: {str(e)}[/red]")
                retry = Confirm.ask("Continue using the application?", default=True)
                if not retry:
                    break


@click.command()
@click.option('--symbol', '-s', help='Stock symbol to analyze directly')
@click.option('--comprehensive', '-c', is_flag=True, help='Use comprehensive analysis mode')
def main(symbol, comprehensive):
    """Financial Research Agent - Rich CLI Version"""
    agent = FinancialAgentRich()
    
    if symbol:
        # Direct analysis mode
        agent.show_banner()
        agent.console.print(f"\nAnalyzing {symbol.upper()}...")
        if comprehensive:
            agent.perform_comprehensive_analysis(symbol.upper())
        else:
            agent.analyze_stock(symbol.upper())
    else:
        # Interactive mode
        agent.run()


if __name__ == "__main__":
    main()