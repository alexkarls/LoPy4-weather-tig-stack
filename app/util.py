import pycom

def heartbeat(on: bool):
    if (on):
        pycom.heartbeat(True)
    else:
        pycom.heartbeat(False)