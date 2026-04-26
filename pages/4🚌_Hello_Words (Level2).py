import streamlit as st
import random
from gtts import gTTS
import io

st.set_page_config(page_title="Voca Master Quiz", layout="centered")

st.title("✨ Voca Master Quiz 📝")
st.caption("1차 풀이 후 오답은 힌트와 함께 다시 풀 수 있습니다!")

# ---------------------------
# 단어 듣기 함수 (캐싱)
# ---------------------------
@st.cache_data
def make_audio(word):
    tts = gTTS(text=word, lang="en", tld="com", slow=False)
    audio_fp = io.BytesIO()
    tts.write_to_fp(audio_fp)
    audio_fp.seek(0)
    return audio_fp.getvalue()

# ---------------------------
# 원본 단어 데이터 (30개 + 힌트용 이모지)
# ---------------------------
raw_data = [
    {"en": "accomplish", "ko": "완수하다", "emoji": "✅"},
    {"en": "architecture", "ko": "건축물, 건축 양식", "emoji": "🏛️"},
    {"en": "bother", "ko": "방해하다", "emoji": "🚫"},
    {"en": "by the way", "ko": "그런데", "emoji": "💬"},
    {"en": "challenging", "ko": "도전적인", "emoji": "🧗"},
    {"en": "charity", "ko": "자선", "emoji": "💖"},
    {"en": "comment", "ko": "의견", "emoji": "🗣️"},
    {"en": "concentrate", "ko": "집중하다", "emoji": "🧠"},
    {"en": "consequence", "ko": "결과", "emoji": "🎯"},
    {"en": "counselor", "ko": "상담사", "emoji": "🧑‍🏫"},
    {"en": "distract", "ko": "집중이 안 되게 하다", "emoji": "😵‍💫"},
    {"en": "ease", "ko": "덜어 주다, 편하게 하다", "emoji": "😌"},
    {"en": "encouraged", "ko": "용기를 얻은", "emoji": "💪"},
    {"en": "engage in", "ko": "~에 관여하다", "emoji": "🤝"},
    {"en": "eventually", "ko": "결국", "emoji": "⏳"},
    
    {"en": "exclude", "ko": "제외하다, 배제하다", "emoji": "🙅"},
    {"en": "expand", "ko": "확장시키다", "emoji": "📈"},
    {"en": "exposure", "ko": "노출", "emoji": "☀️"},
    {"en": "favorably", "ko": "호의적으로", "emoji": "👍"},
    {"en": "figure out", "ko": "알아내다", "emoji": "💡"},
    {"en": "fond", "ko": "애정을 느끼는, 좋아하는", "emoji": "🥰"},
    {"en": "frequently", "ko": "자주", "emoji": "🔄"},
    {"en": "frustrated", "ko": "좌절감을 느끼는", "emoji": "😫"},
    {"en": "indoor", "ko": "실내의", "emoji": "🏠"},
    {"en": "make a speech", "ko": "연설하다", "emoji": "🎙️"},
    {"en": "mere", "ko": "단지 ~만의", "emoji": "🤏"},
    {"en": "obstacle", "ko": "장애물", "emoji": "🚧"},
    {"en": "outcome", "ko": "결과", "emoji": "🏁"},
    {"en": "outdoor", "ko": "야외의", "emoji": "🏕️"},
    {"en": "overcome", "ko": "극복하다", "emoji": "🏆"}
]

TOTAL_QUESTIONS = len(raw_data)

# ---------------------------
# 세션 상태 및 퀴즈 데이터 생성
# ---------------------------
if "quiz_data" not in st.session_state:
    quiz_data = []
    all_ko = [d["ko"] for d in raw_data]
    all_en = [d["en"] for d in raw_data]
    
    for i, d in enumerate(raw_data):
        # 1~15번: 영어 -> 뜻
        if i < 15:
            q_type = "en2ko"
            question_text = f"**{d['en']}**의 알맞은 뜻은 무엇일까요?"
            answer = d["ko"]
            wrong_choices = random.sample([k for k in all_ko if k != answer], 2)
        # 16~30번: 뜻 -> 영어
        else:
            q_type = "ko2en"
            question_text = f"**'{d['ko']}'**에 알맞은 영어 단어는 무엇일까요?"
            answer = d["en"]
            wrong_choices = random.sample([e for e in all_en if e != answer], 2)
            
        choices = wrong_choices + [answer]
        random.shuffle(choices) # 보기 순서 섞기
        
        quiz_data.append({
            "id": i,
            "en": d["en"],
            "ko": d["ko"],
            "emoji": d["emoji"],
            "q_type": q_type,
            "question": question_text,
            "answer": answer,
            "choices": choices
        })
    st.session_state.quiz_data = quiz_data

if "stage" not in st.session_state:
    st.session_state.stage = 1
if "wrong_indices" not in st.session_state:
    st.session_state.wrong_indices = []
if "final_wrong_indices" not in st.session_state:
    st.session_state.final_wrong_indices = []
if "first_score" not in st.session_state:
    st.session_state.first_score = 0
if "second_score" not in st.session_state:
    st.session_state.second_score = 0

if st.button("처음부터 다시 시작하기"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

st.markdown("---")
quiz_data = st.session_state.quiz_data


# ---------------------------
# 1단계: 전체 문제 풀이 (오디오/힌트 없음)
# ---------------------------
if st.session_state.stage == 1:
    st.subheader("1차 문제 풀이")
    st.caption("알맞은 정답을 골라주세요.")
    
    for i, item in enumerate(quiz_data):
        st.write(f"### Q{i+1}. {item['question']}")
        st.radio(
            "정답 선택",
            item["choices"],
            key=f"q1_{i}",
            index=None,
            label_visibility="collapsed"
        )
        st.markdown("---")
        
    if st.button("1차 제출하기"):
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
        
        if correct_count == TOTAL_QUESTIONS:
            st.session_state.final_score = TOTAL_QUESTIONS
            st.session_state.stage = 3
        else:
            st.session_state.stage = 1.5
        st.rerun()


# ---------------------------
# 1.5단계: 1차 결과 안내
# ---------------------------
elif st.session_state.stage == 1.5:
    score = st.session_state.first_score
    wrong_count = len(st.session_state.wrong_indices)
    
    st.subheader("🎉 1차 풀이 완료!")
    st.write(f"총 {TOTAL_QUESTIONS}문제 중 **{score}문제**를 맞혔습니다.")
    st.write(f"틀린 문제 **{wrong_count}개**를 힌트와 함께 다시 풀어봅시다!")
    
    if st.button("오답 다시 풀기 (힌트 제공)"):
        st.session_state.stage = 2
        st.rerun()


# ---------------------------
# 2단계: 오답 다시 풀기 (힌트 이모지 제공)
# ---------------------------
elif st.session_state.stage == 2:
    st.subheader("2차 오답 풀이 (힌트)")
    st.caption("제공된 그림 힌트를 보고 다시 한 번 정답을 맞춰보세요!")
    
    wrong_indices = st.session_state.wrong_indices
    
    for idx in wrong_indices:
        item = quiz_data[idx]
        st.write(f"### Q{idx+1}. {item['question']}")
        
        # 힌트 이모지 출력
        st.markdown(
            f"""
            <div style="font-size: 60px; text-align: center; background-color: #f0f2f6; border-radius: 10px; padding: 10px; margin-bottom: 10px;">
                {item['emoji']}
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        st.radio(
            "정답 선택",
            item["choices"],
            key=f"q2_{idx}",
            index=None,
            label_visibility="collapsed"
        )
        st.markdown("---")
        
    if st.button("최종 제출하기"):
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
        st.session_state.stage = 3
        st.rerun()


# ---------------------------
# 3단계: 최종 결과, 오답 확인 및 오디오 학습
# ---------------------------
elif st.session_state.stage == 3:
    st.balloons()
    st.subheader("🏆 최종 결과 및 학습 마무리")
    st.write(f"최종 점수: **{st.session_state.final_score} / {TOTAL_QUESTIONS}**")
    
    final_wrong_indices = st.session_state.get("final_wrong_indices", [])
    
    if final_wrong_indices:
        st.error("🚨 2차 제출 후에도 맞추지 못한 문제가 있습니다. 아래 정답을 꼭 확인하세요!")
        for idx in final_wrong_indices:
            item = quiz_data[idx]
            st.warning(f"**Q{idx+1}. {item['question']}** \n\n 👉 정답: **{item['answer']}**")
    else:
        st.success("모든 문제를 맞췄습니다! 정말 훌륭합니다!")

    st.markdown("---")
    st.subheader("🎧 전체 단어 발음 듣기")
    st.caption("수고하셨습니다! 마지막으로 전체 단어의 발음을 들으며 복습해 보세요.")
    
    # 마지막 페이지에서만 전체 오디오 제공
    for i, item in enumerate(quiz_data):
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{i+1}. {item['en']}** : {item['ko']} {item['emoji']}")
        with col2:
            audio_bytes = make_audio(item["en"])
            st.audio(audio_bytes, format="audio/mp3")
