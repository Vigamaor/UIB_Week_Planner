import os
from sys import platform, executable
import subprocess

print("This script will install all required dependencies for the UIB_Week_planner application.")
answer = input("Do you want to continue [y/n]: ")

if answer.lower() != "y":
    exit()

while True:
    if "Week_planner.py" not in os.listdir():
        new_dir = input("We cant find the Week_planner python script please provide the folder which Week_planner "
                        "resides in [please input q to quit]")
        if new_dir == "q":
            exit()
        os.chdir(new_dir)

    else:
        break

try:
    import PySide2
    import qdarkstyle
except ImportError:
    subprocess.check_call([executable, "-m", "pip", "install", "pyside2"])
    subprocess.check_call([executable, "-m", "pip", "install", "qdarkstyle"])

try:
    import icalendar
except ImportError:
    subprocess.check_call([executable, "-m", "pip", "install", "icalendar"])
try:
    import requests
except ImportError:
    subprocess.check_call([executable, "-m", "pip", "install", "requests"])


