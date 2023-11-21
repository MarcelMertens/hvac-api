from msmart.device import AirConditioner as AC


class MiteaDevice:
    @staticmethod
    async def create(cfg):
        # build midea device
        device = AC(ip=cfg.get("device_ip"), port=int(cfg.get("device_port")),
                    device_id=int((cfg.get("device_id"))))
        # authenticate to device
        await device.authenticate(cfg.get("device_token"), cfg.get("device_key"))

        # get device status, just test if connection works
        await device.refresh()

        return MiteaDevice(device)

    def __init__(self, cfg, device):
        self._cfg = cfg
        self._device = device

    async def get_cfg(self):
        return self._cfg

    async def get_ac_status(self):
        device = self._device

        # get device status
        await device.refresh()

        # build status dict.
        values = {
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

    async def get_capabilities(self):
        device = self._device

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
