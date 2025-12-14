import streamlit as st
import pandas as pd
import numpy as np
import numpy_financial as npf
import plotly.graph_objects as go

st.set_page_config(page_title="PPP Financial Model", page_icon="📊", layout="wide")

st.title("PPP Financial Modeling Dashboard")
st.markdown("Financial simulation tool for PPP projects")

def run_investment_grade_model(inputs, scenario_adj):
    total_investment = inputs['total_investment'] * (1 + scenario_adj['capex_adj'])
    initial_revenue = inputs['initial_revenue'] * (1 + scenario_adj['revenue_adj'])
    op_cost_ratio = inputs['op_cost_ratio'] / 100 * (1 + scenario_adj['opex_adj'])
    debt_rate = inputs['debt_rate'] * (1 + scenario_adj['debt_rate_adj']) / 100
    project_period = int(inputs['project_period'])
    equity_ratio = inputs['equity_ratio'] / 100
    revenue_growth = inputs['revenue_growth'] / 100
    inflation = inputs['inflation'] / 100
    tax_rate = inputs['tax_rate'] / 100
    discount_rate = inputs['discount_rate'] / 100
    depreciation_period = int(inputs['depreciation_period'])
    
    equity_investment = total_investment * equity_ratio
    debt_investment = total_investment * (1 - equity_ratio)
    
    years = np.arange(1, project_period + 1)
    df = pd.DataFrame(index=pd.Index(years, name='Year'))
    
    df['Revenue'] = initial_revenue * (1 + revenue_growth) ** (years - 1)
    df['OpCost'] = df['Revenue'] * op_cost_ratio * (1 + inflation) ** (years - 1)
    df['EBITDA'] = df['Revenue'] - df['OpCost']
    
    annual_depreciation = total_investment / depreciation_period
    df['Depreciation'] = np.where(years <= depreciation_period, annual_depreciation, 0)
    df['EBIT'] = df['EBITDA'] - df['Depreciation']
    
    df['Debt_Balance_Start'] = np.maximum(0, debt_investment - debt_investment * (project_period - years + 1) / project_period)
    df['Interest_Payment'] = df['Debt_Balance_Start'] * debt_rate
    df['Principal_Repayment'] = np.where(df['Debt_Balance_Start'] > 0, debt_investment / project_period, 0)
    
    df['EBT'] = df['EBIT'] - df['Interest_Payment']
    df['Taxable_Income'] = 0.0
    df['Tax'] = 0.0
    
    cumulative_loss = 0
    for year in df.index:
        income_before_loss = df.loc[year, 'EBT']
        loss_to_use = min(cumulative_loss, max(0, -income_before_loss))
        taxable_income = max(0, income_before_loss + loss_to_use)
        df.loc[year, 'Taxable_Income'] = taxable_income
        df.loc[year, 'Tax'] = max(0, taxable_income * tax_rate)
        
        if income_before_loss < 0:
            cumulative_loss += abs(income_before_loss)
        else:
            cumulative_loss -= loss_to_use
    
    df['CFAds'] = df['EBITDA'] - df['Tax']
    df['Debt_Service'] = df['Principal_Repayment'] + df['Interest_Payment']
    df['DSCR'] = np.where(df['Debt_Service'] > 0, df['CFAds'] / df['Debt_Service'], np.inf)
    
    project_cashflow = [-total_investment] + df['CFAds'].tolist()
    equity_cashflow = [-equity_investment] + (df['CFAds'].tolist() if 'Dividends' in df else [-equity_investment] * project_period)
    
    project_npv = npf.npv(discount_rate, project_cashflow)
    min_dscr = df['DSCR'][df['DSCR'] != np.inf].min()
    avg_dscr = df['DSCR'][df['DSCR'] != np.inf].mean()
    
    return {'cashflow_df': df, 'kpis': {'project_npv': project_npv, 'min_dscr': min_dscr, 'avg_dscr': avg_dscr}}

st.sidebar.header("Model Parameters")
total_inv = st.sidebar.slider("Total Investment ($M)", 1000, 10000, 5000)
equity_pct = st.sidebar.slider("Equity Ratio (%)", 10, 90, 30)
debt_rate = st.sidebar.slider("Debt Rate (%)", 1.0, 20.0, 9.0)
discount_rate = st.sidebar.slider("Discount Rate (%)", 5.0, 30.0, 15.0)
rev_growth = st.sidebar.slider("Revenue Growth (%)", 0.0, 10.0, 3.0)
scenario = st.sidebar.radio("Scenario", ["Base Case", "Downside"])

if scenario == "Base Case":
    scenario_adj = {'capex_adj': 0, 'revenue_adj': 0, 'opex_adj': 0, 'debt_rate_adj': 0}
else:
    scenario_adj = {'capex_adj': 0.1, 'revenue_adj': -0.15, 'opex_adj': 0.05, 'debt_rate_adj': 1.0}

inputs = {
    'total_investment': total_inv,
    'project_period': 25,
    'depreciation_period': 25,
    'equity_ratio': equity_pct,
    'debt_rate': debt_rate,
    'discount_rate': discount_rate,
    'tax_rate': 20.0,
    'initial_revenue': 1000.0,
    'revenue_growth': rev_growth,
    'op_cost_ratio': 35.0,
    'inflation': 3.0
}

if st.sidebar.button("Run Calculation"):
    results = run_investment_grade_model(inputs, scenario_adj)
    
    st.subheader("Key Financial Metrics")
    col1, col2, col3 = st.columns(3)
    col1.metric("NPV", f"${results['kpis']['project_npv']:.2f}M")
    col2.metric("Min DSCR", f"{results['kpis']['min_dscr']:.2f}x")
    col3.metric("Avg DSCR", f"{results['kpis']['avg_dscr']:.2f}x")
    
    st.subheader("Cashflow Table")
    st.dataframe(results['cashflow_df'].head(10))
    
    st.subheader("DSCR Chart")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=results['cashflow_df'].index, y=results['cashflow_df']['DSCR'], mode="lines+markers", name="DSCR"))
    fig.add_hline(y=1.20, line_dash="dot")
    st.plotly_chart(fig, use_container_width=True)
