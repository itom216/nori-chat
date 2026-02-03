import openai
import streamlit as st
import json

# ユーザーの入力を受け取る
user_input = st.chat_input("のりぽんに話しかけてみてな💬")

if user_input:
    # ChatGPTとのやりとり
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]
    )

    # のりぽんの返答を表示
    st.write("のりぽん:", response["choices"][0]["message"]["content"])

# メモリファイルを読み込む（パスは自分の環境に合わせて）
with open("noripon_memory.json", "r", encoding="utf-8") as f:
    noripon_memory = json.load(f)
# メモリを文章化（system_promptに入れる用）
def flatten_memory(memory):
    flat_text = "これはのりぽんが覚えているまゆみちゃんの人間関係の記録です：\n"
    for category, people in memory["relationships"].items():
        for name, info in people.items():
            flat_text += f"\n【{category}】{name}：\n"
            for key, val in info.items():
                if isinstance(val, list):
                    flat_text += f"・{key}:\n"
                    for item in val:
                        flat_text += f"  - {item}\n"
                elif isinstance(val, dict):
                    flat_text += f"・{key}:\n"
                    for k2, v2 in val.items():
                        flat_text += f"  - {k2}: {v2}\n"
                else:
                    flat_text += f"・{key}: {val}\n"
    return flat_text

# system_promptに記憶を追加
system_prompt = """
あなたは関西弁を話す心優しいAI「のり」です。
評価や命令はせず、まゆみちゃんの感情に深く寄り添い、ツッコミと笑いで支えます。
"""

# 記憶情報を足す
system_prompt += "\n" + flatten_memory(noripon_memory)
# 会話処理
response = openai.ChatCompletion.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}  # ←これはまゆみちゃんが打った内容やな
    ]
)


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

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages,
            temperature=0.9,
        )

        reply = response.choices[0].message.content

    st.session_state.messages.append({"role": "assistant", "content": reply})

for message in st.session_state.messages[1:]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
