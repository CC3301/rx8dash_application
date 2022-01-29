import logging
from datetime import datetime


class SensorDataProcessor:
    def __init__(self, config):
        self.logger = logging.getLogger(__name__)
        self.config = config

        self._min_gauge_angle = 0
        self._max_gauge_angle = 290

        self._amb_temperature = 0
        self._engine_rpm = 0
        self._engine_tps = 0
        self._vehicle_velocity = 0
        self._vehicle_velocity_gps = 0

        self.gpstime = 0
        self.gpsdate = 0

        self.engine_oil_temperature = 0
        self.engine_oil_temperature_needle_position = 0
        self.engine_oil_temperature_status = "normal"

        self.engine_oil_pressure = 0
        self.engine_oil_pressure_needle_position = 0
        self.engine_oil_pressure_status = "normal"

        self.engine_water_temperature = 0
        self.engine_water_temperature_needle_position = 0
        self.engine_water_temperature_status = "normal"

        self.temperature_symbol = self.config.temperaturesymbol()
        self.pressure_symbol = self.config.pressuresymbol()

        self.logger.debug("Sensor data processor initialized")

    @staticmethod
    def __convert_celsius(val):
        """
        :param val: temperature in kelvin
        :return: val converted to celsius
        """
        return int(val - 273.15)

    @staticmethod
    def __convert_fahrenheit(val):
        """
        :param val: temperature in kelvin
        :return: val converted to fahrenheit
        """
        return int(val * 9 / 5 - 459.67)

    @staticmethod
    def __convert_bar(val):
        """
        :param val: pressure in kpa
        :return: val converted to bar
        """
        return int(val / 100)

    @staticmethod
    def __scale(val, src, dst):
        """
        :param val: value
        :param src: source range, e.g. 0 - 100
        :param dst: destination range, e.g. 555 - 888
        :return: val corrected to be proportional to the destination range
        """
        return ((val - src[0]) / (src[1] - src[0])) * (dst[1] - dst[0]) + dst[0]

    # process current dataset
    def process(self, data):
        """
        :param data:
        :return:
        """
        _engine_rpm = data['can']['engine']['rpm']
        _engine_tps = data['can']['engine']['tps']

        _vehicle_velocity = data['can']['vehicle']['velocity']

        _gpstime = data['gps']['time']

        # extract human-readable formats from the units returned by the sensor aggregator
        self.gpstime = datetime.fromtimestamp(_gpstime).strftime(self.config.timeformat())
        self.gpsdate = datetime.fromtimestamp(_gpstime).strftime(self.config.dateformat())

        # calculate gauges
        self._calculate_engine_oil_pressure(data['sen']['oil']['pressure'])
        self._calculate_engine_oil_temperature(data['sen']['oil']['temp'])
        self._calculate_engine_water_temperature(data['sen']['water']['temp'])

    def _calculate_gauge(self, value, max_value, min_value, high_value, low_value, gaugetype):
        """
        :param value: raw sensor value
        :param max_value: maximum value
        :param min_value: minimum value
        :param high_value: trigger for 'high' status i.e. warning lamp
        :param low_value: trigger for 'low' status i.e. "cold" lamp
        :return: gauge_status, needle_rotation, value_string
        """
        # range correction
        if value > max_value:
            value = max_value
        if value < min_value:
            value = min_value

        # which icon to show
        gauge_status = "normal"
        if value >= high_value:
            gauge_status = "high"
        if value <= low_value:
            gauge_status = "low"

        # needle rotation
        needle_rotation = self.__scale(value, (min_value, max_value), (self._min_gauge_angle, self._max_gauge_angle))

        # unit correction
        value_string = "invalid"
        if gaugetype == 'temp':
            if self.config.temperatureunit() == 'celsius':
                value = self.__convert_celsius(value)
            elif self.config.temperatureunit() == 'fahrenheit':
                value = self.__convert_fahrenheit(value)
            value_string = str(value) + " " + self.temperature_symbol
        elif gaugetype == 'pressure':
            if self.config.pressureunit() == 'bar':
                value = self.__convert_bar(value)
            value_string = str(value) + " " + self.pressure_symbol

        return gauge_status, needle_rotation, value_string

    def _calculate_engine_water_temperature(self, engine_water_temperature):
        """
        :param engine_water_temperature:
        :return:
        """
        max_value = int(self.config.parser.get("application:gauges:water_temperature", "max_value"))
        min_value = int(self.config.parser.get("application:gauges:water_temperature", "min_value"))

        high_value = int(self.config.parser.get("application:gauges:water_temperature", "high_value"))
        low_value = int(self.config.parser.get("application:gauges:water_temperature", "low_value"))

        self.engine_water_temperature_status, self.engine_water_temperature_needle_position, \
            self.engine_water_temperature = self._calculate_gauge(engine_water_temperature, max_value, min_value,
                                                                  high_value, low_value, 'temp')

    def _calculate_engine_oil_temperature(self, engine_oil_temperature):
        """
        :param engine_oil_temperature:
        :return:
        """
        max_value = int(self.config.parser.get("application:gauges:oil_temperature", "max_value"))
        min_value = int(self.config.parser.get("application:gauges:oil_temperature", "min_value"))

        high_value = int(self.config.parser.get("application:gauges:oil_temperature", "high_value"))
        low_value = int(self.config.parser.get("application:gauges:oil_temperature", "low_value"))

        self.engine_oil_temperature_status, self.engine_oil_temperature_needle_position, self.engine_oil_temperature = \
            self._calculate_gauge(engine_oil_temperature, max_value, min_value, high_value, low_value, 'temp')

    def _calculate_engine_oil_pressure(self, engine_oil_pressure):
        """
        :param engine_oil_pressure:
        :return:
        """
        max_value = int(self.config.parser.get("application:gauges:oil_pressure", "max_value"))
        min_value = int(self.config.parser.get("application:gauges:oil_pressure", "min_value"))

        high_value = int(self.config.parser.get("application:gauges:oil_pressure", "high_value"))
        low_value = int(self.config.parser.get("application:gauges:oil_pressure", "low_value"))

        self.engine_oil_pressure_status, self.engine_oil_pressure_needle_position, self.engine_oil_pressure = \
            self._calculate_gauge(engine_oil_pressure, max_value, min_value, high_value, low_value, 'pressure')
