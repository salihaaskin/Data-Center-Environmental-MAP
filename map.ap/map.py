import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import os

# Get the directory of this script
BASE_DIR = os.path.dirname(__file__)
csv_path = os.path.join(BASE_DIR, "data_centers.csv")

# Load your CSV safely
try:
    df = pd.read_csv(csv_path, encoding="utf-8")
except UnicodeDecodeError:
    # Fallback if UTF-8 fails
    df = pd.read_csv(csv_path, encoding="cp1252")

# Show first few rows in Streamlit
st.subheader("📊 Data Preview")
st.dataframe(df.head())

# Create base map
m = folium.Map(location=[20, 0], zoom_start=2)

# Add markers for each data center
for _, row in df.iterrows():
    popup = f"""
    <b>{row['name']}</b><br>
    🌍 : {row['county']}<br>
    🌡️ : {row['temperature']} °C<br>
    ⚡ : {row['renewable_energy']}%<br>
    🏭 : {row['company']}<br>
    """
    color = "green" if row['renewable_energy'] > 60 else "red"
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=popup,
        icon=folium.Icon(color=color)
    ).add_to(m)

# Add heatmap
HeatMap(df[['latitude', 'longitude', 'temperature']].values.tolist()).add_to(m)

# Display the map in Streamlit
st.subheader("🗺️ Map of Data Centers")
st_folium(m, width=800, height=500)
