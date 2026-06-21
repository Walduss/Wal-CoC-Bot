# Clash of Clans Bot (Wal CoC Bot)
#   -------  B E T A -----------
Folked from other repository: 
Credits to him, but was not working to me, at least Bulder base

I am working to Fix it and adapt to my needs.

Still in progress.

Below info from original repo

My comments:
 - BuilderBot
     - new button to farm only elixir, ..  find attacck and exit


## 📁 Estructura del proyecto

### [builderbot.py](ca://s?q=Explicar_builderbot_py)
Interfaz gráfica (GUI) del bot.  
Gestiona:
- Botones Start/Stop  
- Creación y control del hilo de farmeo  
- Flag `bot_running`  
- Llamadas a `farm_loop()`  

### [gameflow.py](ca://s?q=Explicar_gameflow_py)
Controla el flujo completo del farmeo:
- `farm_until_full()`  
- Ciclos de ataque  
- Rendición  
- Vuelta a Home  
- Recogida de elixir rosa  
- Uso de `smart_sleep()` para permitir STOP inmediato  

### [attacks.py](ca://s?q=Explicar_attacks_py)
Contiene la lógica de ataque:
- `BBFarm()`  
- `SSFarm()`  
- `find()`  
- Taps, swipes y despliegue de tropas  
- Funciones específicas de Builder Base  

### [func.py](ca://s?q=Explicar_func_py)
Funciones utilitarias:
- `tap()`  
- `swipe()`  
- Capturas de pantalla  
- Logs  
- Detección de píxeles  
- Conexión ADB  

### [config/](ca://s?q=Explicar_config_folder)
Carpeta opcional para imágenes, plantillas o configuraciones.

### [README.md](ca://s?q=Explicar_README)
Documentación del proyecto.


####  Original information ------
## Features

- **Customisable Attacks:**  
  Easily switch between different attack strategies (Super Drag, Pekka spam, Builder Base, etc.) by editing the attack type or using the GUI. Attack logic is modular and can be extended in `attacks.py`.

- **Builder Base Compatibility:**  
  Includes a dedicated Builder Base bot (`builderbot.py`) for automating attacks in the Builder Base. The bot  executes attacks, and returns home automatically.

- **Autonomous Loot Farm:**  
  The main bot (`Bot.py`) automatically searches for bases with high loot, attacks them, and repeats the process. It uses OCR to read loot values and only attacks when thresholds are met.

- **Fake Legends League Option:**  
  stays within set trophie range (4930-4970) so you get legends leuge bonus while having unlimited attacks.

## How to Use

1. **Install Requirements:**  
   - Python 3

2. **Configure Emulator:**  
   - Ensure Android emulator is running and accessible via ADB (`platform-tools`).
   - set adb port in the `attacks.py` file

3. **Run the Bot:**  
   - For main base farming:  
     `python Bot.py`
   - For Builder Base farming:  
     `python builderbot.py`

4. **Customise Attacks:**  
   - Edit `attacktype` in `Bot.py` or add new strategies in `attacks.py`.

5. **Fake Legends League:**  
   - Set `trophiebypass = False` in `Bot.py` to enable.

## Files

- `Bot.py` — Main loot farming bot with GUI.
- `builderbot.py` — Builder Base attack automation bot.
- `attacks.py` — Contains all attack strategies.
- `func.py` — Utility functions for screen interaction and OCR.

## Disclaimer

This bot is for educational purposes only. Use at your own risk.  
Automating gameplay may violate Clash of Clans' Terms of Service.
