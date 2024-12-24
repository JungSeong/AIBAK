import streamlit as st
from streamlit_extras.stylable_container import stylable_container
from PIL import Image
from utils import generate_text

import psycopg2

def main():
    # 페이지 아이콘 설정
    st.set_page_config(page_title="capstone", page_icon="🦄", layout="centered")

    # barcode = st.session_state['barcode']
    barcode = 9791172175856
    if 'selected_book_keywords' not in st.session_state:
        st.session_state.selected_book_keywords = []

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
    .title-box {  /* 책 제목 박스 커스텀 */
        padding: 15px;
        border-radius: 10px;
        background-color: #FCD5B5;
        color: #333333;
        font-size: 20px;
        font-weight: 400;
        text-align: center;
        font-family: "Gaegu", sans-serif;
        margin-top: 10px;
        margin-bottom: 30px;
    }
    .key1-button { background-color: #FFB6C1; color: white; }
    </style>
    """, unsafe_allow_html=True)

    # ----------------- UI Configurations ----------------- #
    image_path = "./contents/ui/page_title.jpg" # 이미지 경로
    image = Image.open(image_path)
    st.image(image)

    # ----------------- PostgreSQL ----------------- #
    if 'book_data' not in st.session_state:
        try:
            # PostgreSQL 데이터베이스 연결
            connection = psycopg2.connect(
                dbname="postgres",  # 데이터베이스 이름
                user="postgres",    # PostgreSQL 사용자 이름
                password="asdf1234",  # PostgreSQL 비밀번호
                host="localhost",   # 호스트 (기본값: localhost)
                port="5432"         # 포트 (기본값: 5432)
            )
            cursor = connection.cursor()

            # SQL 쿼리 실행
            query = "SELECT title, author, summary, image_path FROM book WHERE id = %s;"
            cursor.execute(query, (barcode,))

            # 결과 가져오기
            result = cursor.fetchone()

            if result:
                title, author, summary, book_image_path = result
                print(f"책 제목: {title}, 저자: {author}, 요약: {summary}, 이미지 경로: {book_image_path}")
                st.session_state.book_data = {
                    'title': title,
                    'author': author,
                    'summary': summary,
                    'image_path': book_image_path
                }

            else:
                print("해당 바코드 번호에 해당하는 책이 없습니다.")

        except psycopg2.Error as e:
            print(f"데이터베이스 연결 또는 쿼리 실행 중 오류가 발생했습니다: {e}")

        finally:
            # 데이터베이스 연결 닫기
            if connection:
                cursor.close()
                connection.close()
        
        # 키워드 추출
        st.session_state.book_data['keywords'] = generate_text.extract_keywords_from_book(summary)

    # ----------------- Keywords ----------------- #
    # 화면 레이아웃
    book, keyword = st.columns([2, 3])

    # 책 표지 및 제목
    with book:
        with st.expander(label=' ', expanded=True):
            # 책 표지
            book_image_path = st.session_state.book_data['image_path']
            book_image = Image.open(book_image_path)
            st.image(book_image)
            
            # 책 제목
            title = st.session_state.book_data['title']
            st.markdown(f"<div class='title-box'>{title}</div>", unsafe_allow_html=True)
    
    # 책 내용에서 추출한 키워드
    keywords_from_db = st.session_state.book_data['keywords']
    with keyword:
        with st.expander(label=' ', expanded=True):
            # 원하는 단어를 골라주세요 이미지
            book_keywords_path = "./contents/ui/book_keywords.jpg" # 이미지 경로
            book_keywords_image = Image.open(book_keywords_path)
            st.image(book_keywords_image)

            # 키워드 선택
            with stylable_container(
                key="skyblue",
                css_styles="""
                button {
                    width: 180px; /* 버튼의 고정 너비 */
                    height: 60px; /* 높이를 내용에 맞게 조정 */
                    background-color: #DCE6F2;
                    color: black;
                    border: 3px solid #DCE6F2;
                    margin-top: 5px;
                    margin-bottom: 5px;
                    font-size: 10px;
                }""",
            ):  
                cols = st.columns(2)
                for i, keyword in enumerate(keywords_from_db):
                    if cols[i % 2].button(keyword, keyword):
                        st.session_state.selected_book_keywords.append(keyword)
                        print("selected_book_keywords: ", st.session_state.selected_book_keywords)

            # 다음 페이지로 넘어가기
            btn1, btn2 = st.columns(2)
            if btn1.button("단어 추가하기"):
                # 키워드를 .txt 파일에 저장
                with open("./contents/text/selected_keywords.txt", "w", encoding="utf-8") as f:
                    f.write(", ".join(st.session_state.selected_book_keywords))  # 키워드를 쉼표로 구분하여 한 줄로 저장
                st.switch_page("./pages/3_add_keywords.py")

            if btn2.button("동화책 생성"):
                # 키워드를 .txt 파일에 저장
                with open("./contents/text/selected_keywords.txt", "w", encoding="utf-8") as f:
                    f.write(", ".join(st.session_state.selected_book_keywords))  # 키워드를 쉼표로 구분하여 한 줄로 저장
                st.switch_page("./pages/4_generate_book.py")

if __name__ == '__main__':
    main()