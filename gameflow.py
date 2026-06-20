import time as t
import func as f
import attacks as a

import random
from func import tap

#from builderbot import Bbot_running



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
    x = random.randint(50, 200)
    y = random.randint(300, 600)
    tap(x, y)
    t.sleep(1)

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
def OLD_run_farm_cycle():
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

        f.log(">>> Nuevo ciclo de 10 ataques <<<")

        for i in range(10):
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
    
    Bbot_running.clear()






