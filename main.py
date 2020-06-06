import commands

while True:
    command = input("(O)pen or (C)lose doors: ").upper()
    t = input("Time: ")
    if command == "O":
        commands.opendoor(t)
    elif command == "C":
        commands.closedoor(t)
