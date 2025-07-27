
import streamlit as st
import pandas as pd
from ingest.acled import fetch_acled_data
from ai.forecast import prepare_data, forecast
import plotly.express as px

st.set_page_config(page_title="HEWRI Phase 2", layout="wide")
st.title("📊 HEWRI Phase 2 – Forecasting Dashboard")

st.sidebar.header("Filter Data")
days = st.sidebar.slider("Days of History", 30, 365, 180)
df = fetch_acled_data(days_back=days)

if not df.empty:
    df["event_date"] = pd.to_datetime(df["event_date"])
    df["fatalities"] = pd.to_numeric(df["fatalities"], errors="coerce").fillna(0).astype(int)
    df["events"] = 1
    st.success(f"Loaded {len(df)} conflict events")

    # Basic time series preview
    if st.checkbox("📈 Show Overall Forecast"):
        ts = df[["event_date", "fatalities"]].rename(columns={"event_date": "ds", "fatalities": "y"})
        ts = ts.groupby("ds").sum().reset_index()
        model_out = forecast(ts, days=30)
        fig = px.line(model_out, x="ds", y="yhat", title="Total Fatalities Forecast")
        st.plotly_chart(fig)
else:
    st.warning("No data loaded.")
