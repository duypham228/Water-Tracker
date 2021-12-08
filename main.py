#!/usr/bin/env python3
import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
from time  import sleep

try:
    GPIO.setmode(GPIO.BCM)  # set GPIO pin mode to BCM numbering
    # Create an object hx which represents your real hx711 chip
    # Required input parameters are only 'dout_pin' and 'pd_sck_pin'
    hx = HX711(dout_pin=6, pd_sck_pin=5)
    # measure tare and save the value as offset for current channel
    # and gain selected. That means channel A and gain 128
    err = hx.zero()
    # check if successful
    if err:
        raise ValueError('Tare is unsuccessful.')

    reading = 68323
    value = float(135)

        # set s
        # scale ratio for particular channel and gain which is
        # used to calculate the conversion to units. Required argument is only
        # scale ratio. Without arguments 'channel' and 'gain_A' it sets
        # the ratio for current channel and gain.
    ratio = reading / value  # calculate the ratio for channel A and gain 128
    hx.set_scale_ratio(ratio)  # set ratio for current channel
    time_interval = 5
    daily = 2.0
    total = 0
    before = hx.get_weight_mean(20)
    after = 0
    while True:
        
        value = hx.get_weight_mean(20)
        after = value
        dif = before - after
        if ( dif > 5):
            total += dif
            print("You have drink", round(total / 1000, 2), "L")
            daily -= total / 1000
            print("You still need", round(daily,2), "L")
            sleep(time_interval)
        else:
            sleep(2)
        before = after
        

except (KeyboardInterrupt, SystemExit):
    print('Bye :)')

finally:
    GPIO.cleanup()

