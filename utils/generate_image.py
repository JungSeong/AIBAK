from transformers import CLIPTokenizer
from diffusers import StableDiffusionPipeline
import pandas as pd
import os
import torch
import spacy

CSV_FILE_PATH = './contents/text/story_eng.csv'

# CLIP Tokenizer 및 SpaCy 로드
tokenizer = CLIPTokenizer.from_pretrained("openai/clip-vit-base-patch32")
nlp = spacy.load("en_core_web_sm")

def compress_text(prompt, max_tokens=77):
    """긴 텍스트를 키워드 중심으로 압축하여 CLIP의 토큰 제한에 맞춤"""
    doc = nlp(prompt)
    # 키워드 추출: 불용어 및 형용사 제거
    keywords = [token.text for token in doc if token.is_alpha and not token.is_stop]
    # 압축된 키워드 리스트를 77 토큰 내로 제한
    compressed = " ".join(keywords[:max_tokens])
    return compressed

def apply_storybook_template(text):
    """텍스트에 동화책 스타일 템플릿 적용"""
    template = (
        f"{text}, "
        "whimsical cartoon style, soft pastel colors, cute and adorable"
        "proportional body, anatomically correct"                                                                                                                
    )
    return template

# story.csv 파일 불러와서 하나의 scene 에 대한 2개의 prompt 생성
def load_prompts_for_scene(scene_num):
    story = pd.read_csv(CSV_FILE_PATH)
    prompts = story['story'].tolist()[(scene_num-1)*6:scene_num*6]
    prompt1 = ' '.join(prompts[:3])
    prompt2 = ' '.join(prompts[3:])
    scene = [prompt1, prompt2]
    return scene

# 동화 이미지 생성
def generate_image(scene_num):
    print(f"Scene {scene_num} 이미지 생성 시작...")

    # Dreamlike Diffusion 모델 
    print("Dreamlike Diffusion 모델 로드 중...")
    pipe = StableDiffusionPipeline.from_pretrained(
        "dreamlike-art/dreamlike-diffusion-1.0",  
        torch_dtype=torch.float16
    ).to("cuda")

    print("Dreamlike Diffusion 모델 로드 완료")

    negative_prompt = (
        "disfigured, deformed, extra limbs, mutated, low quality, blurry, surreal, unrealistic, unnatural anatomy, "
        "text, watermark, signature, logo, monochrome, grayscale, black and white"
    )

    scenes = load_prompts_for_scene(scene_num)
    # Scene 마다 2개의 이미지 생성
    print("Scene 삽화 생성 시작...")
    for idx, scene in enumerate(scenes):
        # Scene의 구체적 맥락 추가
        scene_prompt = apply_storybook_template(scene)
        # 이미지 생성
        scene_image = pipe(
            scene_prompt, 
            negative_prompt=negative_prompt, 
            num_inference_steps=50
        ).images[0]
        
        # 이미지 저장
        image_path = f'./contents/image/scene_{scene_num}_{idx}.png'
        scene_image.save(image_path)
        print(f"Scene {scene_num} Part {idx} 이미지 저장 완료: {image_path}")

# 커버 이미지 생성
def generate_cover_image(prompts):
    # Dreamlike Diffusion 모델
    print("Dreamlike Diffusion 모델 로드 중...")
    pipe = StableDiffusionPipeline.from_pretrained(
        "dreamlike-art/dreamlike-diffusion-1.0",  
        torch_dtype=torch.float16
    )
    pipe = pipe.to("cuda:0")
    print("Dreamlike Diffusion 모델 로드 완료")

    # 커버 프롬프트 설정
    negative_prompt = (
        "disfigured, deformed, extra limbs, mutated, low quality, blurry, surreal, unrealistic, unnatural anatomy, "
        "text, watermark, signature, logo, monochrome, grayscale, black and white"
    )
    # 커버 이미지 생성
    print("커버 이미지 생성 시작...")
    cover_prompt = apply_storybook_template(prompts)
    cover_image = pipe(cover_prompt, negative_prompt=negative_prompt, num_inference_steps=50).images[0]
    # 커버 이미지 저장
    cover_image_path = './contents/image/cover_img.png'
    cover_image.save(cover_image_path)