'''
Initialize all GUI elements and update them from the values that are put to the val_dict
'''

import Tkinter as tk
import time
import random

val_dict = dict.fromkeys(['roll', 'pitch', 'yaw', 'vx', 'vy', 'vz', 'heading', 'rangefinder', 'lat', 'lon', 'alt', 'airspeed', 'groundspeed', 'gimbal_roll', 'gimbal_pitch', 'gimbal_yaw', 'last_heartbeat'])

# Initialize item in dict : {'val_X', {'lbl_name': <label>, 'lbl_val': <label>, 'value': <value>}}
def init_2labels(val_dict, key, label1_text, row1 ,column1, row2, column2):
    lbl_name = tk.Label(root, text=label1_text,font=('arial', 20, 'bold'), fg='red',bg='white')
    lbl_val = tk.Label(root, font=('arial', 20, 'bold'), fg='red',bg='white')     
    val_dict[key] = {'lbl_name': lbl_name, 'lbl_val': lbl_val, 'value': None}
    val_dict[key]['lbl_name'].grid(row=row1, column=column1, columnspan=1)
    val_dict[key]['lbl_val'].grid(row=row2, column=column2, columnspan=1)

# Initializing GUI
def GUI_init(val_dict):
    init_2labels(val_dict, 'roll', label1_text='Roll: ', row1=1, column1=1, row2=1, column2=2)
    init_2labels(val_dict, 'pitch', label1_text='Pitch: ', row1=2, column1=1, row2=2, column2=2)
    init_2labels(val_dict, 'yaw', label1_text='Yaw: ', row1=3, column1=1, row2=3, column2=2)
    init_2labels(val_dict, 'vx', label1_text='Vx: ', row1=4, column1=1, row2=4, column2=2)
    init_2labels(val_dict, 'vy', label1_text='Vy: ', row1=5, column1=1, row2=5, column2=2)
    init_2labels(val_dict, 'vz', label1_text='Vz: ', row1=6, column1=1, row2=6, column2=2)
    init_2labels(val_dict, 'heading', label1_text='Heading: ', row1=7, column1=1, row2=7, column2=2)
    init_2labels(val_dict, 'rangefinder', label1_text='Rangefinder: ', row1=8, column1=1, row2=8, column2=2)
    init_2labels(val_dict, 'lat', label1_text='Lat: ', row1=9, column1=1, row2=9, column2=2)
    init_2labels(val_dict, 'lon', label1_text='Lon: ', row1=10, column1=1, row2=10, column2=2)
    init_2labels(val_dict, 'alt', label1_text='Alt: ', row1=11, column1=1, row2=11, column2=2)
    init_2labels(val_dict, 'airspeed', label1_text='Airspeed: ', row1=12, column1=1, row2=12, column2=2)
    init_2labels(val_dict, 'groundspeed', label1_text='Groundspeed: ', row1=13, column1=1, row2=13, column2=2)
    init_2labels(val_dict, 'gimbal_roll', label1_text='Gimbal roll: ', row1=14, column1=1, row2=14, column2=2)
    init_2labels(val_dict, 'gimbal_pitch', label1_text='Gimbal pitch: ', row1=15, column1=1, row2=15, column2=2)
    init_2labels(val_dict, 'gimbal_yaw', label1_text='Gimbal yaw: ', row1=16, column1=1, row2=16, column2=2)
    init_2labels(val_dict, 'last_heartbeat', label1_text='Last heartbeat: ', row1=17, column1=1, row2=17, column2=2)
    
    init_2labels(val_dict, 'ch1', label1_text='Ch1: ', row1=1, column1=3, row2=1, column2=4)
    init_2labels(val_dict, 'ch2', label1_text='Ch2: ', row1=2, column1=3, row2=2, column2=4)
    init_2labels(val_dict, 'ch3', label1_text='Ch3: ', row1=3, column1=3, row2=3, column2=4)
    init_2labels(val_dict, 'ch4', label1_text='Ch4: ', row1=4, column1=3, row2=4, column2=4)
    init_2labels(val_dict, 'ch5', label1_text='Ch5: ', row1=5, column1=3, row2=5, column2=4)
    init_2labels(val_dict, 'ch6', label1_text='Ch6: ', row1=6, column1=3, row2=6, column2=4)
    init_2labels(val_dict, 'ch7', label1_text='Ch7: ', row1=7, column1=3, row2=7, column2=4)
    init_2labels(val_dict, 'ch8', label1_text='Ch8: ', row1=8, column1=3, row2=8, column2=4)

    button = tk.Button(root, text='Stop', width=25, command=close)
    button.grid(row=18, column=1, columnspan=2)

# Update the stored value in the dict with the new ones    
def dict_get_new_values(val_dict):
    for key, val in val_dict.iteritems():
        if val['value'] == None:
            val['value'] = 0
        val['value'] += random.randint(1,5)

# Update label value with stored value in dict    
def dict_refresh_values(val_dict):
    for key, val in val_dict.iteritems():
        val['lbl_val'].config(text=str(val['value']))
#    val_dict['roll']['lbl_val'].config(text=str(val_dict['roll']['value']))

def close():
    root.destroy()
    root.quit()

def tick():
    global val_dict
    dict_get_new_values(val_dict)
    dict_refresh_values(val_dict)
    root.after(200, tick)

# Init root
root = tk.Tk()
root.title("GCS GUI")
root.configure(background='white')
#root.geometry('500x500')

# Objects init
GUI_init(val_dict)

root.protocol('WM_DELETE_WINDOW', close)
root.after(0,tick)
root.mainloop()
