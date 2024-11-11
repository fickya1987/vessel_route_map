import streamlit as st
import pandas as pd
import pydeck as pdk

# Load data
data = pd.read_excel('Rute_pelabuhan_asal_tujuan_combined.xlsx')

# Predefined coordinates for each port
port_coordinates = {
    "Samarinda": {"lat": -0.5022, "lon": 117.1536},
    "Priok": {"lat": -6.1045, "lon": 106.8805},
    "Vancouver (Canada)": {"lat": 49.2827, "lon": -123.1207},
    "Yangoon (Myanmar)": {"lat": 16.8661, "lon": 96.1951},
    "Cigading": {"lat": -6.0063, "lon": 105.9920},
    "Paradip (India)": {"lat": 20.3167, "lon": 86.6086},
    "Taicang (China)": {"lat": 31.4515, "lon": 121.1000},
    "Tanjung Pelepas": {"lat": 1.3667, "lon": 103.5333},
    "Panjang": {"lat": -5.4500, "lon": 105.3167},
    "Pangkal Balam": {"lat": -2.0833, "lon": 106.1500},
    "Shanghai": {"lat": 31.2304, "lon": 121.4737},
    "Cilacap": {"lat": -7.7167, "lon": 109.0000},
    "Paranagua": {"lat": -25.5161, "lon": -48.5222},
    "Pasir Gudang (Malaysia)": {"lat": 1.4726, "lon": 103.8780},
    "Singapore": {"lat": 1.3521, "lon": 103.8198},
    "Makassar": {"lat": -5.1477, "lon": 119.4327},
    "Pelintung": {"lat": 1.2000, "lon": 101.2833},
    "Pontianak": {"lat": -0.0263, "lon": 109.3425},
    "Port Klang": {"lat": 3.0000, "lon": 101.4000},
    "Semarang": {"lat": -6.9667, "lon": 110.4167},
    "Kuching (Malaysia)": {"lat": 1.5533, "lon": 110.3593},
    "Minhang (China)": {"lat": 31.1128, "lon": 121.3833},
    "Son Duong (Vietnam)": {"lat": 18.8433, "lon": 106.5000},
    "Yuzhny (Ukraine)": {"lat": 46.6228, "lon": 31.1011},
    "Huizhou (China)": {"lat": 23.1115, "lon": 114.4152},
    "Surabaya": {"lat": -7.2504, "lon": 112.7688},
    "Bima": {"lat": -8.4606, "lon": 118.7268},
    "Bayah": {"lat": -6.9500, "lon": 106.2500},
    "Lhoknga (Aceh)": {"lat": 5.4489, "lon": 95.2100},
    "Fangcheng (China)": {"lat": 21.6869, "lon": 108.3564},
    "Geraldton (Australia)": {"lat": -28.7780, "lon": 114.6140},
    "Jayapura": {"lat": -2.5337, "lon": 140.7181},
    "Banjarmasin": {"lat": -3.3167, "lon": 114.5900},
    "Gresik": {"lat": -7.1566, "lon": 112.6554},
    "Taboneo": {"lat": -4.2000, "lon": 114.5000},
    "Shantou (China)": {"lat": 23.3541, "lon": 116.6819},
    "Belawan": {"lat": 3.7766, "lon": 98.6832},
}

# Add coordinates to data based on port names
def get_coordinates(port):
    return port_coordinates.get(port, {"lat": None, "lon": None})

data['Departure_Coords'] = data['Departure'].apply(get_coordinates)
data['Arrival_Coords'] = data['Arrival'].apply(get_coordinates)

# Filter rows with available coordinates
data = data.dropna(subset=['Departure_Coords', 'Arrival_Coords'])

# Convert coordinates to columns
data['Departure_lat'] = data['Departure_Coords'].apply(lambda x: x['lat'])
data['Departure_lon'] = data['Departure_Coords'].apply(lambda x: x['lon'])
data['Arrival_lat'] = data['Arrival_Coords'].apply(lambda x: x['lat'])
data['Arrival_lon'] = data['Arrival_Coords'].apply(lambda x: x['lon'])

# Streamlit UI
st.title("Geo Map of Departure and Arrival Routes")

# Map visualization
st.write("This map shows the departure and arrival routes of vessels between ports.")

# Set up the pydeck layer for routes
layer = pdk.Layer(
    "LineLayer",
    data=data,
    get_source_position=["Departure_lon", "Departure_lat"],
    get_target_position=["Arrival_lon", "Arrival_lat"],
    get_color=[255, 0, 0],
    get_width=5,
)

# Define the view centered on an approximate central location
view_state = pdk.ViewState(
    latitude=0.0,  # Adjust as needed for your data
    longitude=110.0,  # Adjust as needed for your data
    zoom=3,
    pitch=0,
)

# Render the map with pydeck
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
