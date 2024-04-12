import subprocess
import sys
import os

def restart_app():
    os.execl(sys.executable, sys.executable, *sys.argv) 
    
def skip_activation():
    try:
        subprocess.run(['ideviceactivation', 'activate', '-b'])
        status = 'Device activated'
    except Exception as e:
        if "drmHandshake" in str(e):
            status = 'Please connect to the internet and try again'   
            restart_app()
        else:
            status = str(e)
    return status

