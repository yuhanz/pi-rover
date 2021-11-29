import numpy as np

massBody = 0.15
massCenterLength = 0.12 # meters
massWheel = 0.1
radiusOfWheel = 0.025 # meters
mass = 0.150  # kg
length = 0.06 # meter
g = -9.8     # gravity acceleration

# gyro reading is anglar velocity
# let x be horizontal, y be vertical, z be the axis of the wheel
# theta is the angle between the body and the vertical axis


# torque = 0
# acceleration in x direction
def holdFromFalling(acceleration, anglarVelocity):
    _, _, ang_v_z = anglarVelocity
    # when the body is not falling, anglarVel_z should be 0.

    # TODO: estimated angle: integration of ang_v_z.

    ax, _, _ = acceleration
    # massBody * ax * massCenterLength = tau * inputAnglarAcceleration
    # inputAnglarAcceleration = ax * someConstant

    # TODO: the constant may be related to the angle theta
    constantToLearn = 123  # TODO
    return ax * constantToLearn

def fromBalanceToAngle(acceleration, theta):



def observeGyro():
    acceleration = np.array(Mpu6050.readAcceleration())
    gyro = np.array(Mpu6050.readGyro())

    print("acceleration: ", acceleration)
    print("gyro: ", gyro)

    ay = acceleration[1]
    az = acceleration[2]
    d = az ** 2 + ay ** 2

    cosTheta = (g * ay - u * az) / (g ** 2 - u ** 2)
    sinTheta = np.sqrt( 1 - cosTheta ** 2 )
    thetaDot = gyro[1]

    return [cosTheta, sinTheta, thetaDot]

x_desired = [1.0, 0.0, 0.0]
# when the pendulum is at up-right:
# theta = 0; thetaDot = 0
# x = [cos(theta); sin(theta); theta']
# x.desired = [1, 0, 0]
# u = -K * (X - X.desired) = -K* (X - [1,0,0])
# X' = [-sin(theta); cos(theta); theta"] = Ax + Bu
# theta" = (m*l**2) * u * cos(theta) + g * sin(theta)
# X' = [cos'(theta); sin'(theta); theta"]
# X' = [-sin(theta); cos(theta); mass*length**2 *u +  g* sin(theta)]
# X' = [0* cos(theta) - 1 * sin(theta) + 0*theta' + 0u;
#       1* cos(theta) + 0 * sin(theta) + 0*theta' + 0u;
#       0 * cos(theta) + g * sin(theta) + 0*theta' + mass*length**2 *u]
# X' = Ax + Bu
# A = [0, -1, 0; 1, 0, 0; 0, g, 0]
# B = [0,0,mass*length**2]
# Make up Q and R
# Q = [1, 0, 0; 0, 1, 0; 0, 0, 10]
# R = [0.01]

A = np.matrix('0.0, -1.0, 0.0; 1.0, 0.0, 0.0; 0.0, {}, 0'.format(g))
B = np.matrix('0.0; 0.0; {}'.format(mass*length**2))
Q = np.matrix('1.0, 0.0, 0.0; 0.0, 1.0, 0.0; 0.0, 0.0, 10.0')
R = np.matrix('0.01')

K, S, E = control.lqr(A, B, Q, R)

def stepByLQR(observation):
    x = observation
    u = np.matmul(-K, x - x_desired)
    return u
