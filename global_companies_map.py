import folium.map
import streamlit as st
import pandas as pd
from geopy.geocoders import Nominatim, Photon
import folium
import streamlit.components.v1 as components
from folium.plugins import MarkerCluster
from geopy.extra.rate_limiter import RateLimiter
import time
from geopy.exc import GeocoderTimedOut,GeocoderNotFound,GeocoderQuotaExceeded

PATH_TO_DATA = "./companies_data.csv"


def global_companies_map():
    st.header("Global Distrubution of Top Companies")
    companies_data = pd.read_csv(PATH_TO_DATA, index_col="Ranking")
    # slice and show limited data
    # companies_data = companies_data[0:50]
    st.dataframe(companies_data[["Company", "Country"]])
    geolocator = Nominatim(user_agent="ghwdata24_globalcompaniesdata")
    # geolocator = Photon(user_agent="ghwdata24_globalcompaniesdata")
    # geolocator = Nominatim(user_agent="application")
    map = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodb-darkmatter")
    # add a marker cluster to handle multiple markers
    marker_cluster = MarkerCluster().add_to(map)
    # iterate over df
    for index, row in companies_data.iterrows():
        country_q = row["Country"]
        # st.write(f"country q:{country_q}")
        try:
            # finder = RateLimiter(geolocator.geocode, min_delay_seconds=1)
            location = geolocator.geocode(country_q, timeout=20, language="en")
            # location=finder(country_q)
            if location:
                # st.write(f"country q:{location.latitude,location.longitude}")
                popup = f"{index}:{row['Company']} ,{row['Country']}"
                folium.Marker(
                    location=[location.latitude, location.longitude], popup=popup
                ).add_to(marker_cluster)
            else:
                st.error(f"Geocoding Failure for {index}:{country_q}")
            time.sleep(0.5)
        except (GeocoderQuotaExceeded,GeocoderNotFound,GeocoderTimedOut,Exception) as e:
            st.error(f"Geocoding Error: {e} for {country_q}")
    map.save("companies_map.html")
    HTML_FILE = open("./companies_map.html", "r", encoding="utf-8")
    mapbox = HTML_FILE.read()
    components.html(mapbox, height=700)
