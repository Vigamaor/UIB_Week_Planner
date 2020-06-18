import os
from sys import platform, executable
import subprocess
import tarfile
import zipfile
import time



print("This script will install all required dependencies for the UIB_Week_planner application.")
answer = input("Do you want to continue [y/n]: ")

if answer.lower() != "y":
    exit()

while True:
    if "Week_planner.py" not in os.listdir():
        new_dir = input("We cant find the Week_planner python script please provide the folder which Week_planner resides in [please input q to quit]")
        if new_dir == "q":
            exit()
        os.chdir(new_dir)

    else:
        break


try:
    import wget
except ImportError:
    subprocess.check_call([executable, "-m", "pip", "install", "wget"])
    import wget
try:
    import selenium
except ImportError:
    subprocess.check_call([executable, "-m", "pip", "install", "selenium"])
try:
    import pyside2
except ImportError:
    subprocess.check_call([executable, "-m", "pip", "install", "pyside2"])
    subprocess.check_call([executable, "-m", "pip", "install", "qdarkstyle"])
try:
    import bs4
except ImportError:
    subprocess.check_call([executable, "-m", "pip", "install", "beautifulsoup4"])



if "dep" not in os.listdir():
    os.mkdir("dep")

os.chdir("dep")
if platform == "win32":
    if "geckodriver.exe" not in os.listdir():
        wget.download("https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-win64.zip", "geckodriver-v0.26.0-win64.zip")
        zip_file = zipfile.ZipFile("geckodriver-v0.26.0-win64.zip", mode="r")
        zip_file.extract("geckodriver.exe")
        time.sleep(3)
        os.remove("geckodriver-v0.26.0-win64.zip")
elif platform == "linux" or platform == "linux2":
    if "geckodriver" not in os.listdir():
        wget.download("https://github.com/mozilla/geckodriver/releases/download/v0.26.0/geckodriver-v0.26.0-linux64.tar.gz","geckodriver-v0.26.0-linux64.tar.gz")
        file = tarfile.open("geckodriver-v0.26.0-linux64.tar.gz")
        file.extractall()
        time.sleep(3)
        os.remove("geckodriver-v0.26.0-linux64.tar.gz")

else:
    assert False, f"Expected platform win32, linux or linux2 not {platform}"


