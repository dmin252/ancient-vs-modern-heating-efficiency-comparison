import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.widgets import Button, Slider, TextBox
from PIL import Image

# 이미지 불러오기
img_path = "./old.bmp"
image = Image.open(img_path)
pixels = np.array(image)

# 색상과 인덱스 매핑
color_to_index = {
    (139, 112, 12): 0,   # 갈색 - 지반층
    (169, 169, 169): 1,  # 회색 - 공기 흐름
    (255, 255, 255): 2,  # 흰색 - 공기 흐름 (방)
    (173, 216, 230): 3,  # 연한 파란색 - 난방 통로
    (211, 211, 211): 4,  # 밝은 회색 - 바닥
    (105, 105, 105): 5,  # 어두운 회색 - 연기
    (139, 69, 19): 6,    # 갈색 - 목재 벽
    (255, 0, 0): 7,      # 빨간색 - 화원
    (0, 0, 0): 8         # 검은색 - 경계선
}

# 색상을 인덱스로 변환
indexes = np.zeros(pixels.shape[:2], dtype=int)
for color, index in color_to_index.items():
    mask = np.all(pixels == color, axis=-1)
    indexes[mask] = index


# 초기 온도 분포 설정
room_temp = 25  # 초기 방 온도 설정
temperature = np.ones_like(indexes, dtype=float) * room_temp
fire_temp = 200  # 초기 화원 온도 설정
temperature[indexes == 7] = fire_temp

# 열 확산 시뮬레이션을 위한 변수 초기화
# Thermal conductivity values for each material (W/m·K)
k = np.array([
    1.5,    # Ground layer (soil)
    0.026,  # Airflow
    0.026,  # Airflow (room)
    0.6,    # Heating path (water)
    1.7,    # Floor (concrete)
    0.026,  # Smoke (similar to air)
    0.15,   # Wooden wall
    0.5,    # Fire source (arbitrary value)
    0.1     # Boundary (arbitrary value)
])

delta_x = 0.01   # 공간 간격 (m)
delta_t = 10      # 시간 간격 (s)

# 각 재질의 물성치 설정
rho = np.array([1600, 1.225, 1.225, 1000, 2400, 1.225, 600, 1, 1])
cp = np.array([0.8e3, 1.005e3, 1.005e3, 4.186e3, 0.88e3, 1.005e3, 1.7e3, 1e3, 1e3])
alpha = k / (rho * cp)

# 초기 온도 분포 설정
temperature = np.ones_like(indexes, dtype=float) * 25
temperature[indexes == 7] = 200  # 화원의 온도 설정

def update(frame):
    if not running:
        return [im]  # 실행 중이지 않으면 업데이트 없이 현재 상태 유지

    global temperature
    new_temperature = temperature.copy()
    try:
        T = temperature
        idx = indexes
        a = alpha[idx]
        laplacian = (T[:-2, 1:-1] + T[2:, 1:-1] + T[1:-1, :-2] + T[1:-1, 2:] - 4 * T[1:-1, 1:-1]) / delta_x**2
        new_temperature[1:-1, 1:-1] = T[1:-1, 1:-1] + a[1:-1, 1:-1] * delta_t * laplacian
    except Exception as e:
        print(f"An error occurred: {e}")
        print(f"Temperature values: {T[1:-1, 1:-1]}")
        print(f"Laplacian values: {laplacian}")
        return []

    new_temperature[indexes == 7] = 200  # Keep fire source at 200°C
    temperature = new_temperature
    im.set_array(temperature)
    return [im]

def start(event):
    global running
    running = True

def stop(event):
    global running
    running = False
    
def reset(event):
    global temperature, running
    running = False  # 시뮬레이션 정지
    temperature = np.ones_like(indexes, dtype=float) * room_temp  # 온도를 초기 방 온도로 초기화
    temperature[indexes == 7] = fire_temp  # 화원 온도로 설정
    im.set_array(temperature)
    
# 그래프 설정
fig, ax = plt.subplots(figsize=(10, 10))
plt.subplots_adjust(top=0.85, bottom=0.15)

ax.set_title('Simulation    ')
ax.set_xlabel('X Axis')
ax.set_ylabel('Y Axis')


# 애니메이션을 위한 초기 설정
im = ax.imshow(temperature, cmap='inferno', interpolation='nearest', animated=True, alpha=0.5, extent=[0, pixels.shape[1], pixels.shape[0], 0])

ax_start = plt.axes([0.1, 0.9, 0.1, 0.075])  # 위치 조정
btn_start = Button(ax_start, 'Start')

ax_stop = plt.axes([0.21, 0.9, 0.1, 0.075])  # 위치 조정
btn_stop = Button(ax_stop, 'Stop')

ax_reset = plt.axes([0.33, 0.9, 0.1, 0.075])  # 위치 조정
btn_reset = Button(ax_reset, 'Reset')


# 애니메이션 제어를 위한 상태 변수
running = True


# 원본 이미지 배경에 표시
ax.imshow(pixels, extent=[0, pixels.shape[1], pixels.shape[0], 0])

# 온도 분포를 반투명하게 겹쳐서 표시
im = ax.imshow(temperature, cmap='inferno', interpolation='nearest', animated=True, alpha=0.5, extent=[0, pixels.shape[1], pixels.shape[0], 0])

# 컬러바에 온도 단위 추가
cbar = plt.colorbar(im, ax=ax)
cbar.set_label('Tempertaure (°C)')

# 애니메이션 생성
ani = FuncAnimation(fig, update, frames=200, interval=50, blit=True)

# 버튼에 함수 연결
btn_start.on_clicked(start)
btn_stop.on_clicked(stop)
# Reset 에러
# btn_reset.on_clicked(reset)



axcolor = 'lightgoldenrodyellow'
ax_temp = plt.axes([0.25, 0.04, 0.65, 0.03], facecolor=axcolor)  
ax_fire = plt.axes([0.25, 0.09, 0.65, 0.03], facecolor=axcolor)  

sld_temp = Slider(ax_temp, 'Room Temp', 15, 30, valinit=room_temp)
sld_fire = Slider(ax_fire, 'Fire Temp', 100, 300, valinit=fire_temp)

def update_val(event):
    global fire_temp, room_temp
    fire_temp = sld_fire.val
    room_temp = sld_temp.val
    temperature[indexes == 7] = fire_temp
    temperature[indexes == 2] = room_temp

sld_temp.on_changed(update_val)
sld_fire.on_changed(update_val)

# 애니메이션 시작
ani = FuncAnimation(fig, update, frames=50, interval=50, blit=True)
plt.show()