import threading
import time
from pynput import keyboard, mouse

class AutoKey:
    def __init__(self, key_to_repeat, toggle_key, m_button_to_repeat):
        self.keyboard_ctrl = keyboard.Controller()
        self.mouse_ctrl = mouse.Controller()
        self.key_to_repeat = keyboard.KeyCode.from_char(key_to_repeat)
        self.toggle_key = toggle_key
        self.m_button_to_repeat = m_button_to_repeat
        self.k_repeating = False
        self.m_repeating = False
        self.running = False
        self.active = True

    def on_press(self, key):
        """é chamada quando o listener detectou que pressionou"""
        if key == self.key_to_repeat:
            self.k_repeating = True

        if key == self.toggle_key:
            self.running = not self.running
            print(f"script {'ligado' if self.running else 'desligado'}")

        if key == keyboard.Key.num_lock:
            self.active = False
            return False

    def on_release(self, key):
        """é chamada quando o listener detectou que soltou"""
        if key == self.key_to_repeat:
            self.k_repeating = False

    def on_click(self, x, y, button, pressed):
        if button == self.m_button_to_repeat:
            # print(f"Botão esquerdo {'pressionado' if pressed else 'solto'}")
            self.m_repeating = pressed
    
    def clicker(self):
        """Função que rodará em uma thread separada pra não travar o teclado"""
        while self.active:
            if self.running:
                if self.k_repeating:
                    self.keyboard_ctrl.press(self.key_to_repeat)
                    self.keyboard_ctrl.release(self.key_to_repeat)
                    print("click")
                    time.sleep(0.1)

                if self.m_repeating:
                    self.mouse_ctrl.click(self.m_button_to_repeat)
                    print("mouse click!")
                    time.sleep(0.1)

    def run(self):
        # iniciando a thread do clicker ANTES dos listeners
        t = threading.Thread(target=self.clicker)
        t.daemon = True
        t.start()

        # Iniciando os listeners
        k_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        m_listener = mouse.Listener(on_click=self.on_click)

        k_listener.start()
        m_listener.start()

        print("--- Script Iniciado ---")
        print("Aperte F8 para Ligar/Desligar")
        print("Aperte Alt Gr para encerrar o script")

        try:
            while self.active:
                time.sleep(0.1)
        finally:
            k_listener.stop()
            m_listener.stop()

if __name__ == "__main__":
    app = AutoKey(key_to_repeat='e', toggle_key=keyboard.Key.f8, m_button_to_repeat=mouse.Button.left)
    app.run()
