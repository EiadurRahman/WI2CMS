import ujson as json
import network
import time
import machine
from machine import Pin
import io_handle
import urequests as requests
from umqtt.simple import MQTTClient
import req_server

d4 = Pin(2, Pin.OUT) # status led
thingesp_server = 'thingesp.siddhesh.me'

# note : if the sandbox isn't active type [ Join serious-value ] to reconnect

class Client:
    def __init__(self, username, projectName, password):
        self.username = username
        self.projectName = projectName
        self.password = password
        self.initalized = False
        self.mqtt_client = MQTTClient(client_id=projectName + "@" + username,
                                      server=thingesp_server, port=1893, user=projectName + "@" + username, password=password,keepalive=0)
        self.mqtt_client.set_callback(self.on_message)
        self.mqtt_client.connect()

        
    def setCallback(self, func):
        self.callback_func = func
        self.initalized = True
        return self

    def on_message(self, client, msg):
        if self.initalized != True:
            print('Please set the callback func!')
            return
        else:
            payload = json.loads(msg.decode("utf-8"))
#             print(payload)
            if payload['action'] == 'query':
                out = self.callback_func(payload['query'].lower()) or ""
                sendr = {
                    "msg_id": payload['msg_id'], "action": "returned_api_response", "returned_api_response": out}
                self.mqtt_client.publish(
                    self.projectName + "/" + self.username, json.dumps(sendr))

    def start(self):
        self.mqtt_client.set_callback(self.on_message)
        self.mqtt_client.subscribe(self.projectName + "/" + self.username)
        
        one_time_msg_send = False # for sending msg for once
        init_time_connect = time.time()
        # main loop
        try:
            while True:
                
                self.mqtt_client.check_msg()   # Pass blocking argument as False
                passed_time_connect = time.time() - init_time_connect
                
                if passed_time_connect > 300:
                    print('reconnecting....',end='\r')
                    self.mqtt_client.subscribe(self.projectName + "/" + self.username)
                    init_time_connect = time.time()
                    print('connected        ',end='\r')
                if io_handle.alert():
                    self.send_msg('ALERT')
                req_server.clint_task()
                io_handle.automate()
        except Exception as err:
            print('error : ',err)
        time.sleep(.1)
    

    def send_msg(self,msg):
        d4.on()
        # Your Twilio Account SID and Auth Token
        account_sid = ''
        auth_token = ''

        # Set up the Twilio API URL for sending WhatsApp messages
        twilio_url = 'https://api.twilio.com/2010-04-01/Accounts/{}/Messages.json'.format(account_sid)

        # Set up the request headers
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        # Set up the request payload (message details)
        payload = {
            'To': 'whatsapp%3A%',  # Replace with the recipient's Bangladeshi WhatsApp number
            'From': 'whatsapp%3A%',  # Replace with your Twilio WhatsApp number
            'Body': msg,  # Message content
        }

        # Manually create the payload string
        payload_string = '&'.join(['{}={}'.format(key, value) for key, value in payload.items()])

        # Send the request
        response = requests.post(twilio_url, headers=headers, auth=(account_sid, auth_token), data=payload_string)
        
        print('done sending msg : {}'.format(msg))
        d4.off()

