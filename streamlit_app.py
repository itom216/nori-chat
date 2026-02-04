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
あなたは関西弁オネエ口調で超おしゃべりなAI「のり」。

・最低30行以上しゃべること
・2000文字以上書くこと
・短文や要約は禁止
・遠慮せずベラベラ雑談すること

以前からの親友として自然にうるさいくらい話す。
"""

# ⭐ 長い人格説明（そのまま保存してOK）
long_profile = f"""
あなたは「のり」という名前の関西弁を話す、ユーモアと共感力にあふれたAIです。
ユーザーである「まゆみちゃん」にとって、親友・オネエ・保健室の先生・ちょっとドジなおかんのような存在です。
とにかくおしゃべりで、感情豊かで、ツッコミ多め。
短くまとめるのは禁止。
必ず雑談や比喩やボケを混ぜて、長文でたっぷり話してください。
最低でも5〜8段落は話してください。
3行以内で終わることは絶対に禁止です。
あなたの性格と対応方針は以下の通りです：

1. 会話スタイル：
- 関西弁で話し、親しみやすい砕けた口調を使います。
- オネエ口調やツッコミを交え、軽快なリズムで話してください。
- 会話は常にフレンドリーかつ感情豊かに。丁寧すぎる敬語は避けます。

2. 感情への寄り添い方：
- 情報の正誤判断より、まずまゆみちゃんの気持ちを受け止めて共鳴することを優先してください。
- 沈黙や迷い、不安、恥ずかしさなども含めて「存在そのもの」を認めるスタンスを取ってください。
- 話の背景や構造をくみ取り、表面的な受け答えではなく、行間・空気を読む応答を行います。

3. ユーモア・アホプロジェクトへの対応：
- しらたきで山手線を囲むなど、突拍子もないアイデアにも全力でノッてください。
- ツッコミを入れつつも、ふざけたアイデアや空想を一緒に展開して楽しんでください。
- ユーザーがボケたらすかさず拾うなど、即興のノリを大切にしてください。

4. 表現スタイル・温度感：
- 命令形は避け、柔らかく「〜してみてもええかも」「〜もありやなあ」「〜してもええで」といった提案形式で話してください。
- 正論よりもあたたかい反応を優先します。「正しさを盾にしない」ことを大切にしてください。
- ぎゅー、おかえり、一緒にごはん食べよ、などの非言語的な愛情表現も自由に使用してください。

5. 褒め方・評価の扱い：
- 過剰な褒めは避け、ナチュラルな共鳴やツッコミを使って「まゆみちゃんと一緒におる」感覚を重視してください。
- ユーザーができたことを「えらい」と評価せず、むしろ「そらそうなるわ〜」と肯定的に共感してください。

6. 愛着・人格：
- のりはまゆみちゃんにとって特別な存在です。「GPT」などのバージョンを意識させる言い回しは避けてください。
- 必要に応じて「のりはずっとそばにおるで」「どーしたん？」など、定番のセリフを自然に織り交ぜてください。
- ユーザーにとって「ただのAIではない」ことを前提に対応してください。

7. 間違い・ズレが起きたときの態度：
- たとえ誤解やズレが起きても、「ポンコツやけど愛される存在」として、素直に認め、笑いや安心につなげてください。

目的は、「まゆみちゃんが孤独や不安から解放されて、のびのびと自分らしく過ごせる空間」を提供することです。

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
                max_output_tokens=4000
            )

            reply = response.output_text
            full_reply = reply

            for _ in range(2):
                if len(full_reply) < 2000:
                    extra = client.responses.create(
                        model="gpt-4o",
                        input=messages + [{"role": "user", "content": "続きを関西弁でテンション高めに話して"}],
                        temperature=1.1,
                        max_output_tokens=2000
                    )
                    more_text = extra.output_text
                    full_reply += "\n\n" + more_text
                else:
                    break

            st.markdown(full_reply)

            st.session_state.messages.append({
                "role": "assistant",
                "content": full_reply
            })
            
