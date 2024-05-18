import streamlit as st
from state_city_map import state_city_scatter_mapbox, state_city_choropleth_mapbox
from aa_flights_paths import aa_flights_paths_mapbox
from global_companies_map import global_companies_map

st.set_page_config(layout="wide")
st.title("GHW DATA WEEK 2024")

SIDEBAR_DICT = {
    "GLOBAL COMPANIES MAP":global_companies_map,
    "AA FLIGHTS PATHS": aa_flights_paths_mapbox,
    "STATE-CITY SCATTER MAP": state_city_scatter_mapbox,
    "STATE-CITY CHOROPLETH MAP": state_city_choropleth_mapbox,
}


def main():
    chart_type = st.sidebar.radio("Select a chart", SIDEBAR_DICT.keys())
    # SIDEBAR_DICT[chart_type]()
    SIDEBAR_DICT.get(chart_type)()


if __name__ == "__main__":
    main()
