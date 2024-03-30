import os
import json
import tkinter as tk
from tkinter import messagebox, simpledialog
from get_data import return_data, check_device_unlocked
from gen_label import make_label
import subprocess
import platform
from skip_activation import skip_activation

data = {}
checked_data = False

def get_data_button():
    global data
    if check_device_unlocked() == "True":
        data = return_data()
        if data:
            device_status = 'Device connected' if 'No Device Connected' not in data.values() else 'No device connected'
            device_status_label.config(text=device_status, bg='gray')
            if device_status == 'Device connected':
                tk.messagebox.showinfo('Success', 'Data successfully retrieved')
                get_data_button.config(bg='gray')
                check_data_button.config(bg='red')
        else:
            tk.messagebox.showerror('Error', 'There were errors retrieving data')
    elif check_device_unlocked() == "False":
        tk.messagebox.showerror('Error', 'Device is unactivated')
        tk.messagebox.showinfo('Info', 'Activating the device...')
        status = skip_activation()
        if status == 'Device activated':
            tk.messagebox.showinfo('Info', 'Activated, Please press "Get data" again')
        elif status != 'Device activated':
            tk.messagebox.showerror('Error', status)
        

def check_data_button():
    global checked_data
    if not data:
        tk.messagebox.showinfo('Info', 'Please press "Get data" first')
        return
    if 'No Device Connected' in data.values():
        tk.messagebox.showinfo('Info', 'Please connect a device first')
        return
    for key in ['BatteryHealth', 'Storage', 'IMEI', 'Model', 'Color']:
        if f'Unknown {key}' in data.values():
            tk.messagebox.showinfo('Info', f'Unable to retrieve {key}')
            data[key] = tk.simpledialog.askstring(f'Enter {key}', f'Enter {key}')
    data['Quality'] = tk.simpledialog.askstring('Enter Quality', 'Enter Quality')
    data['PayMethod'] = tk.simpledialog.askstring('Enter Paymethod', 'Enter Paymethod')
    tk.messagebox.showinfo('Success', 'Data successfully checked')
    data_text.config(text=json.dumps(data, indent=4), bg='white')
    checked_data = True
    check_data_button.config(bg='gray')
    make_label_button.config(bg='red')

def make_label_button():
    if not checked_data:
        tk.messagebox.showinfo('Info', 'Please press "Check data" first')
        return
    if 'No Device Connected' in data.values():
        tk.messagebox.showinfo('Info', 'Please connect a device first')
        return
    try:
        make_label(data)
    except Exception as e:
        tk.messagebox.showerror('Error', f'Error generating label: {e}')
        return
    tk.messagebox.showinfo('Success', 'Label generated')
    open_label_button.config(state='normal')
    open_label_button.pack()
    make_label_button.config(bg='gray')

def open_label_button():
    if not checked_data:
        tk.messagebox.showinfo('Info', 'Please press "Check data" first')
        return
    if 'No Device Connected' in data.values():
        tk.messagebox.showinfo('Info', 'Please connect a device first')
        return
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gen_label_path = os.path.join(script_dir, "gen_label.dymo")
    gen_label_path = ("\"" + gen_label_path + "\"")
    print(gen_label_path)
    if platform.system() == 'Darwin':
        subprocess.call(['open', gen_label_path])
    elif platform.system() == 'Windows':
        subprocess.Popen(['start', gen_label_path], shell=True)
root = tk.Tk()
root.configure(bg='gray')

root.title('Label Generator')

title_label = tk.Label(root, text='Auto Dymo Label - Iwannet', font=('Helvetica', 30))
title_label.pack()

get_data_button = tk.Button(root, text='Get Data', bg='red', fg='white', width=12, height=3, command=get_data_button)
get_data_button.pack()

device_status_label = tk.Label(root, text='Device Status:', bg='gray')
device_status_label.pack()

check_data_button = tk.Button(root, text='Check Data', bg='gray', fg='white', width=12, height=3, command=check_data_button)
check_data_button.pack()

make_label_button = tk.Button(root, text='Make Label', bg='gray', fg='white', width=12, height=3, command=make_label_button)
make_label_button.pack()

open_label_button = tk.Button(root, text='Open Label', bg='green', fg='white', width=12, height=3, state=tk.DISABLED, command=open_label_button)
open_label_button.pack_forget()

data_text = tk.Label(root, text='', width=40, height=12, bg='gray')
data_text.pack()

root.mainloop()

