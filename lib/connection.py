import time
import socket
import logging
import threading
import json


class Connection:
    def __init__(self, remote_addr, remote_port):
        self.logger = logging.getLogger(__name__)
        self.remote_addr = remote_addr
        self.remote_port = remote_port
        self.socket = None
        self.t = threading.Thread(target=self._async_listen, name=self.__class__.__name__)
        self.__keep_running = False

        self.data = None
        self.previous_result = None
        self.current_result = None

        self.ups = 0

    def start(self):
        self.__keep_running = True
        self.__connect()
        self.t.start()

    def stop(self):
        self.__keep_running = False
        self.__disconnect()
        self.t.join()

    def fetch(self):
        return self.data

    def get_ups(self):
        return self.ups

    def __connect(self):
        if self.socket:
            self.logger.warning("Already connected")
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.remote_addr, int(self.remote_port)))

    def __disconnect(self):
        self.socket.shutdown(0)

    def _async_listen(self):
        while self.__keep_running:
            try:
                buffer = self.socket.recv(1024)
                while buffer.endswith(b'0'):
                    buffer = buffer[:-1]
                    try:
                        self.data = json.loads(buffer)
                    except json.decoder.JSONDecodeError as e:
                        #self.logger.warning(f"Received incomplete data from endpoint")
                        self.data = None

            except socket.error:
                pass

