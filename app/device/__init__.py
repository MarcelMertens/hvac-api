from configparser import ConfigParser

from app.device.mitea import MiteaDevice

config_parser = ConfigParser()
config_parser.read('app/devices.ini')


def _get_config(configname):
    if config_parser.has_section(configname):
        config = {}
        config['name'] = configname
        for key, value in config_parser.items(configname):
            config[key] = value
        return config
    else:
        return None


def list_devices():
    # TODO: You can iterate over registered devices
    return config_parser.sections()


# hold a reference to all devices
#  <device-name> -> Device
all_devices = {}


async def register_device(device_name):
    cfg = _get_config(device_name)
    if cfg is None:
        raise Exception(f"Device Name '{device_name}' not found")

    modul = cfg.get("modul")

    if modul == 'midea':
        all_devices[device_name] = MiteaDevice.create(cfg)
    # elif modul == 'panasonic':
    #    all_devices[device_name] = PanasonicDevice.create(cfg)

    else:
        raise Exception(f"Device Name '{device_name}' unsupported modul '{modul}'")


async def get_device(device_name):
    if device_name not in all_devices:
        raise Exception(f"Device Name '{device_name}' not found")

    return all_devices[device_name]
