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
        content = content.replace("IMEI", data['IMEI'])
        content = content.replace("MODEL", data['Model'].replace(" ", "").upper())
        content = content.replace("STORAGE", str(data['Storage']).replace(" ", "").upper())
        content = content.replace("model", data['Model'])
        content = content.replace("pcolor", data['Color'])
        content = content.replace("BATTERY", data['BatteryHealth'])
        content = content.replace("QUALITY", data['Quality'])
        content = content.replace("PAYM", data['PayMethod'].replace(" ", "").upper())
        content = content.replace("paym", data['PayMethod'])
        file.seek(0)
        file.write(content)
        file.truncate()
