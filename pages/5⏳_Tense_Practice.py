import streamlit as st

st.set_page_config(page_title="Tense Practice", layout="centered")

st.title("⏳ Tense Practice")
st.caption("현재형, 현재진행형, 과거형, 미래형 중 알맞은 표현을 고르세요.")

TOTAL_QUESTIONS = 20

# ---------------------------
# 문제 목록
# ---------------------------
quiz_data = [
    {
        "sentence": "She (     ) a book now.",
        "answer": "is reading",
        "choices": ["reads", "is reading", "read", "will read"]
    },
    {
        "sentence": "They (     ) soccer yesterday.",
        "answer": "played",
        "choices": ["play", "are playing", "played", "will play"]
    },
    {
        "sentence": "I (     ) breakfast every morning.",
        "answer": "eat",
        "choices": ["am eating", "ate", "will eat", "eat"]
    },
    {
        "sentence": "He (     ) his friend tomorrow.",
        "answer": "will meet",
        "choices": ["meets", "met", "will meet", "is meeting"]
    },
    {
        "sentence": "We (     ) English now.",
        "answer": "are studying",
        "choices": ["studied", "study", "are studying", "will study"]
    },
    {
        "sentence": "My father (     ) coffee every day.",
        "answer": "drinks",
        "choices": ["drinks", "is drinking", "drank", "will drink"]
    },
    {
        "sentence": "The students (     ) to the teacher now.",
        "answer": "are listening",
        "choices": ["listen", "listened", "will listen", "are listening"]
    },
    {
        "sentence": "I (     ) my homework last night.",
        "answer": "did",
        "choices": ["do", "am doing", "did", "will do"]
    },
    {
        "sentence": "She (     ) to school by bus every day.",
        "answer": "goes",
        "choices": ["is going", "went", "will go", "goes"]
    },
    {
        "sentence": "He (     ) TV now.",
        "answer": "is watching",
        "choices": ["watched", "watches", "is watching", "will watch"]
    },
    {
        "sentence": "We (     ) a movie tomorrow.",
        "answer": "will watch",
        "choices": ["watch", "watched", "are watching", "will watch"]
    },
    {
        "sentence": "They (     ) in the park last Sunday.",
        "answer": "walked",
        "choices": ["walked", "walk", "are walking", "will walk"]
    },
    {
        "sentence": "My brother (     ) computer games every weekend.",
        "answer": "plays",
        "choices": ["is playing", "played", "plays", "will play"]
    },
    {
        "sentence": "Look! The baby (     ).",
        "answer": "is sleeping",
        "choices": ["sleeps", "slept", "will sleep", "is sleeping"]
    },
    {
        "sentence": "I (     ) my grandmother next week.",
        "answer": "will visit",
        "choices": ["visit", "visited", "am visiting", "will visit"]
    },
    {
        "sentence": "She (     ) a letter yesterday.",
        "answer": "wrote",
        "choices": ["writes", "is writing", "wrote", "will write"]
    },
    {
        "sentence": "Tom (     ) up at seven every morning.",
        "answer": "gets",
        "choices": ["got", "gets", "is getting", "will get"]
    },
    {
        "sentence": "We (     ) lunch now.",
        "answer": "are having",
        "choices": ["have", "had", "are having", "will have"]
    },
    {
        "sentence": "It (     ) tomorrow.",
        "answer": "will rain",
        "choices": ["rains", "rained", "is raining", "will rain"]
    },
    {
        "sentence": "He (     ) a new bike last month.",
        "answer": "bought",
        "choices": ["buys", "is buying", "bought", "will buy"]
    },
]

# ---------------------------
# 세션 상태 초기화
# ---------------------------
if "stage" not in st.session_state:
    # stage 1: 전체 문제 풀이
    # stage 2: 오답 문제 다시 풀이
    # stage 3: 최종 결과 및 정답 공개
    st.session_state.stage = 1

if "wrong_indices" not in st.session_state:
    st.session_state.wrong_indices = []

if "first_score" not in st.session_state:
    st.session_state.first_score = 0

if "final_score" not in st.session_state:
    st.session_state.final_score = 0

if "show_balloons" not in st.session_state:
    st.session_state.show_balloons = False

# ---------------------------
# 폭죽 표시
# ---------------------------
if st.session_state.show_balloons:
    st.balloons()
    st.session_state.show_balloons = False

# ---------------------------
# 다시 시작
# ---------------------------
if st.button("처음부터 다시 시작"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.markdown("---")

# ---------------------------
# 문제 출력 함수
# ---------------------------
def show_question(i, item, key_prefix, label):
    st.write(f"### {i+1}. {item['sentence']}")

    st.radio(
        label,
        item["choices"],
        key=f"{key_prefix}_{i}",
        index=None
    )

    st.markdown("---")


# ---------------------------
# 1단계: 전체 문제 풀이
# ---------------------------
if st.session_state.stage == 1:
    st.subheader("1차 풀이")
    st.caption("전체 문제를 풀고 제출하세요. 맞힌 문제가 있으면 폭죽이 터집니다.")

    for i, item in enumerate(quiz_data):
        show_question(i, item, "q1", "정답을 고르세요.")

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

        # 1차에서 하나라도 맞히면 폭죽
        if correct_count > 0:
            st.session_state.show_balloons = True

        if len(wrong_indices) == 0:
            st.session_state.final_score = TOTAL_QUESTIONS
            st.session_state.stage = 3
        else:
            st.session_state.stage = 2

        st.rerun()


# ---------------------------
# 2단계: 오답 문제 다시 풀이
# ---------------------------
elif st.session_state.stage == 2:
    st.subheader("1차 결과")
    st.write(f"점수: **{st.session_state.first_score} / {TOTAL_QUESTIONS}**")
    st.warning(f"틀린 문제 수: {len(st.session_state.wrong_indices)}문제")

    st.markdown("---")
    st.subheader("2차 풀이")
    st.caption("1차에서 틀린 문제만 다시 풉니다. 맞힌 문제가 있으면 폭죽이 터집니다.")

    for idx in st.session_state.wrong_indices:
        item = quiz_data[idx]
        show_question(idx, item, "q2", "다시 정답을 고르세요.")

    if st.button("2차 제출"):
        additional_correct = 0
        final_wrong_indices = []

        for idx in st.session_state.wrong_indices:
            item = quiz_data[idx]
            retry_answer = st.session_state.get(f"q2_{idx}")

            if retry_answer == item["answer"]:
                additional_correct += 1
            else:
                final_wrong_indices.append(idx)

        st.session_state.final_score = st.session_state.first_score + additional_correct
        st.session_state.final_wrong_indices = final_wrong_indices

        # 2차에서 하나라도 맞히면 폭죽
        if additional_correct > 0:
            st.session_state.show_balloons = True

        st.session_state.stage = 3
        st.rerun()


# ---------------------------
# 3단계: 최종 결과 + 정답 공개
# ---------------------------
elif st.session_state.stage == 3:
    st.subheader("최종 결과")

    st.write(f"1차 점수: **{st.session_state.first_score} / {TOTAL_QUESTIONS}**")
    st.write(f"최종 점수: **{st.session_state.final_score} / {TOTAL_QUESTIONS}**")

    if st.session_state.final_score == TOTAL_QUESTIONS:
        st.success("만점입니다! 아주 잘했습니다! 🎉")
    elif st.session_state.final_score >= 16:
        st.success("아주 잘했습니다!")
    elif st.session_state.final_score >= 12:
        st.info("잘했습니다.")
    else:
        st.warning("조금 더 연습해 봅시다.")

    st.markdown("---")
    st.subheader("정답 확인")

    final_wrong_indices = st.session_state.get("final_wrong_indices", [])

    for i, item in enumerate(quiz_data):
        first_answer = st.session_state.get(f"q1_{i}")
        second_answer = st.session_state.get(f"q2_{i}") if f"q2_{i}" in st.session_state else None

        st.write(f"### {i+1}. {item['sentence']}")
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
