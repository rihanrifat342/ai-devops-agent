import re
import docker
import pandas as pd
import streamlit as st

from streamlit_autorefresh import st_autorefresh

# =========================
# Auto Refresh
# =========================

st_autorefresh(interval=5000, key="refresh")

# =========================
# Page Config
# =========================

st.set_page_config(
    page_title="AI DevOps Agent",
    layout="wide"
)

# =========================
# Dashboard Title
# =========================

st.title("🤖 AI DevOps Monitoring Dashboard")

# =========================
# System Status
# =========================

st.subheader("System Status")

st.success("Monitoring Agent Running")

# =========================
# Docker Monitoring
# =========================

try:

    client = docker.from_env()

    containers = client.containers.list(all=True)

except Exception as e:

    containers = []

    st.error(f"Docker Error: {e}")

# =========================
# Read Report File
# =========================

try:

    with open("report.txt", "r") as file:

        report = file.read()

except FileNotFoundError:

    report = ""

# =========================
# Severity Counting
# =========================

critical_count = len(re.findall(r"CRITICAL", report))
high_count = len(re.findall(r"HIGH", report))
medium_count = len(re.findall(r"MEDIUM", report))
low_count = len(re.findall(r"LOW", report))

# =========================
# Severity Cards
# =========================

st.subheader("Severity Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("🔴 Critical", critical_count)
col2.metric("🟠 High", high_count)
col3.metric("🟡 Medium", medium_count)
col4.metric("🟢 Low", low_count)

# =========================
# Severity Analytics
# =========================

data = pd.DataFrame({
    "Severity": ["Critical", "High", "Medium", "Low"],
    "Count": [
        critical_count,
        high_count,
        medium_count,
        low_count
    ]
})

st.subheader("Severity Analytics")

st.bar_chart(
    data.set_index("Severity")
)

# =========================
# Docker Containers
# =========================

st.subheader("Docker Containers")

container_data = []

for container in containers:

    container_data.append({
        "Name": container.name,
        "Status": container.status,
        "Container ID": container.short_id
    })

st.table(container_data)

# =========================
# Incident Reports
# =========================

st.subheader("Incident Reports")

if report:

    incidents = report.split("====================")

    for incident in reversed(incidents[-5:]):

        incident = incident.strip()

        if not incident:
            continue

        severity = "LOW"

        if "CRITICAL" in incident:
            severity = "CRITICAL"

        elif "HIGH" in incident:
            severity = "HIGH"

        elif "MEDIUM" in incident:
            severity = "MEDIUM"

        # Severity Styles

        if severity == "CRITICAL":

            st.error(f"🚨 {severity}")

        elif severity == "HIGH":

            st.warning(f"⚠️ {severity}")

        elif severity == "MEDIUM":

            st.info(f"🟡 {severity}")

        else:

            st.success(f"🟢 {severity}")

        with st.expander("View Incident Details"):

            st.code(incident)

else:

    st.warning("No reports generated yet.")

# =========================
# Live Server Logs
# =========================

st.subheader("Live Server Logs")

try:

    with open("server.log", "r") as log_file:

        logs = log_file.readlines()

    latest_logs = logs[-15:]

    log_text = "".join(latest_logs)

    st.text_area(
        "Latest Logs",
        log_text,
        height=300
    )

except FileNotFoundError:

    st.warning("server.log not found.")

# =========================
# AI Healing Timeline
# =========================

st.subheader("AI Healing Timeline")

try:

    with open("healing_log.txt", "r") as heal_file:

        healing_logs = heal_file.readlines()

    latest_heals = healing_logs[-10:]

    for log in reversed(latest_heals):

        st.success(log.strip())

except FileNotFoundError:

    st.info("No healing events recorded yet.")

# =========================
# Final System Status
# =========================

if critical_count > 0:

    st.error("🚨 Critical Issues Detected!")

elif high_count > 0:

    st.warning("⚠️ High Severity Issues Detected!")

else:

    st.success("✅ System Stable")