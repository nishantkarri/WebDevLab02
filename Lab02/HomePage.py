import streamlit as st

st.set_page_config(page_title="Water Intake Dashboard", page_icon="💧")

st.title("💧 Water Intake Dashboard — Lab 02")
st.write("Welcome! This app tracks how much water you drink each week and compares it with your mood.")

st.header("How It Works")
st.write("- **Survey**: enter how many liters of water you drink for each day (Mon–Sun).")
st.write("- **Visuals**: shows three graphs using your water data (from data.csv) and your mood data (from data.json).")

st.header("Steps")
st.write("1. Go to **Survey** and add your daily water data.")
st.write("2. Go to **Visuals** to view your graphs and mood comparison.")

st.caption("Tip: Add at least one week of data before visiting the Visuals page.")
