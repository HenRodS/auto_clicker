import threading
import time
from pynput import keyboard, mouse


# Teclas/mouse para repetir o click
key = 'e'
mouse_click = mouse.Button.left

class AutoKey:
    def __init__(self, toggle_key, key_to_repeat=None, m_button_to_repeat=None):
        self.keyboard_ctrl = keyboard.Controller()
        self.mouse_ctrl = mouse.Controller()
        self.key_to_repeat = keyboard.KeyCode.from_char(key_to_repeat) if key_to_repeat else None
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
                # flag para saber se alguma ação foi tomada
                action_taken = False

                # --- Keyboard --- #
                if self.k_repeating and self.key_to_repeat:
                    self.keyboard_ctrl.press(self.key_to_repeat)
                    self.keyboard_ctrl.release(self.key_to_repeat)
                    print("teste key CLICK!")
                    action_taken = True

                # --- Mouse --- #
                if self.m_repeating and self.m_button_to_repeat:
                    self.mouse_ctrl.click(self.m_button_to_repeat)
                    print("teste mouse CLICK!")
                    action_taken = True

                # Se clicou, usa a taxa de click. Se não, usa um descanso minimo
                time.sleep(0.1 if action_taken else 0.01)
            else:
                time.sleep(0.1) # mais eficiente quando o toggle está desligado

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
        print("Aperte Num Lock para encerrar o script")

        try:
            while self.active:
                time.sleep(0.1)
        finally:
            k_listener.stop()
            m_listener.stop()

if __name__ == "__main__":
    print("=== CONFIGURAÇÃO DO AUTOCLICKER ===")
    
    # Seleção da Tecla de Teclado
    print("\n[1] Teclado")
    k_input = input("Qual tecla deseja repetir? (Deixe vazio para nenhum): ").strip()
    key_to_use = k_input if k_input else None

    # Seleção do Botão do Mouse
    print("\n[2] Mouse")
    print("1. Botão Esquerdo")
    print("2. Botão Direito")
    print("3. Nenhum")
    m_choice = input("Escolha uma opção (1-3): ").strip()

    mouse_to_use = None
    if m_choice == "1":
        mouse_to_use = mouse.Button.left
    elif m_choice == "2":
        mouse_to_use = mouse.Button.right

    print("\n" + "="*35)
    print("Configuração finalizada!")
    print(f"Tecla: {key_to_use if key_to_use else 'Desativado'}")
    print(f"Mouse: {'Esquerdo' if m_choice == '1' else 'Direito' if m_choice == '2' else 'Desativado'}")
    print("Aperte ENTER para carregar o script...")
    input() # Espera o usuário confirmar

    # Agora instanciamos a classe com as escolhas do usuário
    app = AutoKey(
        toggle_key=keyboard.Key.f8,
        key_to_repeat=key_to_use,
        m_button_to_repeat=mouse_to_use
    )
    
    app.run()