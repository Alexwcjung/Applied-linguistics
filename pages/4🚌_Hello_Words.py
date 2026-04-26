import streamlit as st
from gtts import gTTS
import io

st.set_page_config(page_title="Easy English Word Quiz", layout="centered")

st.title("✨Alex선생님과 함께하는 영어 단어 퀴즈🚌")
st.caption("그림을 보고, 발음을 듣고, 영어 단어의 뜻을 고르세요.")

TOTAL_QUESTIONS = 20

# ---------------------------
# 단어 듣기 함수
# ---------------------------
@st.cache_data
def make_audio(word):
    tts = gTTS(text=word, lang="en", tld="com", slow=False)
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    return audio_fp.getvalue()


# ---------------------------
# 단어 목록 20개
# 학생마다 같은 순서로 나오도록 random.shuffle 사용 안 함
# ---------------------------
word_data = [
    {"word": "run", "answer": "달리다", "picture": "🏃", "choices": ["달리다", "말하다", "축구하다"]},
    {"word": "talk", "answer": "말하다", "picture": "🗣️", "choices": ["앉다", "말하다", "닫다"]},
    {"word": "eat", "answer": "먹다", "picture": "🍽️", "choices": ["자다", "걷다", "먹다"]},
    {"word": "sleep", "answer": "자다", "picture": "😴", "choices": ["웃다", "자다", "마시다"]},
    {"word": "drink", "answer": "마시다", "picture": "🥤", "choices": ["열다", "던지다", "마시다"]},
    {"word": "go", "answer": "가다", "picture": "➡️", "choices": ["가다", "오다", "보다"]},
    {"word": "come", "answer": "오다", "picture": "👋", "choices": ["쓰다", "듣다", "오다"]},
    {"word": "see", "answer": "보다", "picture": "👀", "choices": ["팔다", "보다", "씻다"]},
    {"word": "read", "answer": "읽다", "picture": "📖", "choices": ["읽다", "울다", "만들다"]},
    {"word": "write", "answer": "쓰다", "picture": "✏️", "choices": ["타다", "닫다", "쓰다"]},
    {"word": "open", "answer": "열다", "picture": "📂", "choices": ["씻다", "열다", "웃다"]},
    {"word": "close", "answer": "닫다", "picture": "🚪", "choices": ["닫다", "춤추다", "돕다"]},
    {"word": "sit", "answer": "앉다", "picture": "🪑", "choices": ["서다", "자르다", "앉다"]},
    {"word": "stand", "answer": "서다", "picture": "🧍", "choices": ["날다", "서다", "그리다"]},
    {"word": "walk", "answer": "걷다", "picture": "🚶", "choices": ["걷다", "노래하다", "수영하다"]},
    {"word": "jump", "answer": "뛰다", "picture": "🤾", "choices": ["기다리다", "배우다", "뛰다"]},
    {"word": "laugh", "answer": "웃다", "picture": "😂", "choices": ["주다", "웃다", "끝내다"]},
    {"word": "cry", "answer": "울다", "picture": "😭", "choices": ["울다", "찾다", "잃어버리다"]},
    {"word": "sing", "answer": "노래하다", "picture": "🎤", "choices": ["일어나다", "공부하다", "노래하다"]},
    {"word": "swim", "answer": "수영하다", "picture": "🏊", "choices": ["요리하다", "수영하다", "청소하다"]},
]


# ---------------------------
# 세션 상태 초기화
# ---------------------------
if "quiz_data" not in st.session_state:
    st.session_state.quiz_data = word_data.copy()

if "stage" not in st.session_state:
    # 1: 1차 풀이
    # 1.5: 1차 응원 화면
    # 2: 2차 풀이
    # 2.5: 2차 응원 화면
    # 3: 최종 결과 및 정답 공개
    st.session_state.stage = 1

if "wrong_indices" not in st.session_state:
    st.session_state.wrong_indices = []

if "final_wrong_indices" not in st.session_state:
    st.session_state.final_wrong_indices = []

if "first_score" not in st.session_state:
    st.session_state.first_score = 0

if "second_score" not in st.session_state:
    st.session_state.second_score = 0

if "final_score" not in st.session_state:
    st.session_state.final_score = 0

if "first_celebration_shown" not in st.session_state:
    st.session_state.first_celebration_shown = False

if "second_celebration_shown" not in st.session_state:
    st.session_state.second_celebration_shown = False


# ---------------------------
# 다시 시작
# ---------------------------
if st.button("처음부터 다시 시작"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.markdown("---")

quiz_data = st.session_state.quiz_data


# ---------------------------
# 문제 화면 출력 함수
# ---------------------------
def show_question(i, item, radio_key, label):
    picture = item.get("picture", "❓")

    st.write(f"### {i+1}. Listen and choose the meaning.")

    st.markdown(
        f"""
        <div style="
            width: 120px;
            background-color: #f8fbff;
            border: 1.5px solid #dfe8ff;
            border-radius: 16px;
            padding: 10px;
            margin-top: 6px;
            margin-bottom: 10px;
            text-align: center;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        ">
            <div style="
                font-size: 54px;
                line-height: 1.1;
            ">
                {picture}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    audio_bytes = make_audio(item["word"])
    st.audio(audio_bytes, format="audio/mp3")

    st.radio(
        label,
        item["choices"],
        key=radio_key,
        index=None
    )

    st.markdown("---")


# ---------------------------
# 1단계: 전체 문제 풀이
# ---------------------------
if st.session_state.stage == 1:
    st.subheader("1차 풀이")
    st.caption("문제를 보고, 그림과 발음을 확인한 뒤 알맞은 뜻을 고르세요.")

    for i, item in enumerate(quiz_data):
        show_question(i, item, f"q1_{i}", "뜻을 고르세요.")

    if st.button("1차 제출"):
        wrong_indices = []
        correct_count = 0

        for i, item in enumerate(quiz_data):
            user_answer = st.session_state.get(f"q1_{i}")

            if user_answer == item["answer"]:
                correct_count += 1
            else:
                wrong_indices.append(i)

        st.session_state.first_score = correct_count
        st.session_state.wrong_indices = wrong_indices
        st.session_state.first_celebration_shown = False
        st.session_state.stage = 1.5

        st.rerun()


# ---------------------------
# 1.5단계: 1차 응원 화면
# ---------------------------
elif st.session_state.stage == 1.5:
    score = st.session_state.first_score
    wrong_count = len(st.session_state.wrong_indices)

    if not st.session_state.first_celebration_shown:
        st.balloons()
        st.session_state.first_celebration_shown = True

    st.subheader("🎉 1차 풀이 완료!")

    st.markdown(
        f"""
        <div style="
            background-color: #f8fbff;
            border: 2px solid #dfe8ff;
            border-radius: 22px;
            padding: 28px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            margin-bottom: 20px;
        ">
            <div style="font-size: 56px;">👏📚✨</div>
            <h2 style="color:#1f4e79;">잘했어요!</h2>
            <p style="font-size:22px;">
                1차에서 <b>{score}문제</b>를 맞혔습니다.
            </p>
            <p style="font-size:20px;">
                다시 풀 단어는 <b>{wrong_count}개</b>입니다.
            </p>
            <p style="font-size:18px; color:#555;">
                틀린 단어는 아직 익숙하지 않은 단어일 뿐입니다. 한 번 더 보면 더 잘 기억할 수 있어요!
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(score / TOTAL_QUESTIONS)

    if score == TOTAL_QUESTIONS:
        st.success("완벽합니다! 1차에서 모든 단어를 맞혔습니다.")
        if st.button("최종 결과 보기"):
            st.session_state.final_score = TOTAL_QUESTIONS
            st.session_state.second_score = 0
            st.session_state.final_wrong_indices = []
            st.session_state.stage = 3
            st.rerun()
    else:
        st.info("이제 2차에서 틀린 단어만 다시 풀어 봅시다. 충분히 할 수 있습니다!")

        if st.button("2차 오답 다시 풀기 시작하기"):
            st.session_state.stage = 2
            st.rerun()


# ---------------------------
# 2단계: 오답 문제 다시 풀이
# ---------------------------
elif st.session_state.stage == 2:
    wrong_indices = st.session_state.wrong_indices

    st.subheader("2차 풀이")
    st.write(f"1차 점수: **{st.session_state.first_score} / {TOTAL_QUESTIONS}**")
    st.warning(f"다시 풀 단어: {len(wrong_indices)}개")

    st.markdown("---")
    st.caption("1차에서 틀린 단어만 다시 풉니다. 다시 듣고 천천히 골라 보세요.")

    for idx in wrong_indices:
        item = quiz_data[idx]
        show_question(idx, item, f"q2_{idx}", "다시 뜻을 고르세요.")

    if st.button("2차 제출"):
        additional_correct = 0
        final_wrong_indices = []

        for idx in wrong_indices:
            item = quiz_data[idx]
            retry_answer = st.session_state.get(f"q2_{idx}")

            if retry_answer == item["answer"]:
                additional_correct += 1
            else:
                final_wrong_indices.append(idx)

        st.session_state.second_score = additional_correct
        st.session_state.final_score = st.session_state.first_score + additional_correct
        st.session_state.final_wrong_indices = final_wrong_indices
        st.session_state.second_celebration_shown = False
        st.session_state.stage = 2.5

        st.rerun()


# ---------------------------
# 2.5단계: 2차 응원 화면
# ---------------------------
elif st.session_state.stage == 2.5:
    retry_total = len(st.session_state.wrong_indices)
    second_score = st.session_state.second_score
    final_score = st.session_state.final_score
    final_wrong_count = len(st.session_state.final_wrong_indices)

    if not st.session_state.second_celebration_shown:
        st.balloons()
        st.session_state.second_celebration_shown = True

    st.subheader("🌟 2차 풀이 완료!")

    st.markdown(
        f"""
        <div style="
            background-color: #fffdf7;
            border: 2px solid #ffe7b8;
            border-radius: 22px;
            padding: 28px;
            text-align: center;
            box-shadow: 0 4px 12px rgba(0,0,0,0.06);
            margin-bottom: 20px;
        ">
            <div style="font-size: 56px;">💪🔊🌱</div>
            <h2 style="color:#b35c00;">끝까지 다시 도전한 것이 정말 멋집니다!</h2>
            <p style="font-size:22px;">
                2차에서 <b>{retry_total}개 중 {second_score}개</b>를 다시 맞혔습니다.
            </p>
            <p style="font-size:20px;">
                현재 최종 점수는 <b>{final_score} / {TOTAL_QUESTIONS}</b>입니다.
            </p>
            <p style="font-size:18px; color:#555;">
                한 번 틀린 단어를 다시 맞혔다는 것은, 단어가 머릿속에 더 단단히 들어오고 있다는 뜻입니다.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress(final_score / TOTAL_QUESTIONS)

    if final_wrong_count == 0:
        st.success("대단합니다! 2차까지 모두 해결했습니다.")
    else:
        st.info(f"아직 헷갈린 단어는 {final_wrong_count}개입니다. 마지막 정답 확인에서 다시 정리해 봅시다.")

    if st.button("최종 결과와 정답 확인하기"):
        st.session_state.stage = 3
        st.rerun()


# ---------------------------
# 3단계: 최종 결과 + 정답 공개
# ---------------------------
elif st.session_state.stage == 3:
    st.subheader("최종 결과")

    st.write(f"1차 점수: **{st.session_state.first_score} / {TOTAL_QUESTIONS}**")
    st.write(f"2차에서 다시 맞힌 단어 수: **{st.session_state.second_score}개**")
    st.write(f"최종 점수: **{st.session_state.final_score} / {TOTAL_QUESTIONS}**")

    if st.session_state.final_score == TOTAL_QUESTIONS:
        st.success("만점입니다! 정말 훌륭합니다! 🎉")
        st.balloons()
    elif st.session_state.final_score >= 16:
        st.success("아주 잘했습니다! 단어 실력이 좋아지고 있어요!")
    elif st.session_state.final_score >= 12:
        st.info("잘했습니다. 조금만 더 연습하면 더 많은 단어를 기억할 수 있습니다.")
    else:
        st.warning("괜찮습니다. 헷갈린 단어를 다시 보면서 천천히 익혀 봅시다.")

    st.markdown("---")
    st.subheader("정답 확인")

    final_wrong_indices = st.session_state.get("final_wrong_indices", [])

    for i, item in enumerate(quiz_data):
        picture = item.get("picture", "❓")
        word_display = item["word"].capitalize()

        st.write(f"### {i+1}. {word_display}")

        st.markdown(
            f"""
            <div style="
                width: 110px;
                background-color: #fffdf7;
                border: 1.5px solid #ffe7b8;
                border-radius: 16px;
                padding: 10px;
                margin-top: 6px;
                margin-bottom: 10px;
                text-align: center;
                box-shadow: 0 2px 6px rgba(0,0,0,0.04);
            ">
                <div style="
                    font-size: 50px;
                    line-height: 1.1;
                ">
                    {picture}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        audio_bytes = make_audio(item["word"])
        st.audio(audio_bytes, format="audio/mp3")

        first_answer = st.session_state.get(f"q1_{i}")
        second_answer = st.session_state.get(f"q2_{i}") if f"q2_{i}" in st.session_state else None

        st.write(f"- 정답: **{item['answer']}**")

        if second_answer is not None:
            st.write(f"- 1차 선택: {first_answer if first_answer else '미응답'}")
            st.write(f"- 2차 선택: {second_answer if second_answer else '미응답'}")

            if i in final_wrong_indices:
                st.error("최종 오답")
            else:
                st.success("2차에서 정답")
        else:
            st.write(f"- 선택: {first_answer if first_answer else '미응답'}")

            if first_answer == item["answer"]:
                st.success("1차에서 정답")
            else:
                st.error("오답")

        st.markdown("---")
