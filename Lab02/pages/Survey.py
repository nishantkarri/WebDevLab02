import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path

st.set_page_config(page_title="Water Intake Survey", page_icon="💧")
st.title("💧 Water Intake Data Input")

st.write("Enter how many liters of water you drink each day (0–15 liters):")

BASE = Path(__file__).resolve().parents[1]
CSV_PATH = BASE / "data.csv"

if not CSV_PATH.exists():
    df = pd.DataFrame(columns=["timestamp", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    df.to_csv(CSV_PATH, index=False)

mon = st.slider("Mon (liters)", 0.0, 15.0, 0.0, 0.1)
tue = st.slider("Tue (liters)", 0.0, 15.0, 0.0, 0.1)
wed = st.slider("Wed (liters)", 0.0, 15.0, 0.0, 0.1)
thu = st.slider("Thu (liters)", 0.0, 15.0, 0.0, 0.1)
fri = st.slider("Fri (liters)", 0.0, 15.0, 0.0, 0.1)
sat = st.slider("Sat (liters)", 0.0, 15.0, 0.0, 0.1)
sun = st.slider("Sun (liters)", 0.0, 15.0, 0.0, 0.1)

submit = st.button("Submit Weekly Data")

if submit:
    new_row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Mon": mon,
        "Tue": tue,
        "Wed": wed,
        "Thu": thu,
        "Fri": fri,
        "Sat": sat,
        "Sun": sun
    }
    df = pd.read_csv(CSV_PATH)
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_csv(CSV_PATH, index=False)
    st.success("✅ Your weekly water intake has been recorded!")

st.divider()
st.write("Your recorded data:")
try:
    df_display = pd.read_csv(CSV_PATH)
    st.dataframe(df_display, use_container_width=True)
except:
    st.info("No data recorded yet.")
