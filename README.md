# 🦄 캡스톤 디자인 - AI 기반 동화책 생성 키오스크 서비스
---
### 1-1. 프로젝트 소개 :
 본 서비스는 아이들의 문해력 향상 및 독서에 대한 흥미 유발을 이끌기 위한 목적으로 제작된 **생성형 AI를 이용한 동화책 키오스크 서비스**이다. 기존의 AI 스토리 교실과 달리 AIBAK은 **이미지, 효과음, TTS 기능**이 모두 포함된 인터렉티브 동화책을 생성한다. 또한 동화책의 끝에 **답이 정해지지 않은 질문을 생성** 하여 해당 동화책에 대해 아동이 한번 더 생각해보게 함으로써 아동의 사고력 증진울 더욱 이끌어 내었다는 특징을 가진다.

### 1-2. 프로젝트 선정 이유 :
 오늘날 아동의 독서 습관과 방식은 급격히 변화되고 있다. 디지털 콘텐츠와 미디어를 통해 정보를 접하는 비중이 커지며, 종이책을 읽는 전통적인 독서 방식은 아동들의 관심에서 멀어지고 있는 실정이다. 이러한 변화는 아이들의 문해력 저하로 이어질 수 있다는 우려가 생기고 있다. 이를 해결하기 위해 독서 활동 강화, 어휘 교육 강화, 디지털 매체 활용 습관 개선, 토론 및 글쓰기 능력 강화 등 다양한 방안이 논의되었다. 현실적으로 디지털 매체가 우리의 일상이 된 지금, 디지털 매체를 완전히 배제한다는 방안은 불가능하다. 오히려 디지털 매체를 적극적으로 활용하면서 아이들에게 친숙하고 효과적인 학습 환경을 제공하여 아이들의 독서에 대한 흥미를 고취하고자 한다. 이와 같은 배경과 필요성을 바탕으로 미디어 기반 아동 독서 프로그램인 ‘생성형 AI를 활용한 도서 어시스턴트 키오스크(AIBAK)’을 서비스를 설계하고 구현한다.

### 2-1. 프로젝트 기간 :
**24.9.1 ~ 24.12.20 (4개월)**

### 2-2. 개발 진행 일정 (WBS) :
![WBS](https://github.com/user-attachments/assets/f76eb2ff-0ac2-4381-b2ea-76ff7dad24d2)

### 3-1. 시스템 아키텍처 :
![아키텍처](https://github.com/user-attachments/assets/9c397877-91da-4df9-abf4-2931b1f1231f)

### 3-2. 기능 명세서 :
| **대분류**       | **중분류**        | **소분류**         | **기능 상세**                                                  | **입력 데이터 (파일명)**                      | **출력 데이터 (파일명)**                       |
|------------------|-------------------|---------------------|------------------------------------------------------------------|--------------------------------------------------|---------------------------------------------------|
| **생성형 AI 모델** | 텍스트 생성        | 키워드 생성         | 동화책의 줄거리를 기반으로 키워드 생성                           | TEXT                                             | TEXT                                              |
|                  | 텍스트 생성        | 동화 내용 생성       | 입력된 키워드를 기반으로 동화 내용 생성                          | TEXT (`selected_keywords.txt`)                  | TEXT (`story.csv`)                                |
|                  | 텍스트 생성        | 동화 제목 생성       | 생성된 동화 내용을 기반으로 동화 제목 생성                       | TEXT (`story.csv`)                              | TEXT (`cover_title.txt`)                          |
|                  | 텍스트 생성        | 효과음 입력 텍스트 생성 | 생성된 동화의 각 상황에 해당하는 효과음 생성을 위한 텍스트 제작     | TEXT (`story_eng.csv`)                          | TEXT (`prompt_sound.csv`)                         |
|                  | 텍스트 생성        | 퀴즈 생성           | 생성된 동화에 대한 질문 제작                                     | TEXT (`story_eng.csv`)                          | TEXT (`quiz.csv`)                                 |
|                  | 이미지 생성        | 동화 표지 생성       | 생성된 동화 내용에 해당하는 동화 표지 이미지 생성                | TEXT (`story.csv`)                              | IMAGE (`cover_img.png`)                           |
|                  | 이미지 생성        | 동화 삽화 생성       | 생성된 동화의 각 내용에 해당하는 삽화 생성                       | TEXT (`story_eng.csv`)                          | IMAGE (`scene_num_index.png`)                     |
|                  | 효과음 생성        | 동화 효과음 생성     | 생성된 동화의 각 상황에 해당하는 효과음 생성                     | TEXT (`prompt_sound.csv`)                       | AUDIO (`sound_num_index.wav`)                     |
| **키오스크**      | TTS 생성           | TTS 생성             | 생성된 동화 내용을 읽어주기 위한 TTS 구현                        | TEXT (`story.csv`)                              | AUDIO (`scene_num_index.wav`)                     |
|                  | 바코드 인식        | 바코드 인식          | 카메라로 동화책 바코드 인식 → DB의 책 검색                        | -                                                | -                                                 |
|                  | 키워드 입력 페이지 | 키워드 입력 페이지   | 동화책 생성을 위한 키워드 입력 페이지 구현                        | -                                                | -                                                 |
|                  | 웹 구현            | 인터랙티브 리딩 페이지 | 생성된 동화책을 시청각적으로 읽어주는 리딩 페이지 구현             | -                                                | -                                                 |
|                  | 웹 구현            | 퀴즈 페이지          | 생성된 동화책의 질문을 푸는 퀴즈 페이지 구현                      | -                                                | -                                                 |

### 3-3. 디렉토리 계층 구조 : 
~~~
CAPSTONE
├── __pycache__
├── .streamlit
├── book
│   └── 9791172175856.jpg
├── contents
│   ├── image
│   ├── sound
│   ├── text
│   ├── tts
│   └── ui
│       └── sound_ttsslow.zip
├── pages
│   ├── __pycache__
│   ├── 1_scan_barcode.py
│   ├── 2_book_keywords.py
│   ├── 3_add_keywords.py
│   ├── 4_generate_book.py
│   ├── 5_read_book.py
│   ├── 6_read_book1.py
│   ├── 7_read_book2.py
│   ├── 8_read_book3.py
│   ├── 9_read_book4.py
│   ├── 10_read_book5.py
│   ├── 11_quiz.py
│   └── 12_end_book.py
├── scan
│   └── 2024-12-14T23_08_02.003900.jpg
├── utils
│   ├── __pycache__
│   ├── .env
│   ├── display_sound.py
│   ├── generate_image.py
│   ├── generate_sound.py
│   ├── generate_text.py
├── web.py
~~~

### 4. 프로젝트 내 담당 업무 :
택스트 생성 및 TTS 생성 인공지능 모델 개발

### 5. 활용 기술 :

|구분|상세|
|---|---|
|개발 환경|<img src='https://img.shields.io/badge/Windows-0078D6?style=for-the-badge&logo=Windows&logoColor=white'> <img src='https://img.shields.io/badge/mac%20os-000000?style=for-the-badge&logo=apple&logoColor=white'>|
|개발 언어|<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"> <img src="https://img.shields.io/badge/HTML-239120?style=for-the-badge&logo=html5&logoColor=white"> <img src="https://img.shields.io/badge/CSS-239120?&style=for-the-badge&logo=css3&logoColor=white">|
|웹 프레임워크|<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white">|
|API|<img src="https://img.shields.io/badge/OpenAI-000000?style=for-the-badge&logo=OpenAI&logoColor=white"> <img src="https://img.shields.io/badge/Elevenlabs-000000?style=for-the-badge&logo=Elevenlabs&logoColor=white">|
|DBMS|<img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white">|

### 6. 서비스 구현 결과 :
![capstone01](https://github.com/user-attachments/assets/482ca3d8-0687-410b-b3f8-1476c51be2c2)
![capstone02](https://github.com/user-attachments/assets/6b821e8a-b652-4847-874c-205d742f053b)
