import os
import shutil


def make_label(data):

    script_dir = os.path.dirname(os.path.abspath(__file__))
    gen_label_path = os.path.join(script_dir, "gen_label.dymo")

    if not os.path.exists(gen_label_path):
        with open(gen_label_path, "w") as file:
            file.write("")

    my_dymo_path = os.path.join(script_dir, "my.dymo")
    shutil.copy(my_dymo_path, gen_label_path)

    with open(gen_label_path, "r+") as file:
        content = file.read()
        content = content.replace("IMEI", str(data['Imei']))
        content = content.replace("MODEL", str(data['Model']))
        content = content.replace("PCOLOR", str(data['Color']))
        content = content.replace("BATTERY", str(data['BatteryHealth']))
        content = content.replace("QUALITY", str(data['Quality']))
        content = content.replace("PAYM", str(data['PayMethod']))
        content = content.replace("STORAGE", str(data['Storage']))
        file.seek(0)
        file.write(content)
        file.truncate()
