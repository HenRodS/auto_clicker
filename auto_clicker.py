import threading
import time
from pynput.keyboard import Key, Controller, Listener, KeyCode

class AutoKey:
    def __init__(self, key_to_repeat, toggle_key):
        self.keyboard = Controller()
        self.key_to_repeat = KeyCode.from_char(key_to_repeat)
        self.toggle_key = toggle_key
        self.is_pressing = False
        self.active = True

    def on_press(self, key):
        """é chamada quando o listener detectou que soltou"""
        if key == self.key_to_repeat:
            self.is_pressing = True

        if key == Key.alt_gr:
            self.active = False
            return False
        
    def on_release(self, key):
        """é chamada quando o listener detectar que soltou"""
        if key == self.key_to_repeat:
            self.is_pressing = False
    
    def clicker(self):
        """Função que rodará em uma thread separada para não travar o teclado"""
        while self.active:
            if self.is_pressing:
                self.keyboard.press(self.key_to_repeat)
                self.keyboard.release(self.key_to_repeat)
                print("click!")
                time.sleep(0.1)
            else:
                time.sleep(0.1)


if __name__ == "__main__":
    app = AutoKey(key_to_repeat='e', toggle_key=Key. f8)

    print("--- Script Iniciado ---")
    print("Aperte F8 para Ligar/Desligar")
    print("Aperte Alt Gr para encerrar o script")

    # Cria uma thread para que o clicker rode em paralelo
    thread_clicker = threading.Thread(target=app.clicker)
    thread_clicker.start()

    with Listener(on_press=app.on_press, on_release=app.on_release) as listener:
        listener.join()