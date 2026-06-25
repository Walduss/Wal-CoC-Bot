import os
import shutil
import time as t
from PIL import Image, ImageEnhance
from PIL.ImageChops import screen
import easyocr
import cv2
import numpy as np
import random as r
import subprocess
import random

import config

reader = easyocr.Reader(['en'], gpu=False)

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


def ocr_image(filename, region=None, allowlist=None, detail=0):
    """OCR sobre una imagen guardada, opcionalmente recortando una región."""
    with Image.open(filename) as photo:
        if region:
            photo = photo.crop(region)
        photo = photo.convert("L")
        photo = ImageEnhance.Contrast(photo).enhance(2.0)
        image_np = np.array(photo)

    try:
        return reader.readtext(image_np, allowlist=allowlist, detail=detail)
    except Exception as e:
        log(f"[OCR] Error procesando imagen {filename}: {e}")
        return []


def recognize_screenshot(region=None, allowlist=None):
    filename = screenshot()
    return ocr_image(filename, region=region, allowlist=allowlist, detail=0)


def find_template(haystack_path, needle_path, threshold=0.8):
    """Busca una plantilla en una imagen y devuelve la posición si la confianza es suficiente."""
    screen = cv2.imread(haystack_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(needle_path, cv2.IMREAD_GRAYSCALE)

    if screen is None or template is None:
        log(f"[TEMPLATE] No se pudo cargar imagenes: {haystack_path} / {needle_path}")
        return None

    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val < threshold:
        return None

    return {
        "position": max_loc,
        "confidence": float(max_val),
        "size": (template.shape[1], template.shape[0]),
        "scale": 1.0,
    }


def find_template_multiscale(haystack_path, needle_path, scales=(0.9, 1.0, 1.1), threshold=0.8):
    """Busca una plantilla en varios tamaños para soportar pequeñas variaciones."""
    screen = cv2.imread(haystack_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(needle_path, cv2.IMREAD_GRAYSCALE)

    if screen is None or template is None:
        log(f"[TEMPLATE] No se pudo cargar imagenes: {haystack_path} / {needle_path}")
        return None

    best_result = None

    for scale in scales:
        new_w = int(template.shape[1] * scale)
        new_h = int(template.shape[0] * scale)

        if new_w < 10 or new_h < 10 or new_w > screen.shape[1] or new_h > screen.shape[0]:
            continue

        resized = cv2.resize(
            template,
            (new_w, new_h),
            interpolation=cv2.INTER_AREA if scale < 1.0 else cv2.INTER_LINEAR,
        )

        result = cv2.matchTemplate(screen, resized, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(result)

        if max_val < threshold:
            continue

        candidate = {
            "position": max_loc,
            "confidence": float(max_val),
            "size": (new_w, new_h),
            "scale": float(scale),
        }

        if best_result is None or candidate["confidence"] > best_result["confidence"]:
            best_result = candidate

    return best_result


def find_template_on_screen(template_path, threshold=0.8):
    screenshot_path = screenshot()
    return find_template(screenshot_path, template_path, threshold=threshold)


def buscar_carro(total_offset=500):
    log("Iniciando búsqueda del carro...")

    # swipe_pixels = total_offset
    # x1 = random.randint(600, 900)
    # y1 = random.randint(300, 450)
    # x2 = x1 + random.randint(-40, 40)
    # y2 = y1 + swipe_pixels
    # dur = random.randint(250, 400)

    # log(f"[SWIPE] bajando pantalla: ({x1},{y1}) -> ({x2},{y2}) dur={dur}ms")
    # swipe(x1, y1, x2, y2, dur)
    # t.sleep(0.5)

    swipe(900, 300, 900 - total_offset, 300 + total_offset, 300)
    t.sleep(0.3)

    screenshot_path = screenshot()

    # import shutil
    # shutil.copy(screenshot_path, "debug_last_screenshot.png")
    # log("DEBUG: screenshot guardada como debug_last_screenshot.png")

    result = find_template_multiscale(screenshot_path, "templates/carro_lleno.png", scales=(0.9, 1.0, 1.1), threshold=0.75)

    if not result:
        log("No se encontró carro_lleno.png, probando carro_lleno_1.png...")
        result = find_template_multiscale(screenshot_path, "templates/carro_lleno_1.png", scales=(0.9, 1.0, 1.1), threshold=0.75)

    if result:
        log(f"Carro lleno detectado en {result['position']} scale={result['scale']} confidence={result['confidence']:.2f}")

        cx = result["position"][0] + result["size"][0] // 2
        cy = result["position"][1] + result["size"][1] // 2
        log(f"[CARRO] encontrado en {result['position']}, tap en ({cx},{cy}) scale={result['scale']:.2f}")
        tap(cx, cy)
        t.sleep(0.4)
        return True

    log("Carro no encontrado")
    log("[CARRO] no encontrado después del swipe hacia abajo")

    return False


def tap(x, y):
    os.system(f'C:/LDPlayer/LDPlayer9/adb.exe -s {config.ADB_PORT} shell input tap {x} {y}')


def human_tap(x1, y1, x2, y2):
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

# def human_swipe_and_tap_to_cart(total_offset=500):
#     """
#     Hace un swipe hacia abajo, luego busca el carro y, si se localiza, hace tap.
#     """
#     log("[debug] Iniciando human_swipe_and_tap_to_cart()")

#     swipe_pixels = total_offset
#     x1 = random.randint(600, 900)
#     y1 = random.randint(300, 450)
#     x2 = x1 + random.randint(-40, 40)
#     y2 = y1 + swipe_pixels
#     dur = random.randint(250, 400)

#     log(f"[SWIPE] bajando pantalla: ({x1},{y1}) -> ({x2},{y2}) dur={dur}ms")
#     swipe(x1, y1, x2, y2, dur)
#     t.sleep(0.5)

#     screenshot_path = screenshot()
#     log("[debug] screenshot para buscar carro guardada")

#     result = find_template_multiscale(screenshot_path, "templates/carro_lleno.png", scales=(0.9, 1.0, 1.1), threshold=0.75)

#     if result:
#         cx = result["position"][0] + result["size"][0] // 2
#         cy = result["position"][1] + result["size"][1] // 2
#         log(f"[CARRO] encontrado en {result['position']}, tap en ({cx},{cy}) scale={result['scale']:.2f}")
#         tap(cx, cy)
#         t.sleep(0.4)
#         return True

#     log("[CARRO] no encontrado después del swipe hacia abajo")
#     return False


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


