import time
import customtkinter as ctk

class BotInterface(ctk.CTk):
    def __init__(self, on_start_farm, on_stop, on_screenshot, on_recognize, on_buscar_carro, on_test):
        super().__init__()
        
        # Configuración de ventana
        self.title("Wal CoC BBot")
        self.geometry("400x500")
        
        # Guardar callbacks lógicos
        self.on_start_farm = on_start_farm
        self.on_stop = on_stop
        self.on_screenshot = on_screenshot
        self.on_recognize = on_recognize
        self.on_buscar_carro = on_buscar_carro
        self.on_test = on_test

        self._init_components()

    def _init_components(self):
        # ---------- TABS ----------
        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="x", padx=10, pady=10)

        tab_bot = self.tabs.add("Bot")
        tab_tools = self.tabs.add("Herramientas")

        # ---------- TAB BOT ----------
        tab_bot.columnconfigure(0, weight=1)
        tab_bot.columnconfigure(1, weight=1)

        self.button_Farm = ctk.CTkButton(tab_bot, text="Start Farm", command=self.on_start_farm)
        self.button_Farm.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.button_Stop = ctk.CTkButton(tab_bot, text="Stop", command=self.on_stop)
        self.button_Stop.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.attacks_label = ctk.CTkLabel(tab_bot, text="Ataques/ciclo:")
        self.attacks_label.grid(row=1, column=0, padx=5, pady=(10, 2), sticky="w")

        self.attacks_entry = ctk.CTkEntry(tab_bot, placeholder_text="2")
        self.attacks_entry.grid(row=2, column=0, padx=5, pady=2, sticky="ew")

        # ---------- TAB HERRAMIENTAS ----------
        tab_tools.columnconfigure(0, weight=1)
        tab_tools.columnconfigure(1, weight=1)

        self.button_Screenshot = ctk.CTkButton(tab_tools, text="Screenshot", command=self.on_screenshot)
        self.button_Screenshot.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.button_Test = ctk.CTkButton(tab_tools, text="Test", command=self.on_test)
        self.button_Test.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.button_Recognize = ctk.CTkButton(tab_tools, text="Recognize", command=self.on_recognize)
        self.button_Recognize.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

        self.button_Buscar_Carro = ctk.CTkButton(tab_tools, text="Buscar Carro", command=self.on_buscar_carro)
        self.button_Buscar_Carro.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        self.swipe_dx_label = ctk.CTkLabel(tab_tools, text="Swipe dx:")
        self.swipe_dx_label.grid(row=2, column=0, padx=5, pady=(10, 2), sticky="w")
        self.swipe_dx_entry = ctk.CTkEntry(tab_tools, placeholder_text="0")
        self.swipe_dx_entry.grid(row=3, column=0, padx=5, pady=2, sticky="ew")

        self.swipe_dy_label = ctk.CTkLabel(tab_tools, text="Swipe dy:")
        self.swipe_dy_label.grid(row=2, column=1, padx=5, pady=(10, 2), sticky="w")
        self.swipe_dy_entry = ctk.CTkEntry(tab_tools, placeholder_text="400")
        self.swipe_dy_entry.grid(row=3, column=1, padx=5, pady=2, sticky="ew")

        # ---------- LOG ----------
        self.log_frame = ctk.CTkFrame(self)
        self.log_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.log_textbox = ctk.CTkTextbox(self.log_frame, wrap="word")
        self.log_textbox.pack(fill="both", expand=True)

    # Métodos públicos para interactuar con la interfaz desde fuera
    def log(self, message):
        timestamp = time.strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"

        def append():
            textbox = self.log_textbox._textbox
            textbox.tag_configure("spacing", spacing3=8)
            textbox.insert("end", formatted_message + "\n", "spacing")
            textbox.see("end")

        self.after(0, append)

    def get_attacks(self):
        return self.attacks_entry.get()

    def get_swipe_values(self):
        return self.swipe_dx_entry.get(), self.swipe_dy_entry.get()