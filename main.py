from typing import Union
from fastapi import FastAPI
from typing import List, Optional
from pydantic import BaseModel
from configparser import ConfigParser
import os
import uvicorn
import asyncio
import logging
from dotenv import load_dotenv, dotenv_values

from msmart.device import AirConditioner as AC
from msmart.discover import Discover



logging.basicConfig(level=logging.INFO)

'''
# Temp Block for Static AC Device Config
deviceconfig = dotenv_values("kueche.env")
MODUL = deviceconfig["MODULE"]
DEVICE_IP = deviceconfig["DEVICE_IP"]
DEVICE_PORT = deviceconfig["DEVICE_PORT"]
DEVICE_ID = deviceconfig["DEVICE_ID"]
DEVICE_TOKEN = deviceconfig["DEVICE_TOKEN"]
DEVICE_KEY = deviceconfig["DEVICE_KEY"]
device = AC(ip=DEVICE_IP, port=DEVICE_PORT, device_id=int(DEVICE_ID))
'''

# Load Config from devices.ini
config_parser = ConfigParser()	
config_parser.read('devices.ini')
def get_config(configname):
    if config_parser.has_section(configname):
        config = {}
        config['name'] = configname
        for key, value in config_parser.items(configname):
            config[key] = value
        return config
    else:
        return "Provided config not found in config file"




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
        'operational_mode': repr(device.operational_mode),
        'fan_speed': repr(device.fan_speed),
        'swing_mode': repr(device.swing_mode),
        'eco_mode': device.eco_mode,
        'turbo_mode': device.turbo_mode,
        'fahrenheit': device.fahrenheit,
        'indoor_temperature': device.indoor_temperature,
        'outdoor_temperature': device.outdoor_temperature
        }
    return status

def get_capabilities():
    values = {
        'supported_modes': repr(device.supported_operation_modes),
        'supported_swing_modes': repr(device.supported_swing_modes),
        'supported_fan_speeds': repr(device.supported_fan_speeds),
        'supports_eco_mode': device.supports_eco_mode,
        'supports_turbo_mode': device.supports_turbo_mode,
        'max_target_temperature': device.max_target_temperature,
        'min_target_temperature': device.min_target_temperature
        }
    return values

def config_data():
    values = {
        'name': deviceconfig["NAME"],
        'modul': MODUL,
        'device-ip': DEVICE_IP,
        'device-port': DEVICE_PORT,
        'device-id': DEVICE_ID,
        'device-key': DEVICE_KEY,
        'device-token': DEVICE_TOKEN
    }
    return values


app = FastAPI()


@app.get("/{name}/config")
async def read_config(name):
    cfg = get_config(name)
    return cfg


#Show Status of AC Unit
@app.get('/status')
async def ac_status():
    await connect()
    await device.refresh()
    return status()


#Show Capabilites (Mode, Fan Speed, Swing Mode etc) of AC Unit
@app.get('/capabilities')
async def capabilities():
    await connect()
    await device.get_capabilities()
    return get_capabilities()


# Turn AC Unit Off
@app.post('/poweroff')
async def ac_poweroff():
    await connect()
    await device.refresh()
    device.power_state = False
    await device.apply()
    return status()

# Turn AC Unit On
@app.post('/poweron')
async def ac_poweron():
    await connect()
    await device.refresh()
    device.power_state = True
    await device.apply()
    return status()

# Set Temperature
@app.post('/temperature/{temperature}')
async def ac_temperature(temperature: int):
    await connect()
    await device.refresh()
    device.target_temperature = temperature
    await device.apply()
    return status()

# Set Operation Mode
@app.post('/operationmode/{operationmode}')
async def ac_operationmode(operationmode: int):
    await connect()
    await device.refresh()
    device.operational_mode = operationmode
    await device.apply()
    return status()

# Set Fan Speed
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
    
@app.post('/bulk')
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