import time as t
import func as f
import attacks as a

# Puerto del emulador (lo recibimos desde builderbot)
p = None

def set_port(port):
    global p
    p = port


# -----------------------------
#   FIND MATCH (buscar aldea)
# -----------------------------
def find_match():
    f.log("[GameFlow] Buscando aldea…")
    f.find(p)
    t.sleep(5)


# -----------------------------
#   ESPERAR FIN DE BATALLA
# -----------------------------
def wait_for_battle_end():
    f.log("[GameFlow] Esperando fin de batalla…")

    while f.checkpixelBB(p, 888, 900) != (180, 230, 125, 255):
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
    wait_for_battle_end()
    collect_loot()
