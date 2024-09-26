from PIL import Image, ImageDraw, ImageFont
import os
import math

# Set image size
# 이미지 크기 설정
width, height = 800, 600

# Define colors
# 색상 정의

background_color = (255, 255, 255)   # 흰색 (White)

 
 
specific_heat_wood = 1.7       # 목재 (목재 벽)

# Specific heat capacities in kJ/kgK
# Density (kg/m^3)

# soil
density_soil = 1600
specific_heat_soil = 0.8      
soil_color = (139, 112, 12)           # 갈색 - 지반층 (Brown - Ground layer)

# air
density_air = 1.225
specific_heat_air = 1.005
airflow_color = (169, 169, 169)        # 공기 흐름 회색 - Light gray - Convection layer (air flow)

# water
density_water = 1000
specific_heat_water = 4.186    # 물 (난방 통로)
heating_passage_color = (173, 216, 230)  # 연한 파란색 - 물 (난방 통로) (Light blue - Water (heating passage))

# floor
density_floor = 2400
specific_heat_floor = 0.88
floor_color = (211, 211, 211)        # 밝은 회색 - 바닥 (Light gray - Floor)

# smoke
density_smoke = 1.225
specific_heat_air = 1.005
smoke_color = (105, 105, 105)        # 어두운 회색 - 연기 (Dark gray - Smoke)

# wood
density_wood = 600
specific_heat_wood = 1.7
wooden_wall_color = (139, 69, 19)    # 갈색 - 목재  (Brown - Wood)

# fire source
fire_color = (255, 0, 0)             # 빨간색 - 화원 (Red - Fire source)
heat_arrow_color = (255, 165, 0)     # 주황색 - 열 흐름 화살표 (Orange - Heat flow arrows)
border_color = (0, 0, 0)             # 검은색 - 경계선 (Black - Border)

# Image creation
# 이미지 생성
image = Image.new('RGB', (width, height), background_color)
draw = ImageDraw.Draw(image)

# Set height
# 높이 설정
ground_top = height * 10 // 11

airflow_layer_height = 50   # 연기 층 두께
airflow_layer_top = ground_top - airflow_layer_height

heating_passage_height = 50
heating_passage_top = airflow_layer_top - heating_passage_height

floor_thickness = 30
floor_top = heating_passage_top - floor_thickness

# Soil layer
# 지반층
draw.rectangle([(0, ground_top), (width, height)], fill=soil_color)

# Convection layer (air flow)
# 공기 흐름
draw.rectangle([(0, airflow_layer_top), (width, ground_top)], fill=airflow_color)

# Heating passage (represented as water)
# 난방 통로 (물로 표현)
draw.rectangle([(0, heating_passage_top), (width, airflow_layer_top)], fill=heating_passage_color)

# Floor
# 바닥
draw.rectangle([(0, floor_top), (width, heating_passage_top)], fill=floor_color)

# Left Wall
# 좌측 목재 벽
wooden_wall_right = width // 6
draw.rectangle([(0, 0), (wooden_wall_right, floor_top)], fill=wooden_wall_color)


# Right Wall
# 우측 목재 벽
wooden_wall_left = width * 5 // 6
draw.rectangle([(wooden_wall_left, 0), (width, floor_top)], fill=wooden_wall_color)


# Ceil
# 천장
ceiling_height = 50
draw.rectangle([(wooden_wall_right, 0), (wooden_wall_left, ceiling_height)], fill=wooden_wall_color)

# Fire source
# 화원 
fire_base_x = 100
fire_base_y = 555 
fire_width = 35
fire_height = 50

# 불꽃 모양 그리기 (Draw flame shape)
def draw_flame(draw, x, y, width, height):
    flame_color = fire_color
    
    # 불꽃의 기본 형태 (Base shape of the flame)
    points = [
        (x, y),
        (x + width * 0.2, y - height * 0.5),
        (x + width * 0.5, y - height),
        (x + width * 0.8, y - height * 0.5),
        (x + width, y)
    ]
    draw.polygon(points, fill=flame_color)

# 불꽃과 장작 그리기 (Draw flame and logs)
draw_flame(draw, fire_base_x, fire_base_y , fire_width, fire_height)

# Smoke Outlet (Chimney)
# 연기 배출구 (굴뚝)
chimney_width = 20
chimney_left = width - 40
chimney_right = chimney_left + chimney_width
chimney_bottom = 500
chimney_top = 0
draw.rectangle([(chimney_left, chimney_top), (chimney_right, chimney_bottom)], fill=airflow_color)

# 왼쪽 경계선 (Left border)
draw.line([(chimney_left, chimney_top), (chimney_left, chimney_bottom)], fill=border_color, width=1)

# 오른쪽 경계선 (Right border)
draw.line([(chimney_right, chimney_top), (chimney_right, chimney_bottom)], fill=border_color, width=1)


# Define the heat flow arrow function
# 열 흐름 화살표 함수 정의
def draw_arrow(draw, start, end, arrow_color, width=2):
    draw.line([start, end], fill=arrow_color, width=width)
    # Draw the arrowhead
    # 화살표 머리 그리기
    arrowhead_length = 10
    angle = math.atan2(end[1] - start[1], end[0] - start[0]) + math.pi
    left_angle = angle + math.pi / 6
    right_angle = angle - math.pi / 6
    left_x = end[0] + arrowhead_length * math.cos(left_angle)
    left_y = end[1] + arrowhead_length * math.sin(left_angle)
    right_x = end[0] + arrowhead_length * math.cos(right_angle)
    right_y = end[1] + arrowhead_length * math.sin(right_angle)
    draw.polygon([end, (left_x, left_y), (right_x, right_y)], fill=arrow_color)


# Heat flow arrows in the heating passage (change to water flow)
# 난방 통로 내의 열 흐름 화살표 (물 흐름으로 변경)
arrow_y = heating_passage_top + heating_passage_height // 2
for i in range(3):
    start_x = 50 + i * 200
    end_x = start_x + 100
    # draw_arrow(draw, (start_x, arrow_y), (end_x, arrow_y), heat_arrow_color)

# Heat flow arrow pointing
# 바닥으로 향하는 열 흐름 화살표
for i in range(5):
    x = 100 + i * 150
    start_y = heating_passage_top
    end_y = floor_top
    # draw_arrow(draw, (x, start_y), (x, end_y), heat_arrow_color)


save_path = r"./"

file_name = "old.bmp"
file_path = os.path.join(save_path, file_name)

image.save(file_path)
print(f"Image Saved: {file_path}")
