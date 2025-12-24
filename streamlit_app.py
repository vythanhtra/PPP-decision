# streamlit_app.py - Professional PPP Financial Modeling Platform
# Enhanced version with real-time calculations, advanced features, and professional UI

import streamlit as st
import pandas as pd
import numpy as np
from financial_engine import PPPFinancialEngine
from config import (
    APP_TITLE, APP_DESCRIPTION, APP_VERSION, PARAMETER_RANGES, 
    SCENARIO_ADJUSTMENTS, FINANCIAL_BENCHMARKS, UI_CONFIG
)
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ===== PAGE CONFIG =====
st.set_page_config(
    page_title=f"{APP_TITLE} v{APP_VERSION}",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===== CUSTOM CSS =====
st.markdown("""
    <style>
    .metric-box {background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;}
    .metric-value {font-size: 32px; font-weight: bold; color: #1f77b4;}
    .metric-label {font-size: 14px; color: #666;}
    .warning-box {background-color: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107;}
    .success-box {background-color: #d4edda; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;}
    </style>
""", unsafe_allow_html=True)

# ===== STATE MANAGEMENT =====
if 'calculation_done' not in st.session_state:
    st.session_state.calculation_done = False
if 'last_results' not in st.session_state:
    st.session_state.last_results = None

# ===== HEADER & TITLE =====
col1, col2 = st.columns([3, 1])
with col1:
    st.title(f"🏢 {APP_TITLE}")
    st.markdown(f"*{APP_DESCRIPTION}*")
with col2:
    st.markdown(f"**v{APP_VERSION}** | {datetime.now().strftime('%d %b %Y')}")

st.divider()

# ===== SIDEBAR - INPUT PARAMETERS =====
with st.sidebar:
    st.header("📋 Model Parameters")
    
    # Scenario Selection
    scenario = st.radio(
        "Scenario",
        list(SCENARIO_ADJUSTMENTS.keys()),
        help="Select Base Case, Downside, or Upside scenario"
    )
    
    st.subheader("Financial Inputs")
    
    # Total Investment
    total_inv = st.slider(
        "Total Investment ($M)",
        min_value=int(PARAMETER_RANGES['total_investment']['min']),
        max_value=int(PARAMETER_RANGES['total_investment']['max']),
        value=int(PARAMETER_RANGES['total_investment']['default']),
        step=int(PARAMETER_RANGES['total_investment']['step']),
        help="Total project investment required"
    )
    
    # Equity Ratio
    equity_pct = st.slider(
        "Equity Ratio (%)",
        min_value=int(PARAMETER_RANGES['equity_ratio']['min']*100),
        max_value=int(PARAMETER_RANGES['equity_ratio']['max']*100),
        value=int(PARAMETER_RANGES['equity_ratio']['default']*100),
        step=1,
        help="Percentage of investment financed by equity"
    ) / 100
    
    # Debt Rate
    debt_rate = st.slider(
        "Debt Rate (%)",
        min_value=1.0,
        max_value=25.0,
        value=9.0,
        step=0.5,
        help="Annual interest rate on debt"
    )
    
    # Discount Rate
    discount_rate = st.slider(
        "Discount Rate (%)",
        min_value=5.0,
        max_value=30.0,
        value=15.0,
        step=0.5,
        help="WACC for NPV calculation"
    )
    
    # Revenue Growth
    rev_growth = st.slider(
        "Revenue Growth (%)",
        min_value=-5.0,
        max_value=15.0,
        value=3.0,
        step=0.5,
        help="Annual revenue growth rate"
    )
    
    st.subheader("Advanced Settings")
    
    # Operating Cost Ratio
    op_cost_ratio = st.slider(
        "Operating Cost Ratio (%)",
        min_value=10.0,
        max_value=80.0,
        value=35.0,
        step=1.0,
        help="Annual operating costs as % of revenue"
    )
    
    # Project Period
    project_period = st.slider(
        "Project Period (years)",
        min_value=10,
        max_value=40,
        value=25,
        step=1,
        help="Total project concession period"
    )
    
    # Tax Rate
    tax_rate = st.slider(
        "Tax Rate (%)",
        min_value=0.0,
        max_value=50.0,
        value=20.0,
        step=1.0,
        help="Corporate income tax rate"
    )
    
    st.divider()
    
    # Analysis Options
    st.subheader("🔍 Analysis Options")
    show_sensitivity = st.checkbox("Sensitivity Analysis", value=False)
    show_comparison = st.checkbox("Scenario Comparison", value=False)
    show_details = st.checkbox("Show Detailed Cashflow", value=True)
    
    st.divider()
    
    # Calculate Button
    if st.button("🚀 Calculate", use_container_width=True):
        st.session_state.calculation_done = True
        st.rerun()

# ===== MAIN CONTENT AREA =====
if st.session_state.calculation_done:
    # Prepare inputs
    inputs = {
        'total_investment': total_inv,
        'project_period': project_period,
        'depreciation_period': project_period,
        'equity_ratio': equity_pct,
        'debt_rate': debt_rate / 100,
        'discount_rate': discount_rate / 100,
        'tax_rate': tax_rate / 100,
        'initial_revenue': 1000.0,
        'revenue_growth': rev_growth / 100,
        'op_cost_ratio': op_cost_ratio / 100,
        'inflation': 0.03
    }
    
    # Calculate
    engine = PPPFinancialEngine(inputs, scenario)
    result = engine.calculate_project_cashflow()
    kpis = result.summary_kpis
    
    st.session_state.last_results = result
    
    # ===== KPI METRICS =====
    st.subheader("📊 Key Financial Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        npv_val = kpis.get('project_npv', 0)
        st.metric(
            "NPV",
            f"${npv_val:,.0f}M",
            delta="Favorable" if npv_val > 0 else "Unfavorable",
            delta_color="normal" if npv_val > 0 else "off"
        )
    
    with col2:
        irr_val = kpis.get('project_irr')
        st.metric(
            "IRR",
            f"{irr_val*100:.2f}%" if irr_val else "N/A",
            help="Internal Rate of Return"
        )
    
    with col3:
        min_dscr = kpis.get('min_dscr', 0)
        is_healthy = min_dscr >= FINANCIAL_BENCHMARKS['min_dscr']
        st.metric(
            "Min DSCR",
            f"{min_dscr:.2f}x",
            delta="✅ Healthy" if is_healthy else "⚠️ Risk",
            delta_color="normal" if is_healthy else "off"
        )
    
    with col4:
        avg_dscr = kpis.get('avg_dscr', 0)
        st.metric(
            "Avg DSCR",
            f"{avg_dscr:.2f}x",
            help="Average Debt Service Coverage Ratio"
        )
    
    st.divider()
    
    # ===== VISUALIZATIONS =====
    st.subheader("📈 Financial Analysis Charts")
    
    tab1, tab2, tab3 = st.tabs(["Cashflow", "DSCR Trend", "Debt Schedule"])
    
    df = result.cashflow_df
    
    with tab1:
        # Cumulative Cashflow Chart
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=df.index, y=df['Revenue'], name='Revenue', marker_color='#2ecc71'
        ))
        fig.add_trace(go.Bar(
            x=df.index, y=df['OpCost'], name='Operating Cost', marker_color='#e74c3c'
        ))
        fig.add_trace(go.Bar(
            x=df.index, y=df['EBITDA'], name='EBITDA', marker_color='#3498db'
        ))
        fig.update_layout(
            title="Revenue, Cost & EBITDA Trend",
            barmode='group',
            height=500,
            hovermode='x unified'
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        # DSCR Chart
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index, y=df['DSCR'],
            mode='lines+markers', name='DSCR',
            line=dict(color='#9b59b6', width=3),
            marker=dict(size=6)
        ))
        fig.add_hline(
            y=FINANCIAL_BENCHMARKS['min_dscr'],
            line_dash="dash", line_color="red",
            annotation_text="Min Threshold"
        )
        fig.update_layout(
            title="Debt Service Coverage Ratio Trend",
            height=500,
            hovermode='x unified',
            yaxis_title="DSCR",
            xaxis_title="Year"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Debt Schedule
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df.index, y=df['Debt_Balance_Start'],
            fill='tozeroy', name='Debt Balance',
            line=dict(color='#e67e22', width=3)
        ))
        fig.update_layout(
            title="Debt Balance Schedule",
            height=500,
            yaxis_title="Outstanding Debt ($M)",
            xaxis_title="Year"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    st.divider()
    
    # ===== DETAILED CASHFLOW TABLE =====
    if show_details:
        st.subheader("📋 Detailed Cashflow Table")
        display_cols = ['Revenue', 'OpCost', 'EBITDA', 'EBIT', 'Tax', 'CFAds', 'Debt_Service', 'DSCR']
        st.dataframe(
            df[display_cols].style.format('{:.2f}'),
            use_container_width=True,
         height=None,   
        )
    
    st.divider()
    
    # ===== SENSITIVITY ANALYSIS =====
    if show_sensitivity:
        st.subheader("🎯 Sensitivity Analysis")
        sensitivity_var = st.selectbox(
            "Select Variable to Test",
            ['discount_rate', 'debt_rate', 'revenue_growth', 'op_cost_ratio']
        )
        test_range = st.slider(
            f"Test range for {sensitivity_var}",
            0.0, 1.0, (0.3, 0.7)
        )
        if st.button("Run Sensitivity"):
            test_values = np.linspace(test_range[0], test_range[1], 5)
            sens_results = engine.sensitivity_analysis(sensitivity_var, test_values)
            st.dataframe(sens_results, use_container_width=True)
    
    # ===== SCENARIO COMPARISON =====
    if show_comparison:
        st.subheader("⚖️ Scenario Comparison")
        scenarios = list(SCENARIO_ADJUSTMENTS.keys())
        comparison = engine.scenario_analysis(scenarios)
        comparison_df = pd.DataFrame(comparison).T
        st.dataframe(comparison_df.style.format('{:.2f}'), use_container_width=True)
else:
    st.info("👈 Configure parameters in the sidebar and click **Calculate** to generate results")
