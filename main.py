import keyboard
import pygame
import random
import threading
from collections import deque
import logging

#TODO Make graphics
#TODO Uploading and fetchcing unique sounds
#TODO Hotkey to close the program
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='keyboard.log', 
    filemode='w'  # Overwrite log file
)

class CreamyKeyboard:
    def __init__(self):
        # Dictionary mapping specific keys to their sound files
        self.specific_keys = {
            'enter': ['enter1.wav', 'enter2.wav'],
            'space': ['center.wav'],
            'backspace': ['right1.wav', 'right2.wav'],
        }

        # List of sound files for random selection
        self.keyboard_sound = ['left1.wav', 'right1.wav', 'left2.wav', 'right2.wav', 'left3.wav', 'right3.wav']
        self.PATH = "sounds/"

        # Initialize
        pygame.mixer.init()
        self.sound_files = {key: [self.PATH + file for file in files] for key, files in self.specific_keys.items()}

        # Create a queue for keyboard sounds
        self.keyboard_sound_queue = deque(self.PATH + file for file in self.keyboard_sound)

        # Configure logging
        self.logger = logging.getLogger('CreamyKeyboard')

    # Function to get the next keyboard sound
    def get_next_keyboard_sound(self):
        if self.keyboard_sound_queue:
            return self.keyboard_sound_queue.popleft()
        else:
            return None

    # Function to play a sound in a separate thread
    def play_sound_thread(self, sound_file):
        pygame.mixer.Sound(sound_file).play()

    def play_sound(self, key):
        if key in self.specific_keys:
            # Select a random sound file associated with the key
            sound_file = random.choice(self.sound_files[key])
        else:
            # Get the next keyboard sound from the queue
            sound_file = self.get_next_keyboard_sound()

            # If there are no more keyboard sounds in the queue, reload them
            if sound_file is None:
                self.keyboard_sound_queue.extend(self.PATH + file for file in self.keyboard_sound)
                sound_file = self.get_next_keyboard_sound()

        # Check if the sound file exists and play it in a separate thread
        self.logger.info(f"Played {sound_file}")
        if sound_file:
            threading.Thread(target=self.play_sound_thread, args=(sound_file,)).start()

    def main(self):
        self.logger.info("Creamy keyboard is loaded!\n")
        self.logger.info("Press 'Esc' to exit.")

        keyboard.on_press(lambda e: self.play_sound(e.name))  # Pass the key name to play_sound

        try:
            keyboard.wait('esc')  # Wait for the 'Esc' key to exit the program
        except KeyboardInterrupt:
            pass
        finally:
            keyboard.unhook_all()  # Unhook all key press events
            pygame.mixer.quit()

if __name__ == "__main__":
    creamy_keyboard = CreamyKeyboard()
    creamy_keyboard.main()
