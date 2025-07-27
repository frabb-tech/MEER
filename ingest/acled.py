
import requests
import pandas as pd
from datetime import datetime, timedelta

ACLED_API_URL = "https://api.acleddata.com/acled/read"
API_KEY = "yMybbn!rLoARi2nm1olV"

TARGET_COUNTRIES = [
    "SYR", "IRQ", "LBN", "JOR", "ISR", "PSE", "TUR", "AFG", "ARM", "GEO",
    "AZE", "IRN", "YEM", "SAU", "EGY", "SDN", "LBY", "ALB", "BGR", "BIH",
    "SRB", "MKD", "ROU", "MDA"
]

def fetch_acled_data(days_back=7):
    start_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    all_data = []
    for iso3 in TARGET_COUNTRIES:
        params = {
            "key": API_KEY,
            "iso3": iso3,
            "event_date": f">{start_date}",
            "limit": 5000,
            "admin_level": 1
        }
        r = requests.get(ACLED_API_URL, params=params)
        if r.status_code == 200:
            all_data.extend(r.json().get("data", []))
        else:
            print(f"Failed for {iso3}")
    return pd.DataFrame(all_data)
