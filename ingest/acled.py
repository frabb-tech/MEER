
import requests
import pandas as pd
from datetime import datetime, timedelta

BASE_URL = "https://api.acleddata.com/acled/read/"
API_PARAMS = "?key=yMybbn!rLoARi2nm1olV&email=fady_abboud@wvi.org"

TARGET_COUNTRIES = [
    "SYR", "IRQ", "LBN", "JOR", "ISR", "PSE", "TUR", "AFG", "ARM", "GEO",
    "AZE", "IRN", "YEM", "SAU", "EGY", "SDN", "LBY", "ALB", "BGR", "BIH",
    "SRB", "MKD", "ROU", "MDA"
]

def fetch_acled_data(days_back=7):
    start_date = (datetime.utcnow() - timedelta(days=days_back)).strftime("%Y-%m-%d")
    all_data = []
    for iso3 in TARGET_COUNTRIES:
        url = f"{BASE_URL}{API_PARAMS}&iso3={iso3}&event_date=>{start_date}&limit=5000&admin_level=1"
        try:
            r = requests.get(url)
            json_data = r.json()
            if json_data.get("success") == "0":
                print(f"API error: {json_data.get('message')}")
                continue
            all_data.extend(json_data.get("data", []))
        except Exception as e:
            print(f"Error fetching ACLED data for {iso3}: {e}")
    return pd.DataFrame(all_data)
