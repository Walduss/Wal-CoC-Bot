import time as t
import func as f
import attacks as a

import random
from func import tap


# -----------------------------
#   Surrender : Farming in Builder base
# -----------------------------

def tap_surrender_button():
    x = random.randint(24, 246)
    y = random.randint(721, 780)
    tap(x, y)


def confirm_surrender():
    x = random.randint(200, 300)
    y = random.randint(740, 820)
    tap(x, y)


def tap_return_home():
    # Ajusta estos valores si tu botón está en otra zona
    x = random.randint(800, 1100)
    y = random.randint(750, 900)
    tap(x, y)



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

    f.tap(950, 900, p)
    t.sleep(2)

    f.swipe(p)
    t.sleep(1)

    f.tap(871, 521, p)
    t.sleep(1)

    f.tap(1400, 920, p)
    t.sleep(1)

    f.tap(1600, 100, p)
    t.sleep(1)

    f.log("[GameFlow] Botín recogido")


# -----------------------------
#   CICLO DE ATAQUE FARM (1 ciclo)
# -----------------------------
def run_farm_cycle():
    find_match()
    t.sleep(2)          # ← necesario para que cargue la aldea
    a.BBFarm()          # ataque puro


    f.log("[BBF] saco Foto")
    f.screenshot() 
    f.log("[BBF] despues de saco foto") 

    tap_surrender_button()
    t.sleep(1)
    confirm_surrender()


    wait_for_battle_end()
    collect_loot()


def farm_until_full():
    while not is_elixir_full():

        print(">>> Nuevo ciclo de 10 ataques <<<")

        for i in range(10):
            print(f">>> Ataque {i+1}/10 <<<")

            # 1. Atacar
            BBFarm()

            # 2. Rendirse
            tap_surrender_button()
            time.sleep(1)

            # 3. Confirmar rendición
            confirm_surrender()
            time.sleep(2)

            # 4. Volver a Home
            tap_return_home()
            time.sleep(3)

        # 5. Recoger elixir rosa
        collect_pink_elixir()

    print(">>> Almacén lleno. Fin del ciclo. <<<")
