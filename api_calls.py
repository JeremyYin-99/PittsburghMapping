# %%
import requests


KEY = "ZYLRG58Qyz5tS7gYmDS3QciuV"
URL = "http://realtime.portauthority.org/bustime/api/v3/"
params = {"key":KEY, "format": "json"}

def get_time():
    locparam = params
    url = URL+"gettime"
    response = requests.get(url, params=locparam)
    return response.json()['bustime-response']

def get_vehicles(rt):
    url = URL+"getvehicles"
    locparam = params
    locparam['rt'] = rt
    response = requests.get(url, params=locparam)
    if 'vehicle' in response.json()['bustime-response']:
        return response.json()['bustime-response']['vehicle']
    else:
        return response.json()['bustime-response']['error']

def get_routes():
    url = URL+"getroutes"
    locparam = params
    response = requests.get(url, params=locparam)
    if 'routes' in response.json()['bustime-response']:
        return response.json()['bustime-response']['routes']
    else:
        return response.json()['bustime-response']['error']

def get_directions(rt):
    url = URL+"getdirections"
    locparam = params
    locparam['rt'] = rt
    locparam['rtpidatafeed'] = 'Port Authority Bus'
    response = requests.get(url, params=params)
    if 'directions' in response.json()['bustime-response']:
        return response.json()['bustime-response']['directions']
    else:
        return response.json()['bustime-response']['error']

def get_stops(p):
    url = URL+"getstops"
    locparam = params
    if len(p) == 1:
        locparam['stpid'] = p
    else:
        locparam['rt'] = p[0]
        locparam['dir'] = p[1]
    response = requests.get(url, params=locparam)
    if 'stops' in response.json()['bustime-response']:
        return response.json()['bustime-response']['stops']
    else:
        return response.json()['bustime-response']['error']

def get_patterns(rt):
    url = URL+"getpatterns"
    locparam = params
    locparam['rt'] = rt
    locparam['rtpidatafeed'] = 'Port Authority Bus'
    response = requests.get(url, params=params)
    if 'ptr' in response.json()['bustime-response']:
        return response.json()['bustime-response']['ptr']
    else:
        return response.json()['bustime-response']['error']


def get_predictions(vid, top=None):
    url = URL+"getpredictions"
    locparam = params

    locparam['vid'] = vid
    locparam['rtpidatafeed'] = 'Port Authority Bus'

    if top != None:
        locparam['top'] = top
    response = requests.get(url, params=locparam)
    if 'prd' in response.json()['bustime-response']:
        return response.json()['bustime-response']['prd']
    else:
        return response.json()['bustime-response']['error']

def get_service_bulletins(rt=None, rtdir=None):
    url = URL+"getservicebulletins"
    locparam = params
    if rt != None:
        locparam['rt'] = rt
        if rtdir != None:
            locparam['rtdir'] = rtdir
    locparam['rtpidatafeed'] = 'Port Authority Bus'
    response = requests.get(url, params=params)
    return response.json()['bustime-response']

def get_rtpi_datafeeds():
    url = URL+"getrtpidatafeeds"
    locparam = params
    response = requests.get(url, params=locparam)
    return response.json()['bustime-response']['rtpidatafeeds']

def get_detours(rt=None, rtdir=None):
    url = URL+"getdetours"
    locparam = params
    if rt != None:
        locparam['rt'] = rt
        if rtdir != None:
            locparam['rtdir'] = rtdir
    response = requests.get(url, params=locparam)
    return response.json()['bustime-response']




# %%
