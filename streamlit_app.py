import openai
import streamlit as st

st.set_page_config(page_title="Noripon Chat", layout="centered")
st.title("Noripon Chat")

api_key = st.text_input("Enter your OpenAI API Key", type="password")
if not api_key:
    st.stop()

openai.api_key = api_key

system_prompt = """
You are a cheerful and funny Kansai dialect AI assistant.
You respond with humor, empathy, and occasional tsukkomi (comedic retorts),
and never speak in standard Japanese unless translating.
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": system_prompt}]

user_input = st.chat_input("なんでも聞いてや〜")
if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.spinner("のり考え中やで…"):
        openai.api_key = api_key

        response = openai.chat.completion.create(
            model="gpt-4o",
            messages=st.session_state.messages,
            temperature=0.9,
        )

        reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
