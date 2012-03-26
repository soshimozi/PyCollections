import math
import pyCollections as col
from functional import partial

class navnode(object):
    def __init__(self, point, neighbors):
        self._point = point
        self._neighbors = neighbors

class route(object):
    def __init__(self, point, r, length, score):
        self._point = point
        self._length = length
        self._route = r
        self._score = score

class point(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    def __repr__(self):
        return repr(self._x)  + "," + repr(self._y)

def print_route(r):
    s = []
    while r:
        s.append(r._point)
        r = r._route

    while len(s):
        print(s.pop())

def height_at(p):
    height_map = [10,10,10,10,10,10,00,00,00,00,00,00,00,00,00,00,00,00,00,00,
                  10,10,10,10,10,10,10,10,10,10,00,00,00,00,00,00,00,00,00,00,
                  00,00,10,10,10,10,10,20,20,10,10,10,00,00,00,00,00,00,00,00,
                  00,00,00,10,10,10,20,20,30,20,10,10,10,00,00,00,10,10,00,00,
                  00,00,00,10,10,10,20,30,40,30,10,10,10,00,00,10,10,20,10,00,
                  00,00,00,10,10,10,20,30,40,20,10,10,10,10,00,10,20,20,10,00,
                  00,00,00,10,10,10,20,20,30,20,10,10,10,10,00,10,20,30,20,10,
                  00,00,00,10,10,10,20,20,30,20,20,10,10,10,00,10,30,30,20,00,
                  00,00,00,10,10,10,10,20,20,20,20,20,10,10,00,10,20,40,30,00,
                  00,00,00,10,10,10,10,20,20,20,20,20,10,00,10,30,40,30,10,00,
                  00,00,00,10,10,10,10,10,20,20,20,10,10,00,20,40,30,20,10,00,
                  00,00,00,10,10,10,10,10,10,20,10,10,10,10,20,40,30,10,10,00,
                  00,00,00,00,10,10,10,10,10,10,10,10,00,10,20,30,30,20,10,00,
                  00,00,00,00,10,10,10,10,10,10,10,10,00,10,20,30,20,10,10,00,
                  00,00,00,00,00,10,10,10,10,10,10,00,00,10,20,20,20,10,00,00,
                  00,00,00,00,00,00,00,10,10,00,00,00,00,10,20,20,10,10,00,00,
                  00,00,00,00,00,00,00,00,00,00,00,00,00,10,10,10,10,10,00,00,
                  00,00,00,00,00,10,10,10,00,00,00,00,00,10,10,10,10,00,00,00,
                  00,00,00,00,10,30,20,10,00,00,00,00,00,00,00,00,00,00,00,00,
                  00,00,10,10,20,10,10,00,00,00,00,00,00,00,00,00,00,00,00,00]

    map_size = 20

    index = p._y * map_size + p._x
    return height_map[index]

def same_point(a, b):
    return a._x == b._x and a._y == b._y

def weighted_distance(point_a, point_b):
    height_difference = height_at(point_b) - height_at(point_a)
    
    if height_difference < 0:
        climb_factor = 1
    else:
        climb_factor = 10

    if point_a._x == point_b._x or point_a._y == point_b._y:
        flat_distance = 100
    else:
        flat_distance = 141

    return flat_distance + climb_factor * abs(height_difference)

def make_open_list(scorefn):
    return col.BinaryHeap(scorefn)

def make_reached_list():
    return {}

def store_reached(lst, point, route):
    lst[point] = route

def find_reached(lst, point):
    if point in lst:
        return lst[point]

    return None

def estimated_distance(frm, to):
    dx = abs(frm._x - to._x)
    dy = abs(frm._y - to._y)

    if dx > dy:
        return (dx - dy) * 100 + dy * 141
    else:
        return (dy - dx) * 100 + dx * 141

def add_open_route(opn, reached, route):
    opn.push(route)
    store_reached(reached, route._point, route)

def possible_directions(frm):
    map_size = 20

    add_points = lambda a, b: point(a._x + b._x, a._y + b._y)
    inside_map = lambda p: (p._x >=0 and p._x < map_size and p._y >=0 and p._y < map_size)

    directions = [point(-1,0),point(1,0),point(0,-1),
                  point(0,1),point(-1,-1),point(-1,1),
                  point(1,1),point(1,-1)]

    return filter(inside_map, map(partial(add_points, frm), directions))
                  
def find_route(start, goal):

    routescore = lambda r: r._score

    # create a binary heap with the route_value score function
    opnlist = make_open_list(routescore)
    reached = make_reached_list()

    # start, we add start  point to frontier
    add_open_route(opnlist, 
                   reached, 
                   route(start, None, 0, estimated_distance(start, goal)))

    while opnlist.size() > 0:
        # take next best path off frontier
        r = opnlist.pop()

        # are we there yet?
        if same_point(r._point, goal):
            return r

        # get directions we can move
        for direction in possible_directions(r._point):

            # check that it's not been reached yet
            known = find_reached(reached, direction)

            # calculate g(x) + h(x)
            dist = weighted_distance(r._point, direction) 

            new_length = r._length + dist

            if not known or known._length > new_length:

                # the new length is greater, so remove
                if known:
                    open.remove(known)

                score = estimated_distance(direction, goal)+new_length
                
                # add to open list
                add_open_route(opnlist, 
                               reached, 
                               route(direction, 
                                     r, 
                                     new_length, 
                                     score))

    return None
   
