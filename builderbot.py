import time as t
import customtkinter as ctk
import threading

import func as f
import attacks as a
import gameflow as gf
from botstate import Bbot_running, start, stop

print(">>> aqui builder aaaaaa <<<")


# -----------------------------
#   CONFIGURACIÓN INICIAL
# -----------------------------

Bbot_thread = None


# -----------------------------
#   FUNCIONES DE BOTONES
# -----------------------------

def bttn_start_BBot():
    global Bbot_thread
    if not Bbot_running.is_set():
        start()
        Bbot_thread = threading.Thread(target=BBot, daemon=True)
        Bbot_thread.start()
        log("BBot started.")


def bttn_start_Farm():
    global Bbot_thread
    if not Bbot_running.is_set():
        start()
        Bbot_thread = threading.Thread(target=farm_loop, daemon=True)
        Bbot_thread.start()
        log("Farm started.")


def bttn_stop():
    stop()
    log("Stopping bot...")


# -----------------------------
#   BUCLE PRINCIPAL DE FARM
# -----------------------------

def farm_loop():
    while Bbot_running.is_set():
        #gf.OLD_run_farm_cycle()
        full = gf.farm_until_full()

        if full:
            log("Storage full. Stopping bot.")
            stop()
            break

        


# -----------------------------
#   HILO ANTIGUO BBOT
# -----------------------------

def BBot():
    while Bbot_running.is_set():
        f.find()
        t.sleep(5)

        secondattack = False
        log("attack started")

        a.BB()
        t.sleep(10)

        while f.checkpixelBB(p, 888, 900) != (180, 230, 125, 255):
            t.sleep(1)

            if f.checkpixelBB(p, 1862, 815) != (255, 255, 255, 255) and not secondattack:
                secondattack = True
                log("round 2")
                a.BB2()
                t.sleep(10)

        log("attack finished")
        f.tap(950, 900, p)
        t.sleep(2)
        f.swipe(p)
        log("collecting loot")
        t.sleep(0.5)
        f.tap(871, 521, p)
        t.sleep(0.5)
        f.tap(1400, 920, p)
        t.sleep(1)
        f.tap(1600, 100, p)
        t.sleep(1)


# -----------------------------
#   INTERFAZ GRÁFICA
# -----------------------------

App = ctk.CTk()
App.title("Wal CoC BBot")
App.geometry("700x400")

# Marco de botones
App.button_frame = ctk.CTkFrame(App)
App.button_frame.pack(pady=10)

App.button_BBot = ctk.CTkButton(App.button_frame, text="Start BBot", command=bttn_start_BBot)
App.button_BBot.grid(row=0, column=0, padx=5)

App.button_Farm = ctk.CTkButton(App.button_frame, text="Start Farm", command=bttn_start_Farm)
App.button_Farm.grid(row=0, column=1, padx=5)

App.button_Stop = ctk.CTkButton(App.button_frame, text="Stop", command=bttn_stop)
App.button_Stop.grid(row=0, column=2, padx=5)

# Marco principal
App.content_frame = ctk.CTkFrame(App)
App.content_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Log
App.log_textbox = ctk.CTkTextbox(App.content_frame, height=200, wrap="word")
App.log_textbox.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

App.content_frame.columnconfigure(0, weight=3)
App.content_frame.rowconfigure(0, weight=1)


# -----------------------------
#   FUNCIÓN DE LOG
# -----------------------------

def log(message):
    def append():
        textbox = App.log_textbox._textbox
        textbox.tag_configure("spacing", spacing3=8)
        textbox.insert("end", message + "\n", "spacing")
        textbox.see("end")

    App.after(0, append)


# Inyectamos log en func.py
f.log = log


# -----------------------------
#   INICIO DE LA APP
# -----------------------------

App.mainloop()
