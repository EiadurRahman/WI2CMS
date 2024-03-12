from machine import Pin
import time
import json
gpio1 = Pin(13, Pin.OUT)
gpio2 = Pin(12, Pin.OUT)
gpio3 = Pin(14, Pin.OUT)

def dump(data):
    with open('gpio_state.json','w') as file:
        file.write(data)

def parse_dump(string):
    gpios = string.split(',')
    for gpio in gpios:
        gpio_index = gpio.split(':')[0]
        state = int(gpio.split(':')[1])
        if state in [0,1] and gpio_index in ['gpio1','gpio2','gpio3']:
            data = get_data()
            data[gpio_index] = int(state)
            with open('gpio_state.json','w') as file :
                json.dump(data,file)
            output_handle()
            return 'output state has been toggled'
        else:
            print('not a valid state')
            return 'not a valid gpio index / state'

def get_data():
    with open('gpio_state.json','r') as file:
        data = json.load(file)
    return data

def output_handle():
    with open('gpio_state.json','r', encoding='utf-8') as file:
        data = json.load(file)
    gpio1_state = data["gpio1"]
    gpio2_state = data["gpio2"]
    gpio3_state = data["gpio3"] 
    
    def toggle_output(pin,state):
        if state != 0:
            pin.on()
        else:
            pin.off()
    
    toggle_output(gpio1,gpio1_state)
    toggle_output(gpio2,gpio2_state)
    toggle_output(gpio3,gpio3_state)

