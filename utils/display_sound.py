import pygame
import multiprocessing
import os
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
os.environ['PYTHONWARNINGS'] = "ignore"

# 효과음 실행 함수
def play_audio(file_path, volume):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.set_volume(volume/10.0)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(3)

def display_sound(scene_num):
    for index_num in range(6):
        tts_path = f'./contents/tts/slow/scene_{scene_num}_{index_num}.wav'
        sound_path = f'./contents/sound/sound_{scene_num}_{index_num}.wav'

        thread_tts = multiprocessing.Process(target=play_audio, args=(tts_path, 20))
        thread_sound = multiprocessing.Process(target=play_audio, args=(sound_path, 2))

        thread_tts.start()
        thread_sound.start()
        
        thread_tts.join()
        thread_sound.join()