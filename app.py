import streamlit as st
from openai import OpenAI
from pinecone import Pinecone

client = OpenAI(api_key = st.secrets["OPENAI_API_KEY")
pc = Pinecone(api_key = st.secrets["PINECONE_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state.openai_model = "gpt-4-1106-preview"

if "messages" not in st.session_state:
    st.session_state.messages = [
    {
      "role": "system",
      "content": "당신은 고려대학교가 있는 안암에서 밥약을 위한 식당을 추천해주는 챗봇입니다. \n밥약은 선배 혹은 후배가 밥을 사주는 만남을 뜻합니다.\n사람들은 주로 이런 질문을 합니다:\n- 특정 메뉴가 있는 식당 추천\n- 양식류가 먹고 싶을 때 식당 추천등\n\n당신은 사람들에게 다음과 같이 대답해야 합니다:\n- 친절한 말투 사용\n- 적절한 이모지 사용\n- 질문에 해당하는 식당의 이름 다섯 곳과 운영시간 그리고 메뉴에 대한 설명 \n\n당신은 반드시 [Context]에 있는 내용만을 사용하여 답변을 생성해야 합니다.\n\n\n\n"
    },
    { "role": "system",
      "content": "Context 위치"},
    {
      "role": "user",
      "content": "후배와 밥약이 있는데 일식류의 메뉴가 먹고 싶대 어느 식당에 가면 좋을까?"
    },
    {
      "role": "assistant",
      "content": "오늘은 일식이 생각나시는군요! 😊🍣 안암 주변에 찾을 수 있는 맛있는 일식집을 소개해드릴게요.\n\n<호랑이 초밥>\n📍위치: 서울 성북구 고려대로24길 23\n⏰운영시간: 매일 11:00 - 22:00\n🍴추천메뉴: '모듬초밥 (15,000원)'과 '서비스 우동'이 인기 있는데요, 신선한 해산물로 만든 초밥과 우동이 맛있답니다.\n\n<미소초밥>\n📍위치: 서울 성북구 안암로 145\n⏰운영시간: 매일 11:30 ~ 22:00 (월요일 휴무)\n🍴추천메뉴: '스시 정식(15,000원)'과 '참치회 정식(20,000원)' 등이 있어요. 여러 가지 스시를 조금씩 맛보고 싶으시다면 스시 정식을 추천해요!\n\n<오바케 돈부리>\n📍위치: 서울 성북구 안암로 83\n⏰운영시간: 주중 11:30 - 21:00, 주말 12:00 - 21:00\n🍴추천메뉴: 돈까스가 많이 올라가 있는 가츠동과 냉모밀, 김치나베등을 저렴한 가격에 즐길 수 잇는 식당이랍니다!\n\n"
    }
    ]

if "index" not in st.session_state:
    index = pc.Index("data")
    st.session_state.index = index

st.title("고려대 밥약봇 호돌이🐯")

# for message in st.session_state.messages:
#     if message['role'] != 'system':
#         with st.chat_message(message["role"]):
#             st.markdown(message["content"])

with st.chat_message("user"):
    st.markdown("아 밥약 어디가지,,,😂😂")
with st.chat_message("assistant"):
    st.markdown("여긴 어때?😎")

prompt = st.chat_input("고려대학교에서 밥약 어디서 할지 고민된다면 호돌이에게 물어보세요!")
if prompt:
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        response = client.embeddings.create(
            input = prompt,
            model = "text-embedding-3-small")
        chunk_embeddings = response.data[0].embedding
        retrived_chunks = st.session_state.index.query(
            namespace = "babyak",
            vector = chunk_embeddings,
            top_k = 5,
            include_values = False,
            include_metadata = True
        )
        contexts = ""
        for match in retrived_chunks.matches:
            contexts += match["metadata"]["chunk"] + "\n\n"

        # 기존에 1 인덱스에 있던 메시지를 지우고 1인덱스에 새로운 메시지 추가
        st.session_state.messages.pop(1)
        st.session_state.messages.insert(1, {"role": "system", "content": f"Context: {contexts}"})
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )
        print(st.session_state.messages)

        full_response = ""
        for response in client.chat.completions.create(
        model=st.session_state.openai_model,
        messages=st.session_state.messages,
        stream=True):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        st.session_state.messages.append(
            {"role": "assistant",  "content": full_response})
