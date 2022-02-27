import geopy.distance
from math import sqrt
def calculate_area(c1, c2):
    return geopy.distance.distance(c1, c2).km

def calculate_side(diag):
    return sqrt(2)*(diag/2)

