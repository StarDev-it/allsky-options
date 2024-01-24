from http.server import BaseHTTPRequestHandler, HTTPServer
from device.input.pws import PWS as DataHandler
from device.output.ks0212 import RelayFactory
from threading import Thread
from time import sleep
from gpiozero import CPUTemperature
from pprint import pprint as debug
from sys import exit
import json


# Common thread objects
input_handler = DataHandler()
dew_heater = RelayFactory.create('DewHeater')
cpu_temperature = CPUTemperature()
fan = RelayFactory.create('Fan')


def get_status():
    """
    Get internal data status
    :return: Object
    """
    result = {
        'value': {},
        'status': {}
    }
    for metric in input_handler.get():
        if metric is not 'is_rain':
            result['value'][metric] = input_handler.get()[metric]
    result['value']['cpu_temperature'] = cpu_temperature.temperature
    result['status'] = {
        'is_rain': input_handler.get()['is_rain'],
        'is_dew': input_handler.is_dew(),
        'is_frost': input_handler.is_frost(),
        'is_dew_heater_enabled': dew_heater.is_enabled,
        'is_fan_enabled': fan.is_enabled
    }
    return result


class RequestHandler(BaseHTTPRequestHandler):
    """
    Handle server requests
    """

    def do_GET(self):
        """
        Manipulate get requests
        """
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        result = ''
        try:
            if self.path is None:
                pass
            elif self.path.find('/weatherstation/update') == 0:
                input_handler.check_auth(self.path)
                input_handler.set(self.path)
                result = json.dumps({
                    'status': 'success'
                })
            elif self.path.find('/status') == 0:
                result = json.dumps(get_status())
            elif self.path.find('/favicon.ico') == 0:
                self.send_header('Content-type', 'image/gif')
        except ValueError as e:
            debug('exception')
            debug(e)
            import traceback
            traceback.print_exc()
            result = {
                'status': 'error',
                'message': e
            }

        self.send_header('Refresh', '30') # TODO only for test
        self.end_headers()
        self.wfile.write(bytes(result, "utf8"))


class CheckDew:
    """
    Check dew class
    :param max_humidity: int
    :param delta_dew_point: int
    :param interval: int
    """
    def __init__(self, max_humidity=80, delta_dew_point=2, interval=15):
        while True:
            if input_handler.is_dew(max_humidity, delta_dew_point) or input_handler.is_frost():
                dew_heater.enable()
            else:
                dew_heater.disable()
            sleep(interval)


class CheckTemperature:
    """
    Check temperature class
    """
    def __init__(self, max_temperature=40, interval=5):
        """
        Set temperature check
        :param max_temperature: int define the max temperature
        :param interval: int define when check the temperature
        """
        while True:
            if int(cpu_temperature.temperature) >= max_temperature:
                fan.enable()
            else:
                fan.disable()
            sleep(interval)


with HTTPServer(('', 8888), RequestHandler) as server:
    try:
        # Start check dew thread
        dew_thread = Thread(target=CheckDew, name='Temperature', args=[80, 2, 5])
        dew_thread.start()
        # Start check temperature thread
        temperature_thread = Thread(target=CheckTemperature, name='Temperature', args=[35, 60])
        temperature_thread.start()
        # Start HTTP server
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()
    exit(1)
