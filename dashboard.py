import re
import docker
import psutil
import pandas as pd
import streamlit as st
import smtplib

from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# =========================
# Email Alert Function
# =========================

def send_email_alert(message_body):

    sender_email = "rihanrifat342@gmail.com"

    receiver_email = "mohammed.rihan342@gmail.com"

    app_password = "oyws lrct uzib plsx"

    subject = "AI DevOps Critical Alert"

    email_message = f"""
Subject: {subject}

{message_body}
"""

    try:

        server = smtplib.SMTP(
            "smtp.gmail.com",
            587
        )

        server.starttls()

        server.login(
            sender_email,
            app_password
        )

        server.sendmail(
            sender_email,
            receiver_email,
            email_message.encode("utf-8")
        )

        server.quit()

    except Exception as e:

        print(e)

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

st.title("AI DevOps Monitoring Dashboard")

# =========================
# System Status
# =========================

st.subheader("System Status")

st.success("Monitoring Agent Running")

# =========================
# Docker Monitoring
# =========================

st.subheader("Docker Monitoring")

containers = []

docker_available = False

try:

    client = docker.from_env()

    client.ping()

    containers = client.containers.list(all=True)

    docker_available = True

    st.success("Docker Engine Connected")

except Exception:

    st.info(
        "Docker monitoring unavailable on cloud deployment"
    )

# =========================
# Read Report File
# =========================

try:

    with open("report.txt", "r") as file:

        report = file.read()

except FileNotFoundError:

    report = ""

# =========================
# Live System Metrics
# =========================

st.subheader("Live System Metrics")

cpu_usage = psutil.cpu_percent()

ram_usage = psutil.virtual_memory().percent

disk_usage = psutil.disk_usage('/').percent

# =========================
# Save Metrics History
# =========================

timestamp = datetime.now().strftime("%H:%M:%S")

metrics_row = pd.DataFrame({
    "Time": [timestamp],
    "CPU": [cpu_usage],
    "RAM": [ram_usage],
    "Disk": [disk_usage]
})

try:

    old_metrics = pd.read_csv("metrics_log.csv")

    updated_metrics = pd.concat(
        [old_metrics, metrics_row],
        ignore_index=True
    )

except:

    updated_metrics = metrics_row

updated_metrics = updated_metrics.tail(50)

updated_metrics.to_csv(
    "metrics_log.csv",
    index=False
)

# =========================
# Metrics Cards
# =========================

col1, col2, col3 = st.columns(3)

col1.metric("CPU Usage", f"{cpu_usage}%")
col2.metric("RAM Usage", f"{ram_usage}%")
col3.metric("Disk Usage", f"{disk_usage}%")

# =========================
# Progress Bars
# =========================

st.write("CPU Usage")
st.progress(int(cpu_usage))

st.write("RAM Usage")
st.progress(int(ram_usage))

st.write("Disk Usage")
st.progress(int(disk_usage))

# =========================
# AI Anomaly Detection
# =========================

st.subheader("AI Anomaly Detection")

anomalies = []

if cpu_usage > 85:

    anomalies.append(
        "WARNING: High CPU usage detected"
    )

if ram_usage > 85:

    anomalies.append(
        "WARNING: High RAM usage detected"
    )

if disk_usage > 90:

    anomalies.append(
        "WARNING: High Disk usage detected"
    )

if anomalies:

    for anomaly in anomalies:

        st.error(anomaly)

    alert_message = "\n".join(anomalies)

    send_email_alert(alert_message)

else:

    st.success("No anomalies detected")

# =========================
# Historical Metrics Charts
# =========================

st.subheader("Historical System Metrics")

try:

    metrics_data = pd.read_csv("metrics_log.csv")

    st.line_chart(
        metrics_data.set_index("Time")[["CPU", "RAM", "Disk"]]
    )

except Exception as e:

    st.warning(f"Metrics Chart Error: {e}")

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

col1.metric("Critical", critical_count)
col2.metric("High", high_count)
col3.metric("Medium", medium_count)
col4.metric("Low", low_count)

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

if docker_available:

    container_data = []

    try:

        for container in containers:

            container_data.append({
                "Name": container.name,
                "Status": container.status,
                "Container ID": container.short_id
            })

        if container_data:

            st.table(container_data)

        else:

            st.info("No containers found.")

    except Exception as e:

        st.error(
            f"Container Display Error: {e}"
        )

else:

    st.info(
        "Docker containers cannot be displayed on Render cloud"
    )

# =========================
# Incident Reports
# =========================

st.subheader("Incident Reports")

if report.strip():

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

        if severity == "CRITICAL":

            st.error("CRITICAL")

        elif severity == "HIGH":

            st.warning("HIGH")

        elif severity == "MEDIUM":

            st.info("MEDIUM")

        else:

            st.success("LOW")

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

    st.error("Critical Issues Detected")

elif high_count > 0:

    st.warning("High Severity Issues Detected")

else:

    st.success("System Stable")