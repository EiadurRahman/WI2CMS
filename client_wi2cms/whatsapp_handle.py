import io_handle
import gpio
import req_server
def handleResponse(query):
    if query == 'help': # help tempate
        help_template = """
To check moisture status  : moisture status / ms
To check relative humidity : humidity / humd
To check relative temperature : temperature / temp
To check Output status : output status / os
To start the pump : start pump / sp
To control single gpio : gpio{index of gpio}:{state} ex: 'gpio1:1'
    & for multiple gpios : gpio{index of gpio}:{state},gpio{index of gpio}:{state} ex: 'gpio1:1,gpio2:0,gpio3:1'
"""
        return (help_template)
    # check moisture status
    elif query in ['moisture status','ms']:
        value = io_handle.moisture_read()
        return ('soil moisture is : {0}%'.format(value))
        
    # motor handling 
    elif query in  ['start pump','sp'] :
        msg = io_handle.start_pump()
        return msg
    # DHT11 sensor 
    elif query in ['humidity','temperature','humd','temp']:
        if query in ['humidity','humd']:
            humidity = io_handle.humd()
            return ('humidity : {}%'.format(humidity))
        elif query in [ 'temperature', 'temp']:
            temp = io_handle.temp()
            return ('temperature : {}.C'.format(temp))
    # IO handle
    elif 'gpio' in query:
        if 'gpio1' in query:
            return 'gpio1 is already being handle by a function'
        else:
            msg = gpio.parse_dump(query)
            req_server.send_gpio_data()
            return msg
    elif query in ['output status','os']:
        msg = str(gpio.get_data())
        return msg
    else:
        return 'no task is set for [ {} ]'.format(query)