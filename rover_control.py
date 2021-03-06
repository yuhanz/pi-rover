from gpio_dc_control import *

PWM_FREQUENCY = 500
PWM_INITIAL_DUTY = 15
MOTOR_INPUT_VOLTAGE = 6     # measured as 5.24V at L298N output
DC_MAX_VOLTAGE = 4          # TT motor is recommended to run at 6-8V; between 3V~12VDC

GPIO.setmode(GPIO.BCM)

pwmControlWheelRight = PwmDcControl(name = "rightWheel", ena = 25, in1 = 23, in2 = 24, pwmFrequency = PWM_FREQUENCY, pwmDuty = PWM_INITIAL_DUTY, inputVoltage = MOTOR_INPUT_VOLTAGE, dcMaxVoltage = DC_MAX_VOLTAGE)
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
    pwmControlWheelLeft.setStrength(rate)
    pwmControlWheelRight.setStrength(rate)

def setFrequency(frequency):
    pwmControlWheelLeft.setPwmFrequency(frequency)
    pwmControlWheelRight.setPwmFrequency(frequency)

setSpeed(1.0)

#GPIO.cleanup()
