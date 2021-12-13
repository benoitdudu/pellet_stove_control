from django.db import models

class PelletStoveCmd():
    def __init__(self):
        self.send_commands = False
        self.fan1_speed = 5
        self.fan2_speed = 5
        self.flame_power = 3
        self.mode = True

    def __str__(self) -> str:
        s  = 'send_commands = {0}\n'.format(self.send_commands)
        s += 'fan1_speed = {0}\n'.format(self.fan1_speed)
        s += 'fan2_speed = {0}\n'.format(self.fan2_speed)
        s += 'flame_power = {0}\n'.format(self.flame_power)
        s += 'mode = {0}\n'.format(self.mode)
        return s
