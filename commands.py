import RPi.GPIO as GPIO
import time
import logger

logger.init()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)


def command(recieved_data):
    rtrn = ""
    try:
        recieved_data = recieved_data.lower()
        parsed_command = recieved_data.split(';')
        pin_number = int(parsed_command[0])
        is_high = True
        if parsed_command[1] == 'l':
            is_high = False
        if len(parsed_command) == 3:
            delay = int(parsed_command[2])
            GPIO.output(pin_number, is_high)
            rtrn += f"Pin {pin_number} is {is_high} "
            time.sleep(delay)
            GPIO.output(pin_number, not is_high)
            rtrn += f"Pin {pin_number} is {not is_high} "
        elif len(parsed_command) == 2:
            GPIO.output(pin_number, is_high)
            rtrn += f"Pin {pin_number} is {is_high} "
    except ValueError:
        print("!!! Wrong command !!!")
        return str.encode("!!! Wrong command !!!")
    return rtrn
