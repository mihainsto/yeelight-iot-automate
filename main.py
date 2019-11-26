import subprocess
#from yeelight import Bulb
import time
import datetime
import json
import sunset
from sunset import sun
from datetime import date, time, timedelta

GTM_CONSTANT = 2    # +2h
yeelight_strip_address = "192.168.1.104"
pc_address = "192.168.1.225"
phone_address = "192.168.1.125"
#strip = Bulb(yeelight_strip_address)



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
        pass
    def turn_off(self):
        self.__status__ = False
        pass

my_phone = Network_connected_thing(phone_address)
my_pc = Network_connected_thing(pc_address)
my_yeelight = yeeligh_strip(yeelight_strip_address)
#print(my_phone.status())
def work():
    while True:
        time.sleep(30)
        print(my_phone.status())

def get_sunset():
    s = sun(lat=44.43, long=26.09)
    snset = s.sunset(when=datetime.datetime.now())
    manual_datTime = [snset.hour, snset.minute]
    manual_datTime[0] += GTM_CONSTANT
    return manual_datTime

def update():
    curentTime = [datetime.datetime.now().hour, datetime.datetime.now().minute]
    sunsetTime = get_sunset()

    if curentTime[0] > sunsetTime[0] and curentTime[0] < 22 and my_yeelight.get_status() == False:
        if my_phone.status() == True:
            my_yeelight.turn_on()

    elif my_yeelight.get_status() == True and (curentTime[0] > 22 or curentTime[0] < 8):
        if my_pc.status() == False:
            my_yeelight.turn_off()

update()
