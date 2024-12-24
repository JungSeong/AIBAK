import streamlit as st
from PIL import Image
import pandas as pd
import os

import multiprocessing

from utils import generate_image
from utils import generate_sound
from utils import display_sound

def main():
    # 페이지 아이콘 설정
    st.set_page_config(page_title="capstone", page_icon="🦄", layout="centered")

    # ----------------- CSS custom ----------------- #
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gamja+Flower&display=swap'); /* 구글 폰트 불러오기 */
    section[data-testid="stSidebar"][aria-expanded="true"]{ /* 사이드바 접기 */
        display: none;
    }
    [data-testid="StyledFullScreenButton"] {    /* 이미지 확대 버튼 감추기 */
        visibility: hidden;
    }
    [data-testid="stExpanderToggleIcon"] {  /* expander 축소 버튼 감추기 */
            visibility: hidden;
    }
    .title-box {  /* 생성된 이야기 박스 커스텀 */
            padding: 5px;
            padding-top: 15px;
            padding-bottom: 15px;
            padding-right: 30px; 
            padding-left: 30px; 
            border-radius: 10px;
            background-color: #DDF4FB;
            color: #333333;
            font-size: 20px;
            font-weight: 400;
            text-align : justify;
            font-family: "Gamja Flower", sans-serif;
            margin-bottom: 30px;
        }
    [data-testid="stBaseButton-secondary"] {    /* 버튼 커스텀 */
            justify-content: center;
            height: auto;
            padding-top: 15px;
            padding-bottom: 15px;
            padding-right: 35px; 
            padding-left: 35px; 
            background-color: #FFBBD5; 
            color: #D85081; 
            border: 3px solid #FFBBD5;
            margin-top: 20px;
            margin-bottom: 20px;
    }       
    </style>
    """, unsafe_allow_html=True)

    # ----------------- UI Configurations ----------------- #
    image_path = "./contents/ui/page_title.jpg" # 이미지 경로
    image = Image.open(image_path)
    st.image(image)

    # ----------------- Read Book ----------------- # 
    book_image7_path = './contents/image/scene_4_0.png'
    book_image8_path = './contents/image/scene_4_1.png'
    
    if not os.path.exists(book_image8_path):
        generate_image.generate_image(4)

    with st.expander(" ", expanded=True):
        image7, image8 = st.columns(2)
        # 생성된 동화 삽화
        book_image7 = Image.open(book_image7_path)
        image7.image(book_image7)
        book_image8 = Image.open(book_image8_path)
        image8.image(book_image8)

        # 생성된 동화 내용
        csv_file_path = './contents/text/story.csv'
        book_story = pd.read_csv(csv_file_path)
        story_line = ' '.join(book_story['story'].tolist()[18:24])
        st.markdown(f"<div class='centered-box'><div class='title-box'>{story_line}</div></div>", unsafe_allow_html=True)
        
        # 효과음, TTS 재생
        # 다음 Scene 이미지, 효과음, TTS 생성
        if not os.path.exists('./contents/image/scene_5_1.png'):
            # 효과음, TTS 재생
            # 다음 페이지 생성하기 (병렬처리)
            thread_generate_image = multiprocessing.Process(target=generate_image.generate_image, args=(5,))
            thread_generate_sound = multiprocessing.Process(target=generate_sound.generate_sound, args=(5,))
            thread_generate_tts = multiprocessing.Process(target=generate_sound.generate_tts, args=(5,))
    
            thread_generate_image.start()
            thread_generate_sound.start()
            thread_generate_tts.start()
    
            display_sound.display_sound(4)
    
            thread_generate_image.join()
            thread_generate_sound.join()
            thread_generate_tts.join()

        # 동화책 읽기 버튼
        bt1, bt2, bt3, bt4 = st.columns(4)
        if bt2.button("이전 페이지"):
            # 다음 페이지 넣기
            st.switch_page("./pages/8_read_book3.py")
        if bt3.button("다음 페이지"):
            st.switch_page("./pages/10_read_book5.py")

if __name__ == "__main__":
    main()