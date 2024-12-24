import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from PIL import Image
from utils import generate_text

def main():
    # 페이지 아이콘 설정
    st.set_page_config(page_title="capstone", page_icon="🦄", layout="centered")

    if 'selected_user_keywords' not in st.session_state:
        st.session_state.selected_user_keywords = []

    # ----------------- CSS custom ----------------- #
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Gaegu&display=swap'); /* 구글 폰트 불러오기 */

    section[data-testid="stSidebar"][aria-expanded="true"]{ /* 사이드바 접기 */
        display: none;
    }
    [data-testid="StyledFullScreenButton"] {    /* 이미지 확대 버튼 감추기 */
        visibility: hidden;
    }
    [data-testid="stExpanderToggleIcon"] {  /* expander 축소 버튼 감추기 */
        visibility: hidden;
    }            
    [data-testid="stBaseButton-secondary"] {    /* 버튼 커스텀 */
        justify-content: center;
        height: auto;
        padding-top: 10px;
        padding-bottom: 10px;
        padding-right: 40px; 
        padding-left: 40px; 
        background-color: #DEDDFF; 
        color: #986FF9; 
        border: 3px solid #DEDDFF;
        margin-top: 10px;
        margin-bottom: 10px;
    }
    .myButton {
      background-color: #4CAF50; /* Green */
      color: white;
      padding: 16px 20px;
      border: none;
      cursor: pointer;
    }
    </style>
    """, unsafe_allow_html=True)

    # ----------------- UI Configurations ----------------- #
    image_path = "./contents/ui/page_title.jpg" # 이미지 경로
    image = Image.open(image_path)
    st.image(image)

    # ----------------- UI Configurations ----------------- #
    user_keyword_path = "./contents/ui/user_keywords.jpg" # 이미지 경로
    user_keyword_image = Image.open(user_keyword_path)
    st.image(user_keyword_image)

    # ------------------ Add Keywords ------------------ #
    if 'keywords_for_user' not in st.session_state:
        st.session_state.keywords_for_user = generate_text.extract_keywords_for_user()

    with st.expander(label=' ', expanded=True):
        # 키워드 추가 선택
        with stylable_container(
            key="orange",
            css_styles="""
            button {
                width: 210px; /* 버튼의 고정 너비 */
                height: spx; /* 높이를 내용에 맞게 조정 */
                background-color: #F8D784;
                color: black;
                border: 3px solid #F8D784;
                margin-bottom: 10px;
            }""",
        ):  
            cols = st.columns(3)
            for i, keyword in enumerate(st.session_state.keywords_for_user):
                if cols[i % 3].button(keyword, keyword):
                    st.session_state.selected_user_keywords.append(keyword)

        # 다음 페이지로 넘어가기
        btn1, btn2, btn3, btn4 = st.columns(4)
        if btn2.button("이전 단계"):
            with open('./contents/text/selected_keywords.txt', "r+", encoding="utf-8") as f:
                # 기존 파일 내용 읽기
                f.seek(0)
                existing_keywords = f.read().strip()
                add_keywords = ", ".join(st.session_state.selected_user_keywords)

                if existing_keywords:
                    updated_keywords = existing_keywords + ", " + add_keywords
                else:
                    updated_keywords = add_keywords
                
                # 파일 내용 수정
                f.seek(0)
                f.write(updated_keywords)
                f.truncate()

            st.switch_page("./pages/2_book_keywords.py")

        if btn3.button("동화 생성"):
            with open('./contents/text/selected_keywords.txt', "r+", encoding="utf-8") as f:
                # 기존 파일 내용 읽기
                f.seek(0)
                existing_keywords = f.read().strip()
                add_keywords = ", ".join(st.session_state.selected_user_keywords)

                if existing_keywords:
                    updated_keywords = existing_keywords + ", " + add_keywords
                else:
                    updated_keywords = add_keywords
                
                # 파일 내용 수정
                f.seek(0)
                f.write(updated_keywords)
                f.truncate()
                
            st.switch_page("./pages/4_generate_book.py")

if __name__ == '__main__':
    main()