import threading
import time
from pynput.keyboard import Key, Controller, Listener

class AutoKey:
    def __init__(self, key_to_press, toggle_key):
        self.keyboard = Controller()
        self.key_to_press = key_to_press
        self.toggle_key = toggle_key
        self.running = False
        self.active = True

    def toggle_action(self, key):
        if key == self.toggle_key: 
            self.running = not self.running
            print(f"[STATUS] Repetição: {'LIGADA' if self.running else 'DESLIGADA'}")

        if key == Key.alt_r:
            self.active = False
            self.running = False
            return False
        
    def clicker(self):
        """Função que rodará em uma thread separada para não travar o teclado"""
        while self.active:
            if self.running:
                self.keyboard.press(self.key_to_press)
                self.keyboard.release(self.key_to_press)
                time.sleep(0.1)
            else:
                time.sleep(0.1)


if __name__ == "__main__":
    app = AutoKey(key_to_press='e', toggle_key=Key.f8)

    print("--- Script Iniciado ---")
    print("Aperte F8 para Ligar/Desligar")
    print("Aperte ESC para encerrar o script")

    # Cria uma thread para que o clicker rode em paralelo
    thread_clicker = threading.Thread(target=app.clicker)
    thread_clicker.start()

    with Listener(on_press=app.toggle_action) as listener:
        listener.join()