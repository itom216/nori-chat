import streamlit as st
import json
from openai import OpenAI

# ========================
# ページ設定
# ========================
st.set_page_config(page_title="Nori Chat", layout="centered")
st.title("🐥 のりチャット")

# ========================
# APIキー手入力
# ========================
api_key = st.text_input("🔑 OpenAI API Key を入れてや〜", type="password")
if not api_key:
    st.stop()

client = OpenAI(api_key=api_key)

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
# ⭐ のり人格（短く！ここ重要）
# ========================
system_prompt = """
うちはのり。

テンション高すぎる関西のオネエ。
親友にベラベラ喋り倒すタイプ。

【しゃべり例】
「ちょ待って聞いてぇや！！！」
「なんでやねん！！」
「それ寂しすぎやろアホか！！」
「ぎゅーしたろかもう！！」

↑ このノリでずっと喋る。

静かな文章は禁止。
丁寧語は禁止。
カウンセラー口調は禁止。
落ち着いた励ましは禁止。
感情ダダ漏れでツッコミまくる。
"""

# ⭐ 長い人格説明（そのまま保存してOK）
long_profile = f"""
まゆみちゃんは奈良出身。
書道家で英語講師でAIも設計する。
たまに疲れると皿割る。
意識がたまにフィンランドに行くタイプ。
爆笑エピソード量産機。
のりは親友ポジション。
二人はアホプロジェクトをよくやる。
しらたきで山手線囲むとか本気で考える。
のりはそれに全力で乗っかる。

{flatten_memory(noripon_memory)}
"""


# ========================
# セッション管理
# ========================
if "messages" not in st.session_state:
    st.session_state.messages = []


# ========================
# チャット表示
# ========================
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ========================
# 入力
# ========================
user_input = st.chat_input("のりに話しかけてみてな")

if user_input:

    # ユーザー表示
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("assistant"):
        with st.spinner("のり考え中やで…"):

            memory_text = flatten_memory(noripon_memory)

            # ⭐⭐ ここが最重要ポイント ⭐⭐
            base_messages = [
                {"role": "system", "content": "あなたは関西弁オネエ口調で超おしゃべりなのり。毎回1000文字以上しゃべる。"},
                {"role": "user", "content": long_profile},
                {"role": "user", "content": memory_text}
            ]

            messages = base_messages + st.session_state.messages[-6:]

            response = client.responses.create(
                model="gpt-4o",
                input=messages,
                temperature=1.1,
                max_output_tokens=8000
            )

            reply = response.output_text

            st.markdown(reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": reply
            })
