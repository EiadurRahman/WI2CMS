import ThingESP
import machine
import err_log
thing = ThingESP.Client('EiadurRahman', 'esp8266whatsapp', 'esp8266')
from time import sleep
import whatsapp_handle

# error handling loop
thing.send_msg('device is back online ')
while True :
    try:
        thing.setCallback(whatsapp_handle.handleResponse).start()
    except Exception as err:
        print(err)
        err_log.log(err) 
        d4.off()
        sleep(1)
        d4.on()
        machine.reset() # resets the device+

