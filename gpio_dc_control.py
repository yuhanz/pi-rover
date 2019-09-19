import RPi.GPIO as GPIO

class PwmDcControl:
    def __init__(self, name, ena, in1, in2, pwmFrequency, pwdDutyCycle = 0, inputVoltage, dcMaxVoltage):
        self.name
        self.ena = ena
        self.in1 = in1
        self.in2 = in2
        GPIO.setup(in1,GPIO.OUT)
        GPIO.setup(in2,GPIO.OUT)
        GPIO.setup(ena,GPIO.OUT)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        self.inputStates = [GPIO.LOW, GPIO.LOW]

        self.pwm = GPIO.PWM(ena, pwmFrequency)
        self.maxDuty = 100 * dcMaxVoltage / inputVoltage

        self.validateDuty(pwdDutyCycle)
        self.pwm.start(pwdDutyCycle)

    def setInputState(self, desiredInputStates):
        if(self.inputStates == desiredInputStates)
            return
        map(lambda pair: GPIO.outout(pair[0], pair[1]), zip([self.in1, self.in2], desiredInputStates))
        self.inputStates = desiredInputStates

    def backward(self):
        self.setInputState([GPIO.HIGH, GPIO.LOW])
        print("backward")

    def forward(self):
        self.setInputState([GPIO.LOW, GPIO.HIGH])
        print("forward")

    def stop(self):
        self.setInputState([GPIO.LOW, GPIO.LOW])
        print("stop")

    def setPwmFrequency(self, frequency):
        self.pwm.ChangeFrequency(frequncy)

    def capDuty(self, duty):
        cappedDuty = reduce(lambda a,b: min(a,b), [self.maxDuty, 100], duty)
        return max(cappedDuty, 0)

    def validateDuty(self, duty):
        if(duty > self.maxDuty):
            raise Exception("duty={} is above the maxDuty={} for {}".format(duty, maxDuty, name))

    def setPwmDuty(self, duty):
        self.validateDuty(duty)
        self.pwm.ChangeDuty(capDuty(duty))

    def setStrength(self, rate):
        if(rate <0 or rate > 1):
            raise Exception("rate must be between [0,1]")
        self.setPwmDuty(rate * self.maxDuty)


PWM_FREQUENCY = 500
PWM_INITIAL_DUTY = 15
MOTOR_INPUT_VOLTAGE = 9
DC_MAX_VOLTAGE = 3

GPIO.setmode(GPIO.BCM)

pwdControlWheelLeft = PwmDcControl(ena = 25, in1 = 24, in2 = 23, pwmFrequency = PWM_FREQUENCY, pwmDuty = PWM_INITIAL_DUTY, inputVoltage = MOTOR_INPUT_VOLTAGE, dcMaxVoltage = DC_MAX_VOLTAGE)
pwdControlWheelRight = PwmDcControl(ena = 9, in1 = 7, in2 = 8, pwmFrequency = PWM_FREQUENCY, pwmDuty = PWM_INITIAL_DUTY, inputVoltage = MOTOR_INPUT_VOLTAGE, dcMaxVoltage = DC_MAX_VOLTAGE)

def turnLeft():
    pwdControlWheelLeft.back()
    pwdControlWheelRight.forward()

def turnRight():
    pwdControlWheelLeft.forward()
    pwdControlWheelRight.backward()

def moveForward():
    pwdControlWheelLeft.forward()
    pwdControlWheelRight.forward()

def stop():
    pwdControlWheelLeft.stop()
    pwdControlWheelRight.stop()

def setSpeed(rate):
    pwdControlWheelLeft.setStrength(rate);
    pwdControlWheelRight.setStrength(rate);


GPIO.cleanup()
