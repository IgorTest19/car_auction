from django.shortcuts import render
import folium


def maps_index(request):
    # Create a map object
    cars_map = folium.Map()
    cars_map = cars_map._repr_html_()
    return render(request, 'map.html', {'cars_map': cars_map})
