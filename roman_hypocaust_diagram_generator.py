from PIL import Image, ImageDraw, ImageFont
import os
import math

# Set image size
width, height = 800, 600

# Define colors
background_color = (255, 255, 255)   # White

soil_color = (139, 69, 19)           # Brown - Ground layer
stone_color = (169, 169, 169)        # Light gray - Stone layer
heating_passage_color = (173, 216, 230)  # Light blue - Water (Heating passage)
floor_color = (211, 211, 211)        # Light gray - Floor
fire_color = (255, 0, 0)             # Red - Fire source
smoke_color = (105, 105, 105)        # Dark gray - Smoke
heat_arrow_color = (255, 165, 0)     # Orange - Heat flow arrow
cushion_color = (255, 192, 203)      # Pink - Cushion
wooden_wall_color = (139, 69, 19)    # Brown - Wooden wall
border_color = (0, 0, 0)             # Black - Border line

# Create image
image = Image.new('RGB', (width, height), background_color)
draw = ImageDraw.Draw(image)

# Set heights
ground_top = height * 3 // 4

stone_layer_height = 50   # Stone layer thickness
stone_layer_top = ground_top - stone_layer_height

heating_passage_height = 50
heating_passage_top = stone_layer_top - heating_passage_height

floor_thickness = 20
floor_top = heating_passage_top - floor_thickness

# Ground layer
draw.rectangle([(0, ground_top), (width, height)], fill=soil_color, outline=border_color)

# Stone layer
draw.rectangle([(0, stone_layer_top), (width, ground_top)], fill=stone_color, outline=border_color)

# Heating passage (represented by water)
draw.rectangle([(0, heating_passage_top), (width, stone_layer_top)], fill=heating_passage_color, outline=border_color)

# Floor
draw.rectangle([(0, floor_top), (width, heating_passage_top)], fill=floor_color, outline=border_color)

# Right wooden wall
wooden_wall_left = width * 3 // 4
draw.rectangle([(wooden_wall_left, 0), (width, floor_top)], fill=wooden_wall_color, outline=border_color)

# Cushions on the floor
# Cushion 1
cushion1_left = width // 4
cushion1_right = cushion1_left + 60
cushion1_bottom = floor_top - 10
cushion1_top = cushion1_bottom - 30
draw.ellipse([(cushion1_left, cushion1_top), (cushion1_right, cushion1_bottom)], fill=cushion_color, outline=border_color)

# Cushion 2
cushion2_left = width // 2
cushion2_right = cushion2_left + 60
cushion2_bottom = floor_top - 10
cushion2_top = cushion2_bottom - 30
draw.ellipse([(cushion2_left, cushion2_top), (cushion2_right, cushion2_bottom)], fill=cushion_color, outline=border_color)

# Fire source (adjusted downward)
fire_base_x = 20
fire_base_y = heating_passage_top + heating_passage_height + 20  # Adjusted downward
fire_tip_x = fire_base_x + 20
fire_tip_y = fire_base_y - 40
draw.polygon([(fire_base_x, fire_base_y), (fire_tip_x, fire_tip_y), (fire_base_x + 40, fire_base_y)], fill=fire_color, outline=border_color)

# Smoke outlet (chimney)
chimney_width = 20
chimney_left = width - 40
chimney_right = chimney_left + chimney_width
chimney_bottom = heating_passage_top + heating_passage_height // 2
chimney_top = chimney_bottom - 100
draw.rectangle([(chimney_left, chimney_top), (chimney_right, chimney_bottom)], fill=stone_color, outline=border_color)

# Smoke rising from the chimney
smoke_x = (chimney_left + chimney_right) // 2
for i in range(5):
    smoke_radius = 10 + i * 5
    smoke_center_y = chimney_top - i * 15
    draw.ellipse([(smoke_x - smoke_radius, smoke_center_y - smoke_radius),
                  (smoke_x + smoke_radius, smoke_center_y + smoke_radius)],
                 fill=smoke_color, outline=border_color)

# Define heat flow arrow function
def draw_arrow(draw, start, end, arrow_color, width=2):
    draw.line([start, end], fill=arrow_color, width=width)
    # Draw arrowhead
    arrowhead_length = 10
    angle = math.atan2(end[1] - start[1], end[0] - start[0]) + math.pi
    left_angle = angle + math.pi / 6
    right_angle = angle - math.pi / 6
    left_x = end[0] + arrowhead_length * math.cos(left_angle)
    left_y = end[1] + arrowhead_length * math.sin(left_angle)
    right_x = end[0] + arrowhead_length * math.cos(right_angle)
    right_y = end[1] + arrowhead_length * math.sin(right_angle)
    draw.polygon([end, (left_x, left_y), (right_x, right_y)], fill=arrow_color)

# Heat flow arrows inside the heating passage (changed to water flow)
arrow_y = heating_passage_top + heating_passage_height // 2
for i in range(3):
    start_x = 50 + i * 200
    end_x = start_x + 100
    draw_arrow(draw, (start_x, arrow_y), (end_x, arrow_y), heat_arrow_color)

# Heat flow arrows towards the floor
for i in range(5):
    x = 100 + i * 150
    start_y = heating_passage_top
    end_y = floor_top
    draw_arrow(draw, (x, start_y), (x, end_y), heat_arrow_color)

# Get save path from external input
save_path = input("Enter the directory where the image should be saved: ")
if not os.path.exists(save_path):
    os.makedirs(save_path)

file_name = "roman_hypocaust_conceptual_with_borders.bmp"
file_path = os.path.join(save_path, file_name)

# Save image
image.save(file_path)
print(f"Image has been saved: {file_path}")
