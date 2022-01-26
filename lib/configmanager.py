import sys
import os
import configparser


class ConfigManager:
    def __init__(self, configpath):
        self.configpath = configpath

        if not os.path.isfile(self.configpath):
            print(f"No such file or directory: {self.configpath}")
            sys.exit(1)

        self.parser = configparser.ConfigParser()

        try:
            self.parser.read(self.configpath)
        except configparser.Error as e:
            print(f"Failed to read config: {e}")
            sys.exit(2)

    # accesors
    def timeformat(self):
        return self.parser.get('application:core', 'timeformat')

    def dateformat(self):
        return self.parser.get('application:core', 'dateformat')

    def loggingformat(self):
        return self.parser.get('application:core', 'loggingformat')

    def temperatureunit(self):
        return self.parser.get('application:core', 'temperatureunit')

    def valueaccuracy(self):
        return self.parser.get('application:core', 'valueaccuracy')

    def mainbackgroundcolor(self):
        return self.parser.get('application:gui', 'background')

    def mainfontcolor(self):
        return self.parser.get('application:gui', 'fontcolor')

    def windowwidth(self):
        return self.parser.get('hardware:screen', 'width')

    def windowheight(self):
        return self.parser.get('hardware:screen', 'height')
