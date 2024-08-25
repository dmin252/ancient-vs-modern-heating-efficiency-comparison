import numpy as np

# Initialize the boiler map and temperature map
height, width = 200, 200
boiler_map = np.full((height, width), 255, dtype=np.uint8)  # Initialize empty space as white
temp_map = np.full((height, width), 20, dtype=float)  # Set initial temperature to 20°C
