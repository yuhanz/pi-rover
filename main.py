from gpio_dc_control import *

PWM_FREQUENCY = 500
PWM_INITIAL_DUTY = 15
MOTOR_INPUT_VOLTAGE = 9
DC_MAX_VOLTAGE = 3

GPIO.setmode(GPIO.BCM)

pwmControlWheelRight = PwmDcControl(name = "rightWheel", ena = 25, in1 = 24, in2 = 23, pwmFrequency = PWM_FREQUENCY, pwmDuty = PWM_INITIAL_DUTY, inputVoltage = MOTOR_INPUT_VOLTAGE, dcMaxVoltage = DC_MAX_VOLTAGE)
pwmControlWheelLeft = PwmDcControl(name = "leftWheel", ena = 9, in1 = 7, in2 = 8, pwmFrequency = PWM_FREQUENCY, pwmDuty = PWM_INITIAL_DUTY, inputVoltage = MOTOR_INPUT_VOLTAGE, dcMaxVoltage = DC_MAX_VOLTAGE)

print("Wheel configurations:")
print(pwmControlWheelRight.toString())
print(pwmControlWheelLeft.toString())

def turnLeft():
    pwmControlWheelLeft.backward()
    pwmControlWheelRight.forward()

def turnRight():
    pwmControlWheelLeft.forward()
    pwmControlWheelRight.backward()

def moveForward():
    pwmControlWheelLeft.forward()
    pwmControlWheelRight.forward()
def moveBackward():
    pwmControlWheelLeft.backward()
    pwmControlWheelRight.backward()

def stop():
    pwmControlWheelLeft.stop()
    pwmControlWheelRight.stop()

def setSpeed(rate):
    pwmControlWheelLeft.setStrength(rate);
    pwmControlWheelRight.setStrength(rate);


#GPIO.cleanup()
