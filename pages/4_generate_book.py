import streamlit as st
from PIL import Image
import base64
import time

from utils import generate_text
from utils import generate_image
from utils import generate_sound

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
    .centered-gif {
        display: flex;
        justify-content: center;
        margin-bottom: 45px;
    }                
    .custom-font {
        font-family: "Gaegu", sans-serif;
        font-size: 24px;                 
        color: #333333;                   
    }
    </style>
    """, unsafe_allow_html=True)
    
    # ----------------- UI Configurations ----------------- #
    image_path = "./contents/ui/page_title.jpg"
    image = Image.open(image_path)
    st.image(image)

    # ------------------ Generate Book ------------------ #
    with st.status(' ', expanded=True) as status:
        # Loading gif
        gif_path = open("./contents/ui/loading.gif", "rb")
        contents = gif_path.read()
        gif = base64.b64encode(contents).decode("utf-8")
        gif_path.close()
        st.markdown(f"""<div class="centered-gif"><img src="data:image/gif;base64,{gif}" alt="loading gif" class="custom-font"></div>""",unsafe_allow_html=True)
        
        # Load keywords from DB
        with open('./contents/text/selected_keywords.txt', "r", encoding="utf-8") as f:
            keywords_from_db = f.read().strip().split(", ")
            print("keywords_from_db: ", keywords_from_db)

        # Generate full story
        # start = time.time()
        story = generate_text.generate_story(keywords_from_db)
        print("story: ", story)
        st.write('<p class="custom-font">📚 이야기가 완성 되었어요 !</p>', unsafe_allow_html=True)
        # print("generate story time : ", time.time()-start)
        # print("------------------------done------------------------")

        # generate book cover & illustration (scene 1)
        # start = time.time()
        generate_image.generate_cover_image(story)
        generate_image.generate_image(1)
        st.write('<p class="custom-font">🖼️ 이미지가 완성 되었어요 !</p>', unsafe_allow_html=True)
        # print("generate image time : ", time.time()-start)
        
        # generate sound (scene 1)
        # start = time.time()
        generate_sound.generate_sound(1)
        st.write('<p class="custom-font">🔉 효과음이 완성 되었어요 !</p>', unsafe_allow_html=True)
        # print("generate sound time : ", time.time()-start)

        # generate TTS (scene 1)
        # start = time.time()
        generate_sound.generate_tts(1)
        st.write('<p class="custom-font">🗣️ TTS 기능이 완성 되었어요 !</p>', unsafe_allow_html=True)
        # print("generate tts time : ", time.time()-start)

        # 다음 페이지
        st.switch_page("./pages/5_read_book.py")

if __name__ == '__main__':
    main()