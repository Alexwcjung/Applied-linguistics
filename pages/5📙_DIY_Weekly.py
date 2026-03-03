import streamlit as st
import requests

st.set_page_config(page_title="GitHub Markdown Viewer", layout="wide")
RAW_MD_URL = "https://raw.githubusercontent.com/MK316/Applied-linguistics/main/pages/DIY.md"

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_md(url: str) -> tuple[str | None, str | None]:
    try:
        r = requests.get(url, timeout=15)
        if r.status_code != 200:
            return None, f"HTTP {r.status_code}: {r.text[:200]}"
        # Keep as text (GitHub raw is UTF-8)
        return r.text, None
    except Exception as e:
        return None, str(e)

md_text, err = fetch_md(RAW_MD_URL)

st.caption("Source")
st.code(RAW_MD_URL, language="text")

if err:
    st.error(f"Could not load the markdown file.\n\n{err}")
else:
    # Render markdown
    st.markdown(md_text, unsafe_allow_html=False)
