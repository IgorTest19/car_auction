from django.shortcuts import render
import folium

# https://www.youtube.com/watch?v=2uFJ43DvhHg&t=810s&ab_channel=KenBroTech
def maps_main(request):
    # Create a map object
    cars_map = folium.Map()
    cars_map = cars_map._repr_html_()
    return render(request, 'map_main.html', {'cars_map': cars_map})
