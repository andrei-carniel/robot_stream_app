from datetime import datetime


class BcastUdp:
    def __init__(self, ip, port, name):
        self.ip = ip
        self.port = port
        self.name = name
        self.time = datetime.now()
        self.is_dead = False

    def get_formated_name(self):
        prefix = self.is_alive()
        return self.name +  prefix + " -> " + self.ip + ":" + str(self.port)

    def is_alive(self):
        if (datetime.now() - self.time).seconds >= 60:
            self.is_dead = True
            return " (Lost Connection)"

        if (datetime.now() - self.time).seconds >= 30:
            return " (Away)"

        return ""

    def reset_time(self):
        self.time = datetime.now()
        self.is_dead = False