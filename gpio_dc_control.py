import RPi.GPIO as GPIO

class PwmDcControl:
    def __init__(self, name, ena, in1, in2, inputVoltage, dcMaxVoltage, pwmFrequency, pwmDuty = 0):
        self.name = name
        self.ena = ena
        self.in1 = in1
        self.in2 = in2
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(in1,GPIO.OUT)
        GPIO.setup(in2,GPIO.OUT)
        GPIO.setup(ena,GPIO.OUT)
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
        self.pwm = GPIO.PWM(ena, pwmFrequency)
        self.pwmFrequency = pwmFrequency
        self.inputStates = [GPIO.LOW, GPIO.LOW]
        self.maxDuty = 100 * dcMaxVoltage / inputVoltage

        self.validateDuty(pwmDuty)
        self.pwm.start(pwmDuty)
        self.pwmDuty = pwmDuty
        print("init duty={}".format(pwmDuty))
    def toString(self):
        return "name={}, pins(ena,in1,in2)={}, pwm(frequency,duty)={}, constraint(duty,maxDuty)={}".format(self.name, (self.ena, self.in1, self.in2), (self.pwmFrequency,self.pwmDuty), self.maxDuty)
    def setInputState(self, desiredInputStates):
        if(self.inputStates == desiredInputStates):
            return
        GPIO.setmode(GPIO.BCM)
        x = map(lambda pair: [pair[0], pair[1]], zip([self.in1, self.in2], desiredInputStates))
        print(x)

        map(lambda pair: GPIO.output(pair[0], pair[1]), zip([self.in1, self.in2], desiredInputStates))
        self.inputStates = desiredInputStates
    def displayStatus(self, status):
        print("{}:{}".format(self.name, status))
    def backward(self):
        self.setInputState([GPIO.HIGH, GPIO.LOW])
        self.displayStatus("backward")
    def forward(self):
        self.setInputState([GPIO.LOW, GPIO.HIGH])
        self.displayStatus("forward")
    def stop(self):
        self.setInputState([GPIO.LOW, GPIO.LOW])
        self.displayStatus("stop")
    def setPwmFrequency(self, frequency):
        self.pwm.ChangeFrequency(frequency)
    def capDuty(self, duty):
        cappedDuty = reduce(lambda a,b: min(a,b), [self.maxDuty, 100], duty)
        return max(cappedDuty, 0)
    def validateDuty(self, duty):
        if(duty > self.maxDuty):
            raise Exception("duty={} is above the maxDuty={} for {}".format(duty, maxDuty, name))
    def setPwmDuty(self, duty):
        self.validateDuty(duty)
        print("{}.changeDuty={}".format(self.name, duty))
        self.pwm.ChangeDutyCycle(self.capDuty(duty))
        self.pwmDuty = duty
    # Adjust motor strength between [0, 1] at the safe voltage range.
    def setStrength(self, rate):
        if(rate <0 or rate > 1):
            raise Exception("rate must be between [0,1]")
        self.setPwmDuty(rate * self.maxDuty)
