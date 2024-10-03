import fipy as fp
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display, clear_output

# 메쉬 설정
dx = dy = 0.5  # 격자 간격
nx = 50  # X축 격자 수
ny = 100  # Y축 격자 수 (높이를 늘려줌)

mesh = fp.Grid2D(dx=dx, dy=dy, nx=nx, ny=ny)

# 영역 구분: 화덕, 공기층, 바닥층, 실내 공간
# 아래에서부터:
# 0 ~ 5: 화덕
# 5 ~ 25: 공기층 (히포코스트 공간)
# 25 ~ 35: 바닥층
# 35 ~ 100: 실내 공간

# 온도 변수 생성
temperature = fp.CellVariable(name="Temperature", mesh=mesh, value=10.0)

# 재료 열전도율 설정
D_values = np.ones(mesh.numberOfCells) * 1.0  # 기본값

y = mesh.cellCenters[1]

# 화덕 영역 (높은 온도, 열원)
furnace_indices = np.where(y < 5.0)[0]
D_values[furnace_indices] = 1.0  # 열전도율 (예: 벽돌)
temperature.value[furnace_indices] = 100.0  # 화덕 온도

# 공기층 (히포코스트 공간)
hypocaust_indices = np.where((y >= 5.0) & (y < 25.0))[0]
D_values[hypocaust_indices] = 0.1  # 열전도율 (공기)

# 바닥층
floor_indices = np.where((y >= 25.0) & (y < 35.0))[0]
D_values[floor_indices] = 1.5  # 열전도율 (돌이나 콘크리트)

# 실내 공간
room_indices = np.where(y >= 35.0)[0]
D_values[room_indices] = 0.5  # 열전도율 (실내 공기)

# 열전도율을 CellVariable로 설정
D = fp.CellVariable(name="Thermal Conductivity", mesh=mesh, value=D_values)

# 경계 조건 설정
# 좌우 벽은 단열로 가정
temperature.faceGrad.constrain(0.0, where=mesh.exteriorFaces & (mesh.facesLeft | mesh.facesRight))

# 상단은 실내 온도로 유지
ambient_temperature = 20.0
temperature.constrain(ambient_temperature, where=mesh.facesTop)

# 방정식 설정
eq = fp.TransientTerm() == fp.DiffusionTerm(coeff=D)

# 시뮬레이션 설정
timeStepDuration = 1.0  # 시간 간격
steps = 100  # 총 시뮬레이션 단계

# 시각화 설정
fig, ax = plt.subplots(figsize=(6, 12))
for step in range(steps):
    eq.solve(var=temperature, dt=timeStepDuration)
    if step % 10 == 0:
        # 시각화 업데이트
        im = ax.imshow(np.flipud(temperature.value.reshape((ny, nx))), cmap='hot',
                       extent=[0, nx*dx, 0, ny*dy],
                       vmin=ambient_temperature, vmax=100)
        ax.set_title(f"Time Step: {step}")
        ax.set_xlabel('Width')
        ax.set_ylabel('Height')
        if step == 0:
            fig.colorbar(im, ax=ax, orientation='vertical', label='Temperature')
        
        # 이미지 저장
        fig.savefig(f"hypocaust_step_{step}.png")
        
        display(fig)
        clear_output(wait=True)
        plt.pause(0.1)
        ax.clear()

print("시뮬레이션 완료.")
