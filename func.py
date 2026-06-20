import os
import time as t
from PIL import Image, ImageEnhance
#import easyocr
import random as r
import subprocess
import random

import config

# reader = easyocr.Reader(['en'])

def log(msg):
    pass  # será reemplazada por builderbot

def OLD_screenshot(filename):
    cmd = ['C:/LDPlayer/LDPlayer9/adb.exe', '-s', f'emulator-{config.ADB_PORT}', 'exec-out', 'screencap', '-p']
    with open(filename, 'wb') as f:
        f.write(subprocess.check_output(cmd))

def screenshot():
    # Crear carpeta si no existe
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")

    # Nombre con timestamp
    timestamp = t.strftime("%Y%m%d_%H%M%S")
    filename = f"screenshots/screen_{timestamp}.png"

    # Captura directa del emulador
    cmd = f"C:/LDPlayer/LDPlayer9/adb.exe -s {config.ADB_PORT} exec-out screencap -p"
    with open(filename, "wb") as f_out:
        subprocess.run(cmd.split(), stdout=f_out)

    return filename

def tap(x, y):
    os.system(f'C:/LDPlayer/LDPlayer9/adb.exe -s {config.ADB_PORT} shell input tap {x} {y}')


def human_tap(x1, x2, y1, y2):
    x = random.randint(x1, x2)
    y = random.randint(y1, y2)
    tap(x, y)


def swipe(): 
  os.system('C:/LDPlayer/LDPlayer9/adb.exe -s ' + config.ADB_PORT + ' shell  input touchscreen swipe 1450 150 900 650 500 ')

def swipe2(): 
  os.system('C:/LDPlayer/LDPlayer9/adb.exe -s ' + config.ADB_PORT + ' shell  input touchscreen swipe 1900 850 100 850 500 ')

def find(): 
  print(">>> entro en find <<<")
  tap(100, 1000)
  t.sleep(0.3)
  print(">>> find despes de sleeep <<<")
  tap(1375, 650)
  print(">>> find despues de sleep y tap <<<")

def next():
  tap(1750, 800)


def checkloot(port):
    filename = f"Pictures/{port}val.png"
    screenshot(port, filename)
    print("captured")
    t.sleep(0.2)

    with Image.open(filename) as photo:
        (left, upper, right, lower) = (97, 155, 285, 295)
        loot = photo.crop((left, upper, right, lower))

        loot = loot.convert('L')
        loot = ImageEnhance.Contrast(loot).enhance(2.0)
        # Binarize (convert to black and white)
        loot = loot.point(lambda x: 0 if x < 250 else 255)

        loot.save(filename)

        checkloot.result = reader.readtext(filename, allowlist='0123456789', detail=0)
        if len(checkloot.result) < 3:
            checkloot.result = ["0", "0", "0"] # Default values if OCR fails


def checktrophies(port):
    filename = f"Pictures/{port}trophies.png"
    screenshot(port, filename)
    print("captured")
    t.sleep(0.2)

    with Image.open(filename) as photo:
        (left, upper, right, lower) = (130, 160, 255, 210)
        trophies = photo.crop((left, upper, right, lower))

        trophies = trophies.convert('L')
        trophies = ImageEnhance.Contrast(trophies).enhance(2.0)
        trophies = trophies.point(lambda x: 0 if x < 240 else 255)

        trophies.save(filename)

        checktrophies.result = reader.readtext(filename, allowlist='0123456789', detail=0)


def checkpixel(port):
    filename = f"Pictures/{port}return.png"
    screenshot(port, filename)

    checkp = Image.open(filename)
    return checkp.getpixel((898, 909)) == checkp.getpixel((969, 938))



def checkpixelBB(x,y):
    filename = f"Pictures/{config.ADB_PORT}bb.png"
    screenshot(config.ADB_PORT, filename)
    checkp = Image.open(filename)
    return checkp.getpixel((x, y))


