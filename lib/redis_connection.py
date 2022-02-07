import redis


class Connection:
    def __init__(self, remote_addr, remote_port, recv_q):
        self.recv_q = recv_q
        self.redis = redis.Redis()
