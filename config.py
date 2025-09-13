"""
Configuration management for Financial Research Agents
"""
import os
import json
from pathlib import Path
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional


@dataclass
class AnalysisWeights:
    """Weights for different analysis components"""
    fundamental: float = 0.5
    technical: float = 0.3
    sentiment: float = 0.2


@dataclass
class FundamentalWeights:
    """Weights for fundamental analysis metrics"""
    pe_ratio: float = 0.15
    roe: float = 0.20
    debt_to_equity: float = 0.15
    revenue_growth: float = 0.15
    profit_margin: float = 0.15
    current_ratio: float = 0.10
    pb_ratio: float = 0.10


@dataclass
class TechnicalWeights:
    """Weights for technical analysis indicators"""
    trend: float = 0.30
    rsi: float = 0.20
    macd: float = 0.25
    moving_averages: float = 0.25


@dataclass
class RecommendationThresholds:
    """Thresholds for buy/sell/hold recommendations"""
    strong_buy: float = 80.0
    buy: float = 65.0
    hold_upper: float = 64.9
    hold_lower: float = 35.0
    sell: float = 20.0
    strong_sell: float = 0.0


@dataclass
class DisplaySettings:
    """Display and UI settings"""
    show_progress: bool = True
    use_colors: bool = True
    decimal_places: int = 2
    currency_symbol: str = "$"
    percentage_format: str = "{:.1f}%"


@dataclass
class APISettings:
    """API configuration settings"""
    request_timeout: int = 30
    retry_attempts: int = 3
    retry_delay: float = 1.0
    cache_duration: int = 300  # seconds
    rate_limit_delay: float = 0.1


@dataclass
class FinancialAgentConfig:
    """Main configuration class"""
    analysis_weights: AnalysisWeights
    fundamental_weights: FundamentalWeights
    technical_weights: TechnicalWeights
    recommendation_thresholds: RecommendationThresholds
    display_settings: DisplaySettings
    api_settings: APISettings
    watchlist: List[str]
    recent_analyses: List[str]
    
    @classmethod
    def default(cls) -> 'FinancialAgentConfig':
        """Create default configuration"""
        return cls(
            analysis_weights=AnalysisWeights(),
            fundamental_weights=FundamentalWeights(),
            technical_weights=TechnicalWeights(),
            recommendation_thresholds=RecommendationThresholds(),
            display_settings=DisplaySettings(),
            api_settings=APISettings(),
            watchlist=[],
            recent_analyses=[]
        )


class ConfigManager:
    """Configuration file manager"""
    
    def __init__(self, config_dir: Optional[str] = None):
        if config_dir is None:
            self.config_dir = Path.home() / '.financial_agent'
        else:
            self.config_dir = Path(config_dir)
        
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir / 'config.json'
        self.cache_dir = self.config_dir / 'cache'
        self.cache_dir.mkdir(exist_ok=True)
        
        self._config: Optional[FinancialAgentConfig] = None
    
    def load_config(self) -> FinancialAgentConfig:
        """Load configuration from file or create default"""
        if self._config is not None:
            return self._config
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    data = json.load(f)
                
                # Convert dict back to dataclass instances
                config = FinancialAgentConfig(
                    analysis_weights=AnalysisWeights(**data['analysis_weights']),
                    fundamental_weights=FundamentalWeights(**data['fundamental_weights']),
                    technical_weights=TechnicalWeights(**data['technical_weights']),
                    recommendation_thresholds=RecommendationThresholds(**data['recommendation_thresholds']),
                    display_settings=DisplaySettings(**data['display_settings']),
                    api_settings=APISettings(**data['api_settings']),
                    watchlist=data.get('watchlist', []),
                    recent_analyses=data.get('recent_analyses', [])
                )
                
                self._config = config
                return config
                
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                print(f"Error loading config: {e}")
                print("Using default configuration")
        
        # Create and save default config
        config = FinancialAgentConfig.default()
        self.save_config(config)
        self._config = config
        return config
    
    def save_config(self, config: FinancialAgentConfig) -> None:
        """Save configuration to file"""
        try:
            # Convert dataclasses to dictionaries
            config_dict = {
                'analysis_weights': asdict(config.analysis_weights),
                'fundamental_weights': asdict(config.fundamental_weights),
                'technical_weights': asdict(config.technical_weights),
                'recommendation_thresholds': asdict(config.recommendation_thresholds),
                'display_settings': asdict(config.display_settings),
                'api_settings': asdict(config.api_settings),
                'watchlist': config.watchlist,
                'recent_analyses': config.recent_analyses
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config_dict, f, indent=2)
            
            self._config = config
            
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def update_watchlist(self, symbols: List[str]) -> None:
        """Update watchlist and save"""
        config = self.load_config()
        config.watchlist = list(set(symbols))  # Remove duplicates
        self.save_config(config)
    
    def add_to_watchlist(self, symbol: str) -> None:
        """Add symbol to watchlist"""
        config = self.load_config()
        if symbol not in config.watchlist:
            config.watchlist.append(symbol)
            self.save_config(config)
    
    def remove_from_watchlist(self, symbol: str) -> None:
        """Remove symbol from watchlist"""
        config = self.load_config()
        if symbol in config.watchlist:
            config.watchlist.remove(symbol)
            self.save_config(config)
    
    def add_recent_analysis(self, symbol: str) -> None:
        """Add to recent analyses (keep last 10)"""
        config = self.load_config()
        if symbol in config.recent_analyses:
            config.recent_analyses.remove(symbol)
        config.recent_analyses.insert(0, symbol)
        config.recent_analyses = config.recent_analyses[:10]  # Keep only last 10
        self.save_config(config)
    
    def get_cache_file(self, symbol: str) -> Path:
        """Get cache file path for a symbol"""
        return self.cache_dir / f"{symbol}.json"
    
    def clear_cache(self) -> None:
        """Clear all cached data"""
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()


# Global config manager instance
config_manager = ConfigManager()


def get_config() -> FinancialAgentConfig:
    """Get current configuration"""
    return config_manager.load_config()


def save_config(config: FinancialAgentConfig) -> None:
    """Save configuration"""
    config_manager.save_config(config)


def update_analysis_weights(fundamental: float = None, technical: float = None, sentiment: float = None) -> None:
    """Update analysis weights"""
    config = get_config()
    
    if fundamental is not None:
        config.analysis_weights.fundamental = fundamental
    if technical is not None:
        config.analysis_weights.technical = technical
    if sentiment is not None:
        config.analysis_weights.sentiment = sentiment
    
    # Normalize weights to sum to 1.0
    total = config.analysis_weights.fundamental + config.analysis_weights.technical + config.analysis_weights.sentiment
    if total > 0:
        config.analysis_weights.fundamental /= total
        config.analysis_weights.technical /= total
        config.analysis_weights.sentiment /= total
    
    save_config(config)


def reset_to_defaults() -> None:
    """Reset configuration to defaults"""
    config = FinancialAgentConfig.default()
    save_config(config)


# Example usage and testing
if __name__ == "__main__":
    # Test configuration management
    config = get_config()
    print("Current configuration:")
    print(f"Analysis weights: F={config.analysis_weights.fundamental:.2f}, "
          f"T={config.analysis_weights.technical:.2f}, "
          f"S={config.analysis_weights.sentiment:.2f}")
    print(f"Watchlist: {config.watchlist}")
    print(f"Recent analyses: {config.recent_analyses}")
    
    # Test watchlist management
    config_manager.add_to_watchlist("AAPL")
    config_manager.add_to_watchlist("TSLA")
    config_manager.add_recent_analysis("MSFT")
    
    updated_config = get_config()
    print(f"\nUpdated watchlist: {updated_config.watchlist}")
    print(f"Updated recent: {updated_config.recent_analyses}")
    
    # Test weight updates
    update_analysis_weights(fundamental=0.6, technical=0.25, sentiment=0.15)
    final_config = get_config()
    print(f"\nUpdated weights: F={final_config.analysis_weights.fundamental:.2f}, "
          f"T={final_config.analysis_weights.technical:.2f}, "
          f"S={final_config.analysis_weights.sentiment:.2f}")