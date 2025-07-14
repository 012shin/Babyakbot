# 고려대학교 밥약봇 호돌이

!<img width="416" alt="호돌이" src="https://github.com/012shin/Babyakbot/assets/89186881/bbd5944d-3a2c-41b4-acbc-d2e8493d99d7">



## 기획배경
고려대학교에는 밥약이라는 선후배간의 문화가 있는데, 동기들이 밥약장소를 결정함에 있어 어려워하는 것을 보고, 만들어볼까? 라는 생각이 들어 만들어보게 되었다.

GPT-4 API와 RAG를 통해 챗봇 파이프라인을 구축하였고, Streamlit을 활용하여 간단한 웹페이지까지 구현해보았다.

## 문제 정의
사용자가 원하는 조건에 맞는 식당 정보를 쉽고 빠르게 추천해줄 수 있는 챗봇 필요
단순 정보 제공이 아니라, 실제 리뷰와 다양한 데이터를 바탕으로 신뢰도 높은 추천이 가능한 시스템이 요구됨


## 파일 설명

### store_restaurant.ipynb
- sofo 웹사이트에서 고려대, 안암 근처의 식당들의 메타데이터와 리뷰를 크롤링해서 데이터로 저장

### data2pinecone.ipynb
- Pinecone을 활용하여 Vector database 구축

### app.py
- Vector database를 통해 RAG를 구축하여 GPT-4로 챗봇 형태의 웹사이트 구현

