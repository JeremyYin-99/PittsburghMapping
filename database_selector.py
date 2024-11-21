# %%
import sqlite3
import folium
import time

t0 = time.time()

con = sqlite3.connect('database.db')
c = con.cursor()

routes = c.execute(
    "SELECT route_id, route_short_name, route_long_name FROM routes WHERE route_type = 3"
    ).fetchall()


for i in routes:
    # Route creation
    shape_id = c.execute(
        "SELECT DISTINCT shape_id FROM trips WHERE route_id = ?",
        (i[0],)
    ).fetchall()

    query = "SELECT shape_pt_lat, shape_pt_lon FROM shapes WHERE shape_id = ?"
    pram = list(shape_id[0])
    for num in range(len(shape_id)-1):
        query = query + " OR shape_id = ?"
        pram.append(shape_id[num+1][0])
    
    ShapeLatLong = c.execute(
        query, (pram)
    ).fetchall()


    m = folium.Map(location=[40.441, -79.99], zoom_start=12)
    fg_route = folium.FeatureGroup(name=i[1])
    fg_route.add_child(folium.PolyLine(ShapeLatLong, popup=(i[1])+' '+i[2]))
    m.add_child(fg_route)

    # stop creation
    trip_id = c.execute(
        "SELECT DISTINCT trip_id FROM trips WHERE route_id = ?",
        (i[0],)
    ).fetchall()
    
    query = "SELECT DISTINCT stop_id FROM stop_times WHERE trip_id = ?"
    pram = list(trip_id[0])
    for num in range(len(trip_id)-1):
        query = query + " OR trip_id = ?"
        pram.append(trip_id[num+1][0])

    stop_id = c.execute(
        query, (pram)
    ).fetchall()

    query = "SELECT stop_lat, stop_lon FROM stops WHERE stop_id = ?"
    pram = list(stop_id[0])
    for num in range(len(stop_id)-1):
        query = query + " OR stop_id = ?"
        pram.append(stop_id[num+1][0])

    StopLatLong = c.execute(
        query, (pram)
    ).fetchall()

    query = "SELECT stop_name FROM stops WHERE stop_id = ?"
    pram = list(stop_id[0])
    for num in range(len(stop_id)-1):
        query = query + " OR stop_id = ?"
        pram.append(stop_id[num+1][0])

    StopName = c.execute(
        query, (pram)
    ).fetchall()
    
    fg_stop = folium.FeatureGroup(name=i[1])
    for num in range(len(StopName)):
        fg_stop.add_child(folium.Marker(StopLatLong[num], popup=StopName[num]))
    m.add_child(fg_stop)

    

    filename = 'test/'+ str(i[1])+'.html'
    print(filename)
    m.save(filename)

t1 = time.time()
print(t1-t0)
    
    
    
# %%
