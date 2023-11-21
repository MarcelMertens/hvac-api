from fastapi import FastAPI
from typing import List, Optional
from pydantic import BaseModel
import asyncio
import logging

from msmart.device import AirConditioner as AC
from msmart.discover import Discover

from app.device import get_device, list_devices, register_device

logging.basicConfig(level=logging.INFO)


# Build FastAPI app
app = FastAPI(debug=True, # show nice stack-trace directly in web, not need to look in docker output
              title="<replace me with something>")


@app.on_event("startup")
async def startup_event():
    logging.info("startup ...")
    await register_device("kueche")

    logging.info("startup done.")


# Show known devices
@app.get("/devices")
async def show_devices():
    return list_devices()

# Show Configs
@app.get("/{device}/config")
async def get_config(device):
    d = await get_device(device)
    return await d.get_cfg()


# Show Status of AC Unit
@app.get('/{device}/status')
async def ac_status(device):
    d = await get_device(device)
    return await d.get_ac_status()



# Show Capabilites (Mode, Fan Speed, Swing Mode etc) of AC Unit
@app.get('/{device}/capabilities')
async def capabilities(device):
    d = await get_device(device)
    return await d.get_capabilities()



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
