import subprocess
from yeelight import Bulb
import time
import datetime
import json
import sunset
from sunset import sun
from datetime import date, timedelta

GTM_CONSTANT = 0    # +2h
yeelight_strip_address = "192.168.1.104"
pc_address = "192.168.1.225"
phone_address = "192.168.1.125"
#strip = Bulb(yeelight_strip_address)

def log(msg):
    with open('log.txt','a') as f:
        f.write(str(datetime.datetime.now())+'::'+msg)
        f.write('\n')

class Network_connected_thing:
    def __init__(self, ip):
        self.__ip__ = ip
        self.__status__ = 0

    def status(self):
        return self.__ping_to_ip__()

    def __ping_to_ip__(self):
        res = subprocess.call(['ping', '-c', '3', self.__ip__])
        if res == 0:
            return True
        elif res == 2:
            return False
        else:
            return False

class yeeligh_strip:
    def __init__(self, yeelight_strip_address):
        self.__ip__ = yeelight_strip_address
        self.__status__ = True
    def get_status(self):
        return self.__status__
    def turn_on(self):
        self.__status__ = True
        log("Turned on Yeelight")
        strip = Bulb(self.__ip__)
        strip.turn_on()
    def turn_off(self):
        self.__status__ = False
        log("Turned off Yeelight")
        strip = Bulb(self.__ip__)
        strip.turn_off()

my_phone = Network_connected_thing(phone_address)
my_pc = Network_connected_thing(pc_address)
my_yeelight = yeeligh_strip(yeelight_strip_address)

def get_sunset():
    s = sun(lat=44.43, long=26.09)
    snset = s.sunset(when=datetime.datetime.now())
    manual_datTime = [snset.hour, snset.minute]
    manual_datTime[0] += GTM_CONSTANT
    return manual_datTime

def update():
    curentTime = [datetime.datetime.now().hour, datetime.datetime.now().minute]
    sunsetTime = get_sunset()
    log("Checking Time")
    if (curentTime[0] > sunsetTime[0] or (curentTime[0] == sunsetTime[0] and curentTime[1] >= sunsetTime[0])) and curentTime[0] < 20 + GTM_CONSTANT  and my_yeelight.get_status() is False:
        log("Checking phone for status")
        if my_phone.status() is True:
            my_yeelight.turn_on()

    elif my_yeelight.get_status() is True and (curentTime[0] > 20 + GTM_CONSTANT  or curentTime[0] < 6 + GTM_CONSTANT):
        log("Checking PC for status")
        if my_pc.status() is False:
            my_yeelight.turn_off()



log("Execution started")
while True:
    update()
    time.sleep(240)