import json
import FreeSimpleGUI as sg
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
            window['device_status'].update(device_status)
            if device_status == 'Device connected':
                print('Data successfully retrieved\n')
                window['get_data'].update(button_color=('white', 'gray'))
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

    if not data:
        print('Please connect a device and unlock it\n')
        return
    if 'No Device Connected' in data.values():
        print('Please connect a device first\n')
        return
    for key in ['BatteryHealth', 'Storage', 'IMEI', 'Model']:
        if f'Unknown {key}' in data.values():
            print(f'Unable to retrieve {key}\n')
            data[key] = sg.popup_get_text(f'Enter {key}')
    if 'Unknown Color' in data.values():
        color = sg.popup_get_text('Enter Color')
        data['Color'] = color
    if 'No Device Connected' not in data.values():
        data['Quality'] = sg.popup_get_text('Enter Quality')
        cash_payment = sg.popup_yes_no('Was the device paid with cash/card? (yes = Marge, no = BTW)')
        if cash_payment == 'Yes':
            data['PayMethod'] = 'Marge'
        else:
            data['PayMethod'] = 'BTW'
    print('Data successfully checked\n')
    window['data_text'].update(json.dumps(data, indent=4))
    checked_data = True
    window['make_label'].update(button_color=('white', 'green'))

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
    return True

def open_label_():
    if not checked_data:
        print('Please press "Get data" first\n')
        return
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

layout = [
    [sg.Text('Auto Dymo Label - Iwannet', font=('Helvetica', 30))],
    [sg.Button('Get Data', key='get_data', button_color=('white', 'red'), size=(12, 3))],
    [sg.Text('Device Status:', key='device_status')],
    [sg.Button('Make Label', key='make_label', button_color=('white', 'gray'), size=(12, 3))],
    [sg.Multiline('', key='data_text', size=(60, 12), disabled=True)]
]

window = sg.Window('Label Generator', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'get_data':
        get_data_button()
    elif event == 'make_label':
        if make_label_():
            open_label_()
            restart_app()

window.close()