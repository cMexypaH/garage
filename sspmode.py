import os
import time


def init():
    time.sleep(10)
    os.system('sudo hciconfig hci0 sspmode 0')
    print("hci0 sspmode 0")
    time.sleep(1)
    os.system('sudo hciconfig hci0 down')
    print("hci0 DOWN")
    time.sleep(1)
    os.system('sudo hciconfig hci0 up')
    print("hci0 UP")
    time.sleep(1)
    os.system('sudo hciconfig hci0 piscan')
    print("hci0 piscan")
