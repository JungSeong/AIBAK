import streamlit as st
from PIL import Image
import pandas as pd
import base64

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
    .centered-box { /* 중앙 정렬 */
                display: flex;
                justify-content: center;
                align-items: center;
    }
    .title-box {  /* 생성된 이야기 박스 커스텀 */
            padding: 5px;
            padding-top: 10px;
            padding-bottom: 10px;
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
        padding-right: 30px; 
        padding-left: 30px; 
        background-color: #DEDDFF; 
        color: #986FF9; 
        border: 3px solid #DEDDFF;
        margin-top: 20px;
        margin-bottom: 20px;
    </style>
    """, unsafe_allow_html=True)

    # ----------------- UI Configurations ----------------- #
    image_path = "./contents/ui/page_title.jpg" # 이미지 경로
    image = Image.open(image_path)
    st.image(image)

    # ----------------- Quiz UI Configurations ----------------- #
    quiz_path = "./contents/ui/quiz.jpg" # 이미지 경로
    user_keyword_image = Image.open(quiz_path)
    st.image(user_keyword_image)

    # ----------------- Quiz ----------------- #
    with st.expander(" ", expanded=True):
        # 생성된 동화 내용
        csv_file_path = './contents/text/quiz.csv'
        book_story = pd.read_csv(csv_file_path)
        story_line = ''.join(book_story['quiz'].tolist()[0])
        
        for line in story_line.split(','):
            st.markdown(f"<div class='centered-box'><div class='title-box'>{line}</div></div>", unsafe_allow_html=True)

        # 동화책 읽기 버튼
        bt1, bt2, bt3, bt4 = st.columns(4)
        if bt2.button("이전 페이지"):
            # 다음 페이지 넣기
            st.switch_page("./pages/10_read_book5.py")
        if bt3.button("끝내기"):
            st.switch_page("./pages/12_end_book.py")

if __name__ == '__main__':
    main()