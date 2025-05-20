# 📁 File: dashboard/app.py
import streamlit as st
from cassandra.cluster import Cluster
import pandas as pd
import pydeck as pdk
from streamlit_autorefresh import st_autorefresh

# ✅ Page config must be first
st.set_page_config(page_title="Vehicle Telemetry Dashboard", layout="wide")

# 🔄 Auto-refresh every 5 seconds
st_autorefresh(interval=5000, key="data_refresh")

st.title("🚗 Real-Time Vehicle Telemetry Dashboard")

# 🔌 Connect to Cassandra
cluster = Cluster(['127.0.0.1'])
session = cluster.connect('telemetry')

# 🔽 Vehicle ID Dropdown
try:
    vehicle_rows = session.execute("SELECT DISTINCT vehicle_id FROM vehicle_data")
    vehicle_ids = [row.vehicle_id for row in vehicle_rows]
    selected_vehicle = st.selectbox("Filter by Vehicle ID", ["All"] + vehicle_ids)
except Exception as e:
    st.error(f"Error fetching vehicle IDs: {e}")
    st.stop()

# 📥 Fetch vehicle data
try:
    if selected_vehicle == "All":
        rows = session.execute("SELECT * FROM vehicle_data")
    else:
        rows = session.execute("SELECT * FROM vehicle_data WHERE vehicle_id = %s", (selected_vehicle,))

    data = pd.DataFrame([dict(r._asdict()) for r in rows])
except Exception as e:
    st.error(f"Error loading vehicle data: {e}")
    data = pd.DataFrame()

# 📊 Charts
if not data.empty:
    st.subheader("📈 Speed & Fuel Level Over Time")
    try:
        data["timestamp"] = pd.to_datetime(data["timestamp"])
        data = data.sort_values("timestamp")
        st.line_chart(data.set_index("timestamp")[["speed", "fuel_level"]].astype(float))
    except Exception as e:
        st.warning(f"Could not render charts: {e}")
else:
    st.write("No vehicle data available.")

# 📤 Export to CSV
if not data.empty:
    st.subheader("📁 Export Data")
    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button("Download Vehicle Data as CSV", data=csv, file_name="vehicle_data.csv", mime="text/csv")