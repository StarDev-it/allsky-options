from util import AP
import os, yaml
from urllib.parse import urlparse, parse_qs
from util import fahrenheitToCelsius
from pprint import pprint as debug


class PWS:
    """
    Entity authorized to enter data
    :param id: str
    """
    id = ''
    """
    User's password authorized to enter data
    :param password: str
    """
    password = ''
    """
    External temperature measured in Celsius
    :param ext_temperature: float
    """
    ext_temperature = 0
    """
    External air humidity
    :param ext_humidity: float
    """
    ext_humidity = 0
    """
    External air dew point measured in Celsius
    :param ext_dew_point: float
    """
    ext_dew_point = -2
    """
    Is currently raining
    :param is_rain: bool
    """
    is_rain = False
    """
    The max permitted humidity
    :param max_humidity: int
    """
    max_humidity = 0
    """
    The delta dew point
    :param delta_dew_point: int
    """
    delta_dew_point = 0

    def __init__(self):
        """
        Load configuration file
        """
        config_file = AP + os.sep + 'config' + os.sep + 'pws.yml'
        try:
            with open(config_file, 'r') as file:
                config = yaml.safe_load(file)
                self.id = str(config['auth']['id'])
                self.password = str(config['auth']['password'])
        except TypeError as e:
            raise FileNotFoundError('No configuration file found')
        except yaml.YAMLError as e:
            raise FileExistsError('The configuration file is not a YAML file')
        except KeyError as e:
            raise KeyError("The config key %s was not found in pws.yml configuration file" % e)

    def check_auth(self, path):
        """
        Check service authorizations
        :param path: str
        """
        parsed_url = urlparse(path)
        id = parse_qs(parsed_url.query)['ID'][0]
        password = parse_qs(parsed_url.query)['PASSWORD'][0]
        if self.id != id or self.password != password:
            raise PermissionError('Authorization denied, check your ID and PASSWORD settings')

    def set(self, path):
        """
        Permit to external service to set the internal params
        :param path: str
        """
        parsed_url = urlparse(path)
        self.ext_temperature = round(fahrenheitToCelsius(float(parse_qs(parsed_url.query)['tempf'][0])), 2)
        self.ext_humidity = round(float(parse_qs(parsed_url.query)['humidity'][0]), 2)
        self.ext_dew_point = round(fahrenheitToCelsius(float(parse_qs(parsed_url.query)['dewptf'][0])), 2)
        self.is_rain = float(parse_qs(parsed_url.query)['rainin'][0]) > 0

    def get(self):
        """
        Get internal service params
        :return: dict
        """
        return {
            "ext_temperature": self.ext_temperature,
            "ext_humidity": self.ext_humidity,
            "ext_dew_point": self.ext_dew_point,
            "is_rain": self.is_rain
        }

    def is_dew(self, max_humidity=None, delta_dew_point=None):
        """
        There are the necessary conditions to form the dew
        :param max_humidity: int the max humidity value
        :param delta_dew_point: int The delta dew point
        :return:
        """
        if max_humidity is not None:
            self.max_humidity = max_humidity
        if delta_dew_point is not None:
            self.delta_dew_point = delta_dew_point
        return (self.ext_dew_point + self.delta_dew_point >= self.ext_temperature or
                self.ext_humidity > self.max_humidity or self.is_rain)
