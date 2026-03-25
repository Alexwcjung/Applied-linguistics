import streamlit as st
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Advanced T-test Analyzer", layout="wide")
st.title("📊 T-test Analyzer & Visualizer")
st.info("""Sample data link: <br>
        https://docs.google.com/spreadsheets/d/1k8SGYP7_SZDhDSdC4LVFl8rMsqdAUVHm3HK2HEClSDc/edit?usp=sharing


        """)
# --- 1. 데이터 로드부 ---
sheet_url = st.text_input("구글 시트 주소를 입력하세요:", 
                         placeholder="https://docs.google.com/spreadsheets/d/.../edit?usp=sharing")

def get_google_sheet(url):
    try:
        file_id = url.split('/')[-2]
        raw_url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv"
        return pd.read_csv(raw_url)
    except: return None

if sheet_url:
    df = get_google_sheet(sheet_url)
    if df is not None:
        # 데이터 클리닝
        cols = df.columns.tolist()
        col_left, col_right = st.columns(2)
        group_col = col_left.selectbox("독립변수 (Group):", cols)
        value_col = col_right.selectbox("종속변수 (Value):", cols)

        df[value_col] = pd.to_numeric(df[value_col], errors='coerce')
        df = df.dropna(subset=[value_col, group_col])
        groups = df[group_col].unique()

        if len(groups) == 2:
            st.divider()
            
            # --- 2. 기술통계 섹션 ---
            st.subheader("📋 기술통계 (Descriptive Statistics)")
            desc_stats = df.groupby(group_col)[value_col].agg(['count', 'mean', 'std', 'min', 'max']).reset_index()
            st.table(desc_stats)

            # --- 3. T-test 섹션 ---
            g1 = df[df[group_col] == groups[0]][value_col]
            g2 = df[df[group_col] == groups[1]][value_col]
            t_stat, p_val = stats.ttest_ind(g1, g2)

            st.subheader("📝 분석 결과")
            c1, c2, c3 = st.columns(3)
            c1.metric("T-value", f"{t_stat:.4f}")
            c2.metric("P-value", f"{p_val:.4f}")
            c3.metric("Significance", "Significant" if p_val < 0.05 else "Not Sig.")

            # --- 4. 시각화 옵션 설정 (Sidebar 또는 Main) ---
            st.divider()
            st.subheader("📈 시각화 설정 (Visualization)")
            
            v_col1, v_col2 = st.columns([1, 3])
            
            with v_col1:
                st.write("**그래프 옵션**")
                chart_type = st.radio("그래프 종류 선택:", ["Box Plot", "Histogram", "Bar Plot (Mean)"])
                palette_choice = st.selectbox("색상 테마 선택:", 
                                           ["Set2", "Pastel1", "Paired", "rocket", "viridis", "magma"])
                show_points = st.checkbox("개별 데이터 포인트 표시", value=True)

            with v_col2:
                fig, ax = plt.subplots(figsize=(8, 5))
                
                if chart_type == "Box Plot":
                    sns.boxplot(x=group_col, y=value_col, data=df, palette=palette_choice, ax=ax, hue=group_col, legend=False)
                    if show_points:
                        sns.stripplot(x=group_col, y=value_col, data=df, color="black", alpha=0.3, ax=ax)
                    ax.set_title(f"Box Plot of {value_col} by {group_col}")

                elif chart_type == "Histogram":
                    sns.histplot(data=df, x=value_col, hue=group_col, kde=True, palette=palette_choice, ax=ax, element="step")
                    ax.set_title(f"Distribution of {value_col}")

                elif chart_type == "Bar Plot (Mean)":
                    sns.barplot(x=group_col, y=value_col, data=df, palette=palette_choice, ax=ax, hue=group_col, errorbar='sd')
                    ax.set_title(f"Mean comparison with Std Dev")

                st.pyplot(fig)
                
            # --- 5. 결과 보고서 텍스트 ---
            st.subheader("📌 APA Style Report")
            report = f"독립표본 t-검정 결과, {groups[0]} 집단(M={g1.mean():.2f}, SD={g1.std():.2f})과 " \
                     f"{groups[1]} 집단(M={g2.mean():.2f}, SD={g2.std():.2f}) 간에는 " \
                     f"통계적으로 {'유의미한' if p_val < 0.05 else '유의미하지 않은'} 차이가 나타났다 " \
                     f"(t = {t_stat:.2f}, p = {p_val:.4f})."
            st.code(report, language="text")
            st.caption("위 문구를 복사하여 논문이나 보고서에 활용하세요.")

        else:
            st.warning(f"집단(Group)이 2개여야 합니다. 현재: {list(groups)}")
    else:
        st.error("데이터 로드 실패. 링크와 권한을 확인하세요.")
