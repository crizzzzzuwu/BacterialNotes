from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
from pydub import AudioSegment
from pydub.playback import play
import numpy as np
import threading

# Función para generar un tono
def generate_tone(frequency, duration_ms):
    sample_rate = 44100  # Hz
    amplitude = 0.5
    t = (np.arange(duration_ms / 1000.0 * sample_rate) / sample_rate)
    wave = amplitude * np.sin(2 * np.pi * frequency * t)
    return AudioSegment(
        (wave * 32767).astype(np.int16).tobytes(),
        frame_rate=sample_rate,
        sample_width=2,
        channels=1
    )

# Notas musicales en Hz
notes = {
    'C': 261.63,
    'D': 293.66,
    'E': 329.63,
    'F': 349.23,
    'G': 392.00,
    'A': 440.00,
    'B': 493.88
}

class NoteApp(App):
    def build(self):
        self.title = "Reproductor de Notas Musicales"
        
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Crear dropdown para seleccionar nota
        self.dropdown = DropDown()
        self.note_buttons = {}
        for note in notes.keys():
            btn = Button(text=note, size_hint_y=None, height=44)
            btn.bind(on_release=lambda btn: self.select_note(btn.text))
            self.dropdown.add_widget(btn)
            self.note_buttons[note] = btn

        self.note_button = Button(text='Selecciona una nota', size_hint_y=None, height=44)
        self.note_button.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.note_button, 'text', x))
        layout.add_widget(self.note_button)

        # Input para duración
        self.duration_input = TextInput(hint_text='Duración en segundos', multiline=False, input_filter='float')
        layout.add_widget(self.duration_input)

        # Botón para reproducir
        play_button = Button(text='Reproducir', size_hint_y=None, height=44)
        play_button.bind(on_press=self.play_note)
        layout.add_widget(play_button)

        return layout

    def select_note(self, note):
        self.selected_note = note

    def play_note(self, instance):
        if not hasattr(self, 'selected_note'):
            print("No se ha seleccionado ninguna nota.")
            return
        
        duration_str = self.duration_input.text
        if not duration_str:
            print("Por favor, ingresa una duración.")
            return
        
        try:
            duration = float(duration_str) * 1000
        except ValueError:
            print("La duración debe ser un número.")
            return
        
        frequency = notes[self.selected_note]
        tone = generate_tone(frequency, duration)

        def play_audio():
            play(tone)

        threading.Thread(target=play_audio).start()

if __name__ == '__main__':
    NoteApp().run()