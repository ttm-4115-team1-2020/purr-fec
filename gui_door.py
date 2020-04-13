import paho.mqtt.client as mqtt
import logging
from threading import Thread
import json
from appJar import gui
from stmpy import Machine, Driver

# MQTT broker address
MQTT_BROKER = 'mqtt.item.ntnu.no'
MQTT_PORT = 1883

# Topics for communication
MQTT_TOPIC_INPUT = 'ttm4115/team_1/command'
MQTT_TOPIC_OUTPUT = 'ttm4115/team_1/answer'

class DoorComponent:

    def on_connect(self, client, userdata, flags, rc):
        # we just log that we are connected
        self._logger.debug('MQTT connected to {}'.format(client))

    def on_message(self, client, userdata, msg):
        pass

    def __init__(self):
        # get the logger object for the component
        self._logger = logging.getLogger(__name__)
        print('logging under name {}.'.format(__name__))
        self._logger.info('Starting Component')

        # create a new MQTT client
        self._logger.debug('Connecting to MQTT broker {} at port {}'.format(MQTT_BROKER, MQTT_PORT))
        self.mqtt_client = mqtt.Client()
        # callback methods
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_message = self.on_message
        # Connect to the broker
        self.mqtt_client.connect(MQTT_BROKER, MQTT_PORT)
        # start the internal loop to process MQTT messages
        self.mqtt_client.loop_start()

        self.create_gui()

    def create_gui(self):
        self.app = gui("Door GUI")

        def publish_command(command):
            payload = json.dumps(command)
            self._logger.info(command)
            self.mqtt_client.publish(MQTT_TOPIC_INPUT, payload=payload, qos=2)
        
        self.app.startLabelFrame('Door Status:')
        self.app.addLabel('title1', 'Locked')
        self.app.addLabel('title2', 'Closed')
        self.app.stopLabelFrame()

        self.app.startLabelFrame('Door Interactions:')
        def on_button_pressed_push(button):
            self.stm.send('door_pushed')
        self.app.addButton('Cat pushes the door', on_button_pressed_push)
        def on_button_pressed_close(button):
            self.stm.send('door_closed')
        self.app.addButton('The door closes', on_button_pressed_close)
        self.app.stopLabelFrame()
    
    def unlock(self):
        self.app.setLabel('title1', 'Unlocked')
    
    def door_opened(self):
        self.app.setLabel('title2', 'Opened')
    
    def lock(self):
        self.app.setLabel('title1', 'Locked')
        
 
t0 = {'source': 'initial', 'target': 'closed_locked'}
t1 = {'trigger': 'rfid', 'source': 'closed_locked', 'target': 'closed_unlocked',
      'effect': 'unlock; start_timer("t", "5000")'}
t2 = {'trigger': 'door_pushed', 'source': 'closed_unlocked', 'target': 'open_unlocked',
      'effect': 'stop_timer("t"); door_opened'}
t3 = {'trigger': 'door_closed', 'source': 'open_unlocked', 'target': 'closed_unlocked',
      'effect': 'start_timer("t", "5000")'}
t4 = {'trigger': 't', 'source': 'closed_unlocked', 'target': 'closed_locked',
      'effect': 'lock'}

s1 = {'name': 'closed_locked',
      'entry': 'lock'}
s2 = {'name': 'closed_unlocked'}
s3 = {'name': 'open_unlocked'}

# logging.DEBUG: Most fine-grained logging, printing everything
# logging.INFO:  Only the most important informational log items
# logging.WARN:  Show only warnings and errors.
# logging.ERROR: Show only error messages.
debug_level = logging.DEBUG
logger = logging.getLogger(__name__)
logger.setLevel(debug_level)
ch = logging.StreamHandler()
ch.setLevel(debug_level)
formatter = logging.Formatter('%(asctime)s - %(name)-12s - %(levelname)-8s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

d = DoorComponent()

stm_door = Machine(name='stm_door', transitions=[t0, t1, t2, t3, t4], obj=d, states=[s1, s2, s3])
d.stm = stm_door
driver = Driver()
driver.add_machine(stm_door)
driver.start()

d.app.go()
