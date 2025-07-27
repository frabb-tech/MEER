
from prophet import Prophet
import pandas as pd

def prepare_data(df, metric="fatalities"):
    df = df[["event_date", metric]].copy()
    df = df.rename(columns={"event_date": "ds", metric: "y"})
    df = df.groupby("ds").sum().reset_index()
    return df

def forecast(df, days=30):
    model = Prophet()
    model.fit(df)
    future = model.make_future_dataframe(periods=days)
    forecast = model.predict(future)
    return forecast
