import subprocess 
#from yeelight import Bulb
import time
yeelight_strip_address = "192.168.1.104"
pc_address = "192.168.1.225"
phone_address = "192.168.1.125"
#strip = Bulb(yeelight_strip_address)

def ping_to_ip(ip):   
    res = subprocess.call(['ping', '-c', '3', ip])
    if res == 0: 
            return True
    elif res == 2: 
            return False
    else: 
            return False


class Network_connected_thing:
    def __init__(self, ip):
        self.__ip__ = ip
        self.__status__ = 0

    def status(self):
        return ping_to_ip(self.__ip__)


my_phone  = Network_connected_thing(phone_address)
my_pc = Network_connected_thing(pc_address)


while True:
    time.sleep(30)
    print(my_phone.status())


