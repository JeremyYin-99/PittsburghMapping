# This file imports all of the data using pandas into dataframes
# %%
import os
import pandas as pd
import time
import sqlite3

# This is for correcting the cwd if there are problems
# print(os.getcwd())
# os.chdir("../")
# print(os.getcwd())

t0 = time.time()

trip_data = pd.read_csv('general_transit_Bing/trips.txt')
shape_data = pd.read_csv('general_transit_Bing/shapes.txt')
stop_time_data = pd.read_csv('general_transit_Bing/stop_times.txt')
stop_data = pd.read_csv('general_transit_Bing/stops.txt')
route_data = pd.read_csv('general_transit_Bing/routes.txt')
t_end = time.time()

con = sqlite3.connect('database.db')
c = con.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS trips(
        route_id,service_id,trip_id,
        trip_headsign,direction_id,block_id,
        shape_id,wheelchair_accessible
)
""")
con.commit()
trip_data.to_sql('trips', con, if_exists='replace', index = False)

c.execute("""
CREATE TABLE IF NOT EXISTS shapes(
    shape_id,shape_pt_lat,
    shape_pt_lon,shape_pt_sequence
)
""")
con.commit()
shape_data.to_sql('shapes', con, if_exists='replace', index = False)

c.execute("""
CREATE TABLE IF NOT EXISTS stop_times(
    trip_id,arrival_time,departure_time,
    stop_id,stop_sequence,pickup_type,
    drop_off_type,shape_dist_traveled,timepoint
)
""")
con.commit()
stop_time_data.to_sql('stop_times', con, if_exists='replace', index = False)

c.execute("""
CREATE TABLE IF NOT EXISTS stops(
    stop_id,stop_code,stop_name,
    stop_desc,stop_lat,stop_lon,
    zone_id,stop_url,location_type,
    parent_station,wheelchair_boarding
)
""")
con.commit()
stop_data.to_sql('stops', con, if_exists='replace', index = False)

c.execute("""
CREATE TABLE IF NOT EXISTS routes(
    route_id,agency_id,route_short_name,
    route_long_name,route_desc,route_type,
    route_url,route_color
)
""")
con.commit()
route_data.to_sql('routes', con, if_exists='replace', index = False)
con.close()
# %%
