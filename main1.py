import numpy as np

def simulate_boiler(boiler_map, temp_map, iterations):
    height, width = boiler_map.shape
    efficiency_history = []
    temp_maps = [temp_map.copy()]  # Store the initial temperature map
    
    for i in range(iterations):
        new_temp_map = temp_map.copy()
        for y in range(1, height - 1):
            for x in range(1, width - 1):
                if boiler_map[y, x] != 0:  # Only diffuse if not a boundary
                    neighbors = temp_map[y-1:y+2, x-1:x+2]
                    new_temp_map[y, x] = np.mean(neighbors)
        
        temp_map = new_temp_map
        total_heat = np.sum(temp_map[boiler_map > 128])
        heat_inside_boundary = np.sum(temp_map[(boiler_map > 128) & (boiler_map < 255)])
        efficiency = heat_inside_boundary / total_heat if total_heat != 0 else 0
        efficiency_history.append(efficiency)
        temp_maps.append(temp_map.copy())
    
    return temp_map, efficiency_history, temp_maps

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
