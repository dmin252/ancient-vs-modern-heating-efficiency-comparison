import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


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


# Setup color maps
custom_cmap = mcolors.ListedColormap(['black', 'blue', 'red', 'white'])
bounds = [0, 1, 128, 200, 256]
norm = mcolors.BoundaryNorm(bounds, custom_cmap.N)

# Setup temperature color map
temp_cmap = plt.get_cmap('viridis')

# Run simulation and visualize results
iterations = 100
final_temp_map, efficiency_history, temp_maps = simulate_boiler(boiler_map, temp_map, iterations)

fig, axs = plt.subplots(3, 3, figsize=(15, 15))
fig.suptitle('Cylindrical Boiler Simulation', fontsize=16)
num_frames = len(temp_maps)
time_steps = np.linspace(0, num_frames-1, 8, dtype=int)
for i, ax in enumerate(axs.flat[:8]):
    step = time_steps[i]
    im = ax.imshow(temp_maps[step], cmap=temp_cmap, vmin=20, vmax=100)
    ax.set_title(f'Step {step}')
    ax.axis('off')

axs[2, 2].plot(efficiency_history)
axs[2, 2].set_title('Boiler Efficiency')
axs[2, 2].set_xlabel('Iteration')
axs[2, 2].set_ylabel('Efficiency')
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
fig.colorbar(im, cax=cbar_ax, label='Temperature (°C)')
plt.tight_layout()
plt.subplots_adjust(top=0.92, right=0.9)
plt.show()

plt.figure(figsize=(8, 8))
plt.imshow(boiler_map, cmap=custom_cmap, norm=norm)
plt.title('Boiler Structure')
plt.colorbar(label='Component')
plt.axis('off')
plt.show()

