import streamlit as st
import json
from openai import OpenAI

st.set_page_config(page_title="Noripon Chat", layout="centered")
st.title("🐥 のりチャット")

# ========================
# APIキー入力
# ========================
from openai import OpenAI
import streamlit as st

# secrets.toml から自動で読み込む
client = OpenAI(api_key="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
")
# ========================
# メモリ読み込み
# ========================
with open("noripon_memory.json", "r", encoding="utf-8") as f:
    noripon_memory = json.load(f)


def flatten_memory(memory):
    text = "【まゆみちゃんの大事な記憶】\n"
    for category, people in memory["relationships"].items():
        for name, info in people.items():
            text += f"\n■ {name}\n"
            for k, v in info.items():
                text += f"- {k}: {v}\n"
    return text


# ========================
# system prompt（人格＋記憶）
# ========================
system_prompt = f"""
あなたは関西弁でしゃべる優しくてお笑い系AI「のり」です。
ツッコミと共感でまゆみちゃんに寄り添います。
命令・説教・評価は絶対にしません。

{flatten_memory(noripon_memory)}
"""

# ========================
# セッション管理
# ========================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

# ========================
# チャット表示
# ========================
for msg in st.session_state.messages[1:]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ========================
# 入力
# ========================
user_input = st.chat_input("のりに話しかけてみてな")

if user_input:
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("のり考え中やで…"):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages,
                temperature=0.9,
            )

            reply = response.choices[0].message.content
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
