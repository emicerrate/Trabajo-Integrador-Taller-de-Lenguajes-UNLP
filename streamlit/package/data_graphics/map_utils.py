import streamlit as st
import folium
from streamlit_folium import st_folium  # para mostrar el mapa en Streamlit
import pandas as pd


def generate_map():
    attr = (
        '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> '
        'contributors, &copy; <a href="https://cartodb.com/attributions">CartoDB</a>'
    )
    tiles = 'https://wms.ign.gob.ar/geoserver/gwc/service/tms/1.0.0/capabaseargenmap@EPSG%3A3857@png/{z}/{x}/{-y}.png'
    m = folium.Map(
        location=(-33.457606, -65.346857),
        control_scale=True,
        zoom_start=5,
        name='es',
        tiles=tiles,
        attr=attr
    )
    return m

def get_color_empleo(increase: bool):
    return 'green' if increase else 'red'

def get_color_desempleo(increase: bool):
    # Invertido para desempleo: aumento de desempleo = rojo, disminución = verde
    return 'red' if increase else 'green'

def add_marker(row, map, rate):
    # tasa es 'empleo' o 'desempleo'
    # Comparamos tasa del último período con la del primero para saber si aumentó
    if rate == 'empleo':
        col_first = [c for c in row.index if c.startswith('tasa_empleo_')][0]
        col_last = [c for c in row.index if c.startswith('tasa_empleo_')][-1]
        increase = row[col_last] > row[col_first]
        color = get_color_empleo(increase)
    else:
        col_first = [c for c in row.index if c.startswith('tasa_desempleo_')][0]
        col_last = [c for c in row.index if c.startswith('tasa_desempleo_')][-1]
        increase = row[col_last] > row[col_first]
        color = get_color_desempleo(increase)

    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=f"{row['nombre']}<br>{rate.capitalize()} cambio: {'↑' if increase else '↓'}",
        icon=folium.Icon(color=color)
    ).add_to(map)