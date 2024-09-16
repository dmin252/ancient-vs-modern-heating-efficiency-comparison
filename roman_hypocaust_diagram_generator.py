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
