import streamlit as st
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

# --- 1. 페이지 설정 ---
st.set_page_config(page_title="Full T-test Analyzer", layout="wide")

if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'analyzed' not in st.session_state:
    st.session_state.analyzed = False

st.title("📊 Step-by-Step T-test Analyzer")

# --- Sample Data Section ---
with st.expander("📝 테스트용 샘플 데이터 사용하기"):
    sample_link = "https://docs.google.com/spreadsheets/d/1k8SGYP7_SZDhDSdC4LVFl8rMsqdAUVHm3HK2HEClSDc/edit?usp=sharing"
    st.code(sample_link, language="text")
    st.caption("위 링크를 복사하여 아래 URL 입력란에 붙여넣으세요.")

st.divider()

# --- Step 1: 데이터 로드 ---
st.header("1️⃣ Step: Load Data")
sheet_url = st.text_input("구글 시트 주소를 입력하세요:", 
                         placeholder="https://docs.google.com/spreadsheets/d/.../edit")

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
        else:
            st.error("URL을 확인해주세요.")

# --- Step 2: 변수 선택 및 기술통계 ---
if st.session_state.data_loaded:
    st.divider()
    st.header("2️⃣ Step: Select Variables & Descriptives")
    df = st.session_state.df.copy()
    cols = df.columns.tolist()
    
    col1, col2 = st.columns(2)
    group_col = col1.selectbox("독립변수 (Group):", cols, index=0)
    value_col = col2.selectbox("종속변수 (Value):", cols, index=1 if len(cols)>1 else 0)
    
    # 데이터 클리닝
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
        else:
            st.error(f"T-test를 위해서는 집단이 2개여야 합니다. (현재: {len(detected_groups)}개)")

# --- Step 3: 결과 및 시각화 ---
if st.session_state.analyzed:
    st.divider()
    st.header("3️⃣ Step: Results & Visualization")
    
    df = st.session_state.clean_df
    groups = st.session_state.groups
    g_col = st.session_state.group_col
    v_col = st.session_state.value_col
    
    g1 = df[df[g_col] == groups[0]][v_col]
    g2 = df[df[g_col] == groups[1]][v_col]
    
    # 📋 기술통계
    st.subheader("📋 Descriptive Statistics")
    desc = df.groupby(g_col)[v_col].agg(['count', 'mean', 'std']).reset_index()
    st.table(desc)

    # 📝 T-test 결과
    t_stat, p_val = stats.ttest_ind(g1, g2)
    c1, c2, c3 = st.columns(3)
    c1.metric("T-value", f"{t_stat:.4f}")
    c2.metric("P-value", f"{p_val:.4f}")
    c4 = "Significant" if p_val < 0.05 else "Not Sig."
    c3.metric("Result", c4)

    # 📈 시각화 (복구된 옵션들)
    st.subheader("📊 Visualization Options")
    v_col_opt, v_col_plot = st.columns([1, 2.5])
    
    with v_col_opt:
        chart_type = st.radio("그래프 종류:", ["Box Plot", "Histogram", "Bar Plot (Mean)"])
        palette = st.selectbox("색상 테마:", ["Set2", "coolwarm", "viridis", "pastel", "magma"])
        show_points = st.checkbox("데이터 포인트 표시", value=True)
    
    with v_col_plot:
        fig, ax = plt.subplots(figsize=(8, 5))
        if chart_type == "Box Plot":
            sns.boxplot(x=g_col, y=v_col, data=df, palette=palette, ax=ax, hue=g_col, legend=False)
            if show_points:
                sns.stripplot(x=g_col, y=v_col, data=df, color="black", alpha=0.3, ax=ax)
        elif chart_type == "Histogram":
            sns.histplot(data=df, x=v_col, hue=g_col, kde=True, palette=palette, ax=ax, element="step")
        elif chart_type == "Bar Plot (Mean)":
            sns.barplot(x=g_col, y=v_col, data=df, palette=palette, ax=ax, errorbar='sd', hue=g_col)
        
        ax.set_title(f"{chart_type} of {v_col} by {g_col}")
        st.pyplot(fig)

    # 📄 APA 리포트
    st.subheader("📌 APA Style Report")
    report = f"독립표본 t-검정 결과, {groups[0]} 집단(M={g1.mean():.2f}, SD={g1.std():.2f})과 " \
             f"{groups[1]} 집단(M={g2.mean():.2f}, SD={g2.std():.2f}) 간의 차이는 " \
             f"통계적으로 {'유의미하였다' if p_val < 0.05 else '유의미하지 않았다'} " \
             f"(t = {t_stat:.2f}, p = {p_val:.4f})."
    st.code(report, language="text")

    if st.button("🔄 전체 초기화"):
        for key in list(st.session_state.keys()): del st.session_state[key]
        st.rerun()
