import threading
import time as t

import func as f
import attacks as a
import gameflow as gf
import botstate

Bbot_thread = None


def start_farm():
    global Bbot_thread
    if not botstate.is_running():
        botstate.start()
        Bbot_thread = threading.Thread(target=farm_loop, daemon=True)
        Bbot_thread.start()
        f.log("Farm started.")


def stop():
    botstate.stop()
    f.log("Stopping bot...")


def farm_loop():
    while botstate.is_running():
        full = gf.farm_until_full()

        if full:
            f.log("Storage full. Stopping bot.")
            botstate.stop()
            break
