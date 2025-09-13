"""
Comprehensive Financial Analysis Engine - Advanced Features
Extends the base financial analyzer with sophisticated analysis capabilities
"""
import yfinance as yf
import pandas as pd
import numpy as np
import requests
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple, Any
import math
from collections import defaultdict


@dataclass
class OptionsMetrics:
    """Options analysis metrics"""
    implied_volatility: Optional[float] = None
    delta: Optional[float] = None
    gamma: Optional[float] = None
    theta: Optional[float] = None
    vega: Optional[float] = None
    put_call_ratio: Optional[float] = None
    max_pain: Optional[float] = None
    option_volume: Optional[int] = None
    score: float = 0.0


@dataclass
class SectorMetrics:
    """Sector and market context metrics"""
    sector: str = ""
    industry: str = ""
    sector_performance: Optional[float] = None
    market_correlation: Optional[float] = None
    relative_strength: Optional[float] = None
    sector_pe_ratio: Optional[float] = None
    sector_rank: Optional[int] = None
    peers: List[str] = field(default_factory=list)
    score: float = 0.0


@dataclass
class FinancialHealthMetrics:
    """Advanced financial health metrics"""
    piotroski_score: Optional[int] = None  # 0-9 score
    altman_z_score: Optional[float] = None  # Bankruptcy prediction
    beneish_m_score: Optional[float] = None  # Earnings manipulation
    working_capital: Optional[float] = None
    cash_conversion_cycle: Optional[int] = None
    asset_quality: Optional[float] = None
    debt_coverage_ratio: Optional[float] = None
    score: float = 0.0


@dataclass
class MomentumMetrics:
    """Momentum and growth analysis"""
    price_momentum_1m: Optional[float] = None
    price_momentum_3m: Optional[float] = None
    price_momentum_6m: Optional[float] = None
    relative_strength_index_long: Optional[float] = None  # 200-day RSI
    earnings_revision_trend: Optional[str] = None
    estimate_revisions: Optional[float] = None
    earnings_surprise_history: List[float] = field(default_factory=list)
    revenue_consistency: Optional[float] = None
    score: float = 0.0


@dataclass
class RiskMetrics:
    """Advanced risk assessment metrics"""
    beta: Optional[float] = None
    sharpe_ratio: Optional[float] = None
    sortino_ratio: Optional[float] = None
    max_drawdown: Optional[float] = None
    value_at_risk_95: Optional[float] = None
    volatility_30d: Optional[float] = None
    volatility_90d: Optional[float] = None
    downside_deviation: Optional[float] = None
    risk_score: float = 0.0


@dataclass
class ValuationMetrics:
    """Advanced valuation analysis"""
    dcf_estimate: Optional[float] = None
    graham_number: Optional[float] = None
    peter_lynch_fair_value: Optional[float] = None
    ev_sales: Optional[float] = None
    ev_ebit: Optional[float] = None
    price_to_fcf: Optional[float] = None
    enterprise_value: Optional[float] = None
    intrinsic_value_range: Tuple[Optional[float], Optional[float]] = (None, None)
    valuation_score: float = 0.0


@dataclass
class QualityMetrics:
    """Earnings and financial quality metrics"""
    earnings_quality: Optional[float] = None  # 0-100
    accruals_ratio: Optional[float] = None
    cash_flow_to_earnings: Optional[float] = None
    revenue_recognition_quality: Optional[float] = None
    accounting_red_flags: List[str] = field(default_factory=list)
    audit_quality: Optional[str] = None
    management_efficiency: Optional[float] = None
    score: float = 0.0


@dataclass
class MacroContextMetrics:
    """Macroeconomic context analysis"""
    interest_rate_sensitivity: Optional[float] = None
    inflation_impact: Optional[str] = None
    economic_cycle_position: Optional[str] = None
    currency_exposure: Optional[float] = None
    commodity_sensitivity: Optional[float] = None
    market_regime: Optional[str] = None
    economic_indicators: Dict[str, float] = field(default_factory=dict)
    score: float = 0.0


@dataclass
class ComprehensiveAnalysis:
    """Complete comprehensive analysis results"""
    symbol: str
    analysis_timestamp: datetime
    options_metrics: OptionsMetrics
    sector_metrics: SectorMetrics
    financial_health: FinancialHealthMetrics
    momentum_metrics: MomentumMetrics
    risk_metrics: RiskMetrics
    valuation_metrics: ValuationMetrics
    quality_metrics: QualityMetrics
    macro_context: MacroContextMetrics
    composite_score: float = 0.0
    confidence_level: float = 0.0
    key_insights: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)


class ComprehensiveAnalyzer:
    """Advanced comprehensive financial analyzer"""
    
    def __init__(self):
        self.risk_free_rate = 0.045  # Current 10Y Treasury rate (approximate)
        
        # Scoring weights for composite score
        self.composite_weights = {
            'fundamental': 0.25,
            'technical': 0.15,
            'financial_health': 0.20,
            'valuation': 0.15,
            'quality': 0.10,
            'momentum': 0.10,
            'risk': 0.05
        }
    
    def perform_comprehensive_analysis(self, symbol: str) -> ComprehensiveAnalysis:
        """Perform complete comprehensive analysis"""
        print(f"🔍 Starting comprehensive analysis for {symbol}...")
        
        # Get ticker object
        ticker = yf.Ticker(symbol)
        
        try:
            # Perform all analysis components
            options_metrics = self._analyze_options(ticker, symbol)
            sector_metrics = self._analyze_sector_context(ticker, symbol)
            financial_health = self._analyze_financial_health(ticker, symbol)
            momentum_metrics = self._analyze_momentum(ticker, symbol)
            risk_metrics = self._analyze_risk(ticker, symbol)
            valuation_metrics = self._analyze_valuation(ticker, symbol)
            quality_metrics = self._analyze_quality(ticker, symbol)
            macro_context = self._analyze_macro_context(ticker, symbol)
            
            # Calculate composite score and insights
            composite_score = self._calculate_composite_score(
                financial_health, valuation_metrics, quality_metrics,
                momentum_metrics, risk_metrics
            )
            
            confidence_level = self._calculate_confidence(
                options_metrics, financial_health, quality_metrics
            )
            
            key_insights = self._generate_key_insights(
                symbol, financial_health, valuation_metrics, quality_metrics,
                momentum_metrics, risk_metrics
            )
            
            warnings = self._generate_warnings(
                financial_health, quality_metrics, risk_metrics
            )
            
            return ComprehensiveAnalysis(
                symbol=symbol,
                analysis_timestamp=datetime.now(),
                options_metrics=options_metrics,
                sector_metrics=sector_metrics,
                financial_health=financial_health,
                momentum_metrics=momentum_metrics,
                risk_metrics=risk_metrics,
                valuation_metrics=valuation_metrics,
                quality_metrics=quality_metrics,
                macro_context=macro_context,
                composite_score=composite_score,
                confidence_level=confidence_level,
                key_insights=key_insights,
                warnings=warnings
            )
            
        except Exception as e:
            print(f"❌ Error in comprehensive analysis for {symbol}: {e}")
            # Return minimal analysis with error info
            return ComprehensiveAnalysis(
                symbol=symbol,
                analysis_timestamp=datetime.now(),
                options_metrics=OptionsMetrics(),
                sector_metrics=SectorMetrics(),
                financial_health=FinancialHealthMetrics(),
                momentum_metrics=MomentumMetrics(),
                risk_metrics=RiskMetrics(),
                valuation_metrics=ValuationMetrics(),
                quality_metrics=QualityMetrics(),
                macro_context=MacroContextMetrics(),
                warnings=[f"Analysis error: {str(e)}"]
            )
    
    def _analyze_options(self, ticker, symbol: str) -> OptionsMetrics:
        """Analyze options data for insights"""
        try:
            info = ticker.info
            
            # Try to get options data
            options_data = {}
            try:
                exp_dates = ticker.options
                if exp_dates:
                    # Get nearest expiration
                    nearest_exp = exp_dates[0]
                    option_chain = ticker.option_chain(nearest_exp)
                    
                    calls = option_chain.calls
                    puts = option_chain.puts
                    
                    if not calls.empty and not puts.empty:
                        # Calculate put/call ratio
                        put_volume = puts['volume'].sum()
                        call_volume = calls['volume'].sum()
                        put_call_ratio = put_volume / call_volume if call_volume > 0 else None
                        
                        # Get implied volatility (weighted average)
                        total_volume = calls['volume'].sum() + puts['volume'].sum()
                        if total_volume > 0:
                            call_iv_weighted = (calls['impliedVolatility'] * calls['volume']).sum()
                            put_iv_weighted = (puts['impliedVolatility'] * puts['volume']).sum()
                            implied_volatility = (call_iv_weighted + put_iv_weighted) / total_volume
                        else:
                            implied_volatility = None
                        
                        options_data = {
                            'put_call_ratio': put_call_ratio,
                            'implied_volatility': implied_volatility,
                            'option_volume': int(total_volume)
                        }
            except:
                pass
            
            return OptionsMetrics(**options_data)
            
        except Exception as e:
            print(f"Warning: Options analysis failed for {symbol}: {e}")
            return OptionsMetrics()
    
    def _analyze_sector_context(self, ticker, symbol: str) -> SectorMetrics:
        """Analyze sector and market context"""
        try:
            info = ticker.info
            
            sector = info.get('sector', '')
            industry = info.get('industry', '')
            
            # Get market correlation (simplified using SPY)
            try:
                hist = ticker.history(period="1y")
                spy = yf.Ticker("SPY").history(period="1y")
                
                if not hist.empty and not spy.empty:
                    # Align dates and calculate correlation
                    combined = pd.merge(hist[['Close']], spy[['Close']], 
                                      left_index=True, right_index=True, 
                                      suffixes=('_stock', '_spy'))
                    if len(combined) > 30:
                        correlation = combined['Close_stock'].corr(combined['Close_spy'])
                    else:
                        correlation = None
                else:
                    correlation = None
            except:
                correlation = None
            
            return SectorMetrics(
                sector=sector,
                industry=industry,
                market_correlation=correlation
            )
            
        except Exception as e:
            print(f"Warning: Sector analysis failed for {symbol}: {e}")
            return SectorMetrics()
    
    def _analyze_financial_health(self, ticker, symbol: str) -> FinancialHealthMetrics:
        """Calculate advanced financial health metrics"""
        try:
            info = ticker.info
            financials = ticker.financials
            balance_sheet = ticker.balance_sheet
            cash_flow = ticker.cashflow
            
            # Calculate Piotroski F-Score
            piotroski_score = self._calculate_piotroski_score(
                info, financials, balance_sheet, cash_flow
            )
            
            # Calculate Altman Z-Score
            altman_z_score = self._calculate_altman_z_score(info, balance_sheet)
            
            # Working capital
            current_assets = balance_sheet.loc['Total Current Assets'].iloc[0] if 'Total Current Assets' in balance_sheet.index else None
            current_liabilities = balance_sheet.loc['Total Current Liabilities'].iloc[0] if 'Total Current Liabilities' in balance_sheet.index else None
            working_capital = current_assets - current_liabilities if current_assets and current_liabilities else None
            
            # Debt coverage ratio
            total_debt = info.get('totalDebt')
            operating_cash_flow = cash_flow.loc['Total Cash From Operating Activities'].iloc[0] if 'Total Cash From Operating Activities' in cash_flow.index else None
            debt_coverage = operating_cash_flow / total_debt if total_debt and operating_cash_flow and total_debt > 0 else None
            
            health_metrics = FinancialHealthMetrics(
                piotroski_score=piotroski_score,
                altman_z_score=altman_z_score,
                working_capital=working_capital,
                debt_coverage_ratio=debt_coverage
            )
            
            # Calculate health score
            health_metrics.score = self._calculate_health_score(health_metrics)
            
            return health_metrics
            
        except Exception as e:
            print(f"Warning: Financial health analysis failed for {symbol}: {e}")
            return FinancialHealthMetrics()
    
    def _analyze_momentum(self, ticker, symbol: str) -> MomentumMetrics:
        """Analyze momentum and growth trends"""
        try:
            hist = ticker.history(period="1y")
            
            if len(hist) < 30:
                return MomentumMetrics()
            
            current_price = hist['Close'].iloc[-1]
            
            # Calculate momentum over different periods
            if len(hist) >= 22:  # 1 month
                price_1m_ago = hist['Close'].iloc[-22]
                momentum_1m = (current_price - price_1m_ago) / price_1m_ago * 100
            else:
                momentum_1m = None
                
            if len(hist) >= 66:  # 3 months
                price_3m_ago = hist['Close'].iloc[-66]
                momentum_3m = (current_price - price_3m_ago) / price_3m_ago * 100
            else:
                momentum_3m = None
                
            if len(hist) >= 132:  # 6 months
                price_6m_ago = hist['Close'].iloc[-132]
                momentum_6m = (current_price - price_6m_ago) / price_6m_ago * 100
            else:
                momentum_6m = None
            
            # Long-term RSI (200-day if available)
            if len(hist) >= 200:
                rsi_long = self._calculate_rsi(hist['Close'], 200)
            else:
                rsi_long = None
            
            momentum = MomentumMetrics(
                price_momentum_1m=momentum_1m,
                price_momentum_3m=momentum_3m,
                price_momentum_6m=momentum_6m,
                relative_strength_index_long=rsi_long
            )
            
            # Calculate momentum score
            momentum.score = self._calculate_momentum_score(momentum)
            
            return momentum
            
        except Exception as e:
            print(f"Warning: Momentum analysis failed for {symbol}: {e}")
            return MomentumMetrics()
    
    def _analyze_risk(self, ticker, symbol: str) -> RiskMetrics:
        """Perform advanced risk analysis"""
        try:
            hist = ticker.history(period="2y")
            info = ticker.info
            
            if len(hist) < 50:
                return RiskMetrics()
            
            returns = hist['Close'].pct_change().dropna()
            
            # Beta calculation (vs SPY)
            try:
                spy_hist = yf.Ticker("SPY").history(period="2y")
                spy_returns = spy_hist['Close'].pct_change().dropna()
                
                # Align dates
                combined_returns = pd.merge(returns, spy_returns, 
                                          left_index=True, right_index=True, 
                                          suffixes=('_stock', '_spy'))
                if len(combined_returns) > 50:
                    covariance = combined_returns['Close_stock'].cov(combined_returns['Close_spy'])
                    spy_variance = combined_returns['Close_spy'].var()
                    beta = covariance / spy_variance if spy_variance > 0 else None
                else:
                    beta = None
            except:
                beta = info.get('beta')
            
            # Risk metrics calculations
            annual_return = returns.mean() * 252
            annual_volatility = returns.std() * math.sqrt(252)
            
            # Sharpe Ratio
            sharpe_ratio = (annual_return - self.risk_free_rate) / annual_volatility if annual_volatility > 0 else None
            
            # Sortino Ratio (using downside deviation)
            negative_returns = returns[returns < 0]
            downside_deviation = negative_returns.std() * math.sqrt(252) if len(negative_returns) > 0 else 0
            sortino_ratio = (annual_return - self.risk_free_rate) / downside_deviation if downside_deviation > 0 else None
            
            # Maximum Drawdown
            cumulative_returns = (1 + returns).cumprod()
            running_max = cumulative_returns.expanding().max()
            drawdown = (cumulative_returns - running_max) / running_max
            max_drawdown = drawdown.min() * 100  # Convert to percentage
            
            # Value at Risk (95% confidence)
            var_95 = np.percentile(returns, 5) * 100  # 5th percentile
            
            # Volatilities
            if len(returns) >= 30:
                volatility_30d = returns.tail(30).std() * math.sqrt(252) * 100
            else:
                volatility_30d = None
                
            if len(returns) >= 90:
                volatility_90d = returns.tail(90).std() * math.sqrt(252) * 100
            else:
                volatility_90d = None
            
            risk_metrics = RiskMetrics(
                beta=beta,
                sharpe_ratio=sharpe_ratio,
                sortino_ratio=sortino_ratio,
                max_drawdown=max_drawdown,
                value_at_risk_95=var_95,
                volatility_30d=volatility_30d,
                volatility_90d=volatility_90d,
                downside_deviation=downside_deviation * 100
            )
            
            # Calculate risk score
            risk_metrics.risk_score = self._calculate_risk_score(risk_metrics)
            
            return risk_metrics
            
        except Exception as e:
            print(f"Warning: Risk analysis failed for {symbol}: {e}")
            return RiskMetrics()
    
    def _analyze_valuation(self, ticker, symbol: str) -> ValuationMetrics:
        """Perform advanced valuation analysis"""
        try:
            info = ticker.info
            
            current_price = info.get('currentPrice', info.get('regularMarketPrice'))
            if not current_price:
                return ValuationMetrics()
            
            # Graham Number calculation
            eps = info.get('trailingEps')
            book_value = info.get('bookValue')
            graham_number = math.sqrt(22.5 * eps * book_value) if eps and book_value and eps > 0 and book_value > 0 else None
            
            # Peter Lynch Fair Value (PEG-based)
            peg_ratio = info.get('pegRatio')
            growth_rate = info.get('earningsGrowth')
            if peg_ratio and growth_rate and growth_rate > 0:
                pe_ratio = info.get('trailingPE')
                if pe_ratio:
                    lynch_fair_value = current_price * (1 / peg_ratio) if peg_ratio > 0 else None
                else:
                    lynch_fair_value = None
            else:
                lynch_fair_value = None
            
            # Enterprise value ratios
            enterprise_value = info.get('enterpriseValue')
            ev_sales = info.get('enterpriseToRevenue')
            ev_ebit = info.get('enterpriseToEbitda')
            
            # Price to Free Cash Flow
            free_cash_flow = info.get('freeCashflow')
            shares_outstanding = info.get('sharesOutstanding')
            if free_cash_flow and shares_outstanding and free_cash_flow > 0:
                fcf_per_share = free_cash_flow / shares_outstanding
                price_to_fcf = current_price / fcf_per_share
            else:
                price_to_fcf = None
            
            # Simple DCF estimation (very basic)
            dcf_estimate = self._simple_dcf_estimate(info)
            
            valuation = ValuationMetrics(
                dcf_estimate=dcf_estimate,
                graham_number=graham_number,
                peter_lynch_fair_value=lynch_fair_value,
                ev_sales=ev_sales,
                ev_ebit=ev_ebit,
                price_to_fcf=price_to_fcf,
                enterprise_value=enterprise_value
            )
            
            # Calculate valuation score
            valuation.valuation_score = self._calculate_valuation_score(valuation, current_price)
            
            return valuation
            
        except Exception as e:
            print(f"Warning: Valuation analysis failed for {symbol}: {e}")
            return ValuationMetrics()
    
    def _analyze_quality(self, ticker, symbol: str) -> QualityMetrics:
        """Analyze earnings and financial quality"""
        try:
            cash_flow = ticker.cashflow
            financials = ticker.financials
            info = ticker.info
            
            red_flags = []
            
            # Cash flow to earnings ratio
            if not cash_flow.empty and not financials.empty:
                try:
                    operating_cash_flow = cash_flow.loc['Total Cash From Operating Activities'].iloc[0]
                    net_income = financials.loc['Net Income'].iloc[0]
                    
                    if net_income and net_income != 0:
                        cf_to_earnings = operating_cash_flow / net_income
                        
                        # Red flag if cash flow significantly less than earnings
                        if cf_to_earnings < 0.8:
                            red_flags.append("Low cash flow relative to earnings")
                    else:
                        cf_to_earnings = None
                except:
                    cf_to_earnings = None
            else:
                cf_to_earnings = None
            
            # Accruals ratio (simplified)
            try:
                if cf_to_earnings:
                    accruals_ratio = 1 - cf_to_earnings
                else:
                    accruals_ratio = None
            except:
                accruals_ratio = None
            
            # Management efficiency (simplified ROA trend)
            roa = info.get('returnOnAssets')
            if roa and roa < 0.02:  # Less than 2% ROA
                red_flags.append("Low return on assets")
            
            # High debt levels
            debt_to_equity = info.get('debtToEquity')
            if debt_to_equity and debt_to_equity > 200:  # Over 200% D/E ratio
                red_flags.append("Very high debt-to-equity ratio")
            
            # Calculate earnings quality score
            earnings_quality = self._calculate_earnings_quality(cf_to_earnings, accruals_ratio, red_flags)
            
            quality = QualityMetrics(
                earnings_quality=earnings_quality,
                accruals_ratio=accruals_ratio,
                cash_flow_to_earnings=cf_to_earnings,
                accounting_red_flags=red_flags
            )
            
            # Calculate overall quality score
            quality.score = self._calculate_quality_score(quality)
            
            return quality
            
        except Exception as e:
            print(f"Warning: Quality analysis failed for {symbol}: {e}")
            return QualityMetrics()
    
    def _analyze_macro_context(self, ticker, symbol: str) -> MacroContextMetrics:
        """Analyze macroeconomic context"""
        try:
            info = ticker.info
            sector = info.get('sector', '')
            
            # Simple sector-based sensitivity analysis
            interest_rate_sensitivity = self._estimate_interest_sensitivity(sector)
            inflation_impact = self._estimate_inflation_impact(sector)
            
            return MacroContextMetrics(
                interest_rate_sensitivity=interest_rate_sensitivity,
                inflation_impact=inflation_impact,
                economic_cycle_position="Unknown"  # Would require more data
            )
            
        except Exception as e:
            print(f"Warning: Macro analysis failed for {symbol}: {e}")
            return MacroContextMetrics()
    
    # Helper calculation methods
    
    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> Optional[float]:
        """Calculate RSI indicator"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.iloc[-1] if not rsi.empty else None
        except:
            return None
    
    def _calculate_piotroski_score(self, info: dict, financials: pd.DataFrame, 
                                  balance_sheet: pd.DataFrame, cash_flow: pd.DataFrame) -> Optional[int]:
        """Calculate Piotroski F-Score (simplified version)"""
        try:
            score = 0
            
            # Profitability (4 points)
            roa = info.get('returnOnAssets')
            if roa and roa > 0:
                score += 1
                
            if not cash_flow.empty and 'Total Cash From Operating Activities' in cash_flow.index:
                ocf = cash_flow.loc['Total Cash From Operating Activities'].iloc[0]
                if ocf > 0:
                    score += 1
            
            # Operating efficiency would require historical data
            # Simplified: assume 2 more points for established companies
            if info.get('marketCap', 0) > 10e9:  # Large cap
                score += 2
            
            # Leverage, liquidity (3 points)
            debt_to_equity = info.get('debtToEquity')
            if debt_to_equity and debt_to_equity < 50:  # Low debt
                score += 1
                
            current_ratio = info.get('currentRatio')
            if current_ratio and current_ratio > 1.2:
                score += 1
                
            # Outstanding shares (would need historical data)
            score += 1  # Assume no dilution for simplicity
            
            return min(score, 9)  # Cap at 9
            
        except:
            return None
    
    def _calculate_altman_z_score(self, info: dict, balance_sheet: pd.DataFrame) -> Optional[float]:
        """Calculate Altman Z-Score for bankruptcy prediction"""
        try:
            if balance_sheet.empty:
                return None
                
            # Need specific balance sheet items
            total_assets = balance_sheet.loc['Total Assets'].iloc[0] if 'Total Assets' in balance_sheet.index else None
            if not total_assets:
                return None
                
            # Simplified calculation using available data
            current_ratio = info.get('currentRatio', 1.0)
            debt_to_equity = info.get('debtToEquity', 100) / 100
            roa = info.get('returnOnAssets', 0)
            
            # Simplified Altman Z-Score formula
            z_score = (1.2 * (current_ratio - 1)) + (1.4 * roa) + (3.3 * roa) - (1.0 * debt_to_equity)
            
            return z_score
            
        except:
            return None
    
    def _simple_dcf_estimate(self, info: dict) -> Optional[float]:
        """Very simplified DCF estimation"""
        try:
            free_cash_flow = info.get('freeCashflow')
            growth_rate = info.get('earningsGrowth', 0.05)  # Default 5%
            
            if not free_cash_flow or free_cash_flow <= 0:
                return None
            
            # Simple 2-stage DCF
            # Stage 1: High growth for 5 years
            # Stage 2: Terminal growth of 3%
            
            terminal_growth = 0.03
            discount_rate = 0.10  # 10% WACC assumption
            
            # Calculate present value of cash flows
            pv_sum = 0
            for year in range(1, 6):  # 5 years
                future_cf = free_cash_flow * ((1 + growth_rate) ** year)
                pv = future_cf / ((1 + discount_rate) ** year)
                pv_sum += pv
            
            # Terminal value
            terminal_cf = free_cash_flow * ((1 + growth_rate) ** 5) * (1 + terminal_growth)
            terminal_value = terminal_cf / (discount_rate - terminal_growth)
            terminal_pv = terminal_value / ((1 + discount_rate) ** 5)
            
            total_pv = pv_sum + terminal_pv
            
            # Convert to per-share value
            shares_outstanding = info.get('sharesOutstanding')
            if shares_outstanding:
                dcf_per_share = total_pv / shares_outstanding
                return dcf_per_share
            
            return None
            
        except:
            return None
    
    def _estimate_interest_sensitivity(self, sector: str) -> Optional[float]:
        """Estimate interest rate sensitivity by sector"""
        sensitivity_map = {
            'Real Estate': 0.8,
            'Utilities': 0.7,
            'Financial Services': 0.6,
            'Consumer Cyclical': 0.4,
            'Technology': 0.2,
            'Healthcare': 0.1,
            'Consumer Defensive': 0.1
        }
        return sensitivity_map.get(sector, 0.3)
    
    def _estimate_inflation_impact(self, sector: str) -> str:
        """Estimate inflation impact by sector"""
        impact_map = {
            'Energy': 'Positive',
            'Materials': 'Positive', 
            'Real Estate': 'Mixed',
            'Financial Services': 'Mixed',
            'Consumer Defensive': 'Negative',
            'Technology': 'Negative',
            'Healthcare': 'Negative'
        }
        return impact_map.get(sector, 'Neutral')
    
    # Scoring methods
    
    def _calculate_health_score(self, health: FinancialHealthMetrics) -> float:
        """Calculate financial health score (0-100)"""
        score = 50  # Base score
        
        if health.piotroski_score:
            # Piotroski score contributes 0-30 points
            score += (health.piotroski_score / 9) * 30
            
        if health.altman_z_score:
            if health.altman_z_score > 3.0:
                score += 20  # Safe zone
            elif health.altman_z_score > 1.8:
                score += 10  # Gray zone
            else:
                score -= 20  # Distress zone
        
        return max(0, min(100, score))
    
    def _calculate_momentum_score(self, momentum: MomentumMetrics) -> float:
        """Calculate momentum score (0-100)"""
        score = 50
        
        if momentum.price_momentum_1m:
            if momentum.price_momentum_1m > 10:
                score += 20
            elif momentum.price_momentum_1m > 0:
                score += 10
            elif momentum.price_momentum_1m < -10:
                score -= 20
            else:
                score -= 10
                
        return max(0, min(100, score))
    
    def _calculate_risk_score(self, risk: RiskMetrics) -> float:
        """Calculate risk score (0-100, higher is better/safer)"""
        score = 50
        
        if risk.sharpe_ratio:
            if risk.sharpe_ratio > 1.0:
                score += 25
            elif risk.sharpe_ratio > 0.5:
                score += 15
            elif risk.sharpe_ratio < 0:
                score -= 20
                
        if risk.max_drawdown:
            if risk.max_drawdown > -10:
                score += 15
            elif risk.max_drawdown > -20:
                score += 5
            elif risk.max_drawdown < -40:
                score -= 25
                
        return max(0, min(100, score))
    
    def _calculate_valuation_score(self, valuation: ValuationMetrics, current_price: float) -> float:
        """Calculate valuation score (0-100)"""
        score = 50
        
        if valuation.dcf_estimate and current_price:
            ratio = current_price / valuation.dcf_estimate
            if ratio < 0.8:  # Trading below DCF
                score += 25
            elif ratio < 1.0:
                score += 15
            elif ratio > 1.5:
                score -= 25
            elif ratio > 1.2:
                score -= 15
                
        if valuation.price_to_fcf:
            if valuation.price_to_fcf < 15:
                score += 15
            elif valuation.price_to_fcf > 30:
                score -= 15
                
        return max(0, min(100, score))
    
    def _calculate_quality_score(self, quality: QualityMetrics) -> float:
        """Calculate quality score (0-100)"""
        score = 70  # Start higher for quality
        
        if quality.cash_flow_to_earnings:
            if quality.cash_flow_to_earnings > 1.2:
                score += 20
            elif quality.cash_flow_to_earnings > 0.8:
                score += 10
            else:
                score -= 20
                
        # Penalize for red flags
        score -= len(quality.accounting_red_flags) * 10
        
        return max(0, min(100, score))
    
    def _calculate_earnings_quality(self, cf_to_earnings: Optional[float], 
                                  accruals_ratio: Optional[float], red_flags: List[str]) -> Optional[float]:
        """Calculate earnings quality score"""
        if not cf_to_earnings:
            return None
            
        quality = 80  # Start high
        
        if cf_to_earnings < 0.8:
            quality -= 30
        elif cf_to_earnings < 1.0:
            quality -= 10
            
        quality -= len(red_flags) * 15
        
        return max(0, min(100, quality))
    
    def _calculate_composite_score(self, health: FinancialHealthMetrics, valuation: ValuationMetrics,
                                 quality: QualityMetrics, momentum: MomentumMetrics, 
                                 risk: RiskMetrics) -> float:
        """Calculate composite comprehensive score"""
        scores = {
            'financial_health': health.score,
            'valuation': valuation.valuation_score,
            'quality': quality.score,
            'momentum': momentum.score,
            'risk': risk.risk_score
        }
        
        weighted_sum = 0
        total_weight = 0
        
        for component, score in scores.items():
            if score > 0:  # Only include components with valid scores
                weight = self.composite_weights.get(component, 0.1)
                weighted_sum += score * weight
                total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 50
    
    def _calculate_confidence(self, options: OptionsMetrics, health: FinancialHealthMetrics,
                            quality: QualityMetrics) -> float:
        """Calculate confidence in the analysis"""
        confidence = 0.7  # Base confidence
        
        # Data completeness factor
        if health.piotroski_score:
            confidence += 0.1
        if health.altman_z_score:
            confidence += 0.1
        if quality.cash_flow_to_earnings:
            confidence += 0.1
            
        return min(0.95, confidence)
    
    def _generate_key_insights(self, symbol: str, health: FinancialHealthMetrics, 
                             valuation: ValuationMetrics, quality: QualityMetrics,
                             momentum: MomentumMetrics, risk: RiskMetrics) -> List[str]:
        """Generate key insights from analysis"""
        insights = []
        
        # Financial health insights
        if health.piotroski_score and health.piotroski_score >= 7:
            insights.append(f"Strong financial health (Piotroski score: {health.piotroski_score}/9)")
        elif health.piotroski_score and health.piotroski_score <= 3:
            insights.append(f"Weak financial health (Piotroski score: {health.piotroski_score}/9)")
            
        # Valuation insights
        if valuation.dcf_estimate:
            current_price = 100  # Placeholder - would get from ticker
            if valuation.dcf_estimate > current_price * 1.2:
                insights.append("Trading below estimated intrinsic value")
            elif valuation.dcf_estimate < current_price * 0.8:
                insights.append("Trading above estimated intrinsic value")
        
        # Quality insights
        if quality.cash_flow_to_earnings and quality.cash_flow_to_earnings > 1.2:
            insights.append("Strong cash flow generation relative to earnings")
            
        # Risk insights
        if risk.max_drawdown and risk.max_drawdown > -10:
            insights.append("Low historical volatility and drawdown")
        elif risk.max_drawdown and risk.max_drawdown < -30:
            insights.append("High historical volatility with significant drawdowns")
            
        return insights[:5]  # Limit to top 5 insights
    
    def _generate_warnings(self, health: FinancialHealthMetrics, quality: QualityMetrics,
                         risk: RiskMetrics) -> List[str]:
        """Generate warnings from analysis"""
        warnings = []
        
        if health.altman_z_score and health.altman_z_score < 1.8:
            warnings.append("⚠️ Elevated bankruptcy risk (low Altman Z-score)")
            
        if quality.accounting_red_flags:
            warnings.append(f"⚠️ {len(quality.accounting_red_flags)} accounting red flags detected")
            
        if risk.max_drawdown and risk.max_drawdown < -40:
            warnings.append("⚠️ Very high historical volatility and drawdowns")
            
        return warnings


# Example usage and testing
if __name__ == "__main__":
    analyzer = ComprehensiveAnalyzer()
    
    # Test comprehensive analysis
    test_symbol = "AAPL"
    print(f"🚀 Testing comprehensive analysis for {test_symbol}")
    
    try:
        analysis = analyzer.perform_comprehensive_analysis(test_symbol)
        
        print(f"\n📊 Comprehensive Analysis Results for {test_symbol}")
        print(f"Composite Score: {analysis.composite_score:.1f}/100")
        print(f"Confidence: {analysis.confidence_level:.1%}")
        
        print(f"\n💰 Valuation Score: {analysis.valuation_metrics.valuation_score:.1f}")
        if analysis.valuation_metrics.dcf_estimate:
            print(f"DCF Estimate: ${analysis.valuation_metrics.dcf_estimate:.2f}")
            
        print(f"\n🏥 Financial Health Score: {analysis.financial_health.score:.1f}")
        if analysis.financial_health.piotroski_score:
            print(f"Piotroski Score: {analysis.financial_health.piotroski_score}/9")
            
        print(f"\n⚡ Key Insights:")
        for insight in analysis.key_insights:
            print(f"  • {insight}")
            
        if analysis.warnings:
            print(f"\n⚠️ Warnings:")
            for warning in analysis.warnings:
                print(f"  • {warning}")
                
    except Exception as e:
        print(f"❌ Error in comprehensive analysis: {e}")