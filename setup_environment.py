"""
Environment setup and API key management for Financial Research Agent
"""
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Add python-dotenv support if available
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False
    print("Info: python-dotenv not installed. Manual environment variable setup required.")
    print("Install with: pip install python-dotenv")


class EnvironmentSetup:
    """Manages environment variables and API key setup"""
    
    def __init__(self):
        self.env_file = Path(__file__).parent / '.env'
        self.example_file = Path(__file__).parent / '.env.example'
        
        # Load environment variables if dotenv is available
        if DOTENV_AVAILABLE and self.env_file.exists():
            load_dotenv(self.env_file)
    
    def check_required_packages(self) -> Dict[str, bool]:
        """Check if required Python packages are installed"""
        packages = {
            'yfinance': False,
            'textual': False,
            'rich': False,
            'requests': False,
            'pandas': False,
            'numpy': False,
            'praw': False,  # Reddit API
            'textblob': False,  # Sentiment analysis
            'python-dotenv': DOTENV_AVAILABLE
        }
        
        for package in packages:
            try:
                if package == 'python-dotenv':
                    continue  # Already checked
                __import__(package)
                packages[package] = True
            except ImportError:
                packages[package] = False
        
        return packages
    
    def get_api_key_status(self) -> Dict[str, Dict[str, any]]:
        """Check status of all API keys"""
        api_keys = {
            'NewsAPI': {
                'key': 'NEWS_API_KEY',
                'required_for': 'News sentiment analysis',
                'free_tier': '1,000 requests/day',
                'signup_url': 'https://newsapi.org/register'
            },
            'Reddit': {
                'keys': ['REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET', 'REDDIT_USER_AGENT'],
                'required_for': 'Social media sentiment analysis',
                'free_tier': '1,000 requests/minute',
                'signup_url': 'https://www.reddit.com/prefs/apps'
            },
            'Finnhub': {
                'key': 'FINNHUB_API_KEY',
                'required_for': 'Enhanced financial news',
                'free_tier': '60 calls/minute',
                'signup_url': 'https://finnhub.io/register'
            },
            'Alpha Vantage': {
                'key': 'ALPHA_VANTAGE_API_KEY',
                'required_for': 'Additional market data',
                'free_tier': '25 requests/day',
                'signup_url': 'https://www.alphavantage.co/support/#api-key'
            }
        }
        
        status = {}
        for service, info in api_keys.items():
            if 'key' in info:
                # Single key
                key_value = os.getenv(info['key'])
                status[service] = {
                    **info,
                    'configured': bool(key_value),
                    'value_preview': f"{key_value[:8]}..." if key_value else None
                }
            elif 'keys' in info:
                # Multiple keys
                keys_status = {}
                all_configured = True
                for key in info['keys']:
                    key_value = os.getenv(key)
                    keys_status[key] = bool(key_value)
                    if not key_value:
                        all_configured = False
                
                status[service] = {
                    **info,
                    'configured': all_configured,
                    'keys_status': keys_status
                }
        
        return status
    
    def create_env_file_template(self) -> bool:
        """Create .env file from template if it doesn't exist"""
        if self.env_file.exists():
            print(f"✅ .env file already exists at {self.env_file}")
            return True
        
        if not self.example_file.exists():
            print(f"❌ Template file not found at {self.example_file}")
            return False
        
        try:
            # Copy example to .env
            with open(self.example_file, 'r') as src:
                content = src.read()
            
            with open(self.env_file, 'w') as dst:
                dst.write(content)
            
            print(f"✅ Created .env file at {self.env_file}")
            print(f"📝 Please edit {self.env_file} and add your API keys")
            return True
            
        except Exception as e:
            print(f"❌ Error creating .env file: {e}")
            return False
    
    def validate_sentiment_setup(self) -> Dict[str, any]:
        """Validate sentiment analysis setup"""
        validation = {
            'news_available': False,
            'social_available': False,
            'can_run_basic': True,
            'can_run_enhanced': False,
            'missing_packages': [],
            'missing_keys': []
        }
        
        # Check packages
        packages = self.check_required_packages()
        required_packages = ['yfinance', 'requests', 'pandas', 'numpy']
        optional_packages = ['praw', 'textblob', 'python-dotenv']
        
        for package in required_packages:
            if not packages.get(package, False):
                validation['can_run_basic'] = False
                validation['missing_packages'].append(package)
        
        for package in optional_packages:
            if not packages.get(package, False):
                validation['missing_packages'].append(package)
        
        # Check API keys
        api_status = self.get_api_key_status()
        
        if api_status['NewsAPI']['configured']:
            validation['news_available'] = True
        else:
            validation['missing_keys'].append('NEWS_API_KEY')
        
        if api_status['Reddit']['configured']:
            validation['social_available'] = True
        else:
            validation['missing_keys'].extend(['REDDIT_CLIENT_ID', 'REDDIT_CLIENT_SECRET'])
        
        validation['can_run_enhanced'] = validation['news_available'] or validation['social_available']
        
        return validation
    
    def print_setup_status(self):
        """Print comprehensive setup status"""
        print("🏦 Financial Research Agent - Setup Status")
        print("=" * 50)
        
        # Package status
        print("\n📦 Python Packages:")
        packages = self.check_required_packages()
        
        required = ['yfinance', 'textual', 'rich', 'requests', 'pandas', 'numpy']
        optional = ['praw', 'textblob', 'python-dotenv']
        
        print("  Required packages:")
        for package in required:
            status = "✅" if packages.get(package, False) else "❌"
            print(f"    {status} {package}")
        
        print("  Optional packages (for enhanced features):")
        for package in optional:
            status = "✅" if packages.get(package, False) else "⚠️"
            print(f"    {status} {package}")
        
        # API key status
        print(f"\n🔑 API Keys:")
        api_status = self.get_api_key_status()
        
        for service, info in api_status.items():
            status = "✅" if info['configured'] else "❌"
            print(f"  {status} {service}")
            print(f"      Purpose: {info['required_for']}")
            print(f"      Free tier: {info['free_tier']}")
            if not info['configured']:
                print(f"      Sign up: {info['signup_url']}")
        
        # Sentiment analysis readiness
        print(f"\n🎯 Sentiment Analysis Status:")
        validation = self.validate_sentiment_setup()
        
        if validation['can_run_basic']:
            print("  ✅ Basic analysis: Ready")
        else:
            print("  ❌ Basic analysis: Missing packages")
            
        if validation['can_run_enhanced']:
            print("  ✅ Enhanced sentiment: Ready")
            if validation['news_available']:
                print("    📰 News sentiment: Available")
            if validation['social_available']:
                print("    💬 Social sentiment: Available")
        else:
            print("  ⚠️ Enhanced sentiment: API keys needed")
        
        # Installation commands
        if validation['missing_packages']:
            print(f"\n📝 To install missing packages:")
            missing = ' '.join(validation['missing_packages'])
            print(f"   pip install {missing}")
        
        if not self.env_file.exists():
            print(f"\n📝 To set up API keys:")
            print(f"   1. Copy .env.example to .env")
            print(f"   2. Edit .env and add your API keys")
            print(f"   3. Restart the application")
    
    def interactive_setup(self):
        """Interactive setup wizard"""
        print("🚀 Financial Research Agent - Interactive Setup")
        print("=" * 50)
        
        # Check if .env exists
        if not self.env_file.exists():
            print(f"\n📄 Environment file (.env) not found.")
            create = input("Create .env file from template? (y/n): ").lower().strip()
            if create == 'y':
                self.create_env_file_template()
                print(f"\n✏️ Please edit {self.env_file} with your API keys and run setup again.")
                return
        
        # Show current status
        self.print_setup_status()
        
        # Ask about package installation
        packages = self.check_required_packages()
        missing_required = [p for p in ['yfinance', 'textual', 'rich', 'requests', 'pandas', 'numpy'] 
                          if not packages.get(p, False)]
        
        if missing_required:
            print(f"\n⚠️ Missing required packages: {', '.join(missing_required)}")
            install = input("Install missing packages? (y/n): ").lower().strip()
            if install == 'y':
                import subprocess
                try:
                    subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing_required)
                    print("✅ Required packages installed!")
                except subprocess.CalledProcessError as e:
                    print(f"❌ Installation failed: {e}")
        
        # Check API setup
        validation = self.validate_sentiment_setup()
        if not validation['can_run_enhanced']:
            print(f"\n🔑 For enhanced sentiment analysis, you need API keys.")
            print(f"   The application will work with basic features only.")
        
        print(f"\n🎉 Setup complete! You can now run the financial agents.")


def main():
    """Run setup wizard"""
    setup = EnvironmentSetup()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--status':
        setup.print_setup_status()
    else:
        setup.interactive_setup()


if __name__ == "__main__":
    main()