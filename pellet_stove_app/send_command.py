import queue
import os
import logging
from logging.handlers import RotatingFileHandler

def ProcessSendCommand(queueCmd):
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
            if cmd['send_commands'] == 0:
                timeOut = None
            if cmdPrevious == cmd:
                continue
            sequenceNb = 0
            if cmd['mode'] == 0:
                timeOut = 2
            else:
                timeOut = 1
        except queue.Empty:
            sequenceNb += 1
            if cmdPrevious['mode'] == 0:
                if sequenceNb == 3:
                    timeOut = None
            elif sequenceNb > 3:
                timeOut = 10

        cmdPrevious = cmd
        logging.info('{0} sequenceNb {1} timeOut {2}'.format(cmd, sequenceNb, timeOut))

