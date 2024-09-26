import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image

img_path = "./old.bmp"
image = Image.open(img_path)
pixels = np.array(image)
color_to_index = {
    (139, 112, 12): 0,  # 갈색 - 지반층 Brown - Ground layer
    (169, 169, 169): 1,  # 공기 흐름 회색 Gray - Airflow
    (255, 255, 255): 2,  # 공기 흐름 흰색(Room) White - Airflow(Room)
    (173, 216, 230): 3,  # 연한 파란색 - 난방 통로 Light blue - Heating duct
    (211, 211, 211): 4,  # 밝은 회색 - 바닥 Light gray - Floor
    (105, 105, 105): 5,  # 어두운 회색 - 연기 Dark gray - Smoke
    (139, 69, 19): 6,  # 갈색 - 목재 벽 Brown - Wooden wall
    (255, 0, 0): 7,  # 빨간색 - 화원 Red - Furnace
    (0, 0, 0): 8  # 검은색 - 경계선 Black - Boundary
}

indexes = np.zeros(pixels.shape[:2], dtype=int)
for color, index in color_to_index.items():
    mask = (pixels == color).all(axis=2)
    indexes[mask] = index

# Initialization of variables for heat diffusion simulation
k = 0.5  # Thermal conductivity
delta_x = 0.10  # Spatial step (m)
delta_t = 1  # Time step (s)


rho = np.array([1600, 1.225, 1.225, 1000, 2400, 1.225, 600, 1, 1])
cp = np.array([0.8 * 1000, 1.005 * 1000, 1.005 * 1000, 4.186 * 1000, 0.88 * 1000, 1.005 * 1000, 1.7 * 1000, 1000, 1000])
alpha = k / (rho * cp)
temperature = np.ones_like(indexes, dtype=float) * 25
temperature[indexes == 7] = 1000  # 열원 온도 설정

# 그림 업데이트 함수
def update(frame):
    global temperature
    new_temperature = temperature.copy()
    
    # Apply the Finite Difference Method (FDM)
    # Calculate the Laplacian of the temperature distribution
    new_temperature[1:-1, 1:-1] += alpha[indexes[1:-1, 1:-1]] * delta_t / delta_x**2 * (
        temperature[2:, 1:-1] + temperature[:-2, 1:-1] + temperature[1:-1, 2:] + temperature[1:-1, :-2] - 4 * temperature[1:-1, 1:-1]
    )
    
    # Update the temperature distribution
    temperature = new_temperature
    
    # Update the image with the new temperature values
    im.set_array(temperature)
    return [im]

# 애니메이션 설정
fig, ax = plt.subplots()
im = ax.imshow(temperature, cmap='hot', interpolation='nearest', animated=True)
ani = FuncAnimation(fig, update, frames=100, interval=50, blit=True)

plt.colorbar(im)
plt.show()
