# config.py - Centralized Configuration for PPP Financial Model
# This module contains all configuration constants and default parameters

from dataclasses import dataclass
from typing import Dict, Any

# ===== APP CONFIG =====
APP_TITLE = "PPP Financial Modeling Platform"
APP_DESCRIPTION = "Professional-grade financial simulation for Public-Private Partnership (PPP) projects"
APP_VERSION = "2.0.0"
APP_AUTHOR = "PPP Financial Team"

# Layout
PAGE_ICON = "📊"
LAYOUT = "wide"
INITIAL_SIDEBAR_STATE = "expanded"

# ===== FINANCIAL PARAMETERS - DEFAULTS =====
@dataclass
class DefaultFinancialParams:
    """Default financial model parameters"""
    total_investment: float = 5000.0  # $M
    project_period: int = 25  # years
    depreciation_period: int = 25  # years
    equity_ratio: float = 0.30  # 30%
    debt_rate: float = 0.09  # 9%
    discount_rate: float = 0.15  # 15%
    tax_rate: float = 0.20  # 20%
    initial_revenue: float = 1000.0  # $M
    revenue_growth: float = 0.03  # 3%
    op_cost_ratio: float = 0.35  # 35%
    inflation: float = 0.03  # 3%

# ===== PARAMETER RANGES =====
PARAMETER_RANGES = {
    'total_investment': {'min': 500, 'max': 20000, 'default': 5000, 'step': 100},
    'equity_ratio': {'min': 0.05, 'max': 0.95, 'default': 0.30, 'step': 0.01},
    'debt_rate': {'min': 0.01, 'max': 0.25, 'default': 0.09, 'step': 0.005},
    'discount_rate': {'min': 0.05, 'max': 0.30, 'default': 0.15, 'step': 0.005},
    'revenue_growth': {'min': -0.05, 'max': 0.15, 'default': 0.03, 'step': 0.005},
    'project_period': {'min': 10, 'max': 40, 'default': 25, 'step': 1},
    'op_cost_ratio': {'min': 0.10, 'max': 0.80, 'default': 0.35, 'step': 0.01},
}

# ===== SCENARIO ADJUSTMENTS =====
SCENARIO_ADJUSTMENTS = {
    'Base Case': {
        'capex_adj': 0.0,
        'revenue_adj': 0.0,
        'opex_adj': 0.0,
        'debt_rate_adj': 0.0,
    },
    'Downside': {
        'capex_adj': 0.10,  # 10% capex overrun
        'revenue_adj': -0.15,  # 15% revenue drop
        'opex_adj': 0.05,  # 5% opex increase
        'debt_rate_adj': 0.01,  # 1% rate increase
    },
    'Upside': {
        'capex_adj': -0.05,  # 5% capex saving
        'revenue_adj': 0.10,  # 10% revenue boost
        'opex_adj': -0.05,  # 5% opex saving
        'debt_rate_adj': -0.005,  # 0.5% rate decrease
    },
}

# ===== STRESS TEST PARAMETERS =====
STRESS_TESTS = {
    'revenue_shock': [-0.30, -0.20, -0.10, 0, 0.10],  # -30% to +10%
    'opex_shock': [-0.10, 0, 0.10, 0.20, 0.30],  # -10% to +30%
    'debt_rate_shock': [-0.02, -0.01, 0, 0.01, 0.02],  # -2% to +2%
}

# ===== FINANCIAL THRESHOLDS & BENCHMARKS =====
FINANCIAL_BENCHMARKS = {
    'min_dscr': 1.25,  # Minimum DSCR required
    'target_dscr': 1.50,  # Target DSCR
    'min_equity_irr': 0.10,  # Minimum 10% IRR for equity
    'acceptable_npv': 0.0,  # Project should have non-negative NPV
}

# ===== EXPORT/REPORTING CONFIG =====
EXPORT_CONFIG = {
    'pdf_enabled': True,
    'excel_enabled': True,
    'include_charts': True,
    'include_cashflow_table': True,
    'include_sensitivity': True,
    'include_scenarios': True,
    'pdf_font_size': 11,
}

# ===== UI/UX CONFIG =====
UI_CONFIG = {
    'number_format': '.2f',
    'currency_symbol': '$',
    'thousand_separator': ',',
    'chart_height': 500,
    'metric_box_color': '#f0f2f6',
    'warning_threshold_dscr': 1.25,
}

# ===== LOGGING & DEBUG =====
DEBUG_MODE = False
LOG_LEVEL = 'INFO'
LOG_FILE = 'ppp_model.log'
