from configparser import ConfigParser

config_parser = ConfigParser()	
config_parser.read('devices.ini')


# function to get device configuration from device.ini       
def get_config(configname):
    if config_parser.has_section(configname):
        config = {}
        config['name'] = configname
        for key, value in config_parser.items(configname):
            config[key] = value
        return config
    else:
        return "Config Section not found in config file"
    

print(get_config("kuesadche"))