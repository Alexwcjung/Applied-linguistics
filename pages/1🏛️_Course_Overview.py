import streamlit as st

# ---------------------------
# Top Card
# ---------------------------
st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #ffffff, #eef6ff);
        border: 1.5px solid #d9e7ff;
        border-radius: 30px;
        padding: 40px 30px;
        text-align: center;
        box-shadow: 0 8px 24px rgba(31,78,121,0.12);
        margin-bottom: 30px;
    ">
        <div style="font-size: 62px; margin-bottom: 12px;">
            🌱 📚 ✨
        </div>
        <div style="
            display: inline-block;
            background-color: #eaf3ff;
            color: #1f4e79;
            font-size: 16px;
            font-weight: 700;
            padding: 8px 18px;
            border-radius: 999px;
            margin-bottom: 18px;
        ">
            Fun English · Spring 2026
        </div>
        <h1 style="
            color:#1f4e79;
            font-size: 42px;
            font-weight: 800;
            margin: 12px 0 16px 0;
        ">
            Welcome to Fun English!
        </h1>
        <p style="
            font-size: 22px;
            line-height: 1.7;
            color: #34495e;
            margin: 0 auto;
            max-width: 780px;
        ">
            Learn English step by step through words, listening, speaking, reading, and fun activities.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Course Objectives
# ---------------------------
st.markdown(
    """
    <h2 style="
        color:#1f4e79;
        font-size:30px;
        margin-bottom:18px;
    ">
        ✨ Course Objectives
    </h2>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        background-color:#ffffff;
        border: 1.5px solid #e4ebff;
        border-radius: 22px;
        padding: 24px 28px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        margin-bottom: 26px;
    ">
        <p style="font-size:23px; line-height:1.8; margin:10px 0;">
            🔤 <b>Word Quiz</b>: Learn basic words with pictures and sounds
        </p>
        <p style="font-size:23px; line-height:1.8; margin:10px 0;">
            🧰 <b>Class Apps</b>: Use tools for classroom activities
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------
# Goal
# ---------------------------
st.markdown(
    """
    <h2 style="
        color:#1f4e79;
        font-size:30px;
        margin-bottom:14px;
    ">
        🎯 Goal
    </h2>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <div style="
        background: linear-gradient(135deg, #fffdf7, #fff3d9);
        border: 2px solid #ffe7b8;
        border-radius: 22px;
        padding: 22px 26px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    ">
        <p style="
            font-size:24px;
            font-weight:700;
            color:#8a5a00;
            margin:0;
        ">
            English is not just a subject. It is a tool for communication.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
