import streamlit as st
from PIL import Image
import base64

def main():
    # 페이지 아이콘 설정
    st.set_page_config(page_title="capstone", page_icon="🦄", layout="centered")

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
    .centered-box { /* 중앙 정렬 */
                display: flex;
                justify-content: center;
                align-items: center;
    }
    .title-box {  /* 생성된 책 제목 박스 커스텀 */
            padding: 5px;
            padding-right: 70px; 
            padding-left: 70px; 
            border-radius: 10px;
            background-color: #FFE699;
            color: #333333;
            font-size: 32px;
            font-weight: 400;
            text-align: center;
            font-family: "Gaegu", sans-serif;
            margin-top: 30px;
            margin-bottom: 30px;
        }
    [data-testid="stBaseButton-secondary"] {    /* 시작 버튼 커스텀 */
            justify-content: center;
            height: auto;
            padding-top: 20px;
            padding-bottom: 20px;
            padding-right: 50px; 
            padding-left: 50px; 
            background-color: #FFBBD5; 
            color: #D85081; 
            border: 3px solid #FFBBD5;
            margin-bottom: 20px;
    }       
    </style>
    """, unsafe_allow_html=True)

    # ----------------- UI Configurations ----------------- #
    image_path = "./contents/ui/page_title.jpg" # 이미지 경로
    image = Image.open(image_path)
    st.image(image)

    # ----------------- Read Book ----------------- #
    with st.expander(" ", expanded=True):
        # 생성된 동화 표지
        cover_path = './contents/image/cover_img.png'

        with open(cover_path, "rb") as image_file:
            cover_image = base64.b64encode(image_file.read()).decode()
        st.markdown(
            f"""
            <div class="centered-box">
                <img src="data:image/jpeg;base64,{cover_image}" alt="Book Cover" style="width:350px; height:auto;">
            </div>
            """,
            unsafe_allow_html=True
        )

        # 생성된 동화 제목
        book_title_path = "./contents/text/cover_title.txt"
        with open(book_title_path, "r", encoding="utf-8") as file:
            book_title = file.read().strip()  # 파일 내용을 읽고 양 끝 공백 제거
        st.markdown(f"<div class='centered-box'><div class='title-box'>{book_title}</div></div>", unsafe_allow_html=True)

        # 동화책 읽기 버튼
        bt_left, bt_middle, bt_right = st.columns(3)
        if bt_middle.button("동화책 읽기 !"):
            # 다음 페이지 넣기
            st.switch_page("./pages/6_read_book1.py")

if __name__ == '__main__':
    main()