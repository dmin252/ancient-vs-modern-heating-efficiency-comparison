from PIL import Image, ImageDraw
import os
import math

# Set image size
width, height = 800, 600

# Define colors
background_color = (255, 255, 255)    # white
boiler_color = (192, 192, 192)        # gray - boiler body
supply_pipe_color = (255, 0, 0)       # red - supply pipe (hot water)
return_pipe_color = (0, 0, 255)       # blue - return pipe (cold water)
pipe_color = (169, 169, 169)          # light gray - regular pipe
heat_arrow_color = (255, 165, 0)      # orange - heat flow arrow
room_color = (245, 245, 220)          # beige - room interior
floor_color = (211, 211, 211)         # light gray - floor
insulation_color = (255, 228, 181)    # wheat - insulation
border_color = (0, 0, 0)              # black - borders

# Create image
image = Image.new('RGB', (width, height), background_color)
draw = ImageDraw.Draw(image)

# Set room position
room_left = width // 4
room_right = width * 3 // 4
room_top = height // 4
room_bottom = height * 3 // 4

# Set floor structure
floor_thickness = 20
insulation_thickness = 20
heating_pipe_thickness = 20

# Calculate positions of each layer
floor_top = room_bottom - floor_thickness
insulation_top = floor_top - insulation_thickness
heating_pipe_top = insulation_top - heating_pipe_thickness

# Draw room
draw.rectangle([(room_left, room_top), (room_right, floor_top)],
               fill=room_color, outline=border_color)

# Draw floor
draw.rectangle([(room_left, floor_top), (room_right, room_bottom)],
               fill=floor_color, outline=border_color)

# Draw insulation
draw.rectangle([(room_left, insulation_top), (room_right, floor_top)],
               fill=insulation_color, outline=border_color)

# Draw heating pipe layer
draw.rectangle([(room_left, heating_pipe_top), (room_right, insulation_top)],
               fill=floor_color, outline=border_color)

# Draw heating pipes
pipe_spacing = 20
for i in range((room_right - room_left) // pipe_spacing):
    x = room_left + i * pipe_spacing + pipe_spacing // 2
    y_start = heating_pipe_top
    y_end = insulation_top
    draw.line([(x, y_start), (x, y_end)], fill=supply_pipe_color, width=5)

# Draw room walls
wall_thickness = 10
draw.rectangle([(room_left - wall_thickness, room_top),
                (room_left, floor_top)], fill=border_color)
draw.rectangle([(room_right, room_top),
                (room_right + wall_thickness, floor_top)], fill=border_color)
draw.rectangle([(room_left - wall_thickness, room_top - wall_thickness),
                (room_right + wall_thickness, room_top)], fill=border_color)

# Draw boiler body (located outside the room)
boiler_width = 100
boiler_height = 150
boiler_x = room_left - boiler_width - 100
boiler_y = room_bottom - boiler_height
draw.rectangle([(boiler_x, boiler_y),
                (boiler_x + boiler_width, boiler_y + boiler_height)],
               fill=boiler_color, outline=border_color)

# Draw heat source inside the boiler (red rectangle)
heat_source_width = 60
heat_source_height = 30
heat_source_x = boiler_x + (boiler_width - heat_source_width) // 2
heat_source_y = boiler_y + boiler_height // 2 - heat_source_height // 2
draw.rectangle([(heat_source_x, heat_source_y),
                (heat_source_x + heat_source_width, heat_source_y + heat_source_height)],
               fill=heat_arrow_color)

# Draw supply pipe coming out of the boiler
supply_pipe_start_x = boiler_x + boiler_width
supply_pipe_start_y = heat_source_y
supply_pipe_end_x = room_left - wall_thickness
supply_pipe_end_y = heating_pipe_top + (heating_pipe_thickness // 2)
draw.line([(supply_pipe_start_x, supply_pipe_start_y),
           (supply_pipe_start_x + 50, supply_pipe_start_y)], fill=supply_pipe_color, width=10)
draw.line([(supply_pipe_start_x + 50, supply_pipe_start_y),
           (supply_pipe_start_x + 50, supply_pipe_end_y)], fill=supply_pipe_color, width=10)
draw.line([(supply_pipe_start_x + 50, supply_pipe_end_y),
           (supply_pipe_end_x, supply_pipe_end_y)], fill=supply_pipe_color, width=10)

# Draw return pipe
return_pipe_start_x = supply_pipe_end_x
return_pipe_start_y = supply_pipe_end_y + 20
return_pipe_end_x = boiler_x + boiler_width
return_pipe_end_y = heat_source_y + heat_source_height
draw.line([(return_pipe_start_x, return_pipe_start_y),
           (supply_pipe_start_x + 50, return_pipe_start_y)], fill=return_pipe_color, width=10)
draw.line([(supply_pipe_start_x + 50, return_pipe_start_y),
           (supply_pipe_start_x + 50, return_pipe_end_y)], fill=return_pipe_color, width=10)
draw.line([(supply_pipe_start_x + 50, return_pipe_end_y),
           (return_pipe_end_x, return_pipe_end_y)], fill=return_pipe_color, width=10)

# Define function to draw heat flow arrows
def draw_arrow(draw, start, end, arrow_color, width=5):
    draw.line([start, end], fill=arrow_color, width=width)
    # Draw arrowhead
    arrowhead_length = 10
    if start[0] == end[0]:  # Vertical line
        if end[1] < start[1]:  # Arrow pointing up
            head = [(end[0] - arrowhead_length, end[1] + arrowhead_length),
                    (end[0] + arrowhead_length, end[1] + arrowhead_length)]
        else:  # Arrow pointing down
            head = [(end[0] - arrowhead_length, end[1] - arrowhead_length),
                    (end[0] + arrowhead_length, end[1] - arrowhead_length)]
    elif start[1] == end[1]:  # Horizontal line
        if end[0] < start[0]:  # Arrow pointing left
            head = [(end[0] + arrowhead_length, end[1] - arrowhead_length),
                    (end[0] + arrowhead_length, end[1] + arrowhead_length)]
        else:  # Arrow pointing right
            head = [(end[0] - arrowhead_length, end[1] - arrowhead_length),
                    (end[0] - arrowhead_length, end[1] + arrowhead_length)]
    else:
        return  # Do not draw diagonals
    draw.polygon([end] + head, fill=arrow_color)

# Heat flow arrows pointing upwards from heating pipes
for i in range(5):
    x = room_left + (i + 1) * (room_right - room_left) // 6
    start_y = heating_pipe_top
    end_y = room_top + 50
    draw_arrow(draw, (x, start_y), (x, end_y), heat_arrow_color, width=3)

# Set image save path
save_path = r"C:\"
if not os.path.exists(save_path):
    os.makedirs(save_path)

file_name = "modern_gas_boiler_updated.bmp"
file_path = os.path.join(save_path, file_name)

# Save image
image.save(file_path)
print(f"Image has been saved: {file_path}")
