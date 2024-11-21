# %%
from api_calls import *
import numpy as np
import folium
import pandas as pd
import os
import copy
import time


t0 = time.time()

# switch between subset and the whole system
# reduces the number of api calls as the limit per day is 10,000
full = True

# ask whether pattern data should be redownloaded
pattern_download = False

# initialize the vehicle api calls
check = True

# splits list into batches of 10 for the api max
def split_list(L, n):
    assert type(L) is list, "L is not a list"
    l = []
    for i in range(0, len(L), n):
        l.append(L[i:i+n])
    return l


if full: # Get all of the route information for the entire system
    routes = get_routes()
    routes_dict = {}
    for route in routes:
        if route['rtpidatafeed'] in routes_dict:
            routes_dict[route['rtpidatafeed']].append(route)
        else:
            routes_dict[route['rtpidatafeed']] = [route]

    routes = split_list(routes, 10)
else: # Skips the api call for these (testing purposes)
    routes = [[
        {'rt': '61A',
        'rtnm': 'NORTH BRADDOCK',
        'rtclr': '#e0ffff',
        'rtdd': '61A',
        'rtpidatafeed': 'Port Authority Bus'},
        {'rt': '61B',
        'rtnm': 'BRADDOCK-SWISSVALE',
        'rtclr': '#afeeee',
        'rtdd': '61B',
        'rtpidatafeed': 'Port Authority Bus'},
        {'rt': '61C',
        'rtnm': 'MCKEESPORT-HOMESTEAD',
        'rtclr': '#00ffff',
        'rtdd': '61C',
        'rtpidatafeed': 'Port Authority Bus'},
        {'rt': '61D',
        'rtnm': 'MURRAY',
        'rtclr': '#7fffd4',
        'rtdd': '61D',
        'rtpidatafeed': 'Port Authority Bus'},
        {'rt': '71A',
        'rtnm': 'NEGLEY',
        'rtclr': '#dc143c',
        'rtdd': '71A',
        'rtpidatafeed': 'Port Authority Bus'},
        {'rt': '71B',
        'rtnm': 'HIGHLAND PARK',
        'rtclr': '#ffa07a',
        'rtdd': '71B',
        'rtpidatafeed': 'Port Authority Bus'},
        {'rt': '71C',
        'rtnm': 'POINT BREEZE',
        'rtclr': '#f08080',
        'rtdd': '71C',
        'rtpidatafeed': 'Port Authority Bus'},
        {'rt': '71D',
        'rtnm': 'HAMILTON',
        'rtclr': '#cd5c5c',
        'rtdd': '71D',
        'rtpidatafeed': 'Port Authority Bus'},
        {'rt': '75',
        'rtnm': 'ELLSWORTH',
        'rtclr': '#669933',
        'rtdd': '75',
        'rtpidatafeed': 'Port Authority Bus'},
        {'rt': '82',
        'rtnm': 'LINCOLN',
        'rtclr': '#ffd700',
        'rtdd': '82',
        'rtpidatafeed': 'Port Authority Bus'}]]

if pattern_download:
    for routesec in routes:
        for route in routesec:
            pline = {}
            stop = {}
            rtdir = []
            pat = get_patterns(route['rt'])
            grp = 0
            for pt in pat:
                if pt['rtdir'] in pline:
                    pass
                else:
                    pline[pt['rtdir']] = [['lat', 'lon', 'grp']]
                    stop[pt['rtdir']] = [['lat', 'lon', 'stpnm', 'stpid', 'grp']]
                    rtdir.append(pt['rtdir'])

                grp = grp + 1
                for p in pt['pt']:
                    pline[pt['rtdir']].append([p['lat'], p['lon'], grp])
                    if p['typ'] == 'S':
                        stop[pt['rtdir']].append([p['lat'], p['lon'], p['stpnm'], p['stpid'], grp])

            for direct in rtdir:
                filename = route['rt']+"_"+direct+".csv"
                np.savetxt("api/pline/"+filename, pline[direct], delimiter=", ", fmt='% s')
                np.savetxt("api/stop/"+filename, stop[direct], delimiter=", ", fmt='% s')


maps = {}
for routesec in routes:
    for route in routesec:
        j = 0
        for file in os.listdir('api/pline'):
            if file.startswith(route['rt']+'_'):
                fnamep = os.path.join("api/pline", file)
                maps[file] = folium.Map(location=[40.441, -79.99])

                pl = folium.FeatureGroup(route['rt'])
                dfp = pd.read_csv(fnamep)
                dfp = dfp.groupby(dfp[' grp'])
                dflen = 0
                for g in dfp.groups.keys():
                    if dflen <= len(dfp.get_group(g)[['lat', ' lon']]):
                        dflen = len(dfp.get_group(g)[['lat', ' lon']])
                        geop = dfp.get_group(g)[['lat', ' lon']]

                sw = geop.min().values.tolist()
                ne = geop.max().values.tolist()
                geop = geop.values.tolist()
                pl.add_child(folium.PolyLine(geop,popup=route['rt']))
                maps[file].add_child(pl)
                

                stp = folium.FeatureGroup()
                fnames = os.path.join("api/stop", file)
                dfs = pd.read_csv(fnames)
                geos = dfs.values.tolist()
                for g in geos:
                    stp.add_child(folium.Marker([g[0], g[1]], popup=g[2]))
                maps[file].add_child(stp)
                maps[file].fit_bounds([sw, ne])

                # firstlast = folium.FeatureGroup()
                # firstlast.add_child(folium.Marker(geop[0], icon=folium.Icon(color='green')))
                # firstlast.add_child(folium.Marker(geop[-1], icon=folium.Icon(color='red')))
                # maps[file].add_child(firstlast)

                maps[file].save('templates/maps/'+file.removesuffix('.csv')+'.html')
                print('saved base map for route: '+str(route['rt']))
                j = 1

                
print('base map completed')
t1 = time.time()
print('backend time is: ' + str(t1-t0))

while check:
    flag = False
    # get all of the current vehicles in each route
    # this information is stored in batches of 10 routes

    # Contains the get_vehicles info for every route section
    routesec_veh = {}

    route_veh = {}

    # contains a list of tuples. Each tuple is a key to route_veh
    # use this to search for the tuple in the dictionary for a certain route
    # tp = [item for item in route_list if '61A' in item]
    route_list = []

    # loop through the route section of 10
    for routesec in routes:
        # get route string for get_vehicles
        temp = []
        r = ''
        for route in routesec:
            r = r + route['rt'] + ','
            temp.append(route['rt'])
            
        r = r.removesuffix(',')
        route_list.append(tuple(temp))
        routesec_veh[tuple(temp)] = get_vehicles(r)

        # split up the vid for each route
        for route in routesec:
            vid = {}
            v = []
            route_veh[route['rt']] = []
            for veh in routesec_veh[tuple(temp)]:
                if 'msg' in veh:
                    if veh['msg'] == 'No data found for parameter':
                        flag = True
                        
                        break
                if route['rt'] == veh['rt']:
                    v.append(veh['vid'])
                    route_veh[route['rt']].append([veh['lat'], veh['lon'], veh['des'], veh['vid']])
            if flag == True:
                print('skipped '+route['rt'])
                continue
            
            # split the vid into sets of 10
            v = split_list(v, 10)

            des = {}
            
            for vset in v:
                vout = ''
                vl = len(vset)
                for vsetveh in vset:
                    vout = vout+vsetveh+','
                vout = vout.removesuffix(',')
                # try to get the vehicle predictions
                try:
                    prd = get_predictions(vout, vl)
                    for pr in prd:
                        des[pr['des']] = [pr['rtdir'], pr['prdtm'], pr['stpnm']]
                except:
                    print('no predictions for vid: '+vout)
            fgin = folium.FeatureGroup()
            fgout = folium.FeatureGroup()
            for rt in route_veh[route['rt']]:
                if rt[2] in des:
                    if des[rt[2]][0] == 'INBOUND':
                        print([rt[0], rt[1]])
                        vehinfo = 'Vehicle ID: '+str(rt[3])+'\n' + 'Bus is approaching '+str(des[rt[2]][2])+' at '+str(des[rt[2]][1])
                        fgin.add_child(folium.Marker([rt[0], rt[1]], popup=vehinfo, icon=folium.Icon(color='red')))
                    elif des[rt[2]][0] == 'Outbound':
                        print([rt[0], rt[1]])
                        vehinfo = 'Vehicle ID: '+str(rt[3])+'\n' + 'Bus is approaching '+str(des[rt[2]][2])+' at '+str(des[rt[2]][1])
                        fgout.add_child(folium.Marker([rt[0], rt[1]], popup=vehinfo, icon=folium.Icon(color='red')))
                    else:
                        print('nothing added for: '+str(route['rt']))

            try:
                mcopyin = copy.copy(maps[route['rt']+'_'+'INBOUND.csv'])
                mcopyout = copy.copy(maps[route['rt']+'_'+'Outbound.csv'])

                mcopyin.add_child(fgin)
                mcopyin.save('templates/maps/'+route['rt']+'_'+'INBOUND.html')
                mcopyout.add_child(fgout)
                mcopyout.save('templates/maps/'+route['rt']+'_'+'Outbound.html')
                print('completed route: '+str(route['rt']))
            except:
                print('no map data for route: '+str(route['rt']))
            flag = False
            del fgin
            del fgout

    print('Reached end of while')
    t2 = time.time()
    print('total time is: ' + str(t2-t0))
    time.sleep(60)
        


# %%
