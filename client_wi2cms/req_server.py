# main.py (client side)
import urequests
import machine
import time
import io_handle  # Import the io_handle module
import gpio
import settings

FLASK_SERVER_URL_DATA = "http://{}/data".format(settings.server_ip)  # Update with your laptop's IP
FLASK_SERVER_URL_GPIO  = "http://{}/gpio_data".format(settings.server_ip)
d4 = machine.Pin(2, machine.Pin.OUT) # status led

#
def send_data_to_server(data):
    response = urequests.post(FLASK_SERVER_URL_DATA, json=data, timeout=1)
    response_text = response.text
    response.close()
    return response_text

def send_gpio_data():
    gpio_data = gpio.get_data()  # Assuming this function returns GPIO data in JSON format
    response = urequests.post(FLASK_SERVER_URL_GPIO, json=gpio_data, timeout=1)
    response_text = response.text
    response.close()
    print(response_text)
    return response_text

 
def clint_task():
    d4.on()
    # Read sensor data from io_handle.py
    sensor_data = {
        "temperature": io_handle.temp(),
        "humidity": io_handle.humd(),
        "solar": io_handle.solar_read(),
    "moisture": io_handle.moisture_read()
    }
    try:
        data = send_data_to_server(sensor_data)
        print(data)

        if 'gpio1' in data: # 'gpio1' would only allow valid json
            gpio.dump(str(data))
            gpio.output_handle()
        else:
            print('not valid')
    except Exception as err:
        print(err)
    d4.off()
    time.sleep(2)  # Adjust delay as needed



