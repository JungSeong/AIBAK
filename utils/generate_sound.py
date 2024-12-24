import os
import csv
import torch
import scipy.io.wavfile
import pandas as pd
import numpy as np
from scipy.io import wavfile
import wave
from diffusers import AudioLDM2Pipeline

from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs
from pydub import AudioSegment

def load_sound_prompts(scene_num):
    csv_file_path = './contents/text/prompt_sound.csv'
    story = pd.read_csv(csv_file_path)
    sound_prompts = story['prompt'].tolist()[(scene_num-1)*6:scene_num*6]

    return sound_prompts

def load_story(scene_num):
    csv_file_path = './contents/text/story.csv'
    story = pd.read_csv(csv_file_path)
    prompts = story['story'].tolist()[(scene_num-1)*6:scene_num*6]

    return prompts

def generate_sound(scene_num):
    # AudioLDM2Pipeline 모델
    repo_id = "cvssp/audioldm2-large"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print("AudioLDM2Pipeline 초기화 중...")
    pipe = AudioLDM2Pipeline.from_pretrained(repo_id, torch_dtype=torch.float16).to(device)
    print("AudioLDM2Pipeline이 준비되었습니다...")

    # 저장 디렉토리 생성
    output_directory="./contents/sound"
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    # CSV 파일 처리
    scenes_eng = load_sound_prompts(scene_num)

    # Scene 마다 6개의 효과음 생성
    for i, scene in enumerate(scenes_eng):
        print(f"프롬프트 처리 중 : scene{scene_num}_{i}")
        # 오디오 파일 경로
        audio_file_path = os.path.join(output_directory, f"sound_{scene_num}_{i}.wav")

        if scene == "no sound":  # 효과음이 없는 경우
            silence = np.zeros((16000 * 5,), dtype=np.int16)  # 5초 무음, 16kHz 샘플링
            scipy.io.wavfile.write(audio_file_path, rate=16000, data=silence)
            print(f"무음 오디오 저장 완료: {audio_file_path}")
        else:
            # AudioLDM2로 오디오 생성
            audio = pipe(
                scene,
                num_inference_steps=200,
                audio_length_in_s=3.0,
            ).audios
            # 오디오 파일 저장
            scipy.io.wavfile.write(audio_file_path, rate=16000, data=audio[0])
            print(f"오디오 저장 완료: {audio_file_path}")

# TTS 생성 (Lily 성우의 목소리)
def generate_tts(scene_num):
    ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
    client = ElevenLabs(
        api_key=ELEVENLABS_API_KEY,
    )
    # scene 불러오기
    scene_kor = load_story(scene_num)

    for i, scene in enumerate(scene_kor):
        response = client.text_to_speech.convert(
        voice_id="pFZP5JQG7iQjIQuC4Bku", 
        # output_format="mp3_22050_32",
        output_format="pcm_16000",
        text = scene,
        model_id="eleven_turbo_v2_5",
        voice_settings=VoiceSettings(
            stability=0.6,
            similarity_boost=0.6,
            style=0.7,
            use_speaker_boost=True,
        ),
        )
        # slowed_tts = tts  # 길이가 짧으면 속도 조정 안 함
        pcm_path = f"./contents/tts/original/scene_{scene_num}_{i}.pcm"
        with open(pcm_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)
         # PCM 데이터를 RIFF WAV로 변환
        wav_path = f"./contents/tts/original/scene_{scene_num}_{i}.wav"
        with open(pcm_path, "rb") as pcm_file:
            pcm_data = pcm_file.read()

        with wave.open(wav_path, "wb") as wav_file:
            wav_file.setnchannels(1)  # 모노
            wav_file.setsampwidth(2)  # 샘플 폭 2바이트 (16비트)
            wav_file.setframerate(16000)  # 샘플링 속도 16kHz
            wav_file.writeframes(pcm_data)

        # WAV 파일을 읽고 처리
        rate, data = wavfile.read(wav_path)
        # 오디오 길이가 충분히 긴 경우 속도 조정 (샘플링 간격 증가로 속도 느리게)
        if len(data) > rate:  # 약 1초 이상일 경우
            slowed_data = data[::2]  # 데이터 샘플링 속도를 절반으로 줄임
            new_rate = rate // 2
        else:
            slowed_data = data  # 길이가 짧으면 속도 조정 안 함
            new_rate = rate

        # 처리된 WAV 파일 저장
        slowed_tts_path = f"./contents/tts/slow/scene_{scene_num}_{i}.wav"
        wavfile.write(slowed_tts_path, new_rate, slowed_data)