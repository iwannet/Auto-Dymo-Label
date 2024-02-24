import os
import json
import PySimpleGUI as sg
from get_data import return_data, check_device_unlocked
from gen_label import make_label
data = {}
checked_data = False

def get_data_button():
    global data
    if check_device_unlocked() == "True":
        data = return_data()
        if data:
            device_status = 'Device connected' if 'No Device Connected' not in data.values() else 'No device connected'
            window['-DEVICE_STATUS-'].update(value=device_status)
            if device_status == 'Device connected':
                sg.popup('Data successfully retrieved')
        else:
            sg.popup_error('There were errors retrieving data')

def check_data_button():
    global checked_data
    if not data:
        sg.popup('Please press "Get data" first')
        return
    if 'No Device Connected' in data.values():
        sg.popup('Please connect a device first')
        return
    for key in ['BatteryHealth', 'Storage', 'IMEI', 'Model', 'Color']:
        if f'Unknown {key}' in data.values():
            sg.popup(f'Unable to retrieve {key}')
            data[key] = sg.popup_get_text(f'Enter {key}')
    data['Quality'] = sg.popup_get_text('Enter Quality')
    data['PayMethod'] = sg.popup_get_text('Enter Paymethod')
    sg.popup('Data successfully checked')
    window['-DATA_TEXT-'].update(value=json.dumps(data, indent=4))
    checked_data = True

def make_label_button():
    if not checked_data:
        sg.popup('Please press "Check data" first')
        return
    if 'No Device Connected' in data.values():
        sg.popup('Please connect a device first')
        return
    try: make_label(data)
    except Exception as e:
        sg.popup_error(f'Error generating label: {e}')
        return
    sg.popup('Label generated')
    window['-OPEN_LABEL-'].update(visible=True)

def open_label_button():
    if not checked_data:
        sg.popup('Please press "Check data" first')
        return
    if 'No Device Connected' in data.values():
        sg.popup('Please connect a device first')
        return
    script_dir = os.path.dirname(os.path.abspath(__file__))
    gen_label_path = os.path.join(script_dir, "gen_label.dymo")
    os.startfile(gen_label_path)

layout = [
    [sg.Text('Auto Dymo Label - Iwannet', font=('Helvetica', 20), justification='center')],
    [sg.Button('Get Data', button_color=('white', 'blue'), size=(10, 2), key='-GET_DATA-', enable_events=True)],
    [sg.Text('Device Status:', key='-DEVICE_STATUS-', size=(20, 1))],
    [sg.Button('Check Data', button_color=('white', 'blue'), size=(10, 2), key='-CHECK_DATA-', enable_events=True)],
    [sg.Button('Make Label', button_color=('white', 'blue'), size=(10, 2), key='-MAKE_LABEL-', enable_events=True)],
    [sg.Button('Open Label', button_color=('white', 'green'), visible=False, key='-OPEN_LABEL-', enable_events=True)],
    [sg.Text('', key='-DATA_TEXT-', size=(40, 10))]
]

sg.theme('Dark Amber')
window = sg.Window('Label Generator', layout, element_justification='center', margins=(30, 30))

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == '-GET_DATA-':
        get_data_button()
    elif event == '-CHECK_DATA-':
        check_data_button()
    elif event == '-MAKE_LABEL-':
        make_label_button()
    elif event == '-OPEN_LABEL-':
        open_label_button()

window.close()
