from django.db import models
import multiprocessing
from .send_command import ProcessSendCommand
from django.conf import settings

class PelletStoveCmd():
    def __init__(self):
        self.send_commands = False
        self.fan1_speed = 5
        self.fan2_speed = 5
        self.flame_power = 3
        self.mode = True
        self.QueueCmd = multiprocessing.Queue()

        self.p1 = multiprocessing.Process(target=ProcessSendCommand, args=(self.QueueCmd, settings.DATA_ENV['REMOTE_ID']))
        self.p1.start()

    def SendCommand(self):
        self.QueueCmd.put(self.ConvertRequestToDict(), block=False)

    def ConvertRequestToDict(self):
        d = {"send_commands": self.send_commands,
             "fan1_speed": self.fan1_speed,
             "fan2_speed": self.fan2_speed,
             "flame_power": self.flame_power,
             "mode": self.mode}
        return d

    def __str__(self) -> str:
        s  = 'send_commands = {0}\n'.format(self.send_commands)
        s += 'fan1_speed = {0}\n'.format(self.fan1_speed)
        s += 'fan2_speed = {0}\n'.format(self.fan2_speed)
        s += 'flame_power = {0}\n'.format(self.flame_power)
        s += 'mode = {0}\n'.format(self.mode)
        return s
