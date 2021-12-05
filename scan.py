from bluepy.btle import Scanner, DefaultDelegate
from struct import *
import paho.mqtt.client as mqtt

devices = {
    "a4:c1:38:9d:9e:2b" : "Salon",
    "a4:c1:38:43:c1:57" : "Dining",
    "a4:c1:38:23:ed:7c" : "Kitchen",
    "a4:c1:38:a1:74:0d" : "lilias",
    "a4:c1:38:46:44:46" : "Bedroom",
    "a4:c1:38:51:fb:e3" : "Laundry",
    "a4:c1:38:a7:e9:56" : "Ulysses"
}


class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if dev.addr in devices:
            for (adtype, desc, value) in dev.getScanData():
               # print ("%d = %s (%d)" % (adtype, value, len(value)))
                if adtype == 22 and len(value) == 34 and value.startswith("1a18"):
                    temp = unpack('<h', bytes.fromhex(value[16:20]))
                    hum = unpack('<H', bytes.fromhex(value[20:24]))
                    volt = unpack('<H', bytes.fromhex(value[24:28]))
                    bat = unpack('<b', bytes.fromhex(value[28:30]))
                    print ("%s : temp of %d C and hum of %d %% and bat of %d %% and volt of %d mv" % (devices[dev.addr], temp[0], hum[0], bat[0], volt[0]))
                    client.publish("ATCThermometer/%s" % (devices[dev.addr]), "{\"temp\": %d, \"humidity\": %d}" % (temp[0] * 0.01, hum[0] * 0.01))
                    
                
                
client = mqtt.Client()
client.username_pw_set("mrnicoco", "")
client.tls_set()
client.connect("5198535b3dcd4eb19cb816c71d2075a1.s1.eu.hivemq.cloud", 8883)

                    
scanner = Scanner().withDelegate(ScanDelegate())
scanner.start()
while True:
    scanner.process()

