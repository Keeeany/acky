import customtkinter as ctk
import pyautogui
import keyboard
import time
import json
import os
import ctypes
from threading import Thread

# Cargar configuración
CONFIG_FILE = "config.json"
DEFAULT_CONFIG = {"delay": 0.05, "theme": "dark"}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        return DEFAULT_CONFIG.copy()

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

config = load_config()
clicking = False
click_count = 0

ctk.set_appearance_mode(config["theme"])
ctk.set_default_color_theme("dark-blue")

def is_minecraft_active():
    hwnd = ctypes.windll.user32.GetForegroundWindow()
    length = ctypes.windll.user32.GetWindowTextLengthW(hwnd)
    buff = ctypes.create_unicode_buffer(length + 1)
    ctypes.windll.user32.GetWindowTextW(hwnd, buff, length + 1)
    window_title = buff.value
    return "Minecraft" in window_title

def autoclick_loop(delay, status_label, counter_label):
    global clicking, click_count
    while clicking:
        if is_minecraft_active():
            pyautogui.click()
            click_count += 1
            counter_label.configure(text=f"Clics: {click_count}")
            status_label.configure(text="✅ En ejecución (Minecraft activo)", text_color="green")
            time.sleep(delay)
        else:
            status_label.configure(text="⛔ Minecraft no está en primer plano", text_color="orange")
            time.sleep(1)

def toggle_clicking(delay_entry, status_label, counter_label):
    global clicking
    try:
        delay = float(delay_entry.get())
        if delay < 0.01:
            raise ValueError
    except ValueError:
        status_label.configure(text="❌ Delay inválido (> 0.01)", text_color="red")
        return

    config["delay"] = delay
    save_config(config)

    clicking = not clicking
    if clicking:
        t = Thread(target=autoclick_loop, args=(delay, status_label, counter_label), daemon=True)
        t.start()
    else:
        status_label.configure(text="🛑 Detenido", text_color="red")

def reset_stats(counter_label):
    global click_count
    click_count = 0
    counter_label.configure(text="Clics: 0")

def toggle_theme(app):
    new_theme = "dark" if config["theme"] == "light" else "light"
    ctk.set_appearance_mode(new_theme)
    config["theme"] = new_theme
    save_config(config)

def build_gui():
    app = ctk.CTk()
    app.title("acky - AutoClickerKY")
    app.geometry("400x400")
    app.resizable(False, False)

    title = ctk.CTkLabel(app, text="🖱️ acky - AutoClickerKY", font=("Segoe UI", 20, "bold"))
    title.pack(pady=10)

    status_label = ctk.CTkLabel(app, text="🛑 Detenido", text_color="red", font=("Segoe UI", 14))
    status_label.pack(pady=5)

    counter_label = ctk.CTkLabel(app, text=f"Clics: {click_count}", font=("Segoe UI", 12))
    counter_label.pack()

    ctk.CTkLabel(app, text="Delay (segundos):").pack(pady=(20, 5))
    delay_entry = ctk.CTkEntry(app, width=100, justify="center")
    delay_entry.insert(0, str(config["delay"]))
    delay_entry.pack()

    toggle_button = ctk.CTkButton(
        app, text="▶ Iniciar / Detener",
        command=lambda: toggle_clicking(delay_entry, status_label, counter_label),
        fg_color="#4CAF50", hover_color="#45a049", font=("Segoe UI", 14)
    )
    toggle_button.pack(pady=15)

    reset_button = ctk.CTkButton(
        app, text="🔄 Reiniciar contador",
        command=lambda: reset_stats(counter_label),
        fg_color="#3498db"
    )
    reset_button.pack(pady=5)

    theme_button = ctk.CTkButton(
        app, text="🌓 Cambiar Tema",
        command=lambda: toggle_theme(app),
        fg_color="#9b59b6"
    )
    theme_button.pack(pady=5)

    exit_button = ctk.CTkButton(
        app, text="❌ Salir",
        command=app.destroy,
        fg_color="#e74c3c",
        hover_color="#c0392b"
    )
    exit_button.pack(pady=(15, 5))

    app.mainloop()

if __name__ == "__main__":
    build_gui()
