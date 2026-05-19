import re
import pandas as pd
import streamlit as st

from streamlit_autorefresh import st_autorefresh

# Auto refresh every 5 seconds
st_autorefresh(interval=5000, key="refresh")

st.set_page_config(
    page_title="AI DevOps Agent",
    layout="wide"
)

st.title("🤖 AI DevOps Monitoring Dashboard")

st.subheader("System Status")

st.success("Monitoring Agent Running")

# Read report file
try:

    with open("report.txt", "r") as file:

        report = file.read()

except FileNotFoundError:

    report = ""

# Count severity levels
critical_count = len(re.findall(r"CRITICAL", report))
high_count = len(re.findall(r"HIGH", report))
medium_count = len(re.findall(r"MEDIUM", report))
low_count = len(re.findall(r"LOW", report))

# Severity cards
st.subheader("Severity Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🔴 Critical", critical_count)
col2.metric("🟠 High", high_count)
col3.metric("🟡 Medium", medium_count)
col4.metric("🟢 Low", low_count)

# Create analytics dataframe
data = pd.DataFrame({
    "Severity": ["Critical", "High", "Medium", "Low"],
    "Count": [
        critical_count,
        high_count,
        medium_count,
        low_count
    ]
})

# Charts
st.subheader("Severity Analytics")

st.bar_chart(
    data.set_index("Severity")
)

# Latest AI Report
st.subheader("Latest AI Report")

if report:

    st.code(report)

else:

    st.warning("No reports generated yet.")

# Alert section
if critical_count > 0:

    st.error("🚨 Critical Issues Detected!")

elif high_count > 0:

    st.warning("⚠️ High Severity Issues Detected!")

else:

    st.success("✅ System Stable")