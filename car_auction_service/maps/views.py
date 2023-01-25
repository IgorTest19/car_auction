from django.shortcuts import render
import folium

"""
STANDALONE MAPS
"""
# https://www.youtube.com/watch?v=2uFJ43DvhHg&t=810s&ab_channel=KenBroTech
# http://127.0.0.1:8000/maps/maps_main/
def maps_main(request):
    # Create a Map Object
    cars_map = folium.Map(location=[19, -12], zoom_start=1)
    # Get hmtl representation of Map Object
    cars_map = cars_map._repr_html_()
    return render(request, 'maps/map_main.html', {'cars_map': cars_map})
