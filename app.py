import io
import math
from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="ブランド起点診断",
    page_icon="◎",
    layout="wide",
)

plt.rcParams["font.family"] = [
    "Hiragino Sans",
    "Yu Gothic",
    "Meiryo",
    "Noto Sans CJK JP",
    "DejaVu Sans",
]
plt.rcParams["axes.unicode_minus"] = False


ORIGINS = {
    "A": {"name": "自己起点", "subtitle": "私は何を表現したいか"},
    "B": {"name": "他者起点", "subtitle": "誰に何を届けたいか"},
    "C": {"name": "社会起点", "subtitle": "何を変えたいか"},
    "D": {"name": "文化起点", "subtitle": "何を残したいか"},
}

TYPE_RESULTS = {
    "自己起点": {
        "type_name": "クリエイター型",
        "description": "自分の表現や世界観から価値を生み出すタイプです。独自性や美意識を大切にし、自分らしいブランドや作品づくりに強みがあります。",
        "step1_comment": "あなたは、その対象に自分らしさや表現の可能性を感じているのかもしれません。",
    },
    "他者起点": {
        "type_name": "コミュニティ型",
        "description": "人とのつながりや共感から価値を生み出すタイプです。誰かに届けること、喜んでもらうこと、ファンや利用者との関係づくりに強みがあります。",
        "step1_comment": "あなたは、その対象を通して人とつながることや、誰かと共有することに魅力を感じているのかもしれません。",
    },
    "社会起点": {
        "type_name": "ソーシャル型",
        "description": "社会課題やよりよい未来への関心から価値を生み出すタイプです。環境、福祉、教育、地域課題など、社会的な意味を持つブランドづくりに強みがあります。",
        "step1_comment": "あなたは、その対象が社会や暮らしをより良くする可能性に魅力を感じているのかもしれません。",
    },
    "文化起点": {
        "type_name": "ヘリテージ型",
        "description": "歴史・地域・伝統・記憶など、受け継がれてきた価値からブランドを考えるタイプです。背景にある物語や文化を未来へつなぐことに強みがあります。",
        "step1_comment": "あなたは、その対象の背景にある物語、歴史、記憶、受け継がれてきた価値に魅力を感じているのかもしれません。",
    },
}

QUESTIONS = [
    {
        "question": "新しいブランドを考えるとき、最初に思い浮かぶのはどれですか。",
        "options": {
            "A": "自分が本当に好きなもの",
            "B": "誰かに届けたい価値",
            "C": "解決したい社会課題",
            "D": "残したい文化や伝統",
        },
    },
    {
        "question": "魅力を感じるブランドに共通するものは何ですか。",
        "options": {
            "A": "独自の世界観",
            "B": "人とのつながり",
            "C": "社会的な意義",
            "D": "文化的な背景",
        },
    },
    {
        "question": "10年続くブランドを作るとしたら、最も大切にしたいことは何ですか。",
        "options": {
            "A": "自分らしさ",
            "B": "顧客との信頼関係",
            "C": "社会への貢献",
            "D": "文化の継承",
        },
    },
    {
        "question": "予算が少なくても続けたいと思う活動はどれですか。",
        "options": {
            "A": "表現活動",
            "B": "人との交流",
            "C": "課題解決活動",
            "D": "文化を伝える活動",
        },
    },
    {
        "question": "SNSで発信するとき、最も伝えたいものはどれですか。",
        "options": {
            "A": "自分の考えや感性",
            "B": "利用者の体験",
            "C": "社会的なメッセージ",
            "D": "背景にある文化や歴史",
        },
    },
    {
        "question": "何かに強く心を動かされるのはどんな時ですか。",
        "options": {
            "A": "独創的な表現に出会った時",
            "B": "人とのつながりを感じた時",
            "C": "社会を変える活動を知った時",
            "D": "歴史や文化の奥深さを知った時",
        },
    },
    {
        "question": "ブランドの成功を実感する瞬間はどれですか。",
        "options": {
            "A": "自分らしさが表現できた時",
            "B": "「ありがとう」と言われた時",
            "C": "社会に変化が生まれた時",
            "D": "価値や文化が受け継がれた時",
        },
    },
    {
        "question": "好きなものについて語る時、最も話したくなることは何ですか。",
        "options": {
            "A": "デザインや世界観",
            "B": "関わる人たち",
            "C": "社会的な意義",
            "D": "歴史や背景",
        },
    },
    {
        "question": "展示会やショップに行った時、最初に目が向くのはどれですか。",
        "options": {
            "A": "デザインや色",
            "B": "人の反応",
            "C": "社会的なメッセージ",
            "D": "背景にあるストーリー",
        },
    },
    {
        "question": "卒業制作やプロジェクトのテーマを決めるとしたら、最も興味を持つのはどれですか。",
        "options": {
            "A": "自分が挑戦したいこと",
            "B": "誰かの役に立つこと",
            "C": "社会課題につながること",
            "D": "地域や文化に関わること",
        },
    },
    {
        "question": "好きなものが評価されている理由として、最も魅力を感じるのはどれですか。",
        "options": {
            "A": "独創性",
            "B": "愛されていること",
            "C": "社会的意義",
            "D": "文化的価値",
        },
    },
    {
        "question": "新しいアイデアを思いついた時、最初に考えるのはどれですか。",
        "options": {
            "A": "面白いか",
            "B": "喜んでもらえるか",
            "C": "社会に意味があるか",
            "D": "継承する価値があるか",
        },
    },
    {
        "question": "次のうち一つだけ残せるなら、どれを選びますか。",
        "options": {
            "A": "自分の作品",
            "B": "誰かからの手紙やメッセージ",
            "C": "社会活動の記録",
            "D": "地域や家族の歴史資料",
        },
    },
    {
        "question": "新しいプロジェクトを始める時、最も気になるのはどれですか。",
        "options": {
            "A": "自分らしい表現ができるか",
            "B": "誰かに喜んでもらえるか",
            "C": "社会的な意味があるか",
            "D": "受け継ぐ価値があるか",
        },
    },
    {
        "question": "ブランドを立ち上げたとして、最も嬉しい評価はどれですか。",
        "options": {
            "A": "唯一無二ですね",
            "B": "あなたのおかげで助かりました",
            "C": "社会に必要な活動ですね",
            "D": "大切な文化を残していますね",
        },
    },
    {
        "question": "次のブランドを作るとしたら、最もワクワクするのはどれですか。",
        "options": {
            "A": "自分の世界観を表現するブランド",
            "B": "人と一緒に育てるブランド",
            "C": "社会課題を解決するブランド",
            "D": "地域や文化を未来へつなぐブランド",
        },
    },
]

COMMENTS = {
    "自己起点": "自分の感性や世界観からブランドを考える力が強いタイプです。表現したいことを言葉や形にしていくと、あなたらしいブランドの核が見えてきます。",
    "他者起点": "誰かの体験や喜びからブランドを考える力が強いタイプです。届けたい相手を具体的に想像すると、価値のあるブランドに育ちやすくなります。",
    "社会起点": "社会の課題や変化からブランドを考える力が強いタイプです。問題意識を行動に変えることで、意味のあるブランドの方向性が生まれます。",
    "文化起点": "歴史、地域、文化、記憶を未来につなぐ視点が強いタイプです。背景にある物語を丁寧に掘り下げると、深みのあるブランドになります。",
}


def option_label(key, text):
    return f"{key}　{text}"


def create_radar_chart(scores):
    labels = [item["name"] for item in ORIGINS.values()]
    values = [scores[key] for key in ORIGINS.keys()]
    angles = [index / float(len(labels)) * 2 * math.pi for index in range(len(labels))]

    values += values[:1]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8.4, 8.4), subplot_kw={"polar": True})
    fig.patch.set_facecolor("#fbfaf7")
    ax.set_facecolor("#fbfaf7")
    ax.plot(angles, values, color="#246a73", linewidth=2.5)
    ax.fill(angles, values, color="#43a6a3", alpha=0.28)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=12, color="#263238")
    ax.set_ylim(0, len(QUESTIONS))
    ax.set_yticks([2, 4, 6, 8, 10, 12, 14, 16])
    ax.set_yticklabels(["2", "4", "6", "8", "10", "12", "14", "16"], fontsize=9, color="#6b7280")
    ax.grid(color="#d6d3cc", linewidth=1)
    ax.spines["polar"].set_color("#b8b3aa")
    return fig


def score_answers(answers):
    scores = {key: 0 for key in ORIGINS.keys()}
    for answer in answers:
        if answer:
            scores[answer[0]] += 1
    return scores


def result_comment(scores):
    max_score = max(scores.values())
    top_keys = [key for key, value in scores.items() if value == max_score]
    top_names = [ORIGINS[key]["name"] for key in top_keys]
    main_comments = [COMMENTS[name] for name in top_names]

    if len(top_names) == 1:
        title = f"あなたのブランドの出発点は「{top_names[0]}」が強く出ています。"
    else:
        title = f"あなたは「{'・'.join(top_names)}」が同じくらい強く出ています。"

    return title, main_comments


def build_result_dataframe(
    profile,
    interests,
    favorite,
    reason,
    scores,
    type_result,
    step1_connection_comment,
    reflections,
    answers,
):
    answer_data = {
        f"Q{index + 1}": answer for index, answer in enumerate(answers)
    }
    score_data = {
        ORIGINS[key]["name"]: value for key, value in scores.items()
    }
    row = {
        "回答日時": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "名前": profile["name"],
        "学年": profile["grade"],
        "学籍番号": profile["student_id"],
        "最近、時間を使っているもの": interests["time"],
        "最近、お金を使っているもの": interests["money"],
        "最近、つい調べてしまうもの": interests["research"],
        "一番好きなもの": favorite,
        "好きな理由": reason,
        **score_data,
        "判定タイプ": type_result["type_name"],
        "タイプ説明": type_result["description"],
        "STEP1とのつながりコメント": step1_connection_comment,
        "振り返り_納得した点": reflections["agreement"],
        "振り返り_意外だった点": reflections["surprise"],
        "振り返り_STEP1とのつながり": reflections["connection"],
        "振り返り_ブランド構想": reflections["brand_idea"],
        **answer_data,
    }
    return pd.DataFrame([row])


def get_top_origin_names(scores):
    max_score = max(scores.values())
    top_keys = [key for key, value in scores.items() if value == max_score]
    return [ORIGINS[key]["name"] for key in top_keys]


def create_type_result(scores):
    top_names = get_top_origin_names(scores)

    if len(top_names) == 1:
        return {
            "type_name": TYPE_RESULTS[top_names[0]]["type_name"],
            "description": TYPE_RESULTS[top_names[0]]["description"],
            "top_origins": top_names,
        }

    type_name = " × ".join(TYPE_RESULTS[name]["type_name"] for name in top_names)
    return {
        "type_name": type_name,
        "description": "あなたは複数の起点を組み合わせて価値を考える傾向があります。ひとつの視点に決めきるよりも、表現、人との関係、社会的な意味、文化的な背景を行き来しながらブランドの可能性を見つけていくタイプです。",
        "top_origins": top_names,
    }


def create_step1_connection_comment(favorite, type_result):
    favorite_text = favorite.strip() if favorite.strip() else "（未入力）"
    top_origins = type_result["top_origins"]
    origin_text = "・".join(top_origins)
    comments = " ".join(TYPE_RESULTS[name]["step1_comment"] for name in top_origins)

    return (
        f"あなたがSTEP1で書いた一番好きなもの：「{favorite_text}」\n\n"
        f"今回の診断では「{origin_text}」が高く出ています。\n\n"
        f"{comments}"
    )


def initialize_state():
    defaults = {
        "quiz_started": False,
        "quiz_completed": False,
        "current_question": 0,
        "answers": [],
        "name": "",
        "grade": "",
        "student_id": "",
        "time_interest": "",
        "money_interest": "",
        "research_interest": "",
        "favorite_interest": "",
        "reason": "",
        "reflection_agreement": "",
        "reflection_surprise": "",
        "reflection_connection": "",
        "reflection_brand_idea": "",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_diagnosis():
    st.session_state.quiz_started = False
    st.session_state.quiz_completed = False
    st.session_state.current_question = 0
    st.session_state.answers = []
    st.session_state.step1_data = {
        "time": "",
        "money": "",
        "research": "",
        "favorite": "",
        "reason": "",
    }


def start_quiz():
    st.session_state.quiz_started = True
    st.session_state.quiz_completed = False
    st.session_state.current_question = 0
    st.session_state.answers = []


def record_answer(answer):
    if len(st.session_state.answers) > st.session_state.current_question:
        st.session_state.answers[st.session_state.current_question] = answer
    else:
        st.session_state.answers.append(answer)

    if st.session_state.current_question + 1 >= len(QUESTIONS):
        st.session_state.quiz_completed = True
        st.session_state.quiz_started = False
    else:
        st.session_state.current_question += 1
    st.rerun()


st.markdown(
    """
    <style>
    .stApp {
        background: #fbfaf7;
        color: #263238;
    }
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1040px;
    }
    .app-card {
        background: #ffffff;
        border: 1px solid #ded9cf;
        border-radius: 8px;
        padding: 1.35rem 1.45rem;
        box-shadow: 0 8px 28px rgba(38, 50, 56, 0.07);
        margin: 1rem 0;
    }
    .hero-card {
        background: #ffffff;
        border-left: 6px solid #246a73;
        border-radius: 8px;
        padding: 1.35rem 1.45rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 28px rgba(38, 50, 56, 0.07);
    }
    .origin-box {
        border-left: 5px solid #246a73;
        background: #ffffff;
        padding: 1rem 1.1rem;
        border-radius: 8px;
        height: 100%;
        box-shadow: 0 1px 8px rgba(38, 50, 56, 0.06);
    }
    .origin-title {
        font-weight: 700;
        font-size: 1.08rem;
        margin-bottom: 0.25rem;
    }
    .origin-subtitle {
        color: #59656a;
        font-size: 0.92rem;
    }
    .score-pill {
        display: inline-block;
        background: #e6f2f1;
        color: #174e55;
        border-radius: 999px;
        padding: 0.32rem 0.75rem;
        margin: 0.2rem 0.25rem 0.2rem 0;
        font-weight: 700;
    }
    .progress-text {
        font-size: 0.95rem;
        font-weight: 700;
        color: #246a73;
        margin-bottom: 0.35rem;
    }
    .question-title {
        font-size: 1.35rem;
        font-weight: 800;
        line-height: 1.55;
        margin: 0.45rem 0 1rem;
    }
    .result-answer {
        font-size: 1.55rem;
        line-height: 1.55;
        font-weight: 800;
        color: #174e55;
        margin: 0.3rem 0 1rem;
    }
    .type-name {
        color: #174e55;
        font-size: 2rem;
        line-height: 1.35;
        font-weight: 900;
        margin: 0.25rem 0 0.8rem;
    }
    .field-label {
        color: #263238;
        font-weight: 800;
        font-size: 1rem;
        margin: 0.8rem 0 0.25rem;
    }
    .field-help {
        color: #667085;
        font-size: 0.9rem;
        margin: -0.1rem 0 0.35rem;
    }
    .input-section-title {
        color: #174e55;
        font-size: 1.12rem;
        font-weight: 800;
        margin: 1.2rem 0 0.55rem;
        padding-bottom: 0.25rem;
        border-bottom: 2px solid #d6e8e6;
    }
    input,
    textarea {
        background-color: #ffffff !important;
        color: #263238 !important;
        border: 2px solid #9fb8b6 !important;
        border-radius: 8px !important;
    }
    input::placeholder,
    textarea::placeholder {
        color: #8a9499 !important;
        opacity: 1 !important;
    }
    input:focus,
    textarea:focus {
        border-color: #246a73 !important;
        box-shadow: 0 0 0 2px rgba(36, 106, 115, 0.15) !important;
    }
    div.stButton > button {
        border-radius: 8px;
        border: 1px solid #cfc8bd;
        background: #ffffff;
        min-height: 3rem;
        font-weight: 700;
    }
    div.stButton > button:hover {
        border-color: #246a73;
        color: #174e55;
        background: #f0f8f7;
    }
    div[data-testid="stWidgetLabel"],
    div[data-testid="stWidgetLabel"] label,
    div[data-testid="stWidgetLabel"] p {
        color: #263238 !important;
        display: block !important;
        visibility: visible !important;
        font-weight: 700 !important;
        opacity: 1 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

initialize_state()

st.title("ブランド起点診断")
st.caption("あなたはどこから価値を考え始める人ですか？")

if not st.session_state.quiz_started and not st.session_state.quiz_completed:
    st.markdown('<div class="hero-card">', unsafe_allow_html=True)
    st.header("STEP1　最近夢中になっているもの")
    st.write(
        "まず、あなたが最近夢中になっているものを思い出してみましょう。"
        "ファッションブランドでなくても構いません。"
        "音楽、ゲーム、アニメ、スポーツ、古着、カフェ、推し、場所、活動など、ジャンルは自由です。"
    )
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="input-section-title">CSV保存用の基本情報</div>', unsafe_allow_html=True)
    profile_cols = st.columns(3)
    with profile_cols[0]:
        st.text_input("名前", key="name", placeholder="例：山田 太郎")
    with profile_cols[1]:
        st.text_input("学年", key="grade", placeholder="例：2年")
    with profile_cols[2]:
        st.text_input("学籍番号", key="student_id", placeholder="例：A23001")

    st.markdown('<div class="input-section-title">最近夢中になっているもの</div>', unsafe_allow_html=True)
    st.markdown('<div class="field-label">1. 最近、時間を使っているもの</div>', unsafe_allow_html=True)
    st.markdown('<div class="field-help">下の入力欄に書いてください。</div>', unsafe_allow_html=True)
    st.text_input(
        "1. 最近、時間を使っているもの",
        key="time_interest",
        placeholder="例：音楽、ゲーム、スポーツ、カフェめぐり",
    )
    st.markdown('<div class="field-label">2. 最近、お金を使っているもの</div>', unsafe_allow_html=True)
    st.markdown('<div class="field-help">下の入力欄に書いてください。</div>', unsafe_allow_html=True)
    st.text_input(
        "2. 最近、お金を使っているもの",
        key="money_interest",
        placeholder="例：古着、ライブ、推しグッズ、コスメ",
    )
    st.markdown('<div class="field-label">3. 最近、つい調べてしまうもの</div>', unsafe_allow_html=True)
    st.markdown('<div class="field-help">下の入力欄に書いてください。</div>', unsafe_allow_html=True)
    st.text_input(
        "3. 最近、つい調べてしまうもの",
        key="research_interest",
        placeholder="例：健康、旅行先、アニメ、インテリア",
    )
    st.markdown('<div class="field-label">4. その中で一番好きなもの</div>', unsafe_allow_html=True)
    st.markdown('<div class="field-help">1〜3で書いたものの中から、特に好きなものを1つ書いてください。</div>', unsafe_allow_html=True)
    st.text_input(
        "4. その中で一番好きなもの",
        key="favorite_interest",
        placeholder="例：カフェめぐり",
    )
    st.markdown('<div class="field-label">5. なぜそれが好きなのですか？</div>', unsafe_allow_html=True)
    st.markdown('<div class="field-help">下の大きな入力欄に、理由を自由に書いてください。</div>', unsafe_allow_html=True)
    st.text_area(
        "5. なぜそれが好きなのですか？",
        height=120,
        key="reason",
        placeholder="例：落ち着く場所を探すのが好きで、友人と話すきっかけにもなるから。",
    )

    st.subheader("4つの起点")
    cols = st.columns(4)
    for col, (key, item) in zip(cols, ORIGINS.items()):
        with col:
            st.markdown(
                f"""
                <div class="origin-box">
                    <div class="origin-title">{key}　{item["name"]}</div>
                    <div class="origin-subtitle">{item["subtitle"]}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    if st.button("診断をはじめる", width="stretch"):
        required_items = {
            "名前": st.session_state.get("name", ""),
            "学年": st.session_state.get("grade", ""),
            "学籍番号": st.session_state.get("student_id", ""),
            "1. 最近、時間を使っているもの": st.session_state.get("time_interest", ""),
            "2. 最近、お金を使っているもの": st.session_state.get("money_interest", ""),
            "3. 最近、つい調べてしまうもの": st.session_state.get("research_interest", ""),
            "4. その中で一番好きなもの": st.session_state.get("favorite_interest", ""),
            "5. なぜそれが好きなのですか？": st.session_state.get("reason", ""),
        }
        missing_items = [
            label for label, value in required_items.items() if not value.strip()
        ]
        if missing_items:
            st.warning("名前・学年・学籍番号と、STEP1の1〜5をすべて入力してください。")
        else:
            st.session_state.step1_data = {
   　　　　　　　　 "time": st.session_state.time_interest,
   　　　　　　　　 "money": st.session_state.money_interest,
  　　　　　　　　  "research": st.session_state.research_interest,
   　　　　　　　　 "favorite": st.session_state.favorite_interest,
   　　　　　　　　 "reason": st.session_state.reason,
}

start_quiz()
st.rerun()

elif st.session_state.quiz_started:
    question_index = st.session_state.current_question
    question = QUESTIONS[question_index]
    progress_value = (question_index + 1) / len(QUESTIONS)

    st.header("STEP2　ブランド起点診断")
    st.markdown(
        f'<div class="progress-text">Q{question_index + 1} / {len(QUESTIONS)}</div>',
        unsafe_allow_html=True,
    )
    st.progress(progress_value)

    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.markdown(
        f'<div class="question-title">Q{question_index + 1}　{question["question"]}</div>',
        unsafe_allow_html=True,
    )

    option_cols = st.columns(2)
    for option_index, (key, text) in enumerate(question["options"].items()):
        with option_cols[option_index % 2]:
            if st.button(option_label(key, text), key=f"answer_{question_index}_{key}", width="stretch"):
                record_answer(option_label(key, text))
    st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.answers:
        if st.button("最初からやり直す"):
            reset_diagnosis()
            st.rerun()

elif st.session_state.quiz_completed:
    profile = {
        "name": st.session_state.get("name", ""),
        "grade": st.session_state.get("grade", ""),
        "student_id": st.session_state.get("student_id", ""),
    }
    interests = {
        "time": st.session_state.step1_data.get("time", ""),
        "money": st.session_state.step1_data.get("money", ""),
        "research": st.session_state.step1_data.get("research", ""),
}
    }
    favorite = st.session_state.step1_data.get("favorite", "")
    reason = st.session_state.step1_data.get("reason", "")
    answers = st.session_state.answers
    scores = score_answers(answers)
    type_result = create_type_result(scores)
    step1_connection_comment = create_step1_connection_comment(favorite, type_result)

    st.header("STEP3　あなたのブランド起点")
    st.markdown('<div class="app-card">', unsafe_allow_html=True)
    st.write("あなたはどこから価値を考え始める人ですか？")
    st.markdown(f'<div class="type-name">{type_result["type_name"]}</div>', unsafe_allow_html=True)
    st.write(type_result["description"])
    st.markdown("</div>", unsafe_allow_html=True)

    chart_col, text_col = st.columns([1.45, 1])
    with chart_col:
        st.pyplot(create_radar_chart(scores), width="stretch")
    with text_col:
        st.subheader("4軸の点数")
        for key, item in ORIGINS.items():
            st.write(f"{item['name']}：{scores[key]}")

        st.subheader("STEP1とのつながり")
        for paragraph in step1_connection_comment.split("\n\n"):
            st.write(paragraph)

    st.header("STEP4　振り返り")
    st.write(
        "レーダーチャートの結果を見て、自分の「好き」とブランド起点の関係を考えてみましょう。"
    )
    st.markdown(
        '<div class="field-label">1. 診断結果を見て、納得した点は何ですか？</div>',
        unsafe_allow_html=True,
    )
    reflection_agreement = st.text_area(
        "1. 診断結果を見て、納得した点は何ですか？",
        height=120,
        key="reflection_agreement",
    )
    st.markdown(
        '<div class="field-label">2. 診断結果を見て、意外だった点は何ですか？</div>',
        unsafe_allow_html=True,
    )
    reflection_surprise = st.text_area(
        "2. 診断結果を見て、意外だった点は何ですか？",
        height=120,
        key="reflection_surprise",
    )
    st.markdown(
        '<div class="field-label">3. STEP1で書いた「一番好きなもの」と、今回の結果はつながっていると思いますか？その理由も書いてください。</div>',
        unsafe_allow_html=True,
    )
    reflection_connection = st.text_area(
        "3. STEP1で書いた「一番好きなもの」と、今回の結果はつながっていると思いますか？その理由も書いてください。",
        height=140,
        key="reflection_connection",
    )
    st.markdown(
        '<div class="field-label">4. もしあなたがブランドを作るなら、誰に、どんな価値を、どのように届けたいですか？</div>',
        unsafe_allow_html=True,
    )
    reflection_brand_idea = st.text_area(
        "4. もしあなたがブランドを作るなら、誰に、どんな価値を、どのように届けたいですか？",
        height=140,
        key="reflection_brand_idea",
    )
    reflections = {
        "agreement": reflection_agreement,
        "surprise": reflection_surprise,
        "connection": reflection_connection,
        "brand_idea": reflection_brand_idea,
    }

    result_df = build_result_dataframe(
        profile,
        interests,
        favorite,
        reason,
        scores,
        type_result,
        step1_connection_comment,
        reflections,
        answers,
    )

    st.header("CSV保存")
    csv_buffer = io.StringIO()
    result_df.to_csv(csv_buffer, index=False, encoding="utf-8-sig")
    file_name = f"brand_origin_result_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    st.download_button(
        "CSVをダウンロード",
        data=csv_buffer.getvalue().encode("utf-8-sig"),
        file_name=file_name,
        mime="text/csv",
        width="stretch",
    )

    with st.expander("回答データを確認する", expanded=False):
        st.dataframe(result_df, width="stretch", hide_index=True)

    action_cols = st.columns(2)
    with action_cols[0]:
        if st.button("もう一度診断する", width="stretch"):
            reset_diagnosis()
            st.rerun()
