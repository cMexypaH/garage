BOARD = 1
OUT = "OUTPUT"
IN = "INPUT"
HIGH = "ON"
LOW = "OFF"


def setmode(a):
    print("Setmode done!")


def setup(a, b):
    print(f"Pin {a} sets to {b}")


def output(a, b):
    print(f"Pin {a} sets to {b}")


def cleanup():
    print('Cleanup')


def setwarnings(flag):
    print(flag)
