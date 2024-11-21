# This script only runs the gui part of the project without all of the bloat
from pandas_import import route_data
from alive_progress import alive_bar
from route_selection import route_select_t1

route_names = []
print('Creating route to shape classes')
total = len(route_data)
with alive_bar(total=total) as bar:
    for idx, element in route_data.iterrows():
        try:
            route_names.append(element['route_short_name'])
            bar()
        except:
            pass

route_select_t1(route_names)
