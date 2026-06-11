# -----------------------------------------
# Drone Delivery Coordinate Script
# -----------------------------------------

# Store coordinates inside a tuple
destination = (34.0522, -118.2437)

# Print the latitude using index 0
print("Latitude (from index):", destination[0])

# Unpack the tuple into two variables
latitude, longitude = destination

# Print the unpacked values
print("Latitude:", latitude)
print("Longitude:", longitude)

