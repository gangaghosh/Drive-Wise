import subprocess

def drowsiness_detection():
    script_path = r'driver-fatigue-detection-system-master\drowsiness_detection.py'
    subprocess.Popen(['python', script_path], shell=True)



def pedestrian_detection():
    script_path = r'pedstrain\ped.py'
    subprocess.Popen(['python', script_path], shell=True)
