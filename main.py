# This is the project's main file and drives the whole thing
'''
This project aims to take a user input and display the routes and stops associated with that route.
The following packages are used in the project: pandas, tkinter, webbrowser, os, time, and alive_progress.
'''
from alive_progress import alive_bar
import time

from pandas_import import *
from Classes import Trip, Stop, Shape, Route
from mapping import create_map, save_map, add_stop_marker, route_mapping_total, route_mapping
from route_selection import route_select_t1

def main():
    # Initialize dictionary for classes
    trip_classes = {}
    route_classes = {}
    stop_classes = {}
    shape_classes = {}

    # setup trip class
    print('Creating trip classes')
    total = len(trip_data)
    with alive_bar(total=total) as bar:
        for idx, element in trip_data.iterrows():
            if element['trip_id'] in trip_classes:
                trip_classes[element['trip_id']].add_shape(element['shape_id'])
            else:
                trip_classes[element['trip_id']] = Trip(element['trip_id'], element['route_id'], element['trip_headsign'], element['direction_id'], element['block_id'], element['shape_id'])
            bar()
    print("length of trip_classes: ", len(trip_classes))

    # set up stop class
    print('Creating stop classes')
    total = len(stop_time_data)
    with alive_bar(total=total) as bar:
        for idx, element in stop_time_data.iterrows():
            stop_classes[element['stop_id']] = Stop(element['trip_id'], element['arrival_time'], element['stop_id'], element['stop_sequence'], element['shape_dist_traveled'])
            bar()
    print("Finished creating stop classes")
    print("Length of stop_classes: ", len(stop_classes))

    total = len(stop_data)
    with alive_bar(total=total) as bar:
        for idx, element in stop_data.iterrows():
            try:
                stop_classes[element['stop_id']].get_lat_long(element['stop_name'], element['stop_lat'], element['stop_lon'])
            except:
                pass
            bar()
    
    # create map with all of the stop locations and names
    save_map(add_stop_marker(create_map(), stop_classes), 1)

    print('Starting stop id to location link')
    # start the processes of linking routes with stops with latitude and longitude data
    # This is the first step by linking long and lat to stop data
    stop_w_lat_long = {}
    total = len(stop_data)
    with alive_bar(total=total) as bar:
        for idx, element in stop_data.iterrows():
            stop_w_lat_long[element['stop_id']] = [element['stop_lat'], element['stop_lon'], element['stop_name']]
            bar()
    
    print('Starting trip to stop link')
    # this is the second step linking stops to trips
    stop_to_trip = {}
    total = len(stop_time_data)
    with alive_bar(total=total) as bar:
        for idx, element in stop_time_data.iterrows():

            if element['trip_id'] in stop_to_trip:
                stop_to_trip[element['trip_id']].append(stop_w_lat_long[element['stop_id']])
            else:
                stop_to_trip[element['trip_id']] = [stop_w_lat_long[element['stop_id']]]

            bar()

    print('Starting route to trip link')
    # this is the third step linking trips to routes
    trip_to_route = {}
    total = len(trip_data)
    with alive_bar(total=total) as bar:
        for idx, element in trip_data.iterrows():
            try:
                if element['route_id'] in trip_to_route:
                    trip_to_route[element['route_id']].append(stop_to_trip[element['trip_id']])
                else:
                    trip_to_route[element['route_id']] = [stop_to_trip[element['trip_id']]]
            except:
                pass
            bar()
    

    # Create the shape classes
    shape_keys = []
    print('Creating shape classes')
    total = len(shape_data)
    with alive_bar(total=total) as bar:
        for idx, element in shape_data.iterrows():
            if element['shape_id'] in shape_classes:
                if element['shape_id'] == shape_classes[element['shape_id']].shape_id:
                    shape_classes[element['shape_id']].add_shape_data(element['shape_pt_lat'], element['shape_pt_lon'], element['shape_pt_sequence'])# distance at the end of list for GTFS
                else:
                    print("Shape Id adding: ", element['shape_id'], " Shape Id current: ", shape_classes[element['shape_id']].shape_id)
                    exit()
            else:
                shape_keys.append(element['shape_id'])
                shape_classes[element['shape_id']] = Shape(element['shape_id'], element['shape_pt_lat'], element['shape_pt_lon'], element['shape_pt_sequence']) # element[4] for GTFS data
            bar()
    print("Finished creating shape classes")
    print("length of shape classes: ", len(shape_classes))

    # create a map with all of the routes on it
    save_map(route_mapping_total(create_map(), shape_classes), 2)

    # create the route classes
    print('Creating route classes')
    total = len(trip_data)
    with alive_bar(total=total) as bar:
        try:
            for idx, element in trip_data.iterrows():
                if element['route_id'] in route_classes:
                    route_classes[element['route_id']].add_shape(element['shape_id'], shape_classes[element['shape_id']])
                else:
                    route_classes[element['route_id']] = Route(element['route_id'], element['trip_id'], element['shape_id'], shape_classes[element['shape_id']])
                bar()
        except:
            pass     

    # connect the route names with the route ids
    route_to_shape = {}
    route_names = []
    s_name_to_route_id = {}
    print('Creating route to shape classes')
    total = len(route_data)
    with alive_bar(total=total) as bar:
        for idx, element in route_data.iterrows():
            try:
                route_to_shape[element['route_short_name']] = [element['route_id'], element['route_long_name'], route_classes[element['route_id']]]
                route_names.append(element['route_short_name'])
                s_name_to_route_id[element['route_short_name']] = element['route_id']
                bar()
            except:
                pass

    # create all of the maps
    print("Creating the folium maps")
    total = len(route_data)
    with alive_bar(total=total) as bar:
        for element in route_names:
            route_class = route_to_shape[element][2]
            shape_class = route_class.get_shape_class()
            save_map(route_mapping(create_map(), shape_class, element, (element), trip_to_route[s_name_to_route_id[element]][-1]), 2, (element))
            bar()

    t_end = time.time()
    print('The total backend runtime is :', t_end-t0)

    # GUI driver
    route_select_t1(route_names)
    
    
    t_end = time.time()
    print('The total runtime is :', t_end-t0)

    # test_route = '71'
    # test_route_class = route_to_shape[test_route][2]
    # test_shape_class = test_route_class.get_shape_class()
    # save_map(route_mapping(create_map(), test_shape_class, test_route, (test_route+'_test')), 2, (test_route+'_test'))

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

    