import folium
from django.shortcuts import render

"""
STANDALONE MAPS
"""
# https://www.youtube.com/watch?v=2uFJ43DvhHg&t=810s&ab_channel=KenBroTech
# http://127.0.0.1:8000/maps/maps_main/
def maps_main(request):
    # Creating Map Object
    cars_map = folium.Map(location=[50, 20], zoom_start=6)
    # Adding map marker
    folium.Marker([52, 20]).add_to(cars_map)
    # Getting HTML representation of Map Object
    cars_map = cars_map._repr_html_()
    return render(request, 'maps/map_main.html', {'cars_map': cars_map})
