# 🏢 PPP Financial Modeling Platform

**Professional-Grade Financial Simulation for Public-Private Partnership (PPP) Projects**

![Version](https://img.shields.io/badge/version-2.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red)

---

## 📋 Overview

A world-class financial modeling platform for analyzing Public-Private Partnership (PPP) projects. Built with Python and Streamlit, this application provides:

✅ **Real-time Financial Simulations** - Instant recalculations with interactive sliders  
✅ **Advanced Analytics** - Sensitivity analysis, scenario comparison, stress testing  
✅ **Professional Metrics** - NPV, IRR, DSCR, Payback Period, Profitability Index  
✅ **Beautiful Visualizations** - Interactive Plotly charts for cashflow, DSCR, debt schedule  
✅ **Export Capabilities** - PDF & Excel report generation (coming soon)  
✅ **Enterprise-Grade Code** - Modular architecture, comprehensive logging, error handling  

---

## 🚀 Features

### Core Financial Analysis
- **Cashflow Modeling** - 25-year project period with granular annual calculations
- **Debt Service Coverage Ratio (DSCR)** - Track debt repayment ability over time
- **NPV & IRR Calculations** - Time-value of money analysis
- **Tax Calculation** - Support for loss carryforward logic
- **Scenario Analysis** - Base Case, Downside, Upside scenarios

### Advanced Features
- **Sensitivity Analysis** - Test impact of individual parameter changes
- **Multi-Scenario Comparison** - Side-by-side comparison of scenarios
- **Real-Time Updates** - Instant recalculation on parameter changes
- **Professional UI/UX** - Tabbed interface, responsive design, custom CSS
- **Comprehensive Metrics** - Min/Avg DSCR, Payback Period, Profitability Index

---

## 🛠 Tech Stack

### Core Framework
- **Streamlit 1.28+** - Web UI framework
- **Pandas 2.0** - Data manipulation
- **NumPy 1.26** - Numerical computing
- **NumPy-Financial 1.0** - Financial calculations (NPV, IRR)
- **Plotly 5.17** - Interactive visualizations

### Advanced Libraries
- **ReportLab** - PDF generation
- **XLSXWriter** - Excel export
- **Python-PPTX** - PowerPoint reports
- **Loguru** - Advanced logging

---

## 📦 Project Structure

```
ppp-decision/
├── config.py                  # Centralized configuration & constants
├── financial_engine.py        # Core calculation engine
├── streamlit_app.py          # Main Streamlit application
├── requirements.txt           # Python dependencies
├── README.md                 # This file
└── .devcontainer/            # Development container setup
```

### Key Modules

**config.py** - Configuration Management
- Financial parameter ranges & defaults
- Scenario adjustments
- Stress test parameters
- UI/UX configuration

**financial_engine.py** - Core Calculation Logic
- `PPPFinancialEngine` class - Main calculation engine
- `ProjectCashflow` dataclass - Results container
- Methods:
  - `calculate_project_cashflow()` - Full financial analysis
  - `sensitivity_analysis()` - Single-variable sensitivity
  - `scenario_analysis()` - Multi-scenario comparison

**streamlit_app.py** - User Interface
- Responsive sidebar input controls
- Real-time metric display
- Interactive charting with tabs
- Detailed cashflow table
- Optional sensitivity/scenario analysis

---

## 🚀 Getting Started

### Requirements
- Python 3.8+
- pip or conda

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vythanhtra/PPP-decision.git
   cd PPP-decision
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running Locally

```bash
streamlit run streamlit_app.py
```

The app will open at `http://localhost:8501`

### Deploying to Streamlit Cloud

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Select your repository
4. Deploy!

---

## 📊 User Guide

### Setting Parameters

Use the left sidebar to configure:

| Parameter | Range | Default | Description |
|-----------|-------|---------|-------------|
| Total Investment | $500M - $20B | $5B | Total project capex |
| Equity Ratio | 5% - 95% | 30% | Equity financing % |
| Debt Rate | 1% - 25% | 9% | Annual interest rate |
| Discount Rate | 5% - 30% | 15% | WACC for NPV |
| Revenue Growth | -5% - 15% | 3% | Annual growth rate |
| Op Cost Ratio | 10% - 80% | 35% | OpEx as % of Revenue |
| Project Period | 10 - 40 years | 25 | Concession period |
| Tax Rate | 0% - 50% | 20% | Corporate tax rate |

### Interpreting Results

**Key Metrics Dashboard**
- **NPV**: Positive = Project adds value
- **IRR**: Higher = Better returns
- **Min DSCR**: Should be ≥ 1.25x (lender requirement)
- **Avg DSCR**: Should be ≥ 1.50x (healthy)

**Charts**
- **Revenue/Cost/EBITDA**: Trend over project period
- **DSCR Trend**: Monitor debt coverage trajectory
- **Debt Schedule**: Outstanding debt remaining each year

---

## 🧪 Advanced Analysis

### Sensitivity Analysis

Test how changing one variable affects NPV & DSCR:
1. Check "Sensitivity Analysis" checkbox
2. Select variable to test
3. Set test range
4. Click "Run Sensitivity"

### Scenario Comparison

Compare Base Case vs Downside vs Upside:
1. Check "Scenario Comparison" checkbox
2. View side-by-side KPI comparison
3. Identify best/worst case outcomes

---

## 📝 License

MIT License - See LICENSE file for details

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

---

## 📧 Support

For issues, questions, or suggestions:
- Open an [GitHub Issue](https://github.com/vythanhtra/PPP-decision/issues)
- Email: [vythanhtra@example.com](mailto:vythanhtra@example.com)

---

## 🙏 Acknowledgments

- **Streamlit** - Amazing web framework for Python
- **Plotly** - Beautiful interactive visualizations
- **NumPy-Financial** - Reliable financial calculations

---

**Made with ❤️ by PPP Financial Team**

v2.0.0 | December 2025
