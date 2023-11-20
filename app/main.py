from typing import Union
from fastapi import FastAPI
from typing import List, Optional
from pydantic import BaseModel
from configparser import ConfigParser
import uvicorn
import asyncio
import logging
import os
from dotenv import load_dotenv, dotenv_values

from msmart.device import AirConditioner as AC
from msmart.discover import Discover



logging.basicConfig(level=logging.INFO)


# Load Config from devices.ini
print (os.getcwd())
config_parser = ConfigParser()	
config_parser.read('app/devices.ini')

def get_config(configname):
    if config_parser.has_section(configname):
        config = {}
        config['name'] = configname
        for key, value in config_parser.items(configname):
            config[key] = value
        return config
    else:
        return "Provided config not found in config file"




# Build FastAPI app
app = FastAPI()


# Show known devices
@app.get("/devices")
async def show_devices():
    return config_parser.sections()

# Show Configs
@app.get("/{device}/config")
async def read_config(device):
    cfg = get_config(device)
    return cfg


# Show Status of AC Unit
@app.get('/{device}/status')
async def ac_status(device):
    cfg = get_config(device)
    if cfg == "Provided config not found in config file":
        return ("Device Name not found")
    
    # Processing Midea 
    if cfg.get("modul") == "midea":
        # build midea device
        device = AC(ip=cfg.get("device_ip"), port=int(cfg.get("device_port")), device_id=int((cfg.get("device_id"))))
        # authenticate to device
        await device.authenticate(cfg.get("device_token"), cfg.get("device_key"))
        # get device status
        await device.refresh()
        # build status dict.
        values =  {
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
        return values



# Show Capabilites (Mode, Fan Speed, Swing Mode etc) of AC Unit
@app.get('/{device}/capabilities')
async def capabilities(device):
    cfg = get_config(device)
    if cfg == "Provided config not found in config file":
        return ("Device Name not found")
    
    # Processing Midea 
    if cfg.get("modul") == "midea":
        # build midea device
        device = AC(ip=cfg.get("device_ip"), port=int(cfg.get("device_port")), device_id=int((cfg.get("device_id"))))
        # authenticate to device
        await device.authenticate(cfg.get("device_token"), cfg.get("device_key"))
        # get device capabilities
        await device.get_capabilities()
        # build capabilities dict.
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


# Turn AC Unit Off
@app.post('/{device}/poweroff')
async def ac_poweroff(device):
    cfg = get_config(device)
    if cfg == "Provided config not found in config file":
        return ("Device Name not found")
    
    # Processing Midea 
    if cfg.get("modul") == "midea":
        # build midea device
        device = AC(ip=cfg.get("device_ip"), port=int(cfg.get("device_port")), device_id=int((cfg.get("device_id"))))
        # authenticate to device
        await device.authenticate(cfg.get("device_token"), cfg.get("device_key"))
        # get device status
        await device.refresh()
        # set power state = false
        device.power_state = False
        # apply status to device
        await device.apply()
         # build status dict.
        values =  {
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
        return values


# Turn AC Unit On
@app.post('/{device}/poweron')
async def ac_poweron(device):
    cfg = get_config(device)
    if cfg == "Provided config not found in config file":
        return ("Device Name not found")
    # Processing Midea 
    if cfg.get("modul") == "midea":
        # build midea device
        device = AC(ip=cfg.get("device_ip"), port=int(cfg.get("device_port")), device_id=int((cfg.get("device_id"))))
        # authenticate to device
        await device.authenticate(cfg.get("device_token"), cfg.get("device_key"))
        # get device status
        await device.refresh()
        # set power state = True
        device.power_state = True
        # apply status to device
        await device.apply()
         # build status dict.
        values =  {
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
        return values

# Set Temperature
@app.post('/{device}/temperature/{temperature}')
async def ac_temperature(device, temperature: int):
    
    cfg = get_config(device)
    if cfg == "Provided config not found in config file":
        return ("Device Name not found")
    # Processing Midea 
    if cfg.get("modul") == "midea":
        # build midea device
        device = AC(ip=cfg.get("device_ip"), port=int(cfg.get("device_port")), device_id=int((cfg.get("device_id"))))
        # authenticate to device
        await device.authenticate(cfg.get("device_token"), cfg.get("device_key"))
        # get device status
        await device.refresh()
        # set target temperature
        device.target_temperature = temperature
        # apply status to device
        await device.apply()
         # build status dict.
        values =  {
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
        return values

# Set Operation Mode
@app.post('/{device}/operationmode/{operationmode}')
async def ac_operationmode(device, operationmode: int):
    cfg = get_config(device)
    if cfg == "Provided config not found in config file":
        return ("Device Name not found")
    # Processing Midea 
    if cfg.get("modul") == "midea":
        # build midea device
        device = AC(ip=cfg.get("device_ip"), port=int(cfg.get("device_port")), device_id=int((cfg.get("device_id"))))
        # authenticate to device
        await device.authenticate(cfg.get("device_token"), cfg.get("device_key"))
        # get device status
        await device.refresh()
        # set operational_mode
        device.operational_mode = operationmode
        # apply status to device
        await device.apply()
         # build status dict.
        values =  {
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
        return values

# Set Fan Speed
@app.post('/{device}/operationmode/{fanspeed}')
async def ac_fanspeed(device, fanspeed: int):
    cfg = get_config(device)
    if cfg == "Provided config not found in config file":
        return ("Device Name not found")
    # Processing Midea 
    if cfg.get("modul") == "midea":
        # build midea device
        device = AC(ip=cfg.get("device_ip"), port=int(cfg.get("device_port")), device_id=int((cfg.get("device_id"))))
        # authenticate to device
        await device.authenticate(cfg.get("device_token"), cfg.get("device_key"))
        # get device status
        await device.refresh()
        # set operational_mode
        device.fan_speed = fanspeed
        # apply status to device
        await device.apply()
         # build status dict.
        values =  {
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
        return values 


class ac_config(BaseModel):
    power_state: Optional[bool] = None
    target_temperature: Optional[int] = None
    operational_mode: Optional[int] = None
    fan_speed: Optional[int] = None
    swing_mode: Optional[int] = None
    eco_mode: Optional[bool] = None
    turbo_mode: Optional[bool] = None
    
@app.post('/{device}/bulk')
async def parameter_data(device, s1: ac_config):
    cfg = get_config(device)
    if cfg == "Provided config not found in config file":
        return ("Device Name not found")
    # Processing Midea 
    if cfg.get("modul") == "midea":
        # build midea device
        device = AC(ip=cfg.get("device_ip"), port=int(cfg.get("device_port")), device_id=int((cfg.get("device_id"))))
        # authenticate to device
        await device.authenticate(cfg.get("device_token"), cfg.get("device_key"))
        # get device status
        await device.refresh()
        # set operational_mode
        device.power_state = s1.power_state
        device.target_temperature = s1.target_temperature
        device.operational_mode = s1.operational_mode
        device.fan_speed = s1.fan_speed
        device.swing_mode = s1.swing_mode
        device.eco_mode = s1.eco_mode
        device.turbo_mode = s1.turbo_mode
        # apply status to device
        await device.apply()
        await asyncio.sleep(1)
         # build status dict.
        values =  {
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
        return values 
