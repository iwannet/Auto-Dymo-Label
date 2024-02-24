import subprocess

def check_device_unlocked():
    try:
        output = subprocess.check_output(['ideviceinfo', '-k', 'ActivationState'])
        activation_state = output.decode().strip()
        if activation_state == 'Unactivated':
            return "False"
        else:
            return "True"
    except subprocess.CalledProcessError:
        return "No Device Connected"


def get_imei():
    try:
        output = subprocess.check_output(['ideviceinfo', '-k', 'InternationalMobileEquipmentIdentity'])
        return output.decode().strip()
    except subprocess.CalledProcessError:
        return "No Device Connected"


def get_battery_health():
    try:
        try:
            output1 = subprocess.check_output(['idevicediagnostics', 'ioregentry', 'AppleARMPMUCharger'])
            output1 = output1.decode().strip()
        except (subprocess.CalledProcessError, IndexError):
            output1 = None

        try:
            output2 = subprocess.check_output(['idevicediagnostics', 'ioregentry', 'AppleSmartBattery'])
            output2 = output2.decode().strip()
        except (subprocess.CalledProcessError, IndexError):
            output2 = None

        battery_health = output1 or output2

        if battery_health:
            battery_health = battery_health.split('\n')
            applerawmaxcapacity = None
            design_capacity = None
            for i in range(len(battery_health)):
                if 'AppleRawMaxCapacity' in battery_health[i]:
                    if '<integer>' in battery_health[i+1] and '</integer>' in battery_health[i+1]:
                        line = battery_health[i+1]
                        applerawmaxcapacity = int(line.split('<integer>')[1].split('</integer>')[0])
                elif 'DesignCapacity' in battery_health[i]:
                    if '<integer>' in battery_health[i+1] and '</integer>' in battery_health[i+1]:
                        line = battery_health[i+1]
                        design_capacity = int(line.split('<integer>')[1].split('</integer>')[0])
            
            if applerawmaxcapacity is not None and design_capacity is not None:
                battery_health_percent = (applerawmaxcapacity / design_capacity) * 100
                return battery_health_percent

        return "Unknown Battery Health"
    except subprocess.CalledProcessError:
        return "No Device Connected"


def get_color():
    try:
        output = subprocess.check_output(['ideviceinfo', '-k', 'DeviceColor'])
        color_code = output.decode().strip()
        color_mapping = {
            '#3b3b3c': 'Black',
            '#ffffff': 'White',
            '#ff3b30': 'Red',
            '#ff9500': 'Orange',
            '#ffcc00': 'Yellow',
            '#4cd964': 'Green',
            '#5ac8fa': 'Blue',
            '#007aff': 'Light Blue',
            '#5856d6': 'Purple',
            '#ff2d55': 'Pink',
            '#8e8e93': 'Space Gray',
            '#c69c6d': 'Gold',
            '#d0d1d2': 'Silver'
        }
        return color_mapping.get(color_code, 'Unknown Color')
    except subprocess.CalledProcessError:
        return "No Device Connected"


def get_storage():
    try:
        output = subprocess.check_output(['ideviceinfo', '-q', 'com.apple.disk_usage'])
        output_lines = output.decode().strip().split('\n')
        for line in output_lines:
            if line.startswith('TotalDiskCapacity'):
                line_parts = line.split(': ')
                if len(line_parts) > 1:
                    total_disk_capacity = int(line_parts[1].strip())
                    total_disk_capacity_gb = total_disk_capacity // 1000000000
                    return total_disk_capacity_gb
    except subprocess.CalledProcessError:
        return "No Device Connected"

    return "Unknown Disk Capacity"


def get_model():
    try:
        output = subprocess.check_output(['ideviceinfo', '-k', 'ProductType'])
        product_type = output.decode().strip()
        model_mapping = {
            'iPhone1,1': 'iPhone',
            'iPhone1,2': 'iPhone 3G',
            'iPhone2,1': 'iPhone 3GS',
            'iPhone3,1': 'iPhone 4',
            'iPhone3,2': 'iPhone 4',
            'iPhone3,3': 'iPhone 4',
            'iPhone4,1': 'iPhone 4S',
            'iPhone5,1': 'iPhone 5',
            'iPhone5,2': 'iPhone 5',
            'iPhone5,3': 'iPhone 5c',
            'iPhone5,4': 'iPhone 5c',
            'iPhone6,1': 'iPhone 5s',
            'iPhone6,2': 'iPhone 5s',
            'iPhone7,1': 'iPhone 6 Plus',
            'iPhone7,2': 'iPhone 6',
            'iPhone8,1': 'iPhone 6s',
            'iPhone8,2': 'iPhone 6s Plus',
            'iPhone8,4': 'iPhone SE',
            'iPhone9,1': 'iPhone 7',
            'iPhone9,2': 'iPhone 7 Plus',
            'iPhone9,3': 'iPhone 7',
            'iPhone9,4': 'iPhone 7 Plus',
            'iPhone10,1': 'iPhone 8',
            'iPhone10,2': 'iPhone 8 Plus',
            'iPhone10,3': 'iPhone X',
            'iPhone10,4': 'iPhone 8',
            'iPhone10,5': 'iPhone 8 Plus',
            'iPhone10,6': 'iPhone X',
            'iPhone11,2': 'iPhone XS',
            'iPhone11,4': 'iPhone XS Max',
            'iPhone11,6': 'iPhone XS Max',
            'iPhone11,8': 'iPhone XR',
            'iPhone12,1': 'iPhone 11',
            'iPhone12,3': 'iPhone 11 Pro',
            'iPhone12,5': 'iPhone 11 Pro Max',
            'iPhone13,1': 'iPhone 12 Mini',
            'iPhone13,2': 'iPhone 12',
            'iPhone13,3': 'iPhone 12 Pro',
            'iPhone13,4': 'iPhone 12 Pro Max',
            'iPhone14,1': 'iPhone 13 Mini',
            'iPhone14,2': 'iPhone 13',
            'iPhone14,3': 'iPhone 13 Pro',
            'iPhone14,4': 'iPhone 13 Pro Max',
            'iPhone15,1': 'iPhone 14 Mini',
            'iPhone15,2': 'iPhone 14',
            'iPhone15,3': 'iPhone 14 Pro',
            'iPhone15,4': 'iPhone 14 Pro Max',
            'iPad1,1': 'iPad',
            'iPad2,1': 'iPad 2',
            'iPad2,2': 'iPad 2',
            'iPad2,3': 'iPad 2',
            'iPad2,4': 'iPad 2',
            'iPad2,5': 'iPad mini',
            'iPad2,6': 'iPad mini',
            'iPad2,7': 'iPad mini',
            'iPad3,1': 'iPad (3rd generation)',
            'iPad3,2': 'iPad (3rd generation)',
            'iPad3,3': 'iPad (3rd generation)',
            'iPad3,4': 'iPad (4th generation)',
            'iPad3,5': 'iPad (4th generation)',
            'iPad3,6': 'iPad (4th generation)',
            'iPad4,1': 'iPad Air',
            'iPad4,2': 'iPad Air',
            'iPad4,3': 'iPad Air',
            'iPad4,4': 'iPad mini 2',
            'iPad4,5': 'iPad mini 2',
            'iPad4,6': 'iPad mini 2',
            'iPad4,7': 'iPad mini 3',
            'iPad4,8': 'iPad mini 3',
            'iPad4,9': 'iPad mini 3',
            'iPad5,1': 'iPad mini 4',
            'iPad5,2': 'iPad mini 4',
            'iPad5,3': 'iPad Air 2',
            'iPad5,4': 'iPad Air 2',
            'iPad6,3': 'iPad Pro (9.7-inch)',
            'iPad6,4': 'iPad Pro (9.7-inch)',
            'iPad6,7': 'iPad Pro (12.9-inch)',
            'iPad6,8': 'iPad Pro (12.9-inch)',
            'iPad6,11': 'iPad (5th generation)',
            'iPad6,12': 'iPad (5th generation)',
            'iPad7,1': 'iPad Pro (12.9-inch, 2nd generation)',
            'iPad7,2': 'iPad Pro (12.9-inch, 2nd generation)',
            'iPad7,3': 'iPad Pro (10.5-inch)',
            'iPad7,4': 'iPad Pro (10.5-inch)',
            'iPad7,5': 'iPad (6th generation)',
            'iPad7,6': 'iPad (6th generation)',
            'iPad7,11': 'iPad (7th generation)',
            'iPad7,12': 'iPad (7th generation)',
            'iPad8,1': 'iPad Pro (11-inch)',
            'iPad8,2': 'iPad Pro (11-inch)',
            'iPad8,3': 'iPad Pro (11-inch)',
            'iPad8,4': 'iPad Pro (11-inch)',
            'iPad8,5': 'iPad Pro (12.9-inch, 3rd generation)',
            'iPad8,6': 'iPad Pro (12.9-inch, 3rd generation)',
            'iPad8,7': 'iPad Pro (12.9-inch, 3rd generation)',
            'iPad8,8': 'iPad Pro (12.9-inch, 3rd generation)',
            'iPad8,9': 'iPad Pro (11-inch, 2nd generation)',
            'iPad8,10': 'iPad Pro (11-inch, 2nd generation)',
            'iPad8,11': 'iPad Pro (12.9-inch, 4th generation)',
            'iPad8,12': 'iPad Pro (12.9-inch, 4th generation)',
            'iPad11,1': 'iPad mini (5th generation)',
            'iPad11,2': 'iPad mini (5th generation)',
            'iPad11,3': 'iPad Air (3rd generation)',
            'iPad11,4': 'iPad Air (3rd generation)',
            'iPod1,1': 'iPod touch',
            'iPod2,1': 'iPod touch (2nd generation)',
            'iPod3,1': 'iPod touch (3rd generation)',
            'iPod4,1': 'iPod touch (4th generation)',
            'iPod5,1': 'iPod touch (5th generation)',
            'iPod7,1': 'iPod touch (6th generation)',
            'iPod9,1': 'iPod touch (7th generation)'
        }
        return model_mapping.get(product_type, 'Unknown Device')
    except subprocess.CalledProcessError:
        return "No Device Connected"


def return_data():
    imei = get_imei()
    battery_health = get_battery_health()
    battery_health = str(int(round(battery_health, 0))) if isinstance(battery_health, float) else battery_health
    color = get_color()
    storage = get_storage()
    model = get_model()
    return {'IMEI': imei, 'BatteryHealth': battery_health, 'Color': color, 'Storage': storage, 'Model': model}
