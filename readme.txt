Using main.py for mini 1 progress and use api.py/app.py for mini 2

This project aims to take a user input and display the routes and stops associated with that route. The following packages are used in the mini 1 project: pandas, tkinter, webbrowser, os, time, and alive_progress.

The following packages are used in the mini 2 project: pandas, numpy, requests, sqlite, os, time, and flask.

As for the files:
api_calls.py (mini 2) handles all of the api requests and returns the calls as useable data

api.py (mini 2) runs all of the api stuff including updating the folium maps with the vehicle location

classes.py (mini 1) holds all of the class creation

database_selector.py (mini 2) runs the map creating using the database approach

main.py (mini 1) runs the everything from mini 1

main_gui_only.py (mini 1) runs only the gui portion of main.py

mapping.py (mini 1) handles the mapping for main.py

pandas_import.py (mini 1)(mini 2) imports the data for main.py and also database_selector.py

route_selection.py (mini 1) handles the route selection fro the gui