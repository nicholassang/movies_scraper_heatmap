import pydeck as pdk
import streamlit as st

heatmap_data = [
    {"lat": 34.05, "lon": -118.25},   # LA
    {"lat": 51.507, "lon": -0.128},   # London
]

arc_data = [
    {
        "src_lat": 34.05, "src_lon": -118.25,
        "dst_lat": 51.507, "dst_lon": -0.128
    }
]

view_state = pdk.ViewState(
    latitude=0,
    longitude=0,
    zoom=0.3,
    pitch=35
)

heatmap_layer = pdk.Layer(
    "HeatmapLayer",
    data=heatmap_data,
    get_position='[lon, lat]',
    aggregation=pdk.types.String("SUM"),
    radiusPixels=60,
)

arc_layer = pdk.Layer(
    "ArcLayer",
    data=arc_data,
    get_source_position='[src_lon, src_lat]',
    get_target_position='[dst_lon, dst_lat]',
    get_width=2,
    get_source_color=[0, 255, 255],
    get_target_color=[255, 0, 255],
    pickable=True,
)

deck = pdk.Deck(
    views=[pdk.View(type="GlobeView", controller=True)],
    layers=[heatmap_layer, arc_layer],
    initial_view_state=view_state,
)

st.pydeck_chart(deck)