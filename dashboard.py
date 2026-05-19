import streamlit as st

st.set_page_config(
    page_title="AI DevOps Agent",
    layout="wide"
)

st.title("🤖 AI DevOps Monitoring Dashboard")

st.subheader("System Status")

st.success("Monitoring Agent Running")

st.subheader("Latest AI Report")

try:

    with open("report.txt", "r") as file:

        report = file.read()

    st.code(report)

except FileNotFoundError:

    st.warning("No reports generated yet.")

st.subheader("Controls")

if st.button("Refresh Dashboard"):

    st.rerun()