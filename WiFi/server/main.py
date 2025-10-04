# Acces point software for wifi point to point
# from https://forum.core-electronics.com.au/t/pi-pico-w-to-pico-w-simple-communications/16188/15
import network
import socket
import time
import uasyncio as asyncio
from machine import Pin


server = '192.168.2.1'
gateway = '192.168.2.1'
port = 5263
ssid = 'Demo1234'
pw = '12345678' # minimal 8 characters

Onboard_LED = Pin("LED", Pin.OUT, value=0)

async def SensorData(reader, writer):
    
    print("Client connected")
    SW_State = await reader.read(512)     # returns all charaters including b''
    SW_State = str(SW_State)              # convert bytes object to str object
    SW_State = SW_State[2:]               # strip leading b'
    SW_State = SW_State[:-1]              # strip trailing '
    
    if SW_State == 'Toggle':
        Onboard_LED.toggle()

    writer.write(b'Success')          # send msg back 
    await writer.drain()
    await writer.wait_closed()
    print("Client disconnected")

# main
async def main():
# start server monitor task
    asyncio.create_task(asyncio.start_server(SensorData, "0.0.0.0", port))
    print('Server listening on {}:{}'.format(server,port))

# Main loop
    while True:
        # do something
        await asyncio.sleep(5)           # need to wait some time to allow server task to function
        
try:
    print('Setting up AP ...')
    time.sleep(1)
    wlan = network.WLAN(network.AP_IF)
    wlan.config(essid=ssid, password=pw)
    wlan.active(True)
    time.sleep(1)
    wlan.ifconfig((server, '255.255.255.0', gateway, '8.8.8.8'))
    time.sleep(0.1)
    time.sleep(2)

    asyncio.run(main())

except Exception as e:
    print('Error occurred : {}'.format(e))
finally:
    asyncio.new_event_loop()
    wlanAP.disconnect()
    time.sleep(0.1)
    wlanAP.active(False)
    time.sleep(0.1)
    Onboard_LED.off()