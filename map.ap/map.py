import pandas as pd
import folium
from IPython.display import display
from folium.plugins import HeatMap

# Load your CSV file
df = pd.read_csv("data_centers.csv")

# Show first few rows
display(df.head())

# Create base map
m = folium.Map(location=[20, 0], zoom_start=2)

# Add markers for each data center
for _, row in df.iterrows():
    popup = f"""
    <b>{row['name']}</b><br>
    🌍 : {row['county']}<br>
    🌡️ : {row['temperature']} °C<br>
    ⚡ : {row['renewable_energy']}%
    🏭 : {row['company']}<br>
    """
    color = "green" if row['renewable_energy'] > 60 else "red"
    folium.Marker(
        location=[row["latitude"], row["longitude"]],
        popup=popup,
        icon=folium.Icon(color=color)
    ).add_to(m)


HeatMap(df[['latitude', 'longitude', 'temperature']].values.tolist()).add_to(m)

# Display the map in notebook
display(m)
