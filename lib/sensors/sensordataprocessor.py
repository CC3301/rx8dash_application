import logging
import time
from datetime import datetime


class SensorDataProcessor:
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config
        self._engine_oil_temperature = 0
        self._engine_oil_pressure = 0
        self._engine_water_temperature = 0
        self._amb_temperature = 0
        self._engine_rpm = 0
        self._engine_tps = 0
        self._vehicle_velocity = 0
        self._vehicle_velocity_gps = 0
        self._rtctime = 0
        self._rtc_time = 0
        self._rtc_date = 0

        self._temperature_symbol = ''

        self._data_present = False

        self.logger.debug("Sensor data processor initialized")

    def __convert_celsius(self, val):
        return round(val - 273.15, int(self.config.valueaccuracy()))

    def __convert_fahrenheit(self, val):
        return round(val * 9/5 - 459.67, int(self.config.valueaccuracy()))

    def reset(self):
        self._engine_oil_temperature = 0
        self._engine_oil_pressure = 0
        self._engine_water_temperature = 0
        self._amb_temperature = 0
        self._engine_rpm = 0
        self._engine_tps = 0
        self._vehicle_velocity = 0
        self._vehicle_velocity_gps = 0
        self._rtctime = 0
        self._rtc_time = 0
        self._rtc_date = 0

        self._temperature_symbol = ''

        self._data_present = False

    def process(self, data):

        # extract values into separate vars
        self._engine_oil_temperature = data['sen']['oil']['temp']
        self._engine_oil_pressure = data['sen']['oil']['pressure']
        self._engine_water_temperature = data['sen']['water']['temp']

        self._engine_rpm = data['can']['engine']['rpm']
        self._engine_tps = data['can']['engine']['tps']

        self._vehicle_velocity = data['can']['vehicle']['velocity']

        self._rtctime = data['rtc']['time']

        # set some static information derived from the config
        self._temperature_symbol = self.config.temperaturesymbol()

        # extract human-readable formats from the units returned by the sensor aggregator
        self._rtc_time = datetime.fromtimestamp(self._rtctime).strftime(self.config.timeformat())
        self._rtc_date = datetime.fromtimestamp(self._rtctime).strftime(self.config.dateformat())

        # temperatures are returned in kelvin, convert them accordingly
        if self.config.temperatureunit() == 'celsius':
            self._engine_water_temperature = self.__convert_celsius(self._engine_water_temperature)
            self._engine_oil_temperature = self.__convert_celsius(self._engine_oil_temperature)
        elif self.config.temperatureunit() == 'fahrenheit':
            self._engine_water_temperature = self.__convert_fahrenheit(self._engine_water_temperature)
            self._engine_oil_temperature = self.__convert_fahrenheit(self._engine_oil_temperature)

        # allow the accessors to return
        self._data_present = True

    # accessors
    def temperaturesymbol(self):
        if self._data_present:
            return str(self._temperature_symbol)

    def rtctime(self):
        if self._data_present:
            return str(self._rtc_time)

    def rtcdate(self):
        if self._data_present:
            return str(self._rtc_date)

    def engine_oil_temp(self):
        if self._data_present:
            return str(self._engine_oil_temperature)

    def engine_oil_pressure(self):
        if self._data_present:
            return str(self._engine_oil_pressure)

    def engine_water_temp(self):
        if self._data_present:
            return str(self._engine_water_temperature)

    def engine_rpm(self):
        if self._data_present:
            return str(self._engine_rpm)
