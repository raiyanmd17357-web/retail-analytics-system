import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh

# Page title
st.set_page_config(page_title="Retail Analytics Dashboard", layout="wide")

st.markdown("""
# 🛍️ Retail Analytics Dashboard
### AI-Powered Store Monitoring System
---
""")
st_autorefresh(interval=5000, key="refresh")

df = pd.read_csv("data.csv")

df["timestamp"] = pd.to_datetime(df["timestamp"])


# Metrics
total_records = len(df)

latest_people = 0
latest_objects = 0

if not df.empty:
    latest_people = df.iloc[0]["people_count"]
    latest_objects = df.iloc[0]["object_count"]

# Show metrics
col1, col2, col3 = st.columns(3)

col1.metric("📊 Total Records", total_records)
col2.metric("👥 Current People", latest_people)
col3.metric("📦 Objects Detected", latest_objects)

st.markdown("---")
st.markdown("### 📋 Recent Detection Data")

st.dataframe(df.head(20), use_container_width=True)
st.subheader("Visitor Trend")

chart_data = df[["timestamp", "people_count"]].tail(20)
chart_data = chart_data.sort_values(by="timestamp")

st.line_chart(
    chart_data.set_index("timestamp")
)

st.subheader("Object Detection Frequency")

filtered_df = df[df["detected_objects"] != "None"]
object_counts = filtered_df["detected_objects"].value_counts()

st.bar_chart(object_counts)

total_visitors = df["people_count"].sum()


peak_crowd = df["people_count"].max()

col4, col5 = st.columns(2)

col4.metric("🚶 Total Visitors", total_visitors)
col5.metric("🔥 Peak Crowd", peak_crowd)