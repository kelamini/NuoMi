from periphery import PWM
###############################  define ############################
# Pwm limit
PWM_DUTY_MAX = 0.125
PWM_DUTY_MIN = 0.025

# Pitch limit
PIT_DUTY_DOWN = 0.11
PIT_DUTY_UP = 0.03
PIT_DUTY_NOR = 0.07
PIT_PWM_CHIPX = 0     # PWM chip    
PIT_PWM_CH = 0        # PWM ch 
PIT_PWM_HZ = 50
# YAW limit
YAW_DUTY_LEFT = 0.11
YAW_DUTY_RIGHT= 0.03
YAW_DUTY_NOR = 0.08
YAW_PWM_CHIPX = 1     # PWM chip    
YAW_PWM_CH = 0        # PWM ch 
YAW_PWM_HZ = 50
############################  pit #############################
# Open PWM chip 0, channel 0  
pitPwm = PWM(PIT_PWM_CHIPX, PIT_PWM_CH)  # PWM0_M1
# Set frequency to 50 Hz  20ms
pitPwm.frequency = PIT_PWM_HZ
# Set duty cycle to 75%
pitPwm.duty_cycle = PIT_DUTY_NOR
# Set polarity 1
pitPwm.polarity = "normal"
# Enable
pitPwm.enable()

############################  yaw #############################
# Open PWM chip 0, channel 0  
yawPwm = PWM(YAW_PWM_CHIPX, YAW_PWM_CH)  # PWM0_M1
# Set frequency to 50 Hz  20ms
yawPwm.frequency = YAW_PWM_HZ
# Set duty cycle to 75%
yawPwm.duty_cycle = YAW_DUTY_NOR
# Set polarity 1
yawPwm.polarity = "normal"
# Enable
yawPwm.enable()

# PWM 映射参数 将 0.5ms - 2.5ms 映射成 0-100
PWM_DUYT_BASE = 0.025
PWM_DUTY_CAR  = 1000 



#定义舵机类
class Ser(object):

    #init
    def __init__(self, pwmChip, pwmCh, hz, duty, max, min) -> None:
        # self.pwmChip = pwmChip  # PWM chip
        # self.pwmCh = pwmCh      # PWM CH
        # self.hz = hz            # PWM HZ
        # self.duty = duty        # PWM Duyt

        self.max = max
        self.min = min

        self.pwm = PWM(pwmChip, pwmCh)  # PWM0_M1
        # Set frequency to 50 Hz  20ms
        self.pwm.frequency = hz
        # Set duty cycle 
        self.pwm.duty_cycle = self.dutyTrans(duty)
        # Set polarity 1
        self.pwm.polarity = "normal"
        # Enable
        self.pwm.enable()


    # set 0 -100 to 0.5 - 1.5
    def dutyTrans(self, num):
        return num/PWM_DUTY_CAR+PWM_DUYT_BASE
        # self.duty = num/PWM_DUTY_CAR+PWM_DUYT_BASE
        # return self.duty

    def set(self, num):
        
        # limit
        if num > self.max:
            self.pwm.duty_cycle = self.dutyTrans(self.max)
        elif num < self.min:
            self.pwm.duty_cycle = self.dutyTrans(self.min)
        else:
            self.pwm.duty_cycle = self.dutyTrans(num)
