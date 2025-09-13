"""
Data caching system for Financial Research Agents
Reduces API calls and improves performance
"""
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, Union
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
import hashlib

from config import config_manager


@dataclass
class CacheEntry:
    """Cache entry with metadata"""
    data: Any
    timestamp: float
    expires_at: float
    symbol: str
    data_type: str
    
    @property
    def is_expired(self) -> bool:
        """Check if cache entry is expired"""
        return time.time() > self.expires_at
    
    @property
    def age_minutes(self) -> float:
        """Get age of cache entry in minutes"""
        return (time.time() - self.timestamp) / 60
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'data': self.data,
            'timestamp': self.timestamp,
            'expires_at': self.expires_at,
            'symbol': self.symbol,
            'data_type': self.data_type
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'CacheEntry':
        """Create from dictionary"""
        return cls(
            data=data['data'],
            timestamp=data['timestamp'],
            expires_at=data['expires_at'],
            symbol=data['symbol'],
            data_type=data['data_type']
        )


class CacheManager:
    """Manages data caching for stock analysis"""
    
    def __init__(self):
        self.cache_dir = config_manager.cache_dir
        self.default_duration = 300  # 5 minutes default
        
        # Different cache durations for different data types
        self.cache_durations = {
            'stock_data': 60,      # 1 minute - price data changes frequently
            'fundamentals': 3600,   # 1 hour - financial data updates less frequently  
            'technicals': 300,      # 5 minutes - technical indicators update regularly
            'sentiment': 1800,      # 30 minutes - sentiment data updates periodically
            'info': 86400,         # 24 hours - company info rarely changes
        }
    
    def _get_cache_key(self, symbol: str, data_type: str) -> str:
        """Generate cache key for symbol and data type"""
        return f"{symbol}_{data_type}"
    
    def _get_cache_file(self, cache_key: str) -> Path:
        """Get cache file path"""
        return self.cache_dir / f"{cache_key}.json"
    
    def set(self, symbol: str, data_type: str, data: Any, duration: Optional[int] = None) -> None:
        """Store data in cache"""
        if duration is None:
            duration = self.cache_durations.get(data_type, self.default_duration)
        
        cache_key = self._get_cache_key(symbol, data_type)
        cache_file = self._get_cache_file(cache_key)
        
        entry = CacheEntry(
            data=data,
            timestamp=time.time(),
            expires_at=time.time() + duration,
            symbol=symbol.upper(),
            data_type=data_type
        )
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(entry.to_dict(), f, indent=2, default=str)
        except Exception as e:
            print(f"Warning: Failed to save cache for {symbol} {data_type}: {e}")
    
    def get(self, symbol: str, data_type: str) -> Optional[Any]:
        """Retrieve data from cache if valid"""
        cache_key = self._get_cache_key(symbol, data_type)
        cache_file = self._get_cache_file(cache_key)
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'r') as f:
                data = json.load(f)
            
            entry = CacheEntry.from_dict(data)
            
            if entry.is_expired:
                # Clean up expired cache
                cache_file.unlink(missing_ok=True)
                return None
            
            return entry.data
            
        except Exception as e:
            print(f"Warning: Failed to load cache for {symbol} {data_type}: {e}")
            # Clean up corrupted cache file
            cache_file.unlink(missing_ok=True)
            return None
    
    def has_valid_cache(self, symbol: str, data_type: str) -> bool:
        """Check if valid cache exists"""
        return self.get(symbol, data_type) is not None
    
    def invalidate(self, symbol: str, data_type: Optional[str] = None) -> None:
        """Invalidate cache for symbol"""
        if data_type:
            # Invalidate specific data type
            cache_key = self._get_cache_key(symbol, data_type)
            cache_file = self._get_cache_file(cache_key)
            cache_file.unlink(missing_ok=True)
        else:
            # Invalidate all data for symbol
            for data_type in self.cache_durations.keys():
                cache_key = self._get_cache_key(symbol, data_type)
                cache_file = self._get_cache_file(cache_key)
                cache_file.unlink(missing_ok=True)
    
    def clear_expired(self) -> int:
        """Clear all expired cache entries"""
        expired_count = 0
        
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                
                entry = CacheEntry.from_dict(data)
                if entry.is_expired:
                    cache_file.unlink()
                    expired_count += 1
                    
            except Exception:
                # Remove corrupted files
                cache_file.unlink(missing_ok=True)
                expired_count += 1
        
        return expired_count
    
    def clear_all(self) -> int:
        """Clear all cache entries"""
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
            count += 1
        return count
    
    def get_cache_info(self, symbol: Optional[str] = None) -> Dict[str, Any]:
        """Get cache information"""
        info = {
            'total_entries': 0,
            'expired_entries': 0,
            'cache_size_mb': 0,
            'entries_by_type': {},
            'entries_by_symbol': {}
        }
        
        total_size = 0
        
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                file_size = cache_file.stat().st_size
                total_size += file_size
                
                with open(cache_file, 'r') as f:
                    data = json.load(f)
                
                entry = CacheEntry.from_dict(data)
                
                # Filter by symbol if specified
                if symbol and entry.symbol.upper() != symbol.upper():
                    continue
                
                info['total_entries'] += 1
                
                if entry.is_expired:
                    info['expired_entries'] += 1
                
                # Count by data type
                if entry.data_type not in info['entries_by_type']:
                    info['entries_by_type'][entry.data_type] = 0
                info['entries_by_type'][entry.data_type] += 1
                
                # Count by symbol
                if entry.symbol not in info['entries_by_symbol']:
                    info['entries_by_symbol'][entry.symbol] = 0
                info['entries_by_symbol'][entry.symbol] += 1
                
            except Exception:
                continue
        
        info['cache_size_mb'] = round(total_size / (1024 * 1024), 2)
        return info
    
    def get_symbol_cache_status(self, symbol: str) -> Dict[str, Any]:
        """Get cache status for a specific symbol"""
        status = {}
        
        for data_type in self.cache_durations.keys():
            cache_key = self._get_cache_key(symbol, data_type)
            cache_file = self._get_cache_file(cache_key)
            
            if cache_file.exists():
                try:
                    with open(cache_file, 'r') as f:
                        data = json.load(f)
                    
                    entry = CacheEntry.from_dict(data)
                    status[data_type] = {
                        'cached': True,
                        'expired': entry.is_expired,
                        'age_minutes': round(entry.age_minutes, 1),
                        'expires_in_minutes': round((entry.expires_at - time.time()) / 60, 1)
                    }
                except Exception:
                    status[data_type] = {'cached': False, 'error': True}
            else:
                status[data_type] = {'cached': False}
        
        return status


# Global cache manager instance
cache_manager = CacheManager()


# Decorator for caching function results
def cached(data_type: str, duration: Optional[int] = None):
    """Decorator to cache function results"""
    def decorator(func):
        def wrapper(self, symbol: str, *args, **kwargs):
            # Try to get from cache first
            cached_data = cache_manager.get(symbol, data_type)
            if cached_data is not None:
                return cached_data
            
            # Call original function
            result = func(self, symbol, *args, **kwargs)
            
            # Cache the result
            if result is not None:
                cache_manager.set(symbol, data_type, result, duration)
            
            return result
        
        return wrapper
    return decorator


# Utility functions
def warm_cache(symbols: list, data_types: list = None) -> Dict[str, int]:
    """Warm cache for multiple symbols"""
    if data_types is None:
        data_types = list(cache_manager.cache_durations.keys())
    
    results = {'success': 0, 'errors': 0}
    
    # This would typically integrate with the FinancialAnalyzer
    # For now, just return structure
    return results


def cache_maintenance() -> Dict[str, int]:
    """Perform cache maintenance"""
    results = {
        'expired_cleared': cache_manager.clear_expired(),
        'total_entries': 0
    }
    
    info = cache_manager.get_cache_info()
    results['total_entries'] = info['total_entries']
    
    return results


# CLI utility functions
def print_cache_status(symbol: str = None):
    """Print cache status to console"""
    if symbol:
        print(f"\nCache Status for {symbol.upper()}:")
        print("-" * 40)
        
        status = cache_manager.get_symbol_cache_status(symbol)
        for data_type, info in status.items():
            if info.get('cached', False):
                if info.get('expired', False):
                    print(f"{data_type:12}: [EXPIRED] Age: {info['age_minutes']}min")
                else:
                    print(f"{data_type:12}: [VALID] Expires: {info['expires_in_minutes']}min")
            else:
                print(f"{data_type:12}: [NOT CACHED]")
    else:
        print("\nGlobal Cache Status:")
        print("-" * 30)
        
        info = cache_manager.get_cache_info()
        print(f"Total entries: {info['total_entries']}")
        print(f"Expired entries: {info['expired_entries']}")
        print(f"Cache size: {info['cache_size_mb']} MB")
        
        if info['entries_by_type']:
            print("\nEntries by type:")
            for data_type, count in info['entries_by_type'].items():
                print(f"  {data_type}: {count}")
        
        if info['entries_by_symbol']:
            print(f"\nCached symbols ({len(info['entries_by_symbol'])}):")
            for symbol, count in sorted(info['entries_by_symbol'].items()):
                print(f"  {symbol}: {count} entries")


# Example usage and testing
if __name__ == "__main__":
    # Test caching functionality
    print("Testing cache manager...")
    
    # Test basic caching
    test_data = {"price": 150.25, "change": 2.5}
    cache_manager.set("AAPL", "stock_data", test_data)
    
    # Retrieve cached data
    retrieved = cache_manager.get("AAPL", "stock_data")
    print(f"Cached data: {retrieved}")
    
    # Test cache status
    print_cache_status("AAPL")
    print_cache_status()
    
    # Test cache info
    info = cache_manager.get_cache_info()
    print(f"\nCache info: {info}")
    
    # Test cache maintenance
    maintenance_results = cache_maintenance()
    print(f"Maintenance results: {maintenance_results}")