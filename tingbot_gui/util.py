import math

def clamp(minimum, maximum, value):
    """returns value, constrained to be within the specified minimum and maximum"""
    return max(minimum, min(maximum, value))
    
def distance(a,b):
    return math.hypot(a[0]-b[0],a[1]-b[1])
