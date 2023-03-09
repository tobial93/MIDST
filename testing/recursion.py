from travel_test1 import get_directions_to_midpoint_two_modes, midpoint

def find_true_midpoint(loc1, loc2, initial_midpoint, mode1, mode2):
    """
    loc1, loc2, initial_midpoint: (lat,lon)
    """
    # calculate travel time for person 1 to midpoint
    # calculate travel time for person 2 to midpoint
    travel1, travel2 = get_directions_to_midpoint_two_modes(loc1, loc2, initial_midpoint, mode1, mode2)
    # compare travel times
    if travel1 > travel2:
        # change midpoint
        new_midpoint = midpoint(loc1, initial_midpoint)
        print(new_midpoint)
        # call function with new midpoint
        return find_true_midpoint(loc1, loc2, new_midpoint)
    if travel1 < travel2:
        # change midpoint
        new_midpoint = midpoint(loc2, initial_midpoint)
        # call function with new midpoint
        return find_true_midpoint(loc1, loc2, new_midpoint)
    # add tolerance calculation
    if travel1 == travel2:
        return initial
    # add depth restriction = max iterations
    

mode1 = "walking"  # This can be selected from the drop-down menu
mode2 = "bicycling" # calculate weights based on the travel mode to adjust for different travel time
person1 = (52.5547798, 13.37502) 
person2 = (52.5069712, 13.3914743)
print(type(midpoint))
initial = midpoint(person1, person2)
result = find_true_midpoint(person1, person2, initial, mode1, mode2)

print(result)