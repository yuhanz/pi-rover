import numpy as np

mass = 0.150  # kg
length = 0.06 # meter
g = -9.8     # gravity acceleration

def observeGyro():
    acceleration = np.array(Mpu6050.readAcceleration())
    gyro = np.array(Mpu6050.readGyro())

    print("acceleration: ", acceleration)
    print("gyro: ", gyro)

    y = acceleration[1]
    z = acceleration[2]
    d = z **2 + y ** 2

    cosTheta = z / d
    sinTheta = y / d
    thetaDot = gyro[1]

    return [cosTheta, sinTheta, thetaDot]


x_desired = [1.0, 0.0, 0.0]
# when the pendulum is at up-right:
# theta = 0; thetaDot = 0
# x = [cos(theta); sin(theta); theta']
# x.desired = [1, 0, 0]
# u = -K * (X - X.desired) = -K* (X - [1,0,0])
# X' = [-sin(theta); cos(theta); theta"] = Ax + Bu
# theta" = (m*l**2) * u - g*sin(theta)
# m = 1; l = 1; g = 10
# theta" = [u - 10 sin(theta)]
# X' = [cos'(theta); sin'(theta); theta"]
# X' = [-sin(theta); cos(theta); u - 10 sin(theta)]
# X' = [0* cos(theta) -1 * sin(theta) + 0*theta' + 0u;
#       1* cos(theta) +0 * sin(theta) + 0*theta' + 0u;
#       0* cos(theta) -10* sin(theta) + 0*theta' + 1u]
# X' = Ax + Bu
# A = [0, -1, 0; 1, 0, 0; 0, -10, 1]
# B = [0,0,1]
# Make up Q and R
# Q = [1, 0, 0; 0, 1, 0; 0, 0, 10]
# R = [0.01]

mass * length ** 2


A = np.matrix('0.0, -1.0, 0.0; 1.0, 0.0, 0.0; 0.0, {}, {}'.format(g, mass * length ** 2))
B = np.matrix('0.0; 0.0; 1.0')
Q = np.matrix('1.0, 0.0, 0.0; 0.0, 1.0, 0.0; 0.0, 0.0, 3.0')
R = np.matrix('0.1')

K, S, E = control.lqr(A, B, Q, R)

def stepByLQR(observation, env):
    X = observation
    # u = -K * (X - X.desired) = -K* (X - [1,0,0])
    u = np.matmul(-K, X - x_desired)
    return u
