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
            
            if applerawmaxcapacity is not None and design_capacity is not None and design_capacity != 0:
                battery_health_percent = (applerawmaxcapacity / design_capacity) * 100
                if battery_health_percent > 100:
                    battery_health_percent = 100
                return battery_health_percent

        return "Unknown BatteryHealth"
    except subprocess.CalledProcessError:
        return "No Device Connected"


def get_color():
    try:
        output = subprocess.check_output(['ideviceinfo', '-k', 'DeviceEnclosureColor'])
        color_code = output.decode().strip()
        color_mapping = {
            '#3b3b3c': 'Zwart',
            '#ffffff': 'Wit',
            '#ff3b30': 'Rood',
            '#ff9500': 'Oranje',
            '#ffcc00': 'Geel',
            '#4cd964': 'Groen',
            '#5ac8fa': 'Blauw',
            '#007aff': 'Lichtblauw',
            '#5856d6': 'Paars',
            '#ff2d55': 'Roze',
            '#8e8e93': 'Grijs',
            '#c69c6d': 'Goud',
            '#d0d1d2': 'Zilver',
            '1': 'Zwart',
            '2': 'Wit',
            '3': 'Goud',
            '4': 'Roos',
            '5': 'Grijs',
            '6': 'Rood',
            '7': 'Geel',
            '8': 'Oranje',
            '9': 'Blauw'
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

    return "Unknown Storage"


def get_model():
    try:
        output = subprocess.check_output(['ideviceinfo', '-k', 'ProductType'])
        product_type = output.decode().strip()
        model_mapping = {
            'iPhone1,1': 'iPhone',
            'iPhone1,2': '3G',
            'iPhone2,1': '3GS',
            'iPhone3,1': '4',
            'iPhone3,2': '4',
            'iPhone3,3': '4',
            'iPhone4,1': '4S',
            'iPhone5,1': '5',
            'iPhone5,2': '5',
            'iPhone5,3': '5C',
            'iPhone5,4': '5C',
            'iPhone6,1': '5S',
            'iPhone6,2': '5S',
            'iPhone7,1': '6Plus',
            'iPhone7,2': '6',
            'iPhone8,1': '6s',
            'iPhone8,2': '6sPlus',
            'iPhone8,4': 'SE',
            'iPhone9,1': '7',
            'iPhone9,2': '7Plus',
            'iPhone9,3': '7',
            'iPhone9,4': '7Plus',
            'iPhone10,1': '8',
            'iPhone10,2': '8Plus',
            'iPhone10,3': 'X',
            'iPhone10,4': '8',
            'iPhone10,5': '8Plus',
            'iPhone10,6': 'X',
            'iPhone11,2': 'XS',
            'iPhone11,4': 'XSMax',
            'iPhone11,6': 'XSMax',
            'iPhone11,8': 'XR',
            'iPhone12,1': '11',
            'iPhone12,3': '11Pro',
            'iPhone12,5': '11ProMax',
            'iPhone12,8': 'SE2',
            'iPhone13,1': '12Mini',
            'iPhone13,2': '12',
            'iPhone13,3': '12Pro',
            'iPhone13,4': '12ProMax',
            'iPhone14,2': '13Pro',
            'iPhone14,3': '13ProMax',
            'iPhone14,4': '13Mini',
            'iPhone14,5': '13',
            'iPhone14,6': 'SE3',
            'iPhone14,7': '14',
            'iPhone14,8': '14Plus',
            'iPhone15,2': '14Pro',
            'iPhone15,3': '14ProMax',
            'iPhone15,4': '15',
            'iPhone15,5': '15Plus',
            'iPhone16,1': '15Pro',
            'iPhone16,2': '15ProMax',
            'iPad1,1': 'iPad',
            'iPad2,1': 'iPad 2',
            'iPad2,2': 'iPad 2',
            'iPad2,3': 'iPad 2',
            'iPad2,4': 'iPad 2',
            'iPad2,5': 'iPad mini',
            'iPad2,6': 'iPad mini',
            'iPad2,7': 'iPad mini',
            'iPad3,1': 'iPad (3rd gen)',
            'iPad3,2': 'iPad (3rd gen)',
            'iPad3,3': 'iPad (3rd gen)',
            'iPad3,4': 'iPad (4th gen)',
            'iPad3,5': 'iPad (4th gen)',
            'iPad3,6': 'iPad (4th gen)',
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
            'iPad6,11': 'iPad (5th gen)',
            'iPad6,12': 'iPad (5th gen)',
            'iPad7,1': 'iPad Pro (12.9-inch, 2nd gen)',
            'iPad7,2': 'iPad Pro (12.9-inch, 2nd gen)',
            'iPad7,3': 'iPad Pro (10.5-inch)',
            'iPad7,4': 'iPad Pro (10.5-inch)',
            'iPad7,5': 'iPad (6th gen)',
            'iPad7,6': 'iPad (6th gen)',
            'iPad7,11': 'iPad (7th gen)',
            'iPad7,12': 'iPad (7th gen)',
            'iPad8,1': 'iPad Pro (11-inch)',
            'iPad8,2': 'iPad Pro (11-inch)',
            'iPad8,3': 'iPad Pro (11-inch)',
            'iPad8,4': 'iPad Pro (11-inch)',
            'iPad8,5': 'iPad Pro (12.9-inch, 3rd gen)',
            'iPad8,6': 'iPad Pro (12.9-inch, 3rd gen)',
            'iPad8,7': 'iPad Pro (12.9-inch, 3rd gen)',
            'iPad8,8': 'iPad Pro (12.9-inch, 3rd gen)',
            'iPad8,9': 'iPad Pro (11-inch, 2nd gen)',
            'iPad8,10': 'iPad Pro (11-inch, 2nd gen)',
            'iPad8,11': 'iPad Pro (12.9-inch, 4th gen)',
            'iPad8,12': 'iPad Pro (12.9-inch, 4th gen)',
            'iPad11,1': 'iPad mini (5th gen)',
            'iPad11,2': 'iPad mini (5th gen)',
            'iPad11,3': 'iPad Air (3rd gen)',
            'iPad11,4': 'iPad Air (3rd gen)',
            'iPad11,6': 'iPad 8th Gen (WiFi)',
            'iPad11,7': 'iPad 8th Gen (WiFi+Cellular)',
            'iPad12,1': 'iPad 9th Gen (WiFi)',
            'iPad12,2': 'iPad 9th Gen (WiFi+Cellular)',
            'iPad14,1': 'iPad mini 6th Gen (WiFi)',
            'iPad14,2': 'iPad mini 6th Gen (WiFi+Cellular)',
            'iPad13,1': 'iPad Air 4th Gen (WiFi)',
            'iPad13,2': 'iPad Air 4th Gen (WiFi+Cellular)',
            'iPad13,4': 'iPad Pro 11 inch 5th Gen',
            'iPad13,5': 'iPad Pro 11 inch 5th Gen',
            'iPad13,6': 'iPad Pro 11 inch 5th Gen',
            'iPad13,7': 'iPad Pro 11 inch 5th Gen',
            'iPad13,8': 'iPad Pro 12.9 inch 5th Gen',
            'iPad13,9': 'iPad Pro 12.9 inch 5th Gen',
            'iPad13,10': 'iPad Pro 12.9 inch 5th Gen',
            'iPad13,11': 'iPad Pro 12.9 inch 5th Gen',
            'iPad13,16': 'iPad Air 5th Gen (WiFi)',
            'iPad13,17': 'iPad Air 5th Gen (WiFi+Cellular)',
            'iPad13,18': 'iPad 10th Gen',
            'iPad13,19': 'iPad 10th Gen',
            'iPad14,3': 'iPad Pro 11 inch 4th Gen',
            'iPad14,4': 'iPad Pro 11 inch 4th Gen',
            'iPad14,5': 'iPad Pro 12.9 inch 6th Gen',
            'iPad14,6': 'iPad Pro 12.9 inch 6th Gen',
            'iPod1,1': 'iPod touch',
            'iPod2,1': 'iPod touch (2nd gen)',
            'iPod3,1': 'iPod touch (3rd gen)',
            'iPod4,1': 'iPod touch (4th gen)',
            'iPod5,1': 'iPod touch (5th gen)',
            'iPod7,1': 'iPod touch (6th gen)',
            'iPod9,1': 'iPod touch (7th gen)'
        }
        return model_mapping.get(product_type, 'Unknown Model')
    except subprocess.CalledProcessError:
        return "No Device Connected"


def return_data():
    imei = get_imei()
    battery_health = get_battery_health()
    battery_health = str(int(round(battery_health, 0))) if isinstance(battery_health, float) else battery_health
    color = get_color()
    storage = get_storage()
    model = get_model()
    return {'Imei': imei, 'BatteryHealth': battery_health, 'Color': color, 'Storage': storage, 'Model': model}
