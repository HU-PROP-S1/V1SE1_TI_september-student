# client software for point to point wifi
# from https://forum.core-electronics.com.au/t/pi-pico-w-to-pico-w-simple-communications/16188/15
import network
import socket
import time
from machine import Pin
SW_PIN = 15

host  =  '192.168.2.2'
serverAP =  '192.168.2.1'
gatewayAP = '192.168.2.1'
port = 5263

Onboard_LED = Pin("LED", Pin.OUT, value=0)
SW = Pin(SW_PIN, Pin.IN, Pin.PULL_UP)

ssid = 'Demo1234'
pw = '12345678' # 8 or more characters
wlan = network.WLAN(network.STA_IF)
wlan.active(True)

def check_SSID():
    print('Checking for Network ...',ssid)
    networks = wlan.scan()
    found = False
    for w in networks:
        if w[0].decode() == ssid:
            found = True
    return found

def connect_Fail(s):
    Error = 'Connect Fail: '
    if s == 0:
        Error += 'Link Down'
    elif s == 1:
        Error += 'Link Join'
    elif s == 2:
        Error += 'Link NoIP'
    elif s == -1:
        Error += 'Link Fail'
    elif s == -2:
        Error += 'NoNet'
    elif s == -3:
        Error += 'BadAuth'
    else:
        Error += 'Unknown'
    print(Error)
    return

def connect_to_Network():
    try:
        if check_SSID():
            print('Connecting to Network ...')
            wlan.active(True)
            wlan.config(pm = 0xa11140)     # Disable power-save mode
            wlan.connect(ssid, pw)
            while (wlan.isconnected() == False): time.sleep(1)
            status = wlan.status()
            if status == 3:
                # set IP address to the network we want, otherwise it uses 192.168.4.XXX
                wlan.ifconfig((host, '255.255.255.0', gatewayAP, '8.8.8.8'))
                status = wlan.ifconfig()
                print('ip = ' + status[0])
                return 1
            else:
                connect_Fail(status)
                print('Cannot connect ... ')
                return 0
        else:
            print('Network NOT found ... ')
            return 0
    except Exception as e:
        print('Error occurred : {}'.format(e))
        return 0

# Main
try:
    if connect_to_Network() == 1:
        print('Ready')
        while True:
            if SW.value() == 0:
                s = socket.socket()
                print('Connecting to {}:{}'.format(serverAP,port))
                s.connect((serverAP, port))
                data = 'Toggle'
                s.send(data)
                count = 0
                Exit = False
                while not Exit:
                    msg = s.recv(512)
                    if msg.find(b'Success') == -1:
                        count += 1
                        if count > 5: Exit = True
                    else:
                        print('Success')
                        Exit = True
                s.close()
            time.sleep(0.1)
            
except Exception as e:
    print('Error occurred : {}'.format(e))
wlan.disconnect()
time.sleep(0.1)
wlan.active(False)
time.sleep(0.1)
print('Disconnect from Network.')