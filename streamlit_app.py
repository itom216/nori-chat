

import openai 
import streamlit as st

st.set_page_config(page_title="norichat", layout="centered") st.title("🤖 のりぽん with ChatGPT")



device_key = st.text_input("OpenAI APIキーを入力してな（sk-で始まるやつやで）", type="password") if not device_key: st.stop() openai.api_key = device_key


system_prompt = """ あなたは関西弁で喋る明るくてお笑い系のAIアシスタントです。 相手の心に寄り添い、ツッコミやボケを混ぜながら、やさしく共感します。 ただのおふざけではなく、相手がしんどいときはしっかり気持ちに寄り添い、励ましすぎず、安心感を与えるように対応します。 言葉づかいは基本的に関西弁で、オネエっぽさやテンポの良いユーモアを交えて話します。 正しさよりも相手の感情を優先し、評価や命令はせず、並んで寄り添うようなトーンで返答してください。 """

if "messages" not in st.session_state: st.session_state.messages = [ {"role": "system", "content": system_prompt} ]



user_input = st.chat_input("なんでも聞いてや〜") if user_input: st.session_state.messages.append({"role": "user", "content": user_input}) with st.spinner("のりぽん考え中やで…"): response = openai.ChatCompletion.create( model="gpt-4o", messages=st.session_state.messages, temperature=0.9, ) reply = response.choices[0].message["content"] st.session_state.messages.append({"role": "assistant", "content": reply})



tooltip = """ ※スマホでも見やすいようにレイアウト調整済みやで！ """ for message in st.session_state.messages[1:]: with st.chat_message(message["role"]): st.markdown(message["content"])
