import dht
import machine
import gpio
import time
import req_server
import settings


sensor = dht.DHT11(machine.Pin(23))
solar = machine.ADC(machine.Pin(36))
moisture = machine.ADC(39)
alert_pin = machine.Pin(25,machine.Pin.IN,machine.Pin.PULL_UP)

def temp():
    sensor.measure()
    return sensor.temperature()

def humd():
    return sensor.humidity()

def solar_read():
    return round(solar.read()/635,1)

def moisture_read():
#     return round(moisture.read())
    return round(moisture.read()*100/4095)

def start_pump():
    if int(moisture_read()) < 50:
        gpio.parse_dump('gpio1:1')
        return 'starting the pump'
    else:
        gpio.parse_dump('gpio1:0')
        return 'moisture is at {}% no need to water'.format(moisture_read())


def automate():
    ms = int(moisture_read())
    if  ms < 10:
        gpio.parse_dump('gpio1:1')
        settings.after_state = True 
    elif ms > 90:
        gpio.parse_dump('gpio1:0')
        settings.after_state = False
    if not settings.after_state == settings.before_state:
        req_server.send_gpio_data()
        settings.before_state = settings.after_state
        
def alert():
    if alert_pin.value()== 0 and settings.one_time_pressed:
        settings.one_time_pressed = False
        return True 
    elif  alert_pin.value() == 1:
        settings.one_time_pressed = True
        return False 
        
    
    
    
    