import midst.interface.main as mim
from test1 import get_directions_to_midpoint_two_modes, mid_point, get_lat_lon

address_1 = "Schwedstraße 16, Berlin, Germany"
address_2 = "Friedelstarße 52, Berlin, Germany, Berlin, Germany"

loc1 = get_lat_lon(address_1)
loc2 = get_lat_lon(address_2)

mode1 = "walking"  
mode2 = "driving"

def find_true_midpoint(loc1, loc2, initial_midpoint, mode1, mode2, counter=0):
    """
    loc1, loc2 are the latitude and longitude for person 1 and person 2
    initial_midpoint: latitude and longitude of the initial midpoint calculated by average 
    counter: number of recursive calls made so far
    """
    # check if counter has reached maximum number of iterations
    if counter >= 10:
        return initial_midpoint
    
    # calculate travel time for person 1 to midpoint
    # calculate travel time for person 2 to midpoint
    travel1, travel2 = get_directions_to_midpoint_two_modes(address_1, address_2, initial_midpoint, mode1, mode2)
    print(travel1,travel2)
    # check if travel times are within 5 minutes of each other
     # if the travel times are within the threshold, the initial midpoint will be returned
     # if the travel times differ by more than 5 minutes, it will continue to change the midpoint
     # threshold of 5 minutes
    if abs(travel1 - travel2) < 300: # 300 seconds = 5 minutes
        return initial_midpoint
    
    # compare travel times
    # if travel 1 is larger than travel 2, a new midpoint is calculated between location 1 and the inital midpoint
    if travel1 > travel2:
        # change midpoint
        new_midpoint = mid_point(loc1, initial_midpoint)
        # print(new_midpoint)
        # call function with new midpoint and increment counter
        return find_true_midpoint(loc1, loc2, new_midpoint, mode1, mode2, counter=counter+1)
    if travel1 < travel2:
        # change midpoint
        new_midpoint = mid_point(loc2, initial_midpoint)
        # call function with new midpoint and increment counter
        return find_true_midpoint(loc1, loc2, new_midpoint, mode1, mode2, counter=counter+1)
    # # add tolerance calculation
    # if travel1 == travel2:
    #     return initial_midpoint

# Test the function 
initial_midpoint = mid_point(loc1, loc2)
print(initial_midpoint)
new_midpoint = find_true_midpoint(loc1, loc2, initial_midpoint, mode1, mode2)
print(new_midpoint)