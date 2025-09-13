"""
Custom chart widget for stock price visualization in Textual TUI
"""
from textual.widgets import Static
from textual.reactive import reactive
from rich.text import Text
from rich.panel import Panel
from typing import List, Tuple, Optional
import pandas as pd
from datetime import datetime
import math


class StockChart(Static):
    """ASCII-based stock price chart widget"""
    
    # Reactive properties - avoid DataFrame in reactive to prevent comparison issues
    period = reactive("1mo")  # Time period
    chart_height = reactive(20)  # Height of chart in lines
    chart_width = reactive(60)  # Width of chart in characters
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.symbol = ""
        self.data = None  # Store DataFrame as regular attribute
        
    def on_mount(self):
        """Initialize the chart display when mounted"""
        self.update("📈 Stock chart will appear here after analysis...")
        
    def update_data(self, symbol: str, historical_data: pd.DataFrame, period: str):
        """Update chart with new data"""
        self.symbol = symbol
        self.data = historical_data
        self.period = period
        self.render_chart()
    
    def render_chart(self):
        """Render the ASCII stock chart"""
        if self.data is None or self.data.empty:
            self.update("No chart data available")
            return
            
        try:
            chart_text = self.create_ascii_chart()
            panel = Panel(
                chart_text,
                title=f"{self.symbol} - {self.get_period_label()}",
                border_style="green" if self.is_price_up() else "red"
            )
            self.update(panel)
        except Exception as e:
            self.update(f"Chart error: {str(e)}")
    
    def get_period_label(self) -> str:
        """Get human-readable period label"""
        period_labels = {
            "1d": "1 Day",
            "5d": "5 Days", 
            "1mo": "1 Month",
            "3mo": "3 Months",
            "6mo": "6 Months",
            "1y": "1 Year",
            "2y": "2 Years"
        }
        return period_labels.get(self.period, self.period)
    
    def is_price_up(self) -> bool:
        """Check if price is up from first to last"""
        if self.data is None or len(self.data) < 2:
            return True
        return self.data['Close'].iloc[-1] > self.data['Close'].iloc[0]
    
    def create_ascii_chart(self) -> Text:
        """Create ASCII line chart from stock data"""
        if self.data is None or len(self.data) < 2:
            return Text("Insufficient data for chart")
        
        prices = self.data['Close'].tolist()
        dates = self.data['Date'].tolist()
        
        # Normalize prices to chart height
        min_price = min(prices)
        max_price = max(prices)
        price_range = max_price - min_price
        
        if price_range == 0:
            return Text("Price unchanged - no chart to display")
        
        # Create the chart grid
        chart_lines = []
        height = self.chart_height
        width = min(self.chart_width, len(prices))
        
        # Sample data points if we have more data than width
        if len(prices) > width:
            step = len(prices) // width
            prices = prices[::step][:width]
            dates = dates[::step][:width]
        
        # Calculate price levels for each column
        normalized_prices = []
        for price in prices:
            level = int(((price - min_price) / price_range) * (height - 1))
            normalized_prices.append(level)
        
        # Create the chart matrix
        chart_matrix = [[' ' for _ in range(width)] for _ in range(height)]
        
        # Plot the line chart
        for i, level in enumerate(normalized_prices):
            chart_matrix[height - 1 - level][i] = '•'
            
            # Connect points with lines
            if i > 0:
                prev_level = normalized_prices[i-1]
                start_y = height - 1 - prev_level
                end_y = height - 1 - level
                
                # Draw vertical line between points
                min_y = min(start_y, end_y)
                max_y = max(start_y, end_y)
                for y in range(min_y, max_y + 1):
                    if chart_matrix[y][i] == ' ':
                        chart_matrix[y][i] = '│' if abs(start_y - end_y) > 1 else '•'
        
        # Add price labels on the right
        price_labels = []
        for i in range(0, height, max(1, height // 5)):
            price = min_price + ((height - 1 - i) / (height - 1)) * price_range
            price_labels.append(f"${price:.2f}")
        
        # Convert matrix to text with colors
        text = Text()
        
        # Add chart title with price info
        first_price = prices[0]
        last_price = prices[-1]
        change = last_price - first_price
        change_pct = (change / first_price) * 100
        
        color = "green" if change >= 0 else "red"
        change_symbol = "+" if change >= 0 else ""
        
        title_text = f"Price: ${last_price:.2f} ({change_symbol}{change:.2f}, {change_pct:+.1f}%)\n"
        text.append(title_text, style=f"bold {color}")
        text.append("\n")
        
        # Add price scale on the left
        label_idx = 0
        for i, row in enumerate(chart_matrix):
            # Add price label every few rows
            if i % max(1, height // 5) == 0 and label_idx < len(price_labels):
                text.append(f"{price_labels[label_idx]:>8} ", style="dim")
                label_idx += 1
            else:
                text.append("         ", style="dim")
            
            # Add chart data
            for j, char in enumerate(row):
                if char == '•':
                    text.append(char, style=f"bold {color}")
                elif char == '│':
                    text.append(char, style=color)
                else:
                    text.append(char)
            text.append("\n")
        
        # Add time axis
        text.append("         ")  # Padding for price labels
        for i in range(0, width, max(1, width // 5)):
            if i < len(dates):
                date_str = dates[i].strftime("%m/%d") if hasattr(dates[i], 'strftime') else str(dates[i])[:5]
                text.append(f"{date_str:<12}", style="dim")
        
        return text


class ChartControls(Static):
    """Chart control buttons and period selector"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.current_period = "1mo"
        
    def on_mount(self):
        """Initialize the controls display"""
        self.update_display()
        
    def update_display(self):
        """Update the controls display"""
        controls_text = Text()
        
        periods = [
            ("1d", "1 Day"),
            ("5d", "5 Days"), 
            ("1mo", "1 Month"),
            ("3mo", "3 Months"),
            ("6mo", "6 Months"),
            ("1y", "1 Year"),
            ("2y", "2 Years")
        ]
        
        controls_text.append("Time Period: ", style="bold")
        
        for i, (period_key, period_label) in enumerate(periods):
            style = "bold green" if period_key == self.current_period else "dim"
            controls_text.append(f"[{i+1}] {period_label}  ", style=style)
        
        controls_text.append("\nPress 1-7 to change time period")
        
        panel = Panel(controls_text, title="Chart Controls", border_style="blue")
        self.update(panel)
        
    def update_period(self, period: str):
        """Update current period and refresh display"""
        self.current_period = period
        self.update_display()