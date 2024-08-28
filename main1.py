import numpy as np

# Initialize the boiler map and temperature map
height, width = 200, 200
boiler_map = np.full((height, width), 255, dtype=np.uint8)  # Initialize empty space as white
temp_map = np.full((height, width), 20, dtype=float)  # Set initial temperature to 20°C

# Create cylindrical boundary
center_x, center_y = width // 2, height // 2
radius = 80
y, x = np.ogrid[:height, :width]
dist_from_center = np.sqrt((x - center_x)**2 + (y - center_y)**2)
boiler_map[dist_from_center == radius] = 0  # Set boundary to black

# Heat sources
heat_source_mask = (np.abs(x - center_x) < 15) & (np.abs(y - center_y) < 15)
boiler_map[heat_source_mask] = 200
temp_map[heat_source_mask] = 100  # Set temperature of heat sources to 100°C

# Water region
water_mask = (dist_from_center < radius) & (y > center_y)
boiler_map[water_mask] = 128
