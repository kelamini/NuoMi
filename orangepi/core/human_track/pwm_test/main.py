import time
from serve import Ser
from control import DeltaPID
###############################  define ############################
# Pwm limit
PWM_DUTY_MAX = 0.125
PWM_DUTY_MIN = 0.025


# Yaw limit
YAW_DUTY_LEFT = 100
YAW_DUTY_RIGHT= 0
YAW_DUTY_NOR = 56
YAW_PWM_CHIPX = 1     # PWM chip    
YAW_PWM_CH = 0        # PWM ch 
YAW_PWM_HZ = 50

# Pitch limit
PIT_DUTY_DOWN = 25
PIT_DUTY_UP = 75
PIT_DUTY_NOR = 45
PIT_PWM_CHIPX = 0     # PWM chip    
PIT_PWM_CH = 0        # PWM ch 
PIT_PWM_HZ = 50
# ############################  pit #############################
# # Open PWM chip 0, channel 0  
# pitPwm = PWM(PIT_PWM_CHIPX, PIT_PWM_CH)  # PWM0_M1
# # Set frequency to 50 Hz  20ms
# pitPwm.frequency = PIT_PWM_HZ
# # Set duty cycle to 75%
# pitPwm.duty_cycle = PIT_DUTY_NOR
# # Set polarity 1
# pitPwm.polarity = "normal"
# # Enable
# pitPwm.enable()

# ############################  yaw #############################
# # Open PWM chip 0, channel 0  
# yawPwm = PWM(YAW_PWM_CHIPX, YAW_PWM_CH)  # PWM0_M1
# # Set frequency to 50 Hz  20ms
# yawPwm.frequency = YAW_PWM_HZ
# # Set duty cycle to 75%
# yawPwm.duty_cycle = YAW_DUTY_NOR
# # Set polarity 1
# yawPwm.polarity = "normal"
# # Enable
# yawPwm.enable()

yawSer = Ser(YAW_PWM_CHIPX, YAW_PWM_CH, YAW_PWM_HZ, YAW_DUTY_NOR)
pitSer = Ser(PIT_PWM_CHIPX, PIT_PWM_CH, PIT_PWM_HZ, PIT_DUTY_NOR)

while True:
    yaw_duty, pit_duty = map(int, input("please input duty yaw(0-100) and pit(0-100): \r\n").split())
    # if duty >= PWM_DUTY_MAX:
    #      duty = PWM_DUTY_MAX
    # elif duty <= PWM_DUTY_MIN:
    #      duty = PWM_DUTY_MIN

    yawSer.set(int(yaw_duty))
    pitSer.set(int(pit_duty))

    #print("duty is \r\n", yawSer.duty)
    #print("duty is \r\n", pitSer.duty)
    #print("pwm duty is ", yawSer.pwm.duty_cycle)
    
    #pitPwm.duty_cycle = int(duty)

    time.sleep(1)
# cnt -> [0, 100]
# cnt = 0
# duty = 0

# while True:

#     # duty increasing
#     cnt = cnt + 10

#     # duty -> [0.025, 0,125]
#     duty = cnt/1000 + 0.025 
#     if duty >= PWM_DUTY_MAX:
#         duty = PWM_DUTY_MIN
#         cnt = 0

#     print("PWM ON!, Duty is", duty)

#     pitPwm.duty_cycle = duty

    
#     time.sleep(1)

pwm.close()