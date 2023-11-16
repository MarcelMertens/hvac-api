import asyncio
import logging
from msmart.device import AirConditioner as AC
logging.basicConfig(level=logging.INFO)

DEVICE_IP = '192.168.0.165'
DEVICE_PORT = 6444
DEVICE_ID = '144036023305909'

# For V3 devices
DEVICE_TOKEN = '669845c6a4ec707c583c5e79efcf51e5599aeaf8cf241eaae74cf4ff60be284960b949bdaf042f440bd5c37bdae514ed96edb9f6eb81efb17685b5a54052a824'  # 'YOUR_DEVICE_TOKEN'
DEVICE_KEY = 'abc14d289c304abfb3fd38f347e2993fa6bd8157e3234510b35298d93c221c28'  # 'YOUR_DEVICE_KEY'

device = AC(ip=DEVICE_IP, port=6444, device_id=int(DEVICE_ID))

async def connect():
    if DEVICE_TOKEN and DEVICE_KEY:
        await device.authenticate(DEVICE_TOKEN, DEVICE_KEY)


async def ac_get_info():
    # await device.get_capabilities()
    await connect()
    await device.refresh()
    return device

asyncio.run(ac_get_info())

print (device.supported_operation_modes)