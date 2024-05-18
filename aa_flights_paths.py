import folium.map
import pandas as pd
import streamlit as st
import folium
import streamlit.components.v1 as components
import random
from folium.features import CustomIcon

PATH_TO_FLIGHT_DATA = "./aa_flights_paths_data.csv"


def random_color():
    color = "#"
    a = ["A", "B", "C", "D", "E", "F", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for i in range(6):
        ar = random.randint(0, len(a) - 1)
        color += a[ar]
    return color


def aa_flights_paths_mapbox():
    flight_paths = pd.read_csv(PATH_TO_FLIGHT_DATA)
    flight_paths.insert(0, "row_id", range(1, 1 + len(flight_paths)))
    st.subheader("AA Flight Paths")
    st.dataframe(flight_paths, hide_index=True)
    map = folium.Map(location=(37.09, -95.71), zoom_start=4, tiles="cartodb positron")
    # define a list of colors
    # colors = [
    #     "red","green","blue","purple","orange","darkred","pink","darkblue","beige",
    #     "lightred","darkgreen","lightgreen","lightblue","black","gray","lightpink"]
    # color_index = 0
    # iterate over the dataframe
    for index, row in flight_paths.iterrows():
        start_coords = (row["start_lat"], row["start_lon"])
        end_coords = (row["end_lat"], row["end_lon"])
        # st.write(f"Start Coordinates:{start_coords} | End Coordinates:{end_coords}")
        # select color
        # color = colors[color_index % len(colors)]
        # color_index += 1
        color = random_color()
        line = folium.PolyLine(
            locations=[start_coords, end_coords],
            color=color,
            weight=2,
            # dash_array=10,
            popup=f"{row['row_id']}:{row['airport1']} to {row['airport2']}",
        )
        # calculate mid-point of line
        midpoint = [
            (start_coords[0] + end_coords[0]) / 2,
            (start_coords[1] + end_coords[1]) / 2,
        ]
        iconurl = "https://cdn-icons-png.flaticon.com/128/16092/16092645.png"
        icon = CustomIcon(iconurl, icon_size=(16, 16))
        folium.Marker(
            location=midpoint,
            icon=icon,
            popup=f"{row['row_id']}:{row['airport1']} to {row['airport2']}",
        ).add_to(map)
        map.add_child(line)
    map.save("flight_path.html")
    HTML_FILE = open("./flight_path.html", "r", encoding="utf-8")
    mapbox = HTML_FILE.read()
    components.html(mapbox, height=700)
