import pandas as pd
import csv
import os
import time
import re

from dotenv import load_dotenv
import openai
from langchain_core.runnables import RunnableSequence, RunnablePassthrough
from langchain.chains.llm import LLMChain
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

load_dotenv()

# 책 키워드 추출
def extract_keywords_from_book(story):
    # ChatGPT API 요청 템플릿 생성
    prompt = f"""
    다음은 동화의 내용입니다:
    {story}

    위 내용을 기반으로 가장 중요한 키워드 6개를 추출해 주세요.
    키워드는 짧고 명확하게, 한국어 단어로 작성해야 합니다.
    형식: 키워드1, 키워드2, 키워드3, 키워드4, 키워드5, 키워드6
    """

    # OpenAI 모델 초기화
    llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], model_name='gpt-4o-mini', temperature=0.7)

    # ChatGPT 모델을 사용해 키워드 추출
    response = llm.predict(prompt)

    # 응답에서 키워드 추출 및 정리
    keywords = response.strip().split(", ")
    print("키워드 추출 결과: ", keywords)
    return keywords

def extract_keywords_for_user():
    # ChatGPT API 요청 템플릿 생성
    prompt = f"""
    4~6세 아동이 좋아하는 키워드 6개를 추출해 주세요.
    키워드는 짧고 명확하게, 한국어 단어로 작성해야 합니다.
    형식: 키워드1, 키워드2, 키워드3, 키워드4, 키워드5
    """

    # OpenAI 모델 초기화
    llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], model_name='gpt-4o-mini', temperature=0.7)

    # ChatGPT 모델을 사용해 키워드 추출
    response = llm.predict(prompt)

    # 응답에서 키워드 추출 및 정리
    keywords = response.strip().split(", ")
    print("키워드 추출 결과: ", keywords)
    return keywords

# 동화책 템플릿 생성
def fairytale_template():
    fairytale_template = """
    당신은 어린이가 읽는 한국어 동화를 제작합니다.
    동화는 {keywords}의 모든 배열 요소들을 기반으로 생성됩니다.

    각각의 scene은 6문장으로 구성되며, 다음과 같이 5개의 scene으로 나뉩니다(총 30문장):
        - scene_1: 발단
        - scene_2: 전개
        - scene_3: 위기
        - scene_4: 절정
        - scene_5: 결말 (마지막 문장은 주인공의 교훈을 담은 문장)
            예시) "리나는 앞으로 물건을 조심히 다뤄야겠다고 생각했어요.", "민지는 친구를 소중히 대해야겠다고 생각했답니다."
    
    ### 작성 규칙 (아래 3가지의 규칙을 반드시 지켜야 합니다.)
    1. 주인공은 사람으로 설정하고, 모든 등장인물은 고유명사 형식의 이름으로 설정합니다. 예시) 리나, 에밀리, 민주, 현우, 준환, 나라
    2. 인물의 대사는 작은따옴표(' ')로 구분해야 합니다. 예시) '이 열쇠가 무엇인지 알까?' 왕자님은 궁금해했어요.
    3. 동화의 내용은 30문장이 유기적으로 이어져야 합니다.

    1~30번 문장은 위와 같은 규칙으로 작성된 한국어 동화입니다.
    총 30문장을 출력해야 합니다. 

    ### 출력 형식 (아래의 출력 형식을 참고만 하십시오)
    scene_1
    sentence_1: 옛날 옛적에 강아지인 뭉치가 풀밭에 누워있었어요.
    scene_sentence_no: 1/6, sentence_no: 1

    sentence_2: 그 날은 날씨가 정말 좋아서 새들도 즐겁게 노래를 불렀어요.
    scene_sentence_no: 2/6, sentence_no: 2

    sentence_3: 뭉치는 새들의 노랫소리에 따라 신나게 꼬리를 흔들었어요.
    scene_sentence_no: 3/6, sentence_no: 3

    ...  

    scene_5  
    sentence_30: 리나는 앞으로 물건을 조심히 다뤄야겠다고 생각했답니다.  
    scene_sentence_no: 6/6, sentence_no: 30

    """
    return fairytale_template

# 한국어 -> 영어 동화 번역
def translate_story(story_kor):
    csv_data_eng = []
    translation_prompt = PromptTemplate(
        template=
        """
        Translate the following text to English: {text}
        ### 출력 형식 (아래의 출력 형식을 참고만 하십시오)
        scene_1
        sentence_1: 옛날 옛적에 강아지인 뭉치가 풀밭에 누워있었어요.
        scene_sentence_no: 1/6, sentence_no: 1

        sentence_2: 그 날은 날씨가 정말 좋아서 새들도 즐겁게 노래를 불렀어요.
        scene_sentence_no: 2/6, sentence_no: 2

        sentence_3: 뭉치는 새들의 노랫소리에 따라 신나게 꼬리를 흔들었어요.
        scene_sentence_no: 3/6, sentence_no: 3

        ...  

        scene_5  
        sentence_30: 리나는 앞으로 물건을 조심히 다뤄야겠다고 생각했답니다.  
        scene_sentence_no: 6/6, sentence_no: 30

        """,
        input_variables=["text"]
    )
    llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], model_name='gpt-4o-mini', temperature=0.7)
    llm_chain = translation_prompt | llm | StrOutputParser()
    story_eng = llm_chain.invoke(input=f'{story_kor}')

    lines = story_eng.split('\n')
    csv_data_eng = []
    current_scene = None
    current_scene_sentence_no = 0
    
    # story.csv 에 동화 내용 저장
    for line in lines:
        if line.startswith("scene_sentence_no"):
            pass
        # scene 정보 추출
        elif line.startswith("scene_"):
            current_scene_sentence_no = 0
            current_scene = line.strip() # strip() : 문자열 내에서 원하는 문자열 또는 공백 제거
        # sentence 정보 추출
        elif line.startswith("sentence_"):
            current_scene_sentence_no += 1
            sentence = line.split(":")[1].strip()
            csv_data_eng.append([current_scene, current_scene_sentence_no, sentence])

    # 영어 동화 저장 (story_eng.csv)
    with open(os.path.join('./contents/text', 'story_eng.csv'), 'w', newline='', encoding='utf-8') as csvfile_eng:
        csv_writer_eng = csv.writer(csvfile_eng)
        csv_writer_eng.writerow(['scene_no', 'scene_sentence_no', 'story'])
        csv_writer_eng.writerows(csv_data_eng)
    print(f"영어 동화가 './contents/text/story_eng.csv' 파일에 저장되었습니다.")

    return 

def sound_prompt_template(input_text):
    template = f"""
    Enhance this prompt for sound effects: {input_text}
    너는 동화책으로부터 AudioLDM2에게 넣을 프롬프트를 생성하는 AI야.
    다음과 같은 규칙을 통해서 동화책 내용을 영어로 반환해줘.
    1. 반드시 동화책 한 문장을 효과음을 생성하기에 적합한 프롬프트 한 문장으로 변환해줘.
    2. 각 문장에따라 Output을 내주면 돼. 즉 Output:<출력내용1>\nOutput:<출력내용2>.. 이런 식으로 만들어(앞에 prompt 붙이지말고 바로 Output 내줘!).
    3. 문장에서 소리가 나는 물체에 집중해서 해당 물체의 소리를 출력해주고, 만약 실제로 존재하는 소리가 없으면 no sound로 출력해줘.
    4. 소리가 나는 물체의 대상이 바람처럼 추상적이라면, wind blowing in an open field 처럼 뒤에 open field를 붙여서 출력해줘.
    5. 여기에 대해 출력 형태는 Output:<출력내용> 으로 매 문장마다 출력해줘. 그리고 쌍따옴표같은건 절대 쓰지마. 다시한번 말할게. 따옴표 쓰지 마.
    6. 4단어 안으로 표현해줘. 
    7. 실제로 소리가 나지 않는거면 no sound 처리 해줘. 현실에서 들을 수 있는 소리여야만 출력해줘.
    8. 사람의 목소리가 나와야 하는것도 no sound 처리 해줘. 특정 발음 없어야 하는 것만 출력해야해. 예를들어 voice 같은건 안되겠지.
    9. 이 모든걸 엄격하게 처리해줘. 조금이라도 애매하면 전부 no sound 처리해
    10. 스토리가 30줄이니 사운드 프롬프트도 30줄이 나와야해.
    """
    return template

def generate_sound_prompt_line(input_texts):
    # 여러 문장을 한 번에 처리하기 위한 템플릿 생성
    combined_input = "\n".join(f"Input:{text}" for text in input_texts)
    prompt = sound_prompt_template(combined_input)
    
    llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], model_name='gpt-4o-mini', temperature=0.7)
    
    # LLM에서 한 번에 예측을 받아옴
    response_raw = llm.predict(prompt)
    
    # "Output:" 기준으로 결과 분리
    responses = response_raw.strip().split("Output:")
    responses = [response.strip() for response in responses if response.strip()]  # 빈 문자열 제거
    
    return responses  # 각 문장에 해당하는 출력 리스트 반환

def generate_sound_prompt():
    csv_path = './contents/text/story_eng.csv'
    df = pd.read_csv(csv_path, encoding='utf-8')
    story_data = df['story'].tolist()  # 'story' 컬럼만 리스트로 변환
    
    # 모든 문장을 한 번에 처리
    sound_prompts = generate_sound_prompt_line(story_data)
    
    # 새로운 DataFrame으로 결과 저장
    output_df = pd.DataFrame({'prompt': sound_prompts})
    output_csv_path = './contents/text/prompt_sound.csv'
    output_df.to_csv(output_csv_path, index=False, encoding='utf-8')

    print(f"변환된 프롬프트가 '{output_csv_path}'에 저장되었습니다.")

def quiz_template(input_text):
    template = f"""
    동화책 내용 : {input_text}
    너는 동화책의 내용을 보고 아이들에게 문제를 내는 AI야. 
    아이들에게 따로 정답이 없는 생각해볼만한 질문을 두개를 만들어줘. 
    문장 두개만 출력해주고 반드시 문장 두개만 출력해야해! 
    '문장1,문장2' 식으로 출력해줘
    """
    return template

def generate_quiz():
    csv_path = './contents/text/story_eng.csv'
    df = pd.read_csv(csv_path, encoding='utf-8')
    story_data = df['story'].tolist()

    # 동화 전체 내용을 하나로 합침
    full_story_text = " ".join(story_data)

    # 전체 텍스트를 기반으로 퀴즈를 생성
    prompt = quiz_template(full_story_text)  # input_text는 동화 전체 내용
    llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], model_name='gpt-4o-mini', temperature=0.7)
    response_raw = llm.predict(prompt)
    response_raw = response_raw.strip()
    print("response_raw: ", response_raw)
    if "Output:" in response_raw:
        response_raw = response_raw.split("Output:")[1].strip()  # "Output:" 이후 텍스트만 추출
    
    # 퀴즈 결과를 DataFrame에 저장
    output_df = pd.DataFrame({'quiz': [response_raw]})  # 전체 결과를 하나의 row로 저장
    output_csv_path = './contents/text/quiz.csv'
    output_df.to_csv(output_csv_path, index=False, encoding='utf-8')

    print(f"퀴즈가 '{output_csv_path}'에 저장되었습니다.")

    return response_raw  # 퀴즈 2개를 생성해서 반환

# 한국어 동화 생성
def generate_story(keywords):
    prompt = PromptTemplate(template = fairytale_template(), input_variables=["input_text"])
    # temperature : 문장 생성의 다양성
    llm = ChatOpenAI(openai_api_key=os.environ["OPENAI_API_KEY"], model_name='gpt-4o-mini', temperature=0.7)
    llm_chain = prompt | llm | StrOutputParser()
    story = llm_chain.invoke(input=f'{keywords}')
 
    lines = story.split('\n')
    csv_data_kor = []
    current_scene = None
    current_scene_sentence_no = 0
    
    # story.csv 에 동화 내용 저장
    for line in lines:
        if line.startswith("scene_sentence_no"):
            pass
        # scene 정보 추출
        elif line.startswith("scene_"):
            current_scene_sentence_no = 0
            current_scene = line.strip() # strip() : 문자열 내에서 원하는 문자열 또는 공백 제거
        # sentence 정보 추출
        elif line.startswith("sentence_"):
            current_scene_sentence_no += 1
            sentence = line.split(":")[1].strip()         
            csv_data_kor.append([current_scene, current_scene_sentence_no, sentence])
    
    # 한글 동화 저장 (story.csv)
    with open(os.path.join('./contents/text', 'story.csv'), 'w', newline='', encoding='utf-8') as csvfile_kor:
        csv_writer_kor = csv.writer(csvfile_kor)
        csv_writer_kor.writerow(['scene_no', 'scene_sentence_no', 'story'])
        csv_writer_kor.writerows(csv_data_kor)
    print(f"한국어 동화가 './contents/text/story.csv' 파일에 저장되었습니다.")

    # 한글 및 영어 동화 리스트 생성
    story_kor = ' '.join([row[2].strip('"') for row in csv_data_kor])
    # 영어 동화 번역
    translate_story(story_kor)

    # 동화 제목 생성
    book_title = llm.invoke(f'{story_kor}\n'
                      '''
                      위의 동화에 알맞는 한국어 동화 제목을 제작해줘.
                      동화 제목은 간결하고 명확하게 작성해줘.
                      배경에 대한 묘사가 있을 경우 풍경에 빗대어 제목을 작성해줘.
                      서브 주인공이 있을 경우 서브 주인공의 이름도 제목에 넣어줘.
                      문자를 제외한 "/"와 같은 특수 문자는 사용하지 않아야해.
                      제작 규칙 및 형식은 아래의 예시와 같아.
                      예시) 
                      용감한 강아지 메시의 모험
                      다른 말은 출력되면 안돼.
                      '''
                      )
    book_title = book_title.content.replace('"', '')

    # 파일 경로 지정
    book_title_path = "./contents/text/cover_title.txt"

    # 파일에 저장
    with open(book_title_path, "w", encoding="utf-8") as file:
        file.write(book_title)
    print(f"동화 제목이 '{book_title_path}' 파일에 저장되었습니다.")

    # 커버 이미지 생성을 위한 동화 내용 요약
    cover_text = llm.invoke(f'{story_kor}\n'
                '''
                위의 동화로 동화책 삽화를 만들기 위해 사용할 수 있도록 동화 내용을 요약해줘.
                영어 프롬포트로 만들어줘.
                
                프롬포트 제작 규칙은 아래와 같아.
                동화 내용을 20개 단어 이하의 1개의 문장으로 요약해줘.
                '''
                )
    cover_text = cover_text.content

    # 효과음 프롬프트 생성
    generate_sound_prompt()

    return cover_text