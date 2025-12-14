# PPP Loan Analysis Streamlit Application

## Gioi thieu
Ung dung phan tich khoan vay PPP (Paycheck Protection Program) duoc xay dung bang Streamlit.

## Yeu cau
streamlit==1.28.1
pandas==2.0.0
numpy>=1.24.0
numpy-financial>=1.0.0
plotly>=5.17.0

## Cai dat Local

# Tao virtual environment
python -m venv venv
source venv/bin/activate

# Cai dat thu vien
pip install -r requirements.txt

# Chay ung dung
streamlit run ppp_app.py

Ung dung se mo tai http://localhost:8501

## Trien khai tren Streamlit Cloud

1. Fork repository hoac tai len GitHub
2. Truy cap https://share.streamlit.io
3. Ket noi GitHub repository
4. Chon file: ppp_app.py
5. Ung dung se tu dong trien khai

## Ho tro

Neu gap van de, vui long kiem tra:
- Python >= 3.7 da duoc cai dat
- Tat ca thu vien trong requirements.txt da duoc cai dat
- Port 8501 khong bi chiem dung (Streamlit mac dinh)
