"""
Textual-based Financial Research Agent - Interactive TUI
"""
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, Grid
from textual.widgets import (
    Header, Footer, Input, Button, Static, 
    RichLog, ProgressBar, DataTable, TabbedContent, TabPane
)
from textual.reactive import reactive
from textual.binding import Binding
from textual.message import Message
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.align import Align

from finance_core import FinancialAnalyzer, StockData, FundamentalMetrics, TechnicalMetrics, SentimentMetrics, Recommendation
from comprehensive_analyzer import ComprehensiveAnalyzer, ComprehensiveAnalysis
from chart_widget import StockChart, ChartControls


class FinancialAgentTUI(App):
    """Textual TUI for Financial Research Agent"""
    
    CSS = """
    #input-container {
        dock: bottom;
        height: 5;
        background: $surface;
        padding: 1;
    }
    
    #ticker-input {
        width: 50%;
        margin-right: 1;
    }
    
    #standard-button {
        width: 20%;
        min-width: 10;
        margin-right: 1;
    }
    
    #comprehensive-button {
        width: 25%;
        min-width: 12;
    }
    
    #main-content {
        height: 1fr;
    }
    
    #sidebar {
        dock: left;
        width: 25;
        background: $surface;
        border-right: solid $primary;
        padding: 1;
    }
    
    #content-area {
        height: 1fr;
        padding: 1;
    }
    
    .metric-high {
        color: $success;
    }
    
    .metric-medium {
        color: $warning;
    }
    
    .metric-low {
        color: $error;
    }
    
    .recommendation-buy {
        color: $success;
        text-style: bold;
    }
    
    .recommendation-sell {
        color: $error;
        text-style: bold;
    }
    
    .recommendation-hold {
        color: $warning;
        text-style: bold;
    }
    
    #status-bar {
        dock: top;
        height: 3;
        background: $primary;
        padding: 1;
    }
    
    DataTable {
        height: 1fr;
    }
    """
    
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit"),
        Binding("ctrl+c", "clear", "Clear"),
        Binding("ctrl+r", "refresh", "Refresh"),
        Binding("enter", "analyze", "Analyze", show=False),
        Binding("1,2,3,4,5,6,7", "change_chart_period", "Chart Period", show=False),
    ]
    
    # Reactive properties
    current_symbol = reactive("")
    is_analyzing = reactive(False)
    analysis_complete = reactive(False)
    
    def __init__(self):
        super().__init__()
        self.analyzer = FinancialAnalyzer()
        self.comprehensive_analyzer = ComprehensiveAnalyzer()
        self.title = "Financial Research Agent (Textual)"
        self.sub_title = "Advanced Stock Analysis TUI"
        
        # Store analysis results
        self.stock_data: StockData = None
        self.analysis_mode = "standard"  # or "comprehensive"
        self.fundamentals: FundamentalMetrics = None
        self.technicals: TechnicalMetrics = None
        self.sentiment: SentimentMetrics = None
        self.recommendation: Recommendation = None
        self.comprehensive_analysis: ComprehensiveAnalysis = None
        
        # Chart-related properties
        self.current_chart_period = "1mo"
        self.historical_data = None
    
    def compose(self) -> ComposeResult:
        """Create the TUI layout"""
        yield Header(show_clock=True)
        
        # Status bar
        with Container(id="status-bar"):
            yield Static("Ready - Enter a stock ticker to analyze", id="status")
        
        with Container(id="main-content"):
            with Horizontal():
                # Sidebar
                with Vertical(id="sidebar"):
                    yield Static("Quick Info", classes="metric-high")
                    yield Static("No stock selected", id="quick-info")
                    yield Static("")
                    yield Static("Analysis Progress", classes="metric-high")
                    yield ProgressBar(total=100, show_eta=False, id="progress")
                    yield Static("")
                    yield Static("Recent Analyses", classes="metric-high")
                    yield Static("None", id="recent-list")
                
                # Main content area
                with Vertical(id="content-area"):
                    with TabbedContent():
                        with TabPane("Overview", id="overview-tab"):
                            yield Static("Enter a stock ticker below to begin analysis", id="overview-content")
                        
                        with TabPane("Fundamentals", id="fundamentals-tab"):
                            yield DataTable(id="fundamentals-table")
                        
                        with TabPane("Technical", id="technical-tab"):
                            yield DataTable(id="technical-table")
                        
                        with TabPane("Sentiment", id="sentiment-tab"):
                            yield DataTable(id="sentiment-table")
                        
                        with TabPane("Charts", id="charts-tab"):
                            with Vertical():
                                yield ChartControls(id="chart-controls")
                                yield StockChart(id="stock-chart")
                        
                        with TabPane("Comprehensive", id="comprehensive-tab"):
                            yield Static("Use comprehensive analysis mode to view advanced metrics", id="comprehensive-content")
                        
                        with TabPane("Recommendation", id="recommendation-tab"):
                            yield Static("Analysis required", id="recommendation-content")
        
        # Input area
        with Container(id="input-container"):
            with Horizontal():
                yield Input(
                    placeholder="Enter stock ticker (e.g., AAPL, TSLA, MSFT)",
                    id="ticker-input"
                )
                yield Button("📈 Standard", variant="default", id="standard-button")
                yield Button("🔬 Comprehensive", variant="primary", id="comprehensive-button")
        
        yield Footer()
    
    def on_mount(self) -> None:
        """Initialize the app when mounted"""
        self.setup_tables()
        self.update_status("Ready - Enter a stock ticker to analyze")
    
    def setup_tables(self) -> None:
        """Setup data tables"""
        # Fundamentals table
        fund_table = self.query_one("#fundamentals-table", DataTable)
        fund_table.add_columns("Metric", "Value", "Rating")
        
        # Technical table
        tech_table = self.query_one("#technical-table", DataTable)
        tech_table.add_columns("Indicator", "Value", "Signal")
        
        # Sentiment table
        sent_table = self.query_one("#sentiment-table", DataTable)
        sent_table.add_columns("Source", "Rating", "Score")
    
    def update_status(self, message: str) -> None:
        """Update status bar message"""
        status_widget = self.query_one("#status", Static)
        status_widget.update(message)
    
    def update_progress(self, progress_value: int) -> None:
        """Update progress bar"""
        progress = self.query_one("#progress", ProgressBar)
        progress.update(progress=progress_value)
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle input submission"""
        if event.input.id == "ticker-input":
            self.analysis_mode = "standard"  # Default to standard analysis on Enter
            self.analyze_stock()
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Handle button presses"""
        if event.button.id == "standard-button":
            self.analysis_mode = "standard"
            self.analyze_stock()
        elif event.button.id == "comprehensive-button":
            self.analysis_mode = "comprehensive"
            self.analyze_stock()
    
    def analyze_stock(self) -> None:
        """Start stock analysis"""
        ticker_input = self.query_one("#ticker-input", Input)
        symbol = ticker_input.value.strip().upper()
        
        if not symbol:
            self.update_status("Please enter a stock ticker")
            return
        
        if self.is_analyzing:
            self.update_status("Analysis already in progress...")
            return
        
        self.current_symbol = symbol
        self.is_analyzing = True
        self.analysis_complete = False
        
        # Clear previous results
        self.clear_results()
        
        # Start analysis in background
        self.run_worker(self.perform_analysis, exclusive=True, thread=True)
        
        # Clear input
        ticker_input.value = ""
    
    def perform_analysis(self) -> None:
        """Perform the stock analysis (runs in background thread)"""
        try:
            # Fetch basic stock data
            mode_label = "Comprehensive" if self.analysis_mode == "comprehensive" else "Standard"
            self.call_from_thread(self.update_status, f"{mode_label} Analysis: {self.current_symbol}...")
            self.call_from_thread(self.update_progress, 10)
            
            self.call_from_thread(self.update_status, f"Fetching stock data for {self.current_symbol}...")
            self.stock_data = self.analyzer.get_stock_data(self.current_symbol)
            self.call_from_thread(self.update_progress, 25)
            
            # Fundamental analysis
            self.call_from_thread(self.update_status, f"Performing fundamental analysis...")
            self.fundamentals = self.analyzer.analyze_fundamentals(self.current_symbol)
            self.call_from_thread(self.update_progress, 45)
            
            # Technical analysis
            self.call_from_thread(self.update_status, f"Performing technical analysis...")
            self.technicals = self.analyzer.analyze_technicals(self.current_symbol)
            self.call_from_thread(self.update_progress, 65)
            
            # Sentiment analysis
            self.call_from_thread(self.update_status, f"Analyzing market sentiment...")
            self.sentiment = self.analyzer.analyze_sentiment(self.current_symbol)
            self.call_from_thread(self.update_progress, 70)
            
            # Fetch historical data for charts
            self.call_from_thread(self.update_status, f"Fetching historical price data...")
            self.historical_data = self.analyzer.get_historical_data(self.current_symbol, self.current_chart_period)
            self.call_from_thread(self.update_progress, 80)
            
            # Comprehensive analysis if requested
            if self.analysis_mode == "comprehensive":
                self.call_from_thread(self.update_status, f"Advanced comprehensive analysis...")
                self.comprehensive_analysis = self.comprehensive_analyzer.perform_comprehensive_analysis(self.current_symbol)
                self.call_from_thread(self.update_progress, 95)
            else:
                self.comprehensive_analysis = None
            
            # Generate recommendation
            self.call_from_thread(self.update_status, f"Generating recommendation...")
            self.recommendation = self.analyzer.generate_recommendation(
                self.current_symbol, self.fundamentals, self.technicals, self.sentiment
            )
            self.call_from_thread(self.update_progress, 100)
            
            # Update UI
            self.call_from_thread(self.display_results)
            
        except Exception as e:
            self.call_from_thread(self.handle_error, str(e))
    
    def display_results(self) -> None:
        """Display analysis results in the UI"""
        if not all([self.stock_data, self.fundamentals, self.technicals, 
                   self.sentiment, self.recommendation]):
            return
        
        self.update_overview()
        self.update_fundamentals_table()
        self.update_technical_table()
        self.update_sentiment_table()
        self.update_chart()
        if self.comprehensive_analysis:
            self.update_comprehensive_tab()
        self.update_recommendation()
        self.update_sidebar()
        
        self.is_analyzing = False
        self.analysis_complete = True
        self.update_status(f"Analysis complete for {self.stock_data.symbol}")
    
    def update_overview(self) -> None:
        """Update overview tab content"""
        overview = self.query_one("#overview-content", Static)
        
        # Create rich panel with stock overview
        table = Table.grid(padding=1)
        table.add_column(justify="left")
        table.add_column(justify="right")
        
        change_color = "green" if self.stock_data.change_percent >= 0 else "red"
        change_text = f"+{self.stock_data.change_percent:.2f}%" if self.stock_data.change_percent >= 0 else f"{self.stock_data.change_percent:.2f}%"
        
        table.add_row("Company:", self.stock_data.name)
        table.add_row("Symbol:", self.stock_data.symbol)
        table.add_row("Current Price:", f"${self.stock_data.current_price}")
        table.add_row("Change:", f"[{change_color}]{change_text}[/{change_color}]")
        table.add_row("")
        table.add_row("Recommendation:", f"[bold]{self.recommendation.action}[/bold]")
        table.add_row("Confidence:", f"{self.recommendation.confidence}%")
        table.add_row("Risk Level:", self.recommendation.risk_level)
        
        if self.recommendation.price_target:
            table.add_row("Price Target:", f"${self.recommendation.price_target}")
            upside = ((self.recommendation.price_target - self.stock_data.current_price) / self.stock_data.current_price) * 100
            upside_color = "green" if upside >= 0 else "red"
            table.add_row("Upside/Downside:", f"[{upside_color}]{upside:+.1f}%[/{upside_color}]")
        
        panel = Panel(table, title=f"{self.stock_data.symbol} Overview", border_style="blue")
        overview.update(panel)
    
    def update_fundamentals_table(self) -> None:
        """Update fundamentals data table"""
        table = self.query_one("#fundamentals-table", DataTable)
        table.clear()
        
        def get_rating(value, good_threshold, bad_threshold, higher_better=True):
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
        
        fundamentals_data = [
            ("P/E Ratio", f"{self.fundamentals.pe_ratio:.2f}" if self.fundamentals.pe_ratio else "N/A",
             get_rating(self.fundamentals.pe_ratio, 25, 40, False)),
            ("ROE", f"{self.fundamentals.roe:.1f}%" if self.fundamentals.roe else "N/A",
             get_rating(self.fundamentals.roe, 15, 5)),
            ("Profit Margin", f"{self.fundamentals.profit_margin:.1f}%" if self.fundamentals.profit_margin else "N/A",
             get_rating(self.fundamentals.profit_margin, 10, 2)),
            ("Debt/Equity", f"{self.fundamentals.debt_to_equity:.2f}" if self.fundamentals.debt_to_equity else "N/A",
             get_rating(self.fundamentals.debt_to_equity, 0.5, 1.0, False)),
            ("Current Ratio", f"{self.fundamentals.current_ratio:.2f}" if self.fundamentals.current_ratio else "N/A",
             get_rating(self.fundamentals.current_ratio, 1.5, 1.0)),
            ("Revenue Growth", f"{self.fundamentals.revenue_growth:.1f}%" if self.fundamentals.revenue_growth else "N/A",
             get_rating(self.fundamentals.revenue_growth, 10, 0)),
            ("Overall Score", f"{self.fundamentals.score:.1f}/100", 
             "Good" if self.fundamentals.score >= 70 else "Fair" if self.fundamentals.score >= 50 else "Poor")
        ]
        
        for metric, value, rating in fundamentals_data:
            table.add_row(metric, value, rating)
    
    def update_technical_table(self) -> None:
        """Update technical analysis data table"""
        table = self.query_one("#technical-table", DataTable)
        table.clear()
        
        def get_rsi_signal(rsi):
            if rsi is None:
                return "N/A"
            if rsi < 30:
                return "Oversold"
            elif rsi > 70:
                return "Overbought"
            else:
                return "Neutral"
        
        def get_macd_signal(macd, signal):
            if macd is None or signal is None:
                return "N/A"
            return "Bullish" if macd > signal else "Bearish"
        
        technical_data = [
            ("RSI (14)", f"{self.technicals.rsi:.1f}" if self.technicals.rsi else "N/A",
             get_rsi_signal(self.technicals.rsi)),
            ("MACD", f"{self.technicals.macd:.4f}" if self.technicals.macd else "N/A",
             get_macd_signal(self.technicals.macd, self.technicals.macd_signal)),
            ("SMA 20", f"${self.technicals.sma_20:.2f}" if self.technicals.sma_20 else "N/A", 
             "Above" if self.stock_data.current_price > (self.technicals.sma_20 or 0) else "Below"),
            ("SMA 50", f"${self.technicals.sma_50:.2f}" if self.technicals.sma_50 else "N/A",
             "Above" if self.stock_data.current_price > (self.technicals.sma_50 or 0) else "Below"),
            ("Trend", self.technicals.trend, self.technicals.trend),
            ("Support", f"${self.technicals.support_level:.2f}" if self.technicals.support_level else "N/A", ""),
            ("Resistance", f"${self.technicals.resistance_level:.2f}" if self.technicals.resistance_level else "N/A", ""),
            ("Overall Score", f"{self.technicals.score:.1f}/100",
             "Good" if self.technicals.score >= 70 else "Fair" if self.technicals.score >= 50 else "Poor")
        ]
        
        for indicator, value, signal in technical_data:
            table.add_row(indicator, value, signal)
    
    def update_sentiment_table(self) -> None:
        """Update sentiment analysis data table"""
        table = self.query_one("#sentiment-table", DataTable)
        table.clear()
        
        sentiment_data = [
            ("Analyst Rating", self.sentiment.analyst_rating or "N/A", 
             f"{self.sentiment.analyst_score}/100" if self.sentiment.analyst_score else "N/A"),
            ("Analyst Count", f"{self.sentiment.analyst_count}" if self.sentiment.analyst_count else "N/A", "")
        ]
        
        # Add news sentiment if available
        if self.sentiment.news_sentiment is not None:
            sentiment_data.append(("News Sentiment", f"{self.sentiment.news_sentiment:.1f}/100", 
                                 f"{self.sentiment.news_article_count} articles"))
        else:
            sentiment_data.append(("News Sentiment", "No API key", "N/A"))
        
        # Add social sentiment if available
        if self.sentiment.social_sentiment is not None:
            sentiment_data.append(("Social Media", f"{self.sentiment.social_sentiment:.1f}/100", 
                                 f"{self.sentiment.social_post_count} posts"))
        else:
            sentiment_data.append(("Social Media", "No API key", "N/A"))
        
        # Overall score with confidence
        confidence_text = f" ({self.sentiment.confidence:.0f}%)" if self.sentiment.confidence > 0 else ""
        sentiment_data.append(("Overall Score", f"{self.sentiment.score:.1f}/100{confidence_text}",
                              "Good" if self.sentiment.score >= 70 else "Fair" if self.sentiment.score >= 50 else "Poor"))
        
        for source, rating, score in sentiment_data:
            table.add_row(source, rating, score)
    
    def update_chart(self) -> None:
        """Update stock chart with current data"""
        if self.historical_data is not None and self.stock_data is not None:
            try:
                chart = self.query_one("#stock-chart", StockChart)
                chart.update_data(self.stock_data.symbol, self.historical_data, self.current_chart_period)
                
                controls = self.query_one("#chart-controls", ChartControls)
                controls.update_period(self.current_chart_period)
            except Exception as e:
                # Log error for debugging but don't break the app
                self.update_status(f"Chart update error: {str(e)}")
    
    def update_comprehensive_tab(self) -> None:
        """Update comprehensive analysis tab content"""
        comp_content = self.query_one("#comprehensive-content", Static)
        
        if not self.comprehensive_analysis:
            comp_content.update("No comprehensive analysis available")
            return
        
        # Create comprehensive summary table
        table = Table.grid(padding=1)
        table.add_column(justify="left")
        table.add_column(justify="right")
        
        analysis = self.comprehensive_analysis
        
        # Composite Score
        score_color = "green" if analysis.composite_score >= 70 else "yellow" if analysis.composite_score >= 50 else "red"
        table.add_row("Composite Score:", f"[{score_color}]{analysis.composite_score:.1f}/100[/{score_color}]")
        table.add_row("Analysis Confidence:", f"{analysis.confidence_level:.1%}")
        table.add_row("", "")
        
        # Financial Health
        if analysis.financial_health.score > 0:
            health_color = "green" if analysis.financial_health.score >= 70 else "yellow" if analysis.financial_health.score >= 50 else "red"
            table.add_row("Financial Health:", f"[{health_color}]{analysis.financial_health.score:.1f}/100[/{health_color}]")
            
            if analysis.financial_health.piotroski_score is not None:
                table.add_row("Piotroski Score:", f"{analysis.financial_health.piotroski_score}/9")
            
            if analysis.financial_health.altman_z_score is not None:
                z_score = analysis.financial_health.altman_z_score
                if z_score > 3.0:
                    z_color, z_label = "green", "Safe"
                elif z_score > 1.8:
                    z_color, z_label = "yellow", "Gray Zone"
                else:
                    z_color, z_label = "red", "Distress"
                table.add_row("Altman Z-Score:", f"[{z_color}]{z_score:.2f} ({z_label})[/{z_color}]")
        
        table.add_row("", "")
        
        # Risk Analysis
        if analysis.risk_metrics.risk_score > 0:
            risk_color = "green" if analysis.risk_metrics.risk_score >= 70 else "yellow" if analysis.risk_metrics.risk_score >= 50 else "red" 
            table.add_row("Risk Score:", f"[{risk_color}]{analysis.risk_metrics.risk_score:.1f}/100[/{risk_color}]")
            
            if analysis.risk_metrics.max_drawdown:
                dd_color = "green" if analysis.risk_metrics.max_drawdown > -15 else "yellow" if analysis.risk_metrics.max_drawdown > -30 else "red"
                table.add_row("Max Drawdown:", f"[{dd_color}]{analysis.risk_metrics.max_drawdown:.1f}%[/{dd_color}]")
                
            if analysis.risk_metrics.sharpe_ratio:
                table.add_row("Sharpe Ratio:", f"{analysis.risk_metrics.sharpe_ratio:.2f}")
        
        table.add_row("", "")
        
        # Valuation
        if analysis.valuation_metrics.valuation_score > 0:
            val_color = "green" if analysis.valuation_metrics.valuation_score >= 70 else "yellow" if analysis.valuation_metrics.valuation_score >= 50 else "red"
            table.add_row("Valuation Score:", f"[{val_color}]{analysis.valuation_metrics.valuation_score:.1f}/100[/{val_color}]")
            
            if analysis.valuation_metrics.dcf_estimate:
                table.add_row("DCF Estimate:", f"${analysis.valuation_metrics.dcf_estimate:.2f}")
                
        table.add_row("", "")
        
        # Key Insights
        if analysis.key_insights:
            table.add_row("Key Insights:", "")
            for insight in analysis.key_insights[:3]:  # Show top 3
                table.add_row("", f"• {insight}")
        
        # Warnings
        if analysis.warnings:
            table.add_row("", "")
            table.add_row("[red]Warnings:[/red]", "")
            for warning in analysis.warnings[:2]:  # Show top 2
                table.add_row("", f"[red]{warning}[/red]")
        
        panel = Panel(table, title="🔬 Comprehensive Analysis", border_style="magenta")
        comp_content.update(panel)
    
    def update_recommendation(self) -> None:
        """Update recommendation tab content"""
        rec_content = self.query_one("#recommendation-content", Static)
        
        # Create recommendation panel
        table = Table.grid(padding=1)
        table.add_column(justify="left")
        table.add_column(justify="right")
        
        action_color = {
            "STRONG_BUY": "bright_green",
            "BUY": "green",
            "HOLD": "yellow",
            "SELL": "red",
            "STRONG_SELL": "bright_red"
        }.get(self.recommendation.action, "white")
        
        table.add_row("Recommendation:", f"[{action_color}]{self.recommendation.action}[/{action_color}]")
        table.add_row("Confidence Level:", f"{self.recommendation.confidence}%")
        table.add_row("Overall Score:", f"{self.recommendation.overall_score}/100")
        table.add_row("Risk Level:", self.recommendation.risk_level)
        
        if self.recommendation.price_target:
            table.add_row("Price Target:", f"${self.recommendation.price_target}")
        
        table.add_row("", "")
        table.add_row("Key Points:", "")
        
        if self.recommendation.reasoning:
            for reason in self.recommendation.reasoning:
                table.add_row("", f"• {reason}")
        
        panel = Panel(table, title="Investment Recommendation", border_style=action_color)
        rec_content.update(panel)
    
    def update_sidebar(self) -> None:
        """Update sidebar with quick info"""
        quick_info = self.query_one("#quick-info", Static)
        
        info_text = f"""Symbol: {self.stock_data.symbol}
Price: ${self.stock_data.current_price}
Change: {self.stock_data.change_percent:+.2f}%
Rec: {self.recommendation.action}"""
        
        quick_info.update(info_text)
        
        # Reset progress bar
        progress = self.query_one("#progress", ProgressBar)
        progress.update(progress=0)
    
    def clear_results(self) -> None:
        """Clear previous analysis results"""
        overview = self.query_one("#overview-content", Static)
        overview.update("Analyzing...")
        
        rec_content = self.query_one("#recommendation-content", Static)
        rec_content.update("Analysis in progress...")
        
        # Clear tables
        for table_id in ["#fundamentals-table", "#technical-table", "#sentiment-table"]:
            table = self.query_one(table_id, DataTable)
            table.clear()
    
    def handle_error(self, error_msg: str) -> None:
        """Handle analysis errors"""
        self.is_analyzing = False
        self.update_status(f"Error: {error_msg}")
        
        overview = self.query_one("#overview-content", Static)
        overview.update(f"[red]Error analyzing {self.current_symbol}: {error_msg}[/red]")
        
        progress = self.query_one("#progress", ProgressBar)
        progress.update(progress=0)
    
    def action_clear(self) -> None:
        """Clear current analysis"""
        self.clear_results()
        self.current_symbol = ""
        self.is_analyzing = False
        self.analysis_complete = False
        self.update_status("Ready - Enter a stock ticker to analyze")
    
    def action_refresh(self) -> None:
        """Refresh current analysis"""
        if self.current_symbol and not self.is_analyzing:
            self.analyze_stock()
    
    def action_analyze(self) -> None:
        """Analyze action"""
        self.analyze_stock()
    
    def on_key(self, event) -> None:
        """Handle key presses for chart period changes"""
        if event.key in ['1', '2', '3', '4', '5', '6', '7']:
            periods = ["1d", "5d", "1mo", "3mo", "6mo", "1y", "2y"]
            period_index = int(event.key) - 1
            
            if 0 <= period_index < len(periods):
                new_period = periods[period_index]
                if new_period != self.current_chart_period:
                    self.current_chart_period = new_period
                    self.refresh_chart_data()
    
    def refresh_chart_data(self) -> None:
        """Refresh chart with new time period"""
        if self.stock_data and not self.is_analyzing:
            self.run_worker(self.update_chart_period, exclusive=True, thread=True)
    
    def update_chart_period(self) -> None:
        """Update chart period in background thread"""
        try:
            self.call_from_thread(self.update_status, f"Updating chart for {self.current_chart_period}...")
            
            # Fetch new historical data
            self.historical_data = self.analyzer.get_historical_data(self.current_symbol, self.current_chart_period)
            
            # Update chart on main thread
            self.call_from_thread(self.update_chart)
            self.call_from_thread(self.update_status, f"Chart updated to {self.current_chart_period}")
        except Exception as e:
            self.call_from_thread(self.update_status, f"Error updating chart: {str(e)}")


def main():
    """Run the Textual Financial Agent"""
    app = FinancialAgentTUI()
    app.run()


if __name__ == "__main__":
    main()