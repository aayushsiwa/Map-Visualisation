import pandas as pd
import plotly.express as px
import streamlit as st
import json

PATH_TO_DATA = "./state_city_data.json"
PATH_TO_GEOJSON = "./indian_map_coordinates.geojson"

def state_city_scatter_mapbox():
    st.subheader("Visualizing States and Capital Cities of India - Scatter Map")
    # Loading state and city data from JSON file into a pandas dataframe
    state_city_data = pd.read_json(PATH_TO_DATA)
    st.dataframe(state_city_data, hide_index=True)
    fig = px.scatter_mapbox(
        state_city_data,
        lat="lat",
        lon="long",
        hover_name="state",
        hover_data="capital",
        color="capital",
        # color_discrete_sequence=px.colors.qualitative.Plotly,
        # color_continuous_scale=px.colors.cyclical.IceFire,
        zoom=3,
        height=700,
        opacity=0.9,
        center={"lat": 20.59, "lon": 78.96},
    )
    # fig.update_layout(mapbox_style="open-street-map")
    # fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(mapbox_style="carto-darkmatter")
    fig.update_layout(margin={"t": 0, "r": 0, "b": 0, "l": 0})
    return st.plotly_chart(fig)


def state_city_choropleth_mapbox():
    st.subheader("Visualizing States and Capital Cities of India - Choropleth Map")
    state_city_data = pd.read_json(PATH_TO_DATA)
    st.dataframe(state_city_data, hide_index=True)
    fig = px.choropleth_mapbox(
        state_city_data,
        hover_name="state",
        hover_data="capital",
        locations="state",
        color="capital",
        zoom=3,
        height=700,
        opacity=0.9,
        center={"lat": 20.59, "lon": 78.96},
        labels={"capital": "Capital City"},
        geojson=json.load(open(PATH_TO_GEOJSON, "r")),
        featureidkey="properties.ST_NM",
    )
    # fig.update_layout(mapbox_style="carto-positron")
    fig.update_layout(mapbox_style="carto-darkmatter")
    return st.plotly_chart(fig)


