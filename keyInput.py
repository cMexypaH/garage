import keyboard
import winsound  #ONLY WINDOWS play beep sound
frequency = 2500  # Set Frequency To 2500 Hertz
duration = 10  # Set Duration To 1000 ms == 1 second

pass_phrase = ""


def read_keys():
    global pass_phrase
    while True:
        if keyboard.read_key():  #ako ima natisnat buton
            buton = keyboard.read_key()
            print(buton)  # izkarva koi buton e natisnat
            if buton == "delete":
                pass_phrase = ""
            elif buton == "enter":
                print(pass_phrase)
                #break
            else:
                pass_phrase += buton
                winsound.Beep(frequency, duration)  #ONLY WINDOWS
                #print('\a')  #This will send the ASCII Bell character to stdout


read_keys()
