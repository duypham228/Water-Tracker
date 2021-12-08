#!/usr/bin/env python3
import RPi.GPIO as GPIO  # import GPIO
from hx711 import HX711  # import the class HX711
from time  import sleep
from threading import Thread
from rpi_lcd import LCD
from signal import signal, SIGTERM, SIGHUP, pause
import datetime

lcd = LCD()
message1 = "DRINK 0.0L <3"
message2 = "NEED  3.0L <3"
daily = 2.0
total = 0
reading = True
isReset = False
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def reset(channel):
    global daily
    global total
    global isReset
    daily = 3.0
    total = 0
    print("START A NEW DAY")
    print(datetime.datetime.now().strftime("%x"))
    print(daily, " ",total)
    isReset = True
    


def safe_exit(signum, frame):
    exit(1)

def display_lcd():
    global message1
    global message2
    global daily
    global total
    global isReset
    
    while reading:
        if isReset:
            lcd.clear()
            lcd.text("START A NEW DAY",1)
            lcd.text(datetime.datetime.now().strftime("%x"),2)
            sleep(5)
            lcd.clear()
            message1 = "DRINK 0.0L <3"
            message2 = "NEED 3.0L <3"
            isReset = False
        lcd.text(message1 ,1)
        lcd.text(message2 ,2)

        

def read_data():
    global message1
    global message2
    global daily
    global total
    
    time_interval = 5
    
    before = hx.get_weight_mean(20)
    after = 0
    
    while reading:
        
        value = hx.get_weight_mean(20)
        after = value
        dif = before - after
        if ( dif > 5):
            total += dif
            message1 = "DRINK " + '{:1.2f}'.format(total / 1000) + "L " + "<3"
            
            print(message1)
            daily -= total / 1000
            message2 = "NEED  "+ '{:1.2f}'.format(daily) + "L "+ "<3"
            
            print(message2)
            sleep(time_interval)
        else:
            sleep(2)
        before = after
    
 
        

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)
GPIO.add_event_detect(14, GPIO.RISING, callback=reset)
try:
    
    GPIO.setmode(GPIO.BCM)
    hx = HX711(dout_pin=6, pd_sck_pin=5)
    err = hx.zero()
    # check if successful
    if err:
        raise ValueError('Tare is unsuccessful.')
    reading = 68323
    value = float(135)
    ratio = reading / value  # calculate the ratio for channel A and gain 128
    hx.set_scale_ratio(ratio)  # set ratio for current channel
    
    reader = Thread(target=read_data, daemon=True)
    display = Thread(target=display_lcd, daemon=True)
    
    reader.start()
    display.start()
    
    pause()
    
        

except (KeyboardInterrupt, SystemExit):
    print('Bye :)')

finally:
    reading = False
    lcd.clear()
    GPIO.cleanup()
    

