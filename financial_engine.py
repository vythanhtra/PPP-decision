# financial_engine.py - Core Financial Calculation Engine
# Handles all financial modeling and calculations for PPP projects

import numpy as np
import pandas as pd
import numpy_financial as npf
from typing import Dict, List, Tuple, Any
import logging
from dataclasses import dataclass
from config import (
    DefaultFinancialParams, SCENARIO_ADJUSTMENTS, 
    STRESS_TESTS, FINANCIAL_BENCHMARKS
)

logger = logging.getLogger(__name__)

@dataclass
class ProjectCashflow:
    """Store project cashflow results"""
    cashflow_df: pd.DataFrame
    annual_metrics: Dict[str, Any]
    summary_kpis: Dict[str, float]

class PPPFinancialEngine:
    """Core calculation engine for PPP financial modeling"""
    
    def __init__(self, params: Dict[str, float], scenario: str = 'Base Case'):
        self.params = params
        self.scenario = scenario
        self.scenario_adj = SCENARIO_ADJUSTMENTS.get(scenario, SCENARIO_ADJUSTMENTS['Base Case'])
        self.results = None
        
    def calculate_project_cashflow(self) -> ProjectCashflow:
        """Calculate full project cashflow over project period"""
        # Apply scenario adjustments
        adj_params = self._apply_scenario_adjustments()
        
        # Initialize cashflow dataframe
        years = np.arange(1, adj_params['project_period'] + 1)
        df = pd.DataFrame(index=pd.Index(years, name='Year'))
        
        # Revenue & Operating Cost
        df['Revenue'] = adj_params['initial_revenue'] * (1 + adj_params['revenue_growth']) ** (years - 1)
        df['OpCost'] = df['Revenue'] * adj_params['op_cost_ratio'] * (1 + adj_params['inflation']) ** (years - 1)
        df['EBITDA'] = df['Revenue'] - df['OpCost']
        
        # Depreciation & Tax
        annual_depreciation = adj_params['total_investment'] / adj_params['depreciation_period']
        df['Depreciation'] = np.where(years <= adj_params['depreciation_period'], annual_depreciation, 0)
        df['EBIT'] = df['EBITDA'] - df['Depreciation']
        
        # Debt Schedule & Interest
        debt_investment = adj_params['total_investment'] * (1 - adj_params['equity_ratio'])
        annual_principal = debt_investment / adj_params['project_period']
        
        df['Debt_Balance_Start'] = np.maximum(0, debt_investment - annual_principal * (years - 1))
        df['Interest_Payment'] = df['Debt_Balance_Start'] * adj_params['debt_rate']
        df['Principal_Repayment'] = np.where(df['Debt_Balance_Start'] > 0, annual_principal, 0)
        df['Debt_Service'] = df['Interest_Payment'] + df['Principal_Repayment']
        
        # Tax Calculation with Loss Carryforward
        df['EBT'] = df['EBIT'] - df['Interest_Payment']
        df['Taxable_Income'], df['Tax'] = self._calculate_tax_with_loss_carryforward(df, adj_params['tax_rate'])
        
        # Cash Flow to Equity & Debt Service Coverage
        df['CFAds'] = df['EBITDA'] - df['Tax']  # Cash Flow Available for Debt Service
        df['DSCR'] = np.where(df['Debt_Service'] > 0, df['CFAds'] / df['Debt_Service'], np.inf)
        
        # Calculate summary KPIs
        kpis = self._calculate_kpis(df, adj_params)
        
        return ProjectCashflow(
            cashflow_df=df,
            annual_metrics=df.to_dict('list'),
            summary_kpis=kpis
        )
    
    def _apply_scenario_adjustments(self) -> Dict[str, float]:
        """Apply scenario adjustments to base parameters"""
        adj_params = self.params.copy()
        adj_params['total_investment'] *= (1 + self.scenario_adj['capex_adj'])
        adj_params['initial_revenue'] *= (1 + self.scenario_adj['revenue_adj'])
        adj_params['op_cost_ratio'] *= (1 + self.scenario_adj['opex_adj'])
        adj_params['debt_rate'] *= (1 + self.scenario_adj['debt_rate_adj'])
        return adj_params
    
    def _calculate_tax_with_loss_carryforward(self, df: pd.DataFrame, tax_rate: float) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate tax with loss carryforward logic"""
        taxable_income = np.zeros(len(df))
        tax = np.zeros(len(df))
        cumulative_loss = 0
        
        for i, year in enumerate(df.index):
            ebt = df.loc[year, 'EBT']
            loss_to_use = min(cumulative_loss, max(0, -ebt))
            taxable = max(0, ebt + loss_to_use)
            taxable_income[i] = taxable
            tax[i] = max(0, taxable * tax_rate)
            
            if ebt < 0:
                cumulative_loss += abs(ebt)
            else:
                cumulative_loss -= loss_to_use
        
        return taxable_income, tax
    
    def _calculate_kpis(self, df: pd.DataFrame, adj_params: Dict[str, float]) -> Dict[str, float]:
        """Calculate key performance indicators"""
        # NPV Calculation
        equity_investment = adj_params['total_investment'] * adj_params['equity_ratio']
        debt_investment = adj_params['total_investment'] * (1 - adj_params['equity_ratio'])
        
        # Project cashflow for NPV
        project_cf = [-adj_params['total_investment']] + df['CFAds'].tolist()
        project_npv = npf.npv(adj_params['discount_rate'], project_cf)
        
        # IRR Calculation
        try:
            project_irr = npf.irr(project_cf)
        except:
            project_irr = np.nan
        
        # DSCR Statistics
        valid_dscr = df['DSCR'][df['DSCR'] != np.inf]
        min_dscr = valid_dscr.min() if len(valid_dscr) > 0 else np.inf
        avg_dscr = valid_dscr.mean() if len(valid_dscr) > 0 else 0
        
        # Payback Period
        cumsum_cf = np.cumsum(project_cf[1:])
        payback_idx = np.where(cumsum_cf >= 0)[0]
        payback_period = payback_idx[0] + 1 if len(payback_idx) > 0 else np.inf
        
        # Profitability Index
        pv_inflows = sum([df['CFAds'].iloc[i] / ((1 + adj_params['discount_rate']) ** (i+1)) for i in range(len(df))])
        profitability_index = pv_inflows / equity_investment if equity_investment > 0 else 0
        
        return {
            'project_npv': project_npv,
            'project_irr': project_irr if not np.isnan(project_irr) else None,
            'min_dscr': float(min_dscr) if min_dscr != np.inf else None,
            'avg_dscr': float(avg_dscr),
            'payback_period': float(payback_period) if payback_period != np.inf else None,
            'profitability_index': profitability_index,
            'equity_npv': project_npv,
            'debt_coverage': float(avg_dscr),
        }
    
    def sensitivity_analysis(self, variable: str, values: List[float]) -> pd.DataFrame:
        """Perform sensitivity analysis on a single variable"""
        results = []
        for value in values:
            test_params = self.params.copy()
            test_params[variable] = value
            engine = PPPFinancialEngine(test_params, self.scenario)
            result = engine.calculate_project_cashflow()
            kpis = result.summary_kpis.copy()
            kpis[variable] = value
            results.append(kpis)
        
        return pd.DataFrame(results)
    
    def scenario_analysis(self, scenarios: List[str]) -> Dict[str, Dict[str, float]]:
        """Compare multiple scenarios"""
        scenario_results = {}
        for scenario in scenarios:
            engine = PPPFinancialEngine(self.params, scenario)
            result = engine.calculate_project_cashflow()
            scenario_results[scenario] = result.summary_kpis
        
        return scenario_results
