# This is the file containing all of the classes used in the porject
class Trip:

    def __init__(self, trip_id, route_id, head_sign, direction_id, block_id, shape_id):
        self.trip_id = trip_id
        self.route_id = route_id
        self.head_sign = head_sign
        self.direction_id = direction_id
        self.block_id = block_id
        self.shape_id = [shape_id]

    def add_shape(self, shape_id):
        self.shape_id.append(shape_id)

class Stop:

    stop_lat_long = []
    stop_name = ""

    def __init__(self, trip_id, time, stop_id, stop_sequence, shape_dist_travel):
        self.trip_id = set(trip_id)
        self.time = [time]
        self.stop_id = stop_id
        self.stop_sequence = stop_sequence
        self.shape_dist_travel = shape_dist_travel

    def get_lat_long(self, stop_name, stop_lat, stop_long):
        self.stop_name = stop_name
        self.stop_lat_long = [float(stop_lat), float(stop_long)]
        return self.stop_lat_long

class Shape:

    def __init__(self, shape_id, shape_lat, shape_long, shape_sequence): # distance at the end of list for GTFS
        self.shape_id = shape_id
        self.shape_lat_long = [[float(shape_lat), float(shape_long)]]
        self.shape_list =[[float(shape_lat), float(shape_long)], shape_sequence] # distance at the end of list for GTFS

    def add_shape_data(self, shape_lat, shape_long, shape_sequence): # distance at the end of list for GTFS
        self.shape_lat_long.append([float(shape_lat), float(shape_long)])
        self.shape_list.append([[float(shape_lat), float(shape_long)], shape_sequence])# distance at the end of list for GTFS

class Route:

    def __init__(self, route_id, trip_id, shape_id, shape_class = None):
        self.route_id = route_id
        self.trip_id = trip_id
        self.shape_id = [shape_id]
        if shape_class == None:
            self.shape_class = []
        else:
            self.shape_class = [shape_class]
    
    def add_shape(self, shape_id, shape_class):
        self.shape_id.append(shape_id)
        self.shape_class.append(shape_class)

    def get_shape_class(self):
        return self.shape_class
    

            