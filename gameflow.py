import time as t
import func as f
import attacks as a
from botstate import is_running

import random
from func import tap

print(">>> aqui gameflow aaaaaa <<<")


# -----------------------------
#   Surrender : Farming in Builder base
# -----------------------------

def tap_surrender_button():
    x = random.randint(24, 246)
    y = random.randint(721, 780)
    tap(x, y)


def confirm_surrender():
    x = random.randint(1014, 1323)
    y = random.randint(643, 752)
    tap(x, y)


def tap_return_home():
    # Ajusta estos valores si tu botón está en otra zona
    x = random.randint(850, 1065)
    y = random.randint(875, 950)
    tap(x, y)

# -------------------------
#  RECOGER ELIXIR ROSA
# -------------------------
def collect_pink_elixir():
    f.log("[Elixir] Moviendo cámara y abriendo Carro…")

    if not f.buscar_carro(600):
        f.log("[Elixir] Carro no encontrado, no se hace tap de recogida.")
        return

    f.log("[Elixir] Pulsando botón Recoger…")

    # Botón verde "Recoger"
    f.log("[Elixir] AQUI L TAP COMMENTED.")
    f.human_tap(1301, 871, 1510, 944)

    f.log("[Elixir] Recompensa recogida.")
    t.sleep(5)  # Espera un segundo para asegurar que la acción se complete

# -------------------------
#  COMPROBAR SI EL ALMACÉN ESTÁ LLENO
#  (placeholder, tú pones la lógica real)
# -------------------------
def is_elixir_full():
    # TODO: detección real
    return False

# -----------------------------
#   FIND MATCH (buscar aldea)
# -----------------------------
def find_match():
    f.log("[GameFlow] Buscando aldea…")
    f.find()
    t.sleep(5)



# -----------------------------
#   ESPERAR FIN DE BATALLA
# -----------------------------
def wait_for_battle_end():
    f.log("[GameFlow] Esperando fin de batalla…")

    while f.checkpixelBB(888, 900) != (180, 230, 125, 255):
        t.sleep(1)

    f.log("[GameFlow] Batalla terminada")


# -----------------------------
#   RECOGER BOTÍN
# -----------------------------
def collect_loot():
    f.log("[GameFlow] Recogiendo botín…")

    f.tap(950, 900)
    t.sleep(2)

    f.swipe1()
    t.sleep(1)

    f.tap(871, 521)
    t.sleep(1)

    f.tap(1400, 920)
    t.sleep(1)

    f.tap(1600, 100)
    t.sleep(1)

    f.log("[GameFlow] Botín recogido")


# -----------------------------
#   CICLO DE ATAQUE FARM (1 ciclo)
# -----------------------------


def farm_until_full(attacks_per_cycle=2):
    while not is_elixir_full():

        f.log(f">>> Nuevo ciclo de {attacks_per_cycle} ataques <<<")

        for i in range(attacks_per_cycle):  ## numero de ataques por ciclo
            if not is_running():
                return True

            f.log(f">>> Ataque {i+1}/10 <<<")

            # 0. Buscar aldea
            find_match()
            t.sleep(2)          # ← necesario para que cargue la aldea

            # 1. Atacar
            a.BBFarm()

            # 2. Rendirse
            tap_surrender_button()
            t.sleep(1)

            # 3. Confirmar rendición
            #f.screenshot() 
            confirm_surrender()
            t.sleep(1)

            # 4. Volver a Home
            f.log(">>> Return Home <<<")
            #f.screenshot() 
            tap_return_home()
            t.sleep(1)

        # 5. Recoger elixir rosa
        collect_pink_elixir()

    print(">>> Almacén lleno. Fin del ciclo. <<<")
    
    return True   # ← señal para parar







