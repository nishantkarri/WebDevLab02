import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="Water Intake Dashboard", page_icon="💧", layout="wide")

st.title("💧 Water Intake Dashboard — Lab 02")
st.write("Track your weekly water intake in a CSV, and compare it with a simple JSON dataset for your daily mood (1–10).")

st.subheader("How this app is organized")
st.markdown(
    """
- **Survey**: enter liters for each day (Mon–Sun). This writes to `data.csv`.
- **Visuals**: see three graphs using **data.csv** (water) and **data.json** (mood).
- **data.json**: a small manual dataset for mood (it does not update automatically).
"""
)

st.subheader("What to do")
st.markdown(
    """
1. Open **Survey** and submit one or more weekly entries.
2. Open **Visuals** to explore:
   - Line chart of weekly average liters over time (CSV).
   - Bar chart of mood (1–10) with simple adjustments (JSON).
   - Scatter plot comparing Monday vs Sunday liters (CSV).
"""
)

BASE = Path(__file__).resolve().parent
csv_path = BASE / "data.csv"
json_path = BASE / "data.json"

left, right = st.columns(2)

with left:
    st.markdown("**CSV status (data.csv):**")
    try:
        df = pd.read_csv(csv_path)
        st.write("Rows:", len(df))
        st.dataframe(df.tail(5), use_container_width=True)
    except:
        st.info("No CSV found yet. Add entries on the **Survey** page.")

with right:
    st.markdown("**JSON status (data.json):**")
    try:
        text = json_path.read_text(encoding="utf-8")
        st.code(text, language="json")
    except:
        st.info("No data.json found yet. Create or edit it for Part 2.")

st.divider()
st.caption("Tip: If you see no charts, add a few entries in **Survey** first.")
