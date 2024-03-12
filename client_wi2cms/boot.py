# This file is executed on every boot (including wake-boot from deepsleep)

# LIBRARIES

#import esp
#esp.osdebug(None)
import os
from machine import Pin
import network
#os.dupterm(None, 1) # disable REPL on UART(0)
import gc
#import webrepl
#webrepl.start()
gc.collect()

# VARIABLES DICLARATIONS
d4 = Pin(2, Pin.OUT)
btn = Pin(0, Pin.IN , Pin.PULL_UP)

sta = network.WLAN(network.STA_IF)

def do_connect():
    import network
    ssid = 'vivo'
    pas = '123456789'

    sta = network.WLAN(network.STA_IF)
    if not sta.isconnected():
        print('connecting to network...')
        sta.active(True)
        #sta.connect('your wifi ssid', 'your wifi password')
        sta.connect(ssid,pas)
        while not sta.isconnected() and btn.value() == 1:
            d4.on()
            pass
    print('conneted to internet > ',sta.isconnected())
    d4.off()

do_connect()

