import geopy.distance
def calculate_area(c1, c2):
    return geopy.distance.distance(c1, c2).km


