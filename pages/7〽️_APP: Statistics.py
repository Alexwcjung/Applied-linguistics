import streamlit as st
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="T-test Analyzer Pro", layout="wide")

if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False

st.title("📊 Step-by-Step T-test Analyzer")

# --- Sample Data Section ---
with st.expander("📝 테스트용 샘플 데이터 사용하기"):
    sample_link = "https://docs.google.com/spreadsheets/d/1k8SGYP7_SZDhDSdC4LVFl8rMsqdAUVHm3HK2HEClSDc/edit?usp=sharing"
    st.code(sample_link, language="text")

st.divider()

# --- Step 1: 데이터 로드 ---
st.header("1️⃣ Step: Load Data")
sheet_url = st.text_input("구글 시트 주소를 입력하세요:", placeholder="https://docs.google.com/spreadsheets/d/.../edit")

def get_google_sheet(url):
    try:
        file_id = url.split('/')[-2]
        raw_url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv"
        return pd.read_csv(raw_url, skipinitialspace=True)
    except: return None

if st.button("📥 데이터 불러오기"):
    if sheet_url:
        df_raw = get_google_sheet(sheet_url)
        if df_raw is not None:
            st.session_state.df = df_raw
            st.session_state.data_loaded = True
            st.session_state.analyzed = False 
            st.success("데이터를 성공적으로 가져왔습니다!")
        else: st.error("URL을 확인해주세요.")

# --- Step 2: 변수 선택 및 기술통계 ---
if st.session_state.data_loaded:
    st.divider()
    st.header("2️⃣ Step: Select Variables & Descriptives")
    df = st.session_state.df.copy()
    cols = df.columns.tolist()
    
    col1, col2 = st.columns(2)
    group_col = col1.selectbox("독립변수 (Group):", cols, index=0)
    value_col = col2.selectbox("종속변수 (Value):", cols, index=1 if len(cols)>1 else 0)
    
    df[value_col] = pd.to_numeric(df[value_col], errors='coerce')
    clean_df = df.dropna(subset=[group_col, value_col])
    detected_groups = sorted(clean_df[group_col].unique().tolist())
    
    st.write(f"🔍 **데이터 확인:** `{group_col}` 열에서 **{len(detected_groups)}개** 집단 감지: `{detected_groups}`")

    if st.button("🔍 분석 실행"):
        if len(detected_groups) == 2:
            st.session_state.analyzed = True
            st.session_state.clean_df = clean_df
            st.session_state.groups = detected_groups
            st.session_state.group_col = group_col
            st.session_state.value_col = value_col
        else: st.error(f"집단이 2개여야 합니다.")

# --- Step 3: 결과 및 시각화 ---
if st.session_state.analyzed:
    st.divider()
    st.header("3️⃣ Step: Results & Visualization")
    
    df = st.session_state.clean_df
    groups = st.session_state.groups
    g_col = st.session_state.group_col
    v_col = st.session_state.value_col
    
    g1_data = df[df[g_col] == groups[0]][v_col]
    g2_data = df[df[g_col] == groups[1]][v_col]
    
    # 📋 기술통계
    st.subheader("📋 Descriptive Statistics")
    desc = df.groupby(g_col)[v_col].agg(['count', 'mean', 'std']).reset_index()
    st.table(desc)

    # 📝 T-test 결과
    t_stat, p_val = stats.ttest_ind(g1_data, g2_data)
    df_deg = len(g1_data) + len(g2_data) - 2 # 자유도 계산
    
    c1, c2, c3 = st.columns(3)
    c1.metric("T-value", f"{t_stat:.4f}")
    c2.metric("P-value", f"{p_val:.4f}")
    c3.metric("Result", "Significant" if p_val < 0.05 else "Not Sig.")

    # 📈 시각화
    st.subheader("📊 Visualization")
    v_col_opt, v_col_plot = st.columns([1, 2.5])
    with v_col_opt:
        chart_type = st.radio("그래프 종류:", ["Box Plot", "Histogram", "Bar Plot (Mean)"])
        palette = st.selectbox("색상 테마:", ["Set2", "coolwarm", "viridis", "pastel", "magma"])
        show_points = st.checkbox("데이터 포인트 표시", value=True)
    
    with v_col_plot:
        fig, ax = plt.subplots(figsize=(8, 4))
        if chart_type == "Box Plot":
            sns.boxplot(x=g_col, y=v_col, data=df, palette=palette, ax=ax, hue=g_col, legend=False)
            if show_points: sns.stripplot(x=g_col, y=v_col, data=df, color="black", alpha=0.3, ax=ax)
        elif chart_type == "Histogram":
            sns.histplot(data=df, x=v_col, hue=g_col, kde=True, palette=palette, ax=ax, element="step")
        elif chart_type == "Bar Plot (Mean)":
            sns.barplot(x=g_col, y=v_col, data=df, palette=palette, ax=ax, errorbar='sd', hue=g_col)
        st.pyplot(fig)

    # --- 📄 [핵심 추가] Dual-Language APA Report ---
    st.divider()
    st.subheader("📌 APA Style Reporting")
    
    m1, sd1 = g1_data.mean(), g1_data.std()
    m2, sd2 = g2_data.mean(), g2_data.std()
    sig_status_kr = "유의미한" if p_val < 0.05 else "유의미하지 않은"
    sig_status_en = "a statistically significant" if p_val < 0.05 else "no statistically significant"

    tab_kr, tab_en = st.tabs(["🇰🇷 한글 보고서", "🇺🇸 English Report"])
    
    with tab_kr:
        report_kr = f"독립표본 t-검정 결과, {groups[0]} 집단(M={m1:.2f}, SD={sd1:.2f})과 " \
                    f"{groups[1]} 집단(M={m2:.2f}, SD={sd2:.2f}) 간의 평균 차이는 " \
                    f"통계적으로 {sig_status_kr} 차이가 나타났다 " \
                    f"(t({df_deg}) = {t_stat:.2f}, p = {p_val:.4f})."
        st.info("아래 텍스트를 복사하여 보고서에 사용하세요.")
        st.code(report_kr, language="text")

    with tab_en:
        report_en = f"An independent-samples t-test was conducted to compare {v_col} in {groups[0]} and {groups[1]} conditions. " \
                    f"There was {sig_status_en} difference in the scores for {groups[0]} (M={m1:.2f}, SD={sd1:.2f}) " \
                    f"and {groups[1]} (M={m2:.2f}, SD={sd2:.2f}) " \
                    f"(t({df_deg}) = {t_stat:.2f}, p = {p_val:.4f})."
        st.info("Copy the text below for your academic paper.")
        st.code(report_en, language="text")

    if st.button("🔄 전체 초기화"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
