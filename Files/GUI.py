import json
import tkinter as tk
from tkinter import simpledialog
from get_data import return_data, check_device_unlocked
from gen_label import make_label
import subprocess
import platform
from skip_activation import skip_activation
import os
import sys

data = {}
checked_data = False

def get_data_button():
    global data, checked_data
    if check_device_unlocked() == "True":
        data = return_data()
        if data:
            device_status = 'Device connected' if 'No Device Connected' not in data.values() else 'No device connected'
            device_status_label.config(text=device_status, bg='gray')
            if device_status == 'Device connected':
                print('Data successfully retrieved\n')
                get_data_button.config(bg='gray')
        else:
            print('There were errors retrieving data\n')
    elif check_device_unlocked() == "False":
        print('Device is unactivated\n')
        print('Activating the device...\n')
        status = skip_activation()
        if status == 'Device activated':
            print('Activated, Please press "Get data" again\n')
        elif status != 'Device activated':
            print(status + '\n')

    global checked_data
    if not data:
        print('Please connect a device and unlock it\n')
        return
    if 'No Device Connected' in data.values():
        print('Please connect a device first\n')
        return
    for key in ['BatteryHealth', 'Storage', 'IMEI', 'Model']:
        if f'Unknown {key}' in data.values():
            print(f'Unable to retrieve {key}\n')
            data[key] = tk.simpledialog.askstring(f'Enter {key}', f'Enter {key}')
    if 'Unknown Color' in data.values():
        color = tk.simpledialog.askstring('Enter Color', 'Enter Color')
        data['Color'] = color
    if 'No Device Connected' not in data.values():
        data['Quality'] = tk.simpledialog.askstring('Enter Quality', 'Enter Quality')
        cash_payment = tk.messagebox.askyesno('Payment', 'Was the device paid with cash/card?')
        if cash_payment:
            data['PayMethod'] = 'Marge'
        else:
            data['PayMethod'] = 'BTW'
    print('Data successfully checked\n')
    data_text.config(text=json.dumps(data, indent=4), bg='white')
    checked_data = True
    make_label_button.config(bg='green')

def make_label_():
    if not checked_data:
        print('Please press "Get data" first\n')
        return
    if 'No Device Connected' in data.values():
        print('Please connect a device first\n')
        return
    try:
        make_label(data)
    except Exception as e:
        print(f'Error generating label: {e}\n')
        return
    print('Label generated\n')
    make_label = True
def open_label_():
    if not checked_data:
        print('Please press "Get data" first\n')
        return
    if not make_label:
        print('Please press "Make label" first\n')
    if 'No Device Connected' in data.values():
        print('Please connect a device first\n')
        return
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gen_label_path = os.path.join(script_dir, "Files/gen_label.dymo")  # Update the file path
    gen_label_path = os.path.join(script_dir, "gen_label.dymo")
    gen_label_path = os.path.abspath(gen_label_path)
    if platform.system() == 'Darwin':
        subprocess.run(['open', gen_label_path])
    elif platform.system() == 'Windows':
        subprocess.run(['start', gen_label_path], shell=True)

def restart_app():
    os.execl(sys.executable, sys.executable, *sys.argv) 
       
root = tk.Tk()
root.configure(bg='gray')

root.title('Label Generator')

title_label = tk.Label(root, text='Auto Dymo Label - Iwannet', font=('Helvetica', 30))
title_label.pack()

get_data_button = tk.Button(root, text='Get Data', bg='red', fg='white', width=12, height=3, command=get_data_button)
get_data_button.pack()

device_status_label = tk.Label(root, text='Device Status:', bg='gray')
device_status_label.pack()

def make_label_button_click():
    make_label_()
    open_label_()
    restart_app()

make_label_button = tk.Button(root, text='Make Label', bg='gray', fg='white', width=12, height=3, command=make_label_button_click)
make_label_button.pack()

data_text = tk.Label(root, text='', width=40, height=12, bg='gray')
data_text.pack()

root.mainloop()
