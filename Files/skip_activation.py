import subprocess

def skip_activation():
    try:
        subprocess.run(['ideviceactivation', 'activate', '-b'])
        status = 'Device activated'
    except Exception as e:
        status = e
    return status
    
