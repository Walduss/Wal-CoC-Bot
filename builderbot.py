import customtkinter as ctk

import func as f
import botcontroller as controller

print(">>> aqui builder aaaaaa <<<")


# -----------------------------
#   FUNCIONES DE BOTONES
# -----------------------------

def bttn_start_Farm():
    controller.start_farm()


def bttn_stop():
    controller.stop()


def bttn_screenshot():
    try:
        filename = f.screenshot()
        log(f"Screenshot saved: {filename}")
    except Exception as e:
        log(f"Screenshot failed: {e}")


def bttn_test():
    log("Running test: test_swipe_and_tap_cart()")
    try:
        f.test_swipe_and_tap_cart()
        log("Test swipe completed")
    except Exception as e:
        log(f"Test swipe failed: {e}")


# -----------------------------
#   INTERFAZ GRÁFICA
# -----------------------------

App = ctk.CTk()
App.title("Wal CoC BBot")
# Ventana más estrecha para no tapar tanto lo que hay detrás
App.geometry("400x360")

# Marco de botones
App.button_frame = ctk.CTkFrame(App)
App.button_frame.pack(pady=10, padx=10)
App.button_frame.columnconfigure(0, weight=1)
App.button_frame.columnconfigure(1, weight=1)

App.button_Farm = ctk.CTkButton(App.button_frame, text="Start Farm", command=bttn_start_Farm)
App.button_Farm.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

App.button_Stop = ctk.CTkButton(App.button_frame, text="Stop", command=bttn_stop)
App.button_Stop.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

App.button_Screenshot = ctk.CTkButton(App.button_frame, text="Screenshot", command=bttn_screenshot)
App.button_Screenshot.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

App.button_Test = ctk.CTkButton(App.button_frame, text="Test", command=bttn_test)
App.button_Test.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

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
