import queue
import os
import logging
from logging.handlers import RotatingFileHandler
import sys
import serial

def generate_data(fan_model = 1, seq_number = 0, remote_id_hex = 0x0, beep = 0, fan1_speed = 6,
                  fan2_speed = 6, fan3_speed = 0, flame_power = 3, mode = 1):
    cmd = "0C 43 {:02X} {:02X} {:06X} {:02X} {:02X} {:1X}{:1X} {:02X} {:02X} 00".format(fan_model, seq_number, remote_id_hex,
                                                                                        beep, fan1_speed, fan3_speed, fan2_speed, flame_power, mode)
    cmd = bytearray.fromhex(cmd)
    return cmd

def waitMinutes(nb_sec):
    return nb_sec * 60

def getTimeoutInMinutes(inTimeout):
    if inTimeout is None:
        return None
    return inTimeout / 60

def ProcessSendCommand(queueCmd, remoteId):
    remoteId = int(remoteId, base=16)
    log_formatter = logging.Formatter('%(asctime)s:%(message)s')

    logFile = os.path.dirname(os.path.abspath(__file__)) + '/ProcessSendCommand.log'
    my_handler = RotatingFileHandler(logFile, maxBytes=1*1024*1024, backupCount=1)
    my_handler.setFormatter(log_formatter)

    logging.basicConfig(level=logging.INFO, handlers=[my_handler])
    logging.info('ProcessSendCommand {}'.format(os.getpid()))

    timeOut = None
    sequenceNb = 0
    cmdPrevious = {}
    while True:
        try:
            cmd = queueCmd.get(True, timeOut)
            if not cmd['send_commands']:
                timeOut = None
                continue
            if cmdPrevious == cmd:
                continue
            sequenceNb = 0
            if cmd['mode'] == 0:
                timeOut = waitMinutes(0.5)
            else:
                timeOut = waitMinutes(1)
        except queue.Empty:
            sequenceNb += 1
            if cmdPrevious['mode'] == 0:
                if sequenceNb == 3:
                    timeOut = None
            elif sequenceNb > 3:
                timeOut = waitMinutes(10)

        cmdPrevious = cmd
        logging.info('{0} sequenceNb {1} timeOut {2}'.format(cmd, sequenceNb, getTimeoutInMinutes(timeOut)))

        try:
            with serial.Serial('/dev/ttyUSB-RFX433XL', 38400, timeout=10) as ser:
                data = generate_data(seq_number = sequenceNb, remote_id_hex = remoteId
                                    ,fan1_speed = cmd['fan1_speed'], fan2_speed = cmd['fan2_speed']
                                    ,flame_power = cmd['flame_power'], mode = cmd['mode'])
                #logging.info(data.hex())
                ser.write(data)
        except:
            e = sys.exc_info()[0]
            v = sys.exc_info()[1]
            logging.info("Error: {}\n{}".format(e, v))
