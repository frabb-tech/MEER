
import streamlit as st
from ingest.acled import fetch_acled_data
from ai.forecast import prepare_data, forecast
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="HEWRI – Conflict Dashboard", layout="wide")
st.title("🛰️ HEWRI: Conflict Early Warning System (ACLED Data)")

st.sidebar.header("Filters")
days = st.sidebar.slider("Days Back", 1, 30, 7)
country_filter = st.sidebar.multiselect("Select Countries", options=[
    "Syria", "Iraq", "Lebanon", "Jordan", "Israel", "Palestine", "Turkey",
    "Afghanistan", "Armenia", "Georgia", "Azerbaijan", "Iran", "Yemen", "Saudi Arabia",
    "Egypt", "Sudan", "Libya", "Albania", "Bulgaria", "Bosnia", "Serbia", "North Macedonia", "Romania", "Moldova"
], default=[])

with st.spinner("Fetching conflict data..."):
    df = fetch_acled_data(days)
    if not df.empty:
        df["fatalities"] = pd.to_numeric(df["fatalities"], errors="coerce").fillna(0).astype(int)
        df["event_date"] = pd.to_datetime(df["event_date"])
        df["events"] = 1
        df_filtered = df[df["country"].isin(country_filter)] if country_filter else df

        st.success(f"Loaded {len(df_filtered)} events.")
        st.metric("Total Events", len(df_filtered))
        st.metric("Total Fatalities", df_filtered['fatalities'].sum())
        st.dataframe(df_filtered[["event_date", "country", "admin1", "event_type", "fatalities"]])

        csv = df_filtered.to_csv(index=False).encode("utf-8")
        st.download_button("Download CSV", csv, "acled_events.csv", "text/csv")

        if st.checkbox("📈 Show Forecasts"):
            selected_country = st.selectbox("Choose a Country", sorted(df_filtered["country"].unique()))
            admin1_list = sorted(df_filtered[df_filtered["country"] == selected_country]["admin1"].dropna().unique())
            selected_admin1 = st.selectbox("Optional: Choose Admin1", ["All"] + admin1_list)
            metric = st.radio("Forecast metric", ["fatalities", "events"], horizontal=True)

            country_df = df_filtered[df_filtered["country"] == selected_country]
            if selected_admin1 != "All":
                country_df = country_df[country_df["admin1"] == selected_admin1]

            if len(country_df) >= 5:
                data = prepare_data(country_df, metric=metric)
                result = forecast(data, days=7)

                fig = px.line(result, x="ds", y="yhat", title=f"{metric.capitalize()} Forecast for {selected_country} - {selected_admin1 if selected_admin1 != 'All' else 'All Admin1'}")
                fig.add_scatter(x=result["ds"], y=result["yhat_lower"], mode='lines', name='Lower Bound', line=dict(dash='dot'))
                fig.add_scatter(x=result["ds"], y=result["yhat_upper"], mode='lines', name='Upper Bound', line=dict(dash='dot'))
                st.plotly_chart(fig)
            else:
                st.warning("Not enough data for forecasting. Try selecting a different region.")
    else:
        st.warning("No data found.")
