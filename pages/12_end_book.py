import streamlit as st
from PIL import Image

# 페이지 전환 함수
def navigate_to(page):
    st.session_state.page = page

def main():
    # 페이지 아이콘 설정
    st.set_page_config(page_title="capstone", page_icon="🦄", layout="centered")

    # ----------------- CSS custom ----------------- #
    st.markdown("""
    <style>
    section[data-testid="stSidebar"][aria-expanded="true"]{ /* 사이드바 접기 */
        display: none;
    }
    [data-testid="StyledFullScreenButton"] {    /* 이미지 확대 버튼 감추기 */
        visibility: hidden;
    }            
    [data-testid="stBaseButton-secondary"] {    /* 시작 버튼 커스텀 */
        justify-content: center;
        height: auto;
        padding-top: 20px;
        padding-bottom: 20px;
        padding-right: 70px; 
        padding-left: 70px; 
        background-color: #DDD9C3; 
        color: #A9905F; 
        border: 3px solid #DDD9C3; 
    }
    </style>
    """, unsafe_allow_html=True)

    # ----------------- UI Configurations ----------------- #
    # 시작화면 이미지
    image_path = "./contents/ui/title.jpg" # 이미지 경로
    image = Image.open(image_path)
    st.image(image)

    # 시작화면 버튼
    bt_left, bt_middle, bt_right = st.columns([1,2,1])
    if bt_middle.button("시작 화면으로 돌아가기"):
        # 다음 페이지 넣기
        st.switch_page("./web.py")

if __name__ == '__main__':
    main()