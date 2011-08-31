import random
import time

print "Press enter when the rider is stable or type q and press enter to quit"

command = None

while command != 'q':
    fromKeyboard = raw_input()
    if fromKeyboard == 'q':
        command = fromKeyboard
    else:
        print "wait..."
        command = random.choice([True, False])
        commands = ['Push', 'Pull']
        time.sleep(random.uniform(0., 5.))
        print commands[command]
