import streamlit as st

import cv2
from PIL import Image
import pyzbar.pyzbar as pyzbar
from datetime import datetime
import numpy as np
import time

def main():
    # 페이지 아이콘 설정
    st.set_page_config(page_title="capstone", page_icon="🦄", layout="centered")

    # ----------------- CSS custom ----------------- #
    st.markdown("""
    <style>
    section[data-testid="stSidebar"][aria-expanded="true"]{
        display: none;
    }
    [data-testid="StyledFullScreenButton"] {
        visibility: hidden;
    }            
    </style>
    """, unsafe_allow_html=True)

    # ---------------- UI Configurations ---------------- #
    image_path = "./contents/ui/scan_barcode.jpg"
    image = Image.open(image_path)
    st.image(image)

    # ------------ Camera & Image Processing ------------ #
    # 카메라 실행
    img_file_buffer = st.camera_input(" ")

    # 이미지 처리 (바코드 스캔)
    if img_file_buffer is not None:
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        decoded_objects = pyzbar.decode(cv2_img)
        if decoded_objects:
            # 첫 번째로 인식된 바코드만 처리
            code = decoded_objects[0]
            # 바코드 데이터 디코딩
            barcode = code.data.decode('utf-8')
            print("인식 성공 : ", barcode)
            
            # 현재 시간으로 파일 저장
            current_time = datetime.now()
            filename = current_time.isoformat().replace(":", "_")
            cv2.imwrite('./scan/'+filename + '.png', cv2_img)

            st.session_state['barcode'] = barcode
            # 다음 페이지로 이동
            st.switch_page("./pages/2_book_keywords.py")

if __name__ == '__main__':
    main()