import re
import docker
import psutil
import pandas as pd
import streamlit as st
import smtplib
from kubernetes import client, config

from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# =========================
# Login Credentials
# =========================

USERNAME = "rihan342"

PASSWORD = "admin123"

# =========================
# Login Authentication
# =========================

if "authenticated" not in st.session_state:

    st.session_state.authenticated = False

if not st.session_state.authenticated:

    st.title("Login - AI DevOps Platform")

    username = st.text_input("Username")

    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if (
            username == USERNAME
            and password == PASSWORD
        ):

            st.session_state.authenticated = True

            st.success("Login successful")

            st.rerun()

        else:

            st.error("Invalid username or password")

    st.stop()

# =========================
# Email Alert Function
# =========================

def send_email_alert(message_body):

    sender_email = "rihanrifat342@gmail.com"

    receiver_email = "mohammed.rihan342@gmail.com"

    app_password = "glck hchu yyye zfvy"

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

root_causes = []

# =========================
# CPU Analysis
# =========================

if cpu_usage > 85:

    anomalies.append(
        "WARNING: High CPU usage detected"
    )

    root_causes.append({
        "Issue": "High CPU Usage",
        "Cause": (
            "Heavy container workload or "
            "infinite background process."
        ),
        "Impact": (
            "System slowdown and unstable "
            "performance."
        ),
        "Fix": (
            "Restart overloaded services "
            "and optimize CPU-intensive tasks."
        )
    })

# =========================
# RAM Analysis
# =========================

if ram_usage > 85:

    anomalies.append(
        "WARNING: High RAM usage detected"
    )

    root_causes.append({
        "Issue": "High RAM Usage",
        "Cause": (
            "Memory leak or excessive "
            "application caching."
        ),
        "Impact": (
            "Application crashes and "
            "reduced responsiveness."
        ),
        "Fix": (
            "Clear unused memory and "
            "restart memory-heavy services."
        )
    })

# =========================
# Disk Analysis
# =========================

if disk_usage > 90:

    anomalies.append(
        "WARNING: High Disk usage detected"
    )

    root_causes.append({
        "Issue": "High Disk Usage",
        "Cause": (
            "Large logs, temporary files "
            "or storage overflow."
        ),
        "Impact": (
            "Storage exhaustion and "
            "service interruptions."
        ),
        "Fix": (
            "Delete unnecessary files "
            "and rotate old logs."
        )
    })

# =========================
# Show Anomalies
# =========================

if anomalies:

    for anomaly in anomalies:

        st.error(anomaly)

    alert_message = "\n".join(anomalies)

    send_email_alert(alert_message)

else:

    st.success("No anomalies detected")

# =========================
# AI Root Cause Analysis
# =========================

st.subheader("AI Root Cause Analysis")

if root_causes:

    for item in root_causes:

        with st.expander(item["Issue"]):

            st.write(
                f"Possible Cause: {item['Cause']}"
            )

            st.write(
                f"Impact: {item['Impact']}"
            )

            st.write(
                f"Recommended Fix: {item['Fix']}"
            )

else:

    st.success(
        "No critical root causes identified"
    )
    
    # =========================
# AI Severity Prediction
# =========================

st.subheader("AI Severity Prediction")

risk_score = (
    (cpu_usage * 0.4)
    + (ram_usage * 0.4)
    + (disk_usage * 0.2)
)

failure_probability = int(risk_score)

predicted_risk = "LOW"

if risk_score > 85:

    predicted_risk = "CRITICAL"

elif risk_score > 70:

    predicted_risk = "HIGH"

elif risk_score > 50:

    predicted_risk = "MEDIUM"
    
# =========================
# Predictive Failure Forecasting
# =========================

st.subheader("Predictive Failure Forecasting")

forecast_message = ""

system_stability = 100 - int(risk_score)

# =========================
# Failure Forecast Logic
# =========================

if cpu_usage > 90 and ram_usage > 90:

    forecast_message = (
        "System may experience a critical "
        "failure within 10-15 minutes due "
        "to extreme CPU and RAM usage."
    )

elif ram_usage > 85:

    forecast_message = (
        "High memory consumption may cause "
        "application instability or crashes "
        "if usage continues increasing."
    )

elif cpu_usage > 85:

    forecast_message = (
        "Sustained CPU overload could lead "
        "to service slowdown and degraded "
        "system responsiveness."
    )

elif disk_usage > 95:

    forecast_message = (
        "Storage exhaustion risk detected. "
        "Services may fail if disk cleanup "
        "is not performed soon."
    )

else:

    forecast_message = (
        "System forecast indicates stable "
        "operations with low failure risk."
    )

# =========================
# Display Forecast
# =========================

if (
    cpu_usage > 90
    or ram_usage > 90
    or disk_usage > 95
):

    st.error(forecast_message)

elif (
    cpu_usage > 80
    or ram_usage > 80
):

    st.warning(forecast_message)

else:

    st.success(forecast_message)

# =========================
# Stability Score
# =========================

st.metric(
    "System Stability Score",
    f"{system_stability}%"
)

# =========================
# AI Forecast Recommendation
# =========================

if system_stability < 40:

    st.error(
        "AI Forecast: Immediate intervention "
        "recommended to prevent outage."
    )

elif system_stability < 70:

    st.warning(
        "AI Forecast: System should be "
        "closely monitored for instability."
    )

else:

    st.success(
        "AI Forecast: Infrastructure "
        "operating within safe conditions."
    )    

# =========================
# Display Prediction
# =========================

if predicted_risk == "CRITICAL":

    st.error(
        f"Predicted Risk Level: {predicted_risk}"
    )

elif predicted_risk == "HIGH":

    st.warning(
        f"Predicted Risk Level: {predicted_risk}"
    )

elif predicted_risk == "MEDIUM":

    st.info(
        f"Predicted Risk Level: {predicted_risk}"
    )

else:

    st.success(
        f"Predicted Risk Level: {predicted_risk}"
    )

st.metric(
    "Failure Probability",
    f"{failure_probability}%"
)

# =========================
# AI Recommendation
# =========================

if predicted_risk in ["CRITICAL", "HIGH"]:

    st.warning(
        "AI Recommendation: Immediate system "
        "optimization and monitoring required."
    )

elif predicted_risk == "MEDIUM":

    st.info(
        "AI Recommendation: Monitor system "
        "resources closely."
    )

else:

    st.success(
        "AI Recommendation: System operating "
        "within safe limits."
    )

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
# Kubernetes Monitoring
# =========================

st.subheader("Kubernetes Cluster Monitoring")

kubernetes_available = False

try:

    config.load_kube_config()

    v1 = client.CoreV1Api()

    pods = v1.list_pod_for_all_namespaces(
        watch=False
    )

    kubernetes_available = True

    st.success(
        "Kubernetes Cluster Connected"
    )

except Exception as e:

    st.warning(
        f"Kubernetes unavailable: {e}"
    )

# =========================
# Display Pod Information
# =========================

if kubernetes_available:

    pod_data = []

    failed_pods = 0

    running_pods = 0

    for pod in pods.items:

        pod_name = pod.metadata.name

        pod_namespace = (
            pod.metadata.namespace
        )

        pod_status = pod.status.phase

        if pod_status == "Running":

            running_pods += 1

        else:

            failed_pods += 1

        pod_data.append({
            "Pod": pod_name,
            "Namespace": pod_namespace,
            "Status": pod_status
        })

    # =========================
    # Cluster Metrics
    # =========================

    col1, col2 = st.columns(2)

    col1.metric(
        "Running Pods",
        running_pods
    )

    col2.metric(
        "Non-Running Pods",
        failed_pods
    )

    # =========================
    # Pod Table
    # =========================

    st.dataframe(pod_data)

    # =========================
    # AI Cluster Analysis
    # =========================

    st.subheader(
        "AI Kubernetes Analysis"
    )

    if failed_pods > 0:

        st.error(
            "AI detected unstable "
            "Kubernetes workloads."
        )

        st.warning(
            "Recommendation: Restart "
            "failing pods or deployments."
        )

    else:

        st.success(
            "AI Analysis: Cluster "
            "operating normally."
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