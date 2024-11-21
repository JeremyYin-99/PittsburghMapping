# this file handles all of the folium mapping
from os import name
import webbrowser
import folium
from folium.map import Popup

output_file = "Maps/full_stops_map.html"
route_file = "Maps/full_route_map.html"

# create a new map
def create_map():
    m = folium.Map(location=[40.441, -79.99], zoom_start=12)
    return m

# used for the full marker map
def add_stop_marker(m, stop_classes, fg_name="bus stops"):
    fg = folium.FeatureGroup(fg_name)
    for element in stop_classes:
        if stop_classes[element].stop_lat_long:
            popup_name = ''.join('"<i>' + stop_classes[element].stop_name + '</i>"')
            popup_name = popup_name.replace('"', '')
            fg.add_child(folium.Marker(stop_classes[element].stop_lat_long, popup=popup_name))
    m.add_child(fg)
    m.save(output_file)

# used for the full route map
def route_mapping_total(m, shape_classes, fg_name=None, fname=None):
    for element_list in shape_classes:
        fg = folium.FeatureGroup(shape_classes[element_list].shape_id)
        lat_long_list = []
        for element in shape_classes[element_list].shape_lat_long:
            if element:
                lat_long_list.append(element)

        if fg_name == None:
            fg.add_child(folium.PolyLine(lat_long_list))
        else:
            fg.add_child(folium.PolyLine(lat_long_list, popup=fg_name))
        m.add_child(fg)
    if fname == None:
        m.save(route_file)
    else:
        filename = fname+'.html'
        m.save(filename)

# This is the main function which maps everying
def route_mapping(m, shape_classes, fg_name=None, fname=None, stop_list=None):
    fg = folium.FeatureGroup(name=fg_name)
    for element in shape_classes:
        lat_long_list = []
        for lat_long in element.shape_lat_long:
            if element:
                lat_long_list.append(lat_long)
        if fg_name == None:
            fg.add_child(folium.PolyLine(lat_long_list))
        else:
            fg.add_child(folium.PolyLine(lat_long_list, popup=fg_name))
        m.add_child(fg)

        fg2 = folium.FeatureGroup(fg_name)
    for element in stop_list:
        fg2.add_child(folium.Marker([element[0], element[1]], popup=element[2]))
    
    m.add_child(fg2)

    if fname == None:
        m.save(route_file)
    else:
        filename = 'Maps/'+fname+'.html'
        m.save(filename)

# save the html map file
def save_map(m, file_type, fname = None):
    if file_type == 1:
        browser = webbrowser.get('macosx').open(output_file, new=2)
    elif file_type == 2:
        browser = webbrowser.get('macosx').open(route_file, new=2)
    elif file_type == 3:
        browser = webbrowser.get('macosx').open(('Maps/'+fname+'.html'), new=2)
    else:
        browser = 0
    return browser

# test mapping function
def base_mapping():
    base_map = "Maps/base_map.html"
    m2 = folium.Map(location=[40.441, -79.99], zoom_start=12)
    folium.Marker([40.441, -79.99], popup="<i>test</i>").add_to(m2)
    fg2 = folium.FeatureGroup("test points")
    fg2.add_child(folium.Marker([40.441, -79.97], popup="<i>test2</i>"))
    m2.add_child(fg2)
    m2.save(base_map)
    browser = webbrowser.get('macosx').open(base_map, new=2)
    return browser
