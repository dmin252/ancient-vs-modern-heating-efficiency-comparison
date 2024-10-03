import fipy as fp
import numpy as np

# 메쉬 생성: 층 구조를 고려하여 Y축 방향으로 다른 간격을 설정합니다.
nx = 50  # X축 격자 수
dx = 0.02  # X축 간격

# 층별 두께 설정 (단위: m)
thicknesses = [0.02, 0.05, 0.03]  # 바닥재, 난방 층, 단열재
ny_layers = [int(t / dx) for t in thicknesses]

# 각 층의 메쉬 생성
meshes = [fp.Grid2D(dx=dx, dy=dx, nx=nx, ny=ny) for ny in ny_layers]

# 전체 메쉬 합치기
mesh = fp.CellVariable(mesh=fp.CellVariable(mesh=meshes[0]).mesh)
for m in meshes[1:]:
    mesh = mesh.mesh + m.mesh

# 온도 변수 생성
temperature = fp.CellVariable(name="temperature", mesh=mesh, value=10.0)

# 층별 열전도율 설정 (단위: W/(m·K))
# 온도에 따라 열전도율이 변하도록 함수로 설정
def thermal_conductivity(T):
    k_floor = 0.15  # 바닥재
    k_heating = 1.5  # 난방 층
    k_insulation = 0.04  # 단열재
    # 온도에 따른 변화 (예시로 선형 변화 적용)
    return k_floor + 0.001 * (T - 10)

# 열전도율 변수 생성
k = fp.CellVariable(name="thermal_conductivity", mesh=mesh, value=0.15)

# 열전도율을 온도에 따라 업데이트하는 함수
def update_conductivity():
    k.setValue(thermal_conductivity(temperature))

# 경계 조건 설정
# 바닥 열원: 난방 층 하단에 40°C를 적용
faces_bottom = mesh.facesBottom
temperature.constrain(40.0, faces_bottom)

# 주변 공기와의 대류 열 손실 고려 (뉴턴 냉각 법칙 적용)
h_conv = 10.0  # 대류 열 전달 계수 (W/(m²·K))
T_air = 10.0  # 주변 공기 온도 (°C)

# 대류 열 손실을 위한 계면 설정
faces_top = mesh.facesTop
convective_flux = h_conv * (temperature - T_air)
temperature.faceGrad.constrain(convective_flux, faces_top)

# 방정식 설정
eq = fp.TransientTerm() == fp.DiffusionTerm(coeff=k)

# 시뮬레이션 시간 설정
timeStepDuration = 60.0  # 1분
steps = 100  # 총 시뮬레이션 단계

# 시뮬레이션 실행
for step in range(steps):
    update_conductivity()
    eq.solve(var=temperature, dt=timeStepDuration)
    if step % 10 == 0:
        print(f"Time step {step+1}: Max Temp = {np.max(temperature.value)}")

# 결과 시각화
viewer = fp.Viewer(vars=temperature, datamin=10., datamax=40.)
viewer.plot()

