import fipy as fp
import numpy as np

# 메쉬의 복잡도를 증가시킵니다.
nx = 50  # X축 격자 수
ny = 50  # Y축 격자 수
dx = 0.02  # X축 간격
dy = 0.02  # Y축 간격

# 구조적 변화를 추가하기 위해 메쉬를 조정합니다.
mesh = fp.Grid2D(dx=dx, dy=dy, nx=nx, ny=ny)

# 온도 변수 생성
temperature = fp.CellVariable(name="temperature", mesh=mesh, value=0)

# 바닥 열원 설정
temperature.constrain(40.0, mesh.facesBottom)

# 주변 열 손실 조건 설정
temperature.constrain(10.0, mesh.facesTop)
temperature.constrain(10.0, mesh.facesLeft)
temperature.constrain(10.0, mesh.facesRight)

# 열 확산 계수 설정
D = 1.0  # 재료의 열전도율

# 방정식 설정
eq = fp.TransientTerm() == fp.DiffusionTerm(coeff=D)

# 시뮬레이션 시간 설정
timeStepDuration = 300.0  # 5분
steps = 20  # 총 시뮬레이션 단계

# 시뮬레이션 실행
for step in range(steps):
    eq.solve(var=temperature, dt=timeStepDuration)
    print(f"Time step {step + 1}: Max Temp = {np.max(temperature.value)}")

# 결과 시각화
viewer = fp.Viewer(vars=temperature, datamin=0., datamax=40.)
viewer.plot()

# 플롯 창을 오래 열어두기 위한 코드 추가
print("Close the plot window to end the program.")
input("Press Enter to close...")  # 사용자가 Enter를 누를 때까지 대기

