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



def swipe(x1, y1, x2, y2, duration_ms):
    """
    Swipe genérico usando ADB.
    x1, y1 = punto inicial
    x2, y2 = punto final
    duration_ms = duración en milisegundos
    """
    log(f"[SWIPE] x1={x1}, y1={y1}, x2={x2}, y2={y2}, dur={duration_ms}ms")

    cmd = (
        f'{config.ADB_PATH} -s {config.ADB_PORT} shell input touchscreen swipe '
        f'{x1} {y1} {x2} {y2} {duration_ms}'
    )
    os.system(cmd)

    

def swipe1():  # borrar si no esta en uso 
  os.system('C:/LDPlayer/LDPlayer9/adb.exe -s ' + config.ADB_PORT + ' shell  input touchscreen swipe 1450 150 900 650 500 ')


def swipe2(): 
  os.system('C:/LDPlayer/LDPlayer9/adb.exe -s ' + config.ADB_PORT + ' shell  input touchscreen swipe 1900 850 100 850 500 ')

def simple_swipe_up(pixels, duration_ms=300):
    """
    Hace un swipe hacia arriba exactamente 'pixels' píxeles.
    No hace nada más.
    """
    # Punto inicial (centro aproximado de la pantalla)
    x1 = random.randint(750, 850)
    y1 = random.randint(950, 1050)

    # Punto final (misma X, subir 'pixels')
    x2 = x1 - int(pixels * 0.5)   
    y2 = y1 + pixels

    log(f"[SIMPLE SWIPE] {x1},{y1} -> {x2},{y2} dur={duration_ms}ms")

    swipe(x1, y1, x2, y2, duration_ms)

def test_swipe_and_tap_cart():
    """
    Primera versión simple:
    - dx, dy aleatorios
    - Swipe de (200+dx, 400+dy)
    - TAP en (1270-dx, 420-dy)
    """

    # Aleatorio suave, ajusta el rango si quieres más o menos variación
    dx = random.randint(-50, 50)
    dy = random.randint(-50, 50)

    base_sx = 200
    base_sy = 400

    swipe_x = base_sx + dx   # horizontal (hacia la izquierda)
    swipe_y = base_sy + dy   # vertical (hacia abajo)

    # Punto inicial del swipe (puedes cambiarlo si quieres)
    x1 = 800
    y1 = 1000

    # Punto final: izquierda y abajo
    x2 = x1 - swipe_x
    y2 = y1 + swipe_y

    log(f"[TEST SWIPE] dx={dx}, dy={dy}, swipe=({x1},{y1})->({x2},{y2})")
    swipe(x1, y1, x2, y2, 300)

"""
    # TAP compensado
    tap_x = 1270 - dx
    tap_y = 420 - dy

    log(f"[TEST TAP] tap=({tap_x},{tap_y})")
    human_tap(tap_x, tap_y, 60, 60)
"""

def human_swipe_and_tap_to_cart(total_offset=500):
    """
    Mueve la cámara hacia arriba de forma humana y luego pulsa directamente
    el Carro de Elixir, compensando lo que falte tras el swipe.
    """
    log("[debug] Iniciando human_swipe_and_tap_to_cart()")
    # 1) Elegimos cuánto del movimiento será swipe
    swipe_part = random.randint(int(total_offset * 0.5), int(total_offset * 0.8))
    tap_part = total_offset - swipe_part  # lo que falta

    # 2) Swipe humano hacia arriba
    x1 = random.randint(600, 900)
    y1 = random.randint(900, 1100)

    x2 = x1 + random.randint(-40, 40)
    y2 = y1 - swipe_part

    dur = random.uniform(0.18, 0.35)
    swipe(x1, y1, x2, y2, dur)

    t.sleep(random.uniform(0.15, 0.35))

    # 3) Tap final compensado (este es el que toca el Carro)
    #    Se calcula en función de lo que falta por subir
    carro_x = random.randint(200, 300)
    carro_y = (y1 - swipe_part) - tap_part + random.randint(-10, 10)

    #human_tap(carro_x, carro_y, 80, 80)
    log("[debug] aqui el tap de human_swipe_and_tap_to_cart()")
    t.sleep(1.0)


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


