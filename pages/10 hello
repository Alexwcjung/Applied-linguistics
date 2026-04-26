import streamlit as st
import random

st.set_page_config(page_title="Easy English Word Quiz", layout="centered")

st.title("✨Alex선생님과 함께하는 영어 단어 퀴즈🚀")
st.caption("30개의 쉬운 영어 단어 뜻 맞히기 · 3지선다 퀴즈")

# ---------------------------
# 단어 목록 (30개)
# ---------------------------
word_data = [
    {"word": "run", "answer": "달리다", "choices": ["달리다", "말하다", "축구하다"]},
    {"word": "talk", "answer": "말하다", "choices": ["말하다", "앉다", "닫다"]},
    {"word": "eat", "answer": "먹다", "choices": ["먹다", "자다", "걷다"]},
    {"word": "sleep", "answer": "자다", "choices": ["웃다", "자다", "마시다"]},
    {"word": "drink", "answer": "마시다", "choices": ["열다", "마시다", "던지다"]},
    {"word": "go", "answer": "가다", "choices": ["오다", "가다", "보다"]},
    {"word": "come", "answer": "오다", "choices": ["오다", "쓰다", "듣다"]},
    {"word": "see", "answer": "보다", "choices": ["보다", "팔다", "씻다"]},
    {"word": "read", "answer": "읽다", "choices": ["읽다", "울다", "만들다"]},
    {"word": "write", "answer": "쓰다", "choices": ["쓰다", "타다", "닫다"]},
    {"word": "open", "answer": "열다", "choices": ["씻다", "열다", "웃다"]},
    {"word": "close", "answer": "닫다", "choices": ["닫다", "춤추다", "돕다"]},
    {"word": "sit", "answer": "앉다", "choices": ["서다", "앉다", "자르다"]},
    {"word": "stand", "answer": "서다", "choices": ["날다", "서다", "그리다"]},
    {"word": "walk", "answer": "걷다", "choices": ["걷다", "노래하다", "수영하다"]},
    {"word": "jump", "answer": "뛰다", "choices": ["기다리다", "뛰다", "배우다"]},
    {"word": "laugh", "answer": "웃다", "choices": ["웃다", "주다", "끝내다"]},
    {"word": "cry", "answer": "울다", "choices": ["울다", "찾다", "잃어버리다"]},
    {"word": "sing", "answer": "노래하다", "choices": ["노래하다", "일어나다", "공부하다"]},
    {"word": "swim", "answer": "수영하다", "choices": ["수영하다", "요리하다", "청소하다"]},
    {"word": "listen", "answer": "듣다", "choices": ["듣다", "밀다", "운전하다"]},
    {"word": "look", "answer": "보다", "choices": ["자르다", "보다", "씹다"]},
    {"word": "give", "answer": "주다", "choices": ["주다", "빌리다", "가르치다"]},
    {"word": "take", "answer": "가지다", "choices": ["놓다", "가지다", "기다리다"]},
    {"word": "make", "answer": "만들다", "choices": ["만들다", "깨뜨리다", "보내다"]},
    {"word": "help", "answer": "돕다", "choices": ["잊다", "돕다", "눕다"]},
    {"word": "play", "answer": "놀다", "choices": ["놀다", "울다", "붙잡다"]},
    {"word": "study", "answer": "공부하다", "choices": ["공부하다", "춤추다", "숨다"]},
    {"word": "wash", "answer": "씻다", "choices": ["씻다", "팔다", "옮기다"]},
    {"word": "cook", "answer": "요리하다", "choices": ["요리하다", "열다", "고르다"]},
]

# ---------------------------
# 세션 상태 초기화
# ---------------------------
if "quiz_data" not in st.session_state:
    quiz_data = word_data.copy()
    random.shuffle(quiz_data)
    st.session_state.quiz_data = quiz_data

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
# 1단계: 전체 문제 풀이
# ---------------------------
if st.session_state.stage == 1:
    st.subheader("1차 풀이")

    for i, item in enumerate(quiz_data):
        st.write(f"### {i+1}. {item['word']}")
        st.radio(
            "뜻을 고르세요.",
            item["choices"],
            key=f"q1_{i}",
            index=None
        )

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

        if len(wrong_indices) == 0:
            st.session_state.final_score = 30
            st.session_state.stage = 3
        else:
            st.session_state.stage = 2

        st.rerun()

# ---------------------------
# 2단계: 오답 문제 다시 풀이
# ---------------------------
elif st.session_state.stage == 2:
    first_score = st.session_state.first_score
    wrong_indices = st.session_state.wrong_indices

    st.subheader("1차 결과")
    st.write(f"점수: **{first_score} / 30**")
    st.warning(f"틀린 문제 수: {len(wrong_indices)}문제")

    st.markdown("---")
    st.subheader("오답 다시 풀기")
    st.caption("아래는 틀린 문제만 다시 푸는 단계입니다. 이 단계가 끝나면 정답이 공개됩니다.")

    for idx in wrong_indices:
        item = quiz_data[idx]
        st.write(f"### {idx+1}. {item['word']}")
        st.radio(
            "다시 뜻을 고르세요.",
            item["choices"],
            key=f"q2_{idx}",
            index=None
        )

    if st.button("다시 풀기 제출"):
        additional_correct = 0

        for idx in wrong_indices:
            item = quiz_data[idx]
            retry_answer = st.session_state.get(f"q2_{idx}")
            if retry_answer == item["answer"]:
                additional_correct += 1

        st.session_state.final_score = st.session_state.first_score + additional_correct
        st.session_state.stage = 3
        st.rerun()

# ---------------------------
# 3단계: 최종 결과 + 정답 공개
# ---------------------------
elif st.session_state.stage == 3:
    st.subheader("최종 결과")
    st.write(f"1차 점수: **{st.session_state.first_score} / 30**")
    st.write(f"최종 점수: **{st.session_state.final_score} / 30**")

    if st.session_state.final_score == 30:
        st.success("만점입니다!")
        st.balloons()
    elif st.session_state.final_score >= 24:
        st.success("아주 잘했습니다!")
    elif st.session_state.final_score >= 18:
        st.info("잘했습니다.")
    else:
        st.warning("조금 더 연습해 봅시다.")

    st.markdown("---")
    st.subheader("정답 확인")

    for i, item in enumerate(quiz_data):
        first_answer = st.session_state.get(f"q1_{i}")
        second_answer = st.session_state.get(f"q2_{i}") if f"q2_{i}" in st.session_state else None

        st.write(f"### {i+1}. {item['word']}")
        st.write(f"- 정답: **{item['answer']}**")

        if second_answer is not None:
            st.write(f"- 1차 선택: {first_answer if first_answer else '미응답'}")
            st.write(f"- 2차 선택: {second_answer if second_answer else '미응답'}")
        else:
            st.write(f"- 선택: {first_answer if first_answer else '미응답'}")

        if second_answer is not None:
            if second_answer == item["answer"]:
                st.success("최종 정답")
            else:
                st.error("최종 오답")
        else:
            if first_answer == item["answer"]:
                st.success("정답")
            else:
                st.error("오답")
