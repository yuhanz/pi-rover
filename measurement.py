import math
import time
import threading
from mpu6050 import mpu6050

sensor = mpu6050(0x68)
accel_data = None
gyro_data = None
applied_force = 0
gravity = 0
cosTheta = 0
thetaDot = 0

lastThetaDot = 0
lastThetaDotTime = 0

def getMeasuredGravity():
  return gravity

def getMeasuredAngle():
  return cosTheta

def getGravityMagnitude(ax, ay, az):
  return math.sqrt(ax**2 + ay**2 + az**2)

def getThetaDot(thetaDotX, thetaDotY, thetaDotZ):
  return thetaDotY

def recordCurrentThetaDot(thetaDotX, thetaDotY, thetaDotZ):
  global lastThetaDot
  lastThetaDot = getThetaDot(thetaDotX, thetaDotY, thetaDotZ)
  lastThetaDotTime = time.time()

def getThetaDot2(thetaDotX, thetaDotY, thetaDotZ):
  thetaDot = getThetaDot(thetaDotX, thetaDotY, thetaDotZ)
  delta = thetaDot - lastThetaDot
  time = time.time()
  timeDelta = time - lastThetaDotTime
  return delta / timeDelta


# output in radian.
# works only when there's no external force.
# f * g * cosA = ax
def getCosThetaByGravity(ax, ay, az, g = None):
  if not g:
    g = getGravityMagnitude(ax, ay, az)
  largestA = max([abs(ax), abs(ay), abs(az)])
  cosTheta = abs(largestA) / g
  return cosTheta

# acceleration caused by external force
def getAppliedForce(ax, ay, az, gravity):
    g = getGravityMagnitude(ax, ay, az)
    return g - gravity

def worker_main():
  print("worker started")
  time.sleep(1.0)
  while 1:
    global accel_data
    global gyro_data
    accel_data = sensor.get_accel_data()
    gyro_data = sensor.get_gyro_data()
    global gravity
    # TODO: gravity should be measure at the beginning.
    ax = accel_data.x
    ay = accel_data.y
    az = accel_data.z
    gravity = getGravityMagnitude(ax, ay, az)
    applied_force = getAppliedForce(ax, ay, az, gravity)
    global cosTheta
    cosTheta = getCosThetaByGravity(ax, ay, az, gravity)
    time.sleep(1.0)

worker_thread = threading.Thread(target=worker_main)
worker_thread.start()
