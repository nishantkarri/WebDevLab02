import streamlit as st
import csv

st.set_page_config(page_title="Water Intake Survey", page_icon="💧")

st.title("💧 Water Intake Data Input")
st.write("Enter how many liters of water you drink each day (0–15 liters):")

csv_file = "Lab02/data.csv"

if st.button("Reset CSV (erase all data)"):
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    st.success("CSV reset. Submit a new week to add data.")

try:
    open(csv_file, "r").close()
except:
    with open(csv_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])

mon = st.slider("Mon (liters)", 0.0, 15.0, 0.0, 0.1)
tue = st.slider("Tue (liters)", 0.0, 15.0, 0.0, 0.1)
wed = st.slider("Wed (liters)", 0.0, 15.0, 0.0, 0.1)
thu = st.slider("Thu (liters)", 0.0, 15.0, 0.0, 0.1)
fri = st.slider("Fri (liters)", 0.0, 15.0, 0.0, 0.1)
sat = st.slider("Sat (liters)", 0.0, 15.0, 0.0, 0.1)
sun = st.slider("Sun (liters)", 0.0, 15.0, 0.0, 0.1)

if st.button("Submit Weekly Data"):
    with open(csv_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([mon, tue, wed, thu, fri, sat, sun])
    st.success("✅ Your weekly water intake has been recorded!")

st.divider()
st.write("Your recorded data:")

try:
    with open(csv_file, "r") as f:
        reader = csv.reader(f)
        header = next(reader)
        rows = list(reader)
    if len(rows) == 0:
        st.info("No data recorded yet.")
    else:
        for row in rows[-5:]:
            st.write(row)
except:
    st.info("No data file found yet.")
