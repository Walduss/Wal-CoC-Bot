import func as f
import botcontroller as controller
import paint as p
from gui import BotInterface

# Helper
def parse_int(value, default=0):
    try:
        return int(value)
    except Exception:
        return default

# -----------------------------
#   FUNCIONES MANEJADORAS (LOGIC)
# -----------------------------

def bttn_start_Farm():
    attacks = parse_int(app.get_attacks(), default=2)
    controller.start_farm(attacks_per_cycle=attacks)

def bttn_stop():
    controller.stop()

def bttn_screenshot():
    try:
        filename = f.screenshot()
        app.log(f"Screenshot saved: {filename}")
    except Exception as e:
        app.log(f"Screenshot failed: {e}")

def bttn_recognize():
    try:
        result = f.recognize_screenshot()
        app.log(f"OCR result: {result}")
    except Exception as e:
        app.log(f"Image recognition failed: {e}")

def bttn_buscar_carro():
    try:
        _, dy_val = app.get_swipe_values()
        dy = parse_int(dy_val, default=400)
        f.buscar_carro(dy, debug=True)
    except Exception as e:
        app.log(f"Buscar Carro failed: {e}")

def bttn_test():
    app.log("Running test: hago swipe")
    try:
        xi, yi = 1450, 150
        _, dy_val = app.get_swipe_values()
        dy = parse_int(dy_val, default=400)

        app.log("=== TEST INICIADO ===")
        filename = f.screenshot()
        app.log(f"Screenshot antes de saved: {filename}")

        p.paint_test()
        f.swipe(xi, yi, xi, yi + dy, 500)

        filename = f.screenshot()
        app.log(f"Screenshot despues de saved: {filename}")
        app.log("Test swipe completed")
    except Exception as e:
        app.log(f"Test swipe failed: {e}")

# -----------------------------
#   INICIALIZACIÓN
# -----------------------------

# Instanciar pasándole los callbacks
app = BotInterface(
    on_start_farm=bttn_start_Farm,
    on_stop=bttn_stop,
    on_screenshot=bttn_screenshot,
    on_recognize=bttn_recognize,
    on_buscar_carro=bttn_buscar_carro,
    on_test=bttn_test
)

# Inyectar el método log en el módulo de funciones secundarias
f.log = app.log

if __name__ == "__main__":
    app.mainloop()