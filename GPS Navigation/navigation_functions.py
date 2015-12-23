"""
File: geo_edited.py
Description: This is an edited version of geo.py
to work with the pyboard.
"""

import math

EARTH_RADIUS = 6370000
MAG_LAT = 82.7
MAG_LON = -114.4

direction_names = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S",
                   "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"]

directions_num = len(direction_names)
directions_step = 360 / directions_num


def calculate_bearing(position1, position2):
    ''' Calculate the bearing between two GPS coordinates
    Equations from: http://www.movable-type.co.uk/scripts/latlong.html
    Input arguments:
        position1 = lat/long pair in decimal degrees DD.dddddd
        position2 = lat/long pair in decimal degrees DD.dddddd
    Returns:
        bearing = initial bearing from position 1 to position 2 in degrees
    Created: Joshua Vaughan - joshua.vaughan@louisiana.edu - 04/23/14
    Modified:
        *
    '''
    print(position1[0])
    lat1 = math.radians(position1[0])
    long1 = math.radians(position1[1])
    lat2 = math.radians(position2[0])
    long2 = math.radians(position2[1])

    dLon = long2 - long1

    y = math.sin(dLon) * math.cos(lat2)
    x = math.cos(lat1)*math.sin(lat2) - math.sin(lat1)*math.cos(lat2)*math.cos(dLon)

    bearing = (math.degrees(math.atan2(y, x)) + 360) % 360

    return bearing


def calculate_distance(position1, position2):
    ''' Calculate the distance between two lat/long coordinates using a unit sphere
    Copied from: John Cook at http://www.johndcook.com/python_longitude_latitude.html
    Input arguments:
        position1 = lat/long pair in decimal degrees DD.dddddd
        position2 = lat/long pair in decimal degrees DD.dddddd
    Returns:
        distance = distance from position 1 to position 2 in meters
    Modified:
        *Joshua Vaughan - joshua.vaughan@louisiana.edu - 04/23/14
            - Additional commenting
            - Modified to match "theme" of CRAWLAB
            - Inputs change to long/lat array slices
    '''

    lat1, long1 = position1
    lat2, long2 = position2

    R = 6373000        # Radius of the earth in m

    # Convert latitude and longitude to spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0

    # phi = 90 - latitude
    phi1 = math.radians(90.0 - lat1)
    phi2 = math.radians(90.0 - lat2)

    # theta = longitude
    theta1 = math.radians(long1)
    theta2 = math.radians(long2)

    # Compute spherical distance from spherical coordinates.

    # For two locations in spherical coordinates
    # (1, theta, phi) and (1, theta, phi)
    # cosine( arc length ) =
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length

    cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) +
           math.cos(phi1) * math.cos(phi2))

    arc = math.acos(cos)

    # Multiply arc by the radius of the earth
    distance = arc * R

    return distance

def calculate_simple_distance(position1, position2):
    ''' Calculate the distance between two lat/long coords using simple cartesian math
    
    Equation from: http://www.movable-type.co.uk/scripts/latlong.html
    
    Input arguments:
        position1 = lat/long pair in decimal degrees DD.dddddd
        position2 = lat/long pair in decimal degrees DD.dddddd
    
    Returns:
        distance = distance from position 1 to position 2 in meters
    
    
    Created: Joshua Vaughan - joshua.vaughan@louisiana.edu - 04/24/14
    
    Modified:
        *
    
    '''
    
    R = 6373000        # Radius of the earth in m
    
    lat1, long1 = position1
    lat2, long2 = position2
    lat1 = math.radians(lat1)
    long1 = math.radians(long1)
    lat2 = math.radians(lat2)
    long2 = math.radians(long2)

    dLat = lat2 - lat1
    dLon = long2 - long1
    
    x = dLon * math.cos((lat1+lat2)/2)
    distance = math.sqrt(x**2 + dLat**2) * R
    
    return distance



# converting functions from Dr. Vaughan
def convert_longitude(long_EW):
    """ Function to convert deg m E/W longitude to DD.dddd (decimal degrees)
    Arguments:
      long_EW : tuple representing longitude
                in format of MicroGPS gps.longitude
    Returns:
      float representing longtidue in DD.dddd
    """

    return (long_EW[0] + long_EW[1] / 60) * (1.0 if long_EW[2] == 'E' else -1.0)


def convert_latitude(lat_NS):
    """ Function to convert deg m N/S latitude to DD.dddd (decimal degrees)
    Arguments:
      lat_NS : tuple representing latitude
                in format of MicroGPS gps.latitude
    Returns:
      float representing latitidue in DD.dddd
    """

    return (lat_NS[0] + lat_NS[1] / 60) * (1.0 if lat_NS[2] == 'N' else -1.0)

def vector(a, b):
    """Function to create a vector from a to b
    Arguments:
        a and b are 3D cartesian coordinates
    Returns:
        A 3D vector
    """

    vector = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    return vector


def dot(p1, p2):

    """ Dot product of two vectors """
    return p1[0] * p2[0] + p1[1] * p2[1] + p1[2] * p2[2]

def cross(p1, p2):

    """ Cross product of two vectors """
    x = p1[1] * p2[2] - p1[2] * p2[1]
    y = p1[2] * p2[0] - p1[0] * p2[2]
    z = p1[0] * p2[1] - p1[1] * p2[0]
    return x, y, z

def determinant(p1,p2,p3):

    """ Determinant of three vectors """
    return dot(p1, cross(p2, p3))

def normalize_angle(angle):

    """ Takes angle in degrees and returns angle from 0 to 360 degrees """
    cycles = angle / 360
    normalized_cycles = cycles - math.floor(cycles)
    return normalized_cycles * 360

def sgn(x):
    """ Returns sign of number """
    if x == 0:
        return 0.
    elif x > 0:
        return 1.
    else:
        return -1.

def angle(v1, v2, n=None):
    """ Returns angle between v1 and v2 in degrees. n can be a vector that
        points to an observer who is looking at the plane containing v1 and v2.
        This way, you can get well-defined signs. """
    if n == None:
        n = cross(v1, v2)

    prod = dot(v1, v2) / math.sqrt(dot(v1, v1) * dot(v2, v2))
    if prod > 1:
        prod = 1.0 # avoid numerical problems for very small angles
    rad = sgn(determinant(v1, v2, n)) * math.acos(prod)
    deg = math.degrees(rad)
    return normalize_angle(deg)

def great_circle_angle(p1,p2,p3):
    """ Returns angle w(p1,p2,p3) in degrees. Needs p1 != p2 and p2 != p3. """
    n1 = cross(p1, p2)
    n2 = cross(p3, p2)
    return angle(n1, n2, p2)

def distance(p1, p2, r=EARTH_RADIUS):
    """ Returns length of curved way between two points p1 and p2 on a sphere
        with radius r. """
    return math.radians(angle(p1, p2)) * r

def direction_name(angle):
    """ Returns a name for a direction given in degrees. Example:
        direction_name(0.0) returns "N", direction_name(90.0) returns "O",
        direction_name(152.0) returns "SSO". """
    index = int(round(normalize_angle(angle) / directions_step))
    index %= directions_num
    return direction_names[index]

magnetic_northpole = xyz(MAG_LAT, MAG_LON)
geographic_northpole = xyz(90, 0)