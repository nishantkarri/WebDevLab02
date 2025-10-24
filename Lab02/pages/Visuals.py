import streamlit as st
import csv
import json
import os

st.set_page_config(page_title="Visuals", page_icon="📊")
st.title("📊 Water Intake and Mood Graphs")

# Try both common locations so it works no matter where you run Streamlit from
possible_csv = ["data.csv", "../data.csv"]
possible_json = ["data.json", "../data.json"]

def pick_path(paths):
    for p in paths:
        if os.path.exists(p):
            return p
    return None

csv_file = pick_path(possible_csv)
json_file = pick_path(possible_json)

days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def read_csv_data(filename):
    info = []
    try:
        with open(filename, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                info.append(row)
    except:
        info = []
    return info

def read_json_data(filename):
    info = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        if "data_points" in data:
            for item in data["data_points"]:
                info.append({"day": item.get("label", ""), "mood": item.get("value", 0)})
    except:
        info = []
    return info

def safe_number(x):
    try:
        return float(x)
    except:
        return None

def has_day_columns(rows):
    if len(rows) == 0:
        return False
    row = rows[0]
    for d in days:
        if d not in row:
            return False
    return True

def get_weekly_averages(csv_data):
    avgs = []
    for row in csv_data:
        total = 0
        count = 0
        for d in days:
            val = safe_number(row.get(d, 0))
            if val is not None:
                total += val
                count += 1
        if count > 0:
            avgs.append(total / count)
        else:
            avgs.append(0)
    return avgs

def get_day_averages(csv_data):
    totals = {d: 0 for d in days}
    counts = {d: 0 for d in days}
    for row in csv_data:
        for d in days:
            val = safe_number(row.get(d, 0))
            if val is not None:
                totals[d] += val
                counts[d] += 1
    avgs = {}
    for d in days:
        if counts[d] > 0:
            avgs[d] = totals[d] / counts[d]
        else:
            avgs[d] = 0
    return avgs

def get_mood_data(json_data):
    mood = {}
    for item in json_data:
        label = item.get("day", "")
        value = safe_number(item.get("mood", 0))
        if label != "" and value is not None:
            mood[label] = value
    return mood

# Status panel so you can see what's going on
with st.expander("Status (click to open)"):
    st.write("Working folder:", os.getcwd())
    st.write("CSV candidates:", possible_csv)
    st.write("JSON candidates:", possible_json)
    st.write("Chosen CSV path:", csv_file if csv_file else "(not found)")
    st.write("Chosen JSON path:", json_file if json_file else "(not found)")

csv_data = read_csv_data(csv_file) if csv_file else []
json_data = read_json_data(json_file) if json_file else []

with st.expander("File checks (click to open)"):
    st.write("CSV rows:", len(csv_data))
    if len(csv_data) > 0:
        st.write("CSV columns (first row):", list(csv_data[0].keys()))
        if not has_day_columns(csv_data):
            st.warning("Your CSV does not have Mon–Sun columns. Open the Survey page and submit a new weekly entry.")
    else:
        st.info("No CSV data loaded yet.")
    st.write("JSON points:", len(json_data))

if "min_avg" not in st.session_state:
    st.session_state.min_avg = 0.0
if "chosen_days" not in st.session_state:
    st.session_state.chosen_days = list(days)
if "min_day_avg" not in st.session_state:
    st.session_state.min_day_avg = 0.0

st.subheader("Dynamic Graph 1 — Weekly Average Water (CSV)")

if not csv_file:
    st.error("Could not find data.csv. Make sure it is in the same folder as HomePage.py.")
elif len(csv_data) == 0:
    st.info("No data yet. Add entries on the Survey page.")
elif not has_day_columns(csv_data):
    st.warning("Your CSV still uses the old format. Submit a new weekly entry on the Survey page to create Mon–Sun columns.")
else:
    st.session_state.min_avg = st.slider("Show only weeks with average ≥", 0.0, 15.0, st.session_state.min_avg, 0.1)
    weekly = get_weekly_averages(csv_data)
    filtered = []
    for v in weekly:
        if v >= st.session_state.min_avg:
            filtered.append(v)
    if len(filtered) == 0:
        st.warning("No weeks meet that amount.")
    else:
        st.line_chart(filtered)
        st.caption("Line chart showing weekly average liters. Adjust the slider to filter weeks.")

st.divider()
st.subheader("Dynamic Graph 2 — Average by Day (CSV)")

if not csv_file:
    st.error("Could not find data.csv.")
elif len(csv_data) == 0:
    st.info("No data yet. Add entries on the Survey page.")
elif not has_day_columns(csv_data):
    st.warning("Your CSV still uses the old format. Submit a new weekly entry on the Survey page to create Mon–Sun columns.")
else:
    by_day = get_day_averages(csv_data)
    st.session_state.chosen_days = st.multiselect("Pick days to show", days, default=st.session_state.chosen_days)
    st.session_state.min_day_avg = st.slider("Show only days with average ≥", 0.0, 15.0, st.session_state.min_day_avg, 0.1)
    shown_vals = []
    shown_labels = []
    for d in days:
        if d in st.session_state.chosen_days:
            val = by_day[d]
            if val >= st.session_state.min_day_avg:
                shown_vals.append(val)
                shown_labels.append(d)
    if len(shown_vals) == 0:
        st.warning("No days match your choices.")
    else:
        st.bar_chart(shown_vals)
        st.caption("Bar chart showing average liters by day. Adjust days and minimum average.")
        st.write("Days shown:", ", ".join(shown_labels))

st.divider()
st.subheader("Static Graph — Mood vs Water Intake")

if not csv_file or not json_file:
    st.error("Missing data.csv or data.json.")
elif len(csv_data) == 0 or len(json_data) == 0:
    st.info("Need both CSV water data and JSON mood data to see this chart.")
elif not has_day_columns(csv_data):
    st.warning("Your CSV still uses the old format. Submit a new weekly entry on the Survey page to create Mon–Sun columns.")
else:
    by_day = get_day_averages(csv_data)
    mood = get_mood_data(json_data)
    water_vals = []
    mood_vals = []
    for d in days:
        if d in by_day and d in mood:
            water_vals.append(by_day[d])
            mood_vals.append(mood[d])
    if len(water_vals) == 0:
        st.warning("Could not match days between mood and water data.")
    else:
        data = {"Water": water_vals, "Mood": mood_vals}
        st.scatter_chart(data, x="Water", y="Mood")
        st.caption("Scatter plot showing how mood (1–10) relates to average daily water intake.")
