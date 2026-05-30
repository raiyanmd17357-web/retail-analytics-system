import streamlit as st
import pandas as pd
from streamlit_autorefresh import st_autorefresh
import plotly.express as px

# Page title
st.set_page_config(page_title="Retail Analytics Dashboard", layout="wide")

st.markdown("""
# 🛍️ Retail Analytics Dashboard
### AI-Powered Store Monitoring System
---
""")

st.sidebar.markdown("---")

selected_rows = st.sidebar.slider(
    "Records to Display",
    10,
    100,
    50
)


st_autorefresh(interval=5000, key="refresh")
st.success("🟢 System Active | YOLO Detection Running")


st.sidebar.title("🔧 Controls")

st.sidebar.markdown("""
**Project Info**
- Model: YOLOv8
- Data Source: MySQL
- Refresh: 5 sec
""")

use_local_db = False  # change to True for local MySQL

if use_local_db:
    import mysql.connector

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Raiyan@4328",
        database="retail_analytics"
    )

    query = "SELECT * FROM visitors ORDER BY timestamp DESC LIMIT 50;"
    df = pd.read_sql(query, conn)
    conn.close()

else:
    df = pd.read_csv("data.csv")

df = df.sort_values(by="timestamp", ascending=False)

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

st.dataframe(
    df.head(selected_rows),
    use_container_width=True
)

st.markdown("### 📈 Visitor Trend Analysis")

chart_data = df[["timestamp", "people_count"]].tail(20)
chart_data = chart_data.sort_values(by="timestamp")

fig = px.line(
    chart_data,
    x="timestamp",
    y="people_count",
    title="Visitor Trend Over Time",
    markers=True
)

fig.update_layout(
    xaxis_title="Time",
    yaxis_title="People Count",
    height=450
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("### 📊 Object Detection Analytics")

filtered_df = df[df["detected_objects"] != "None"]
object_counts = filtered_df["detected_objects"].value_counts()

object_df = object_counts.reset_index()
object_df.columns = ["Object", "Count"]

fig2 = px.bar(
    object_df,
    x="Object",
    y="Count",
    text="Count",
    title="Object Detection Frequency"
)

fig2.update_traces(textposition="outside")

fig3 = px.pie(
    object_df,
    names="Object",
    values="Count",
    title="Object Distribution"
)

col_left, col_right = st.columns(2)

with col_left:
    st.plotly_chart(fig2, use_container_width=True)

with col_right:
    st.plotly_chart(fig3, use_container_width=True)

total_visitors = df["people_count"].sum()


peak_crowd = df["people_count"].max()

col4, col5 = st.columns(2)

col4.metric("🚶 Total Visitors", total_visitors)
col5.metric("🔥 Peak Crowd", peak_crowd)