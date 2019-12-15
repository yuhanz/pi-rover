import smbus

class Mpu6050:
    PWR_M   = 0x6B
    DIV   = 0x19
    CONFIG       = 0x1A
    GYRO_CONFIG  = 0x1B
    INT_EN   = 0x38

    ACCEL_X = 0x3B
    ACCEL_Y = 0x3D
    ACCEL_Z = 0x3F

    GYRO_X  = 0x43
    GYRO_Y  = 0x45
    GYRO_Z  = 0x47
    TEMP = 0x41
    bus = smbus.SMBus(1)

    ACCELERATION_UNIT = 1   # 1g
    GYRO_UNIT = 125     # degree /sec

    @staticmethod
    def InitMPU():
       bus.write_byte_data(Device_Address, DIV, 7)
       bus.write_byte_data(Device_Address, PWR_M, 1)
       bus.write_byte_data(Device_Address, CONFIG, 0)
       bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
       bus.write_byte_data(Device_Address, INT_EN, 1)

    @staticmethod
    def readMPU(addr):
       high = bus.read_byte_data(Device_Address, addr)
       low = bus.read_byte_data(Device_Address, addr+1)
       value = ((high << 8) | low)
       if(value > 32768):
             value = value - 65536
       return value / 32768.0

    @staticmethod
    def readAcceleration():
        return (readMPU(ACCEL_X) * ACCELERATION_UNIT, readMPU(ACCEL_Y) * ACCELERATION_UNIT, readMPU(ACCEL_Z) * ACCELERATION_UNIT)

    @staticmethod
    def readGyro():
        return (readMPU(GYRO_X) * GYRO_UNIT, readMPU(GYRO_Y) * GYRO_UNIT, readMPU(GYRO_Z) * GYRO_UNIT)

    @staticmethod
    def readTemperature():
        return readMPU(TEMP)
