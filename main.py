from typing import Union
from fastapi import FastAPI
from typing import List, Optional
from pydantic import BaseModel

import uvicorn
import asyncio
import logging

from msmart.device import AirConditioner as AC
from msmart.discover import Discover

logging.basicConfig(level=logging.INFO)

DEVICE_IP = '192.168.0.165'
DEVICE_PORT = 6444
DEVICE_ID = '144036023305909'

# For V3 devices
DEVICE_TOKEN = '669845c6a4ec707c583c5e79efcf51e5599aeaf8cf241eaae74cf4ff60be284960b949bdaf042f440bd5c37bdae514ed96edb9f6eb81efb17685b5a54052a824'  # 'YOUR_DEVICE_TOKEN'
DEVICE_KEY = 'abc14d289c304abfb3fd38f347e2993fa6bd8157e3234510b35298d93c221c28'  # 'YOUR_DEVICE_KEY'




async def main():

    # There are 2 ways to connect

    # Discover.discover_single can automatically construct a device from IP or hostname
    #  - V3 devices will be automatically authenticated
    #  - The Midea cloud will be accessed for V3 devices to fetch the token and key
    # device = await Discover.discover_single(DEVICE_IP)

    # Manually construct the device
    #  - See midea-discover to read ID, token and key
    device = AC(ip=DEVICE_IP, port=6444, device_id=int(DEVICE_ID))
    if DEVICE_TOKEN and DEVICE_KEY:
        await device.authenticate(DEVICE_TOKEN, DEVICE_KEY)

    # Get device capabilities
    await device.get_capabilities()

    # Refresh the state
    await device.refresh()


device = AC(ip=DEVICE_IP, port=6444, device_id=int(DEVICE_ID))

async def connect():
    if DEVICE_TOKEN and DEVICE_KEY:
        await device.authenticate(DEVICE_TOKEN, DEVICE_KEY)
        

def status():
    status =  {
        'id': device.id,
        'ip': device.ip,
        'online': device.online,
        'supported': device.supported,
        'power_state': device.power_state,
        'beep': device.beep,
        'target_temperature': device.target_temperature,
        'operational_mode': device.operational_mode,
        'fan_speed': device.fan_speed,
        'swing_mode': device.swing_mode,
        'eco_mode': device.eco_mode,
        'turbo_mode': device.turbo_mode,
        'fahrenheit': device.fahrenheit,
        'indoor_temperature': device.indoor_temperature,
        'outdoor_temperature': device.outdoor_temperature
        }
    return status


app = FastAPI()

@app.get('/')
async def ac_status():
    await connect()
    await device.refresh()
    return status()

@app.get('/capabilities')
async def capabilities():
    await connect()
    await device.get_capabilities()
    return {
        'supported_modes': device.supported_operation_modes,
        'supported_swing_modes': device.supported_swing_modes,
        'supported_fan_speeds': device.supported_fan_speeds,
        'supports_eco_mode': device.supports_eco_mode,
        'supports_turbo_mode': device.supports_turbo_mode,
        'max_target_temperature': device.max_target_temperature,
        'min_target_temperature': device.min_target_temperature
        }

@app.post('/poweroff')
async def ac_poweroff():
    await connect()
    await device.refresh()
    device.power_state = False
    await device.apply()
    return status()
    
@app.post('/poweron')
async def ac_poweron():
    await connect()
    await device.refresh()
    device.power_state = True
    await device.apply()
    return status()

@app.post('/temperature/{temperature}')
async def ac_temperature(temperature: int):
    await connect()
    await device.refresh()
    device.target_temperature = temperature
    await device.apply()
    return status()

@app.post('/operationmode/{operationmode}')
async def ac_operationmode(operationmode: int):
    await connect()
    await device.refresh()
    device.operational_mode = operationmode
    await device.apply()
    return status()

@app.post('/fanspeed/{fanspeed}')
async def ac_fanspeed(fanspeed: int):
    await connect()
    await device.refresh()
    device.fanspeed = fanspeed
    await device.apply()
    return status()    
    
    
class ac_config(BaseModel):
    power_state: Optional[bool] = None
    target_temperature: Optional[int] = None
    operational_mode: Optional[int] = None
    fan_speed: Optional[int] = None
    swing_mode: Optional[int] = None
    eco_mode: Optional[bool] = None
    turbo_mode: Optional[bool] = None
    
    
@app.post('/config')
async def parameter_data(s1: ac_config):
    await connect()
    await device.refresh()
    device.power_state = s1.power_state
    device.target_temperature = s1.target_temperature
    device.operational_mode = s1.operational_mode
    device.fan_speed = s1.fan_speed
    device.swing_mode = s1.swing_mode
    device.eco_mode = s1.eco_mode
    device.turbo_mode = s1.turbo_mode
    
    # await device.apply()
    await asyncio.sleep(1)
    await device.refresh()
    return status()