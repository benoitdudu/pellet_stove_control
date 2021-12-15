import queue
import os

def ProcessSendCommand(queueCmd):
    print('ProcessSendCommand {}'.format(os.getpid()))
    timeOut = None
    sequenceNb = 0
    cmdPrevious = {}
    while True:
        try:
            cmd = queueCmd.get(True, timeOut)
            if cmdPrevious == cmd:
                continue
            sequenceNb = 0
            if cmd['mode'] == 0:
                timeOut = 2
            else:
                timeOut = 1
        except queue.Empty:
            print('{} timeout reached '.format(cmd))
            sequenceNb += 1
            if cmdPrevious['mode'] == 0:
                if sequenceNb == 3:
                    timeOut = None
            elif sequenceNb > 3:
                timeOut = 10

        cmdPrevious = cmd
        print('{0} sequenceNb {1}'.format(cmd, sequenceNb))

