# ❄️ Streamlit Guideline

+ Web link: https://streamlit.io


### 1. Overview
![streamlit](https://github.com/MK316/Applied-linguistics/raw/main/pages/images/streamlit-intro.png)


### 2. App deployment online
+ Gradio
+ [Huggingface](https://github.com/MK316/Coding4ET/blob/main/Lessons/huggingface_deploy.ipynb)
+ Streamlit
+ And more

![streamlit](https://github.com/MK316/Applied-linguistics/raw/main/pages/images/deploy1.png)

### Sample app code

#### 1. TTS application

##### App Design Description

1. Text input module
The app provides a text box where the user enters the text to be converted into speech.

2. Language selection module
A dropdown menu allows the user to choose the target language or accent for audio generation.

3. Audio generation trigger
A button initiates the text-to-speech process only when the user is ready.

4. Text-to-speech conversion module
The input text is processed through Google TTS, with language-specific settings applied according to the selected option.

5. Audio playback module
The generated speech is immediately returned as playable audio within the same interface.

6. Example text support
Sample multilingual captions are displayed below the main tool to help users test the app quickly.

###### Compact summary

text input → language selection → conversion trigger → TTS generation → audio playback → sample text support

🌀 Code to copy

```
import streamlit as st
from gtts import gTTS
import io

st.subheader("Text-to-Speech Converter (using Google TTS)")

text_input = st.text_area("Enter the text you want to convert to speech:")

language = st.selectbox(
    "Choose a language: 🇰🇷 🇺🇸 🇬🇧 🇷🇺 🇫🇷 🇪🇸 🇯🇵 ",
    [
        "Korean",
        "English (American)",
        "English (British)",
        "Russian",
        "Spanish",
        "French",
        "Japanese"
    ]
)

tts_button = st.button("Convert Text to Speech")

if tts_button and text_input:
    lang_codes = {
        "Korean": ("ko", None),
        "English (American)": ("en", "com"),
        "English (British)": ("en", "co.uk"),
        "Russian": ("ru", None),
        "Spanish": ("es", None),
        "French": ("fr", None),
        "Japanese": ("ja", None)
    }

    language_code, tld = lang_codes[language]

    if tld:
        tts = gTTS(text=text_input, lang=language_code, tld=tld, slow=False)
    else:
        tts = gTTS(text=text_input, lang=language_code, slow=False)

    speech = io.BytesIO()
    tts.write_to_fp(speech)
    speech.seek(0)

    st.audio(speech.getvalue(), format="audio/mp3")

st.markdown("---")
st.caption("🇺🇸 English text: Teacher-designed coding applications create tailored learning experiences, making complex concepts easier to understand through interactive and adaptive tools. They enhance engagement, provide immediate feedback, and support active learning.")
st.caption("🇰🇷 Korean text: 교사가 직접 만든 코딩 기반 애플리케이션은 학습자의 필요에 맞춘 학습 경험을 제공하고, 복잡한 개념을 쉽게 이해하도록 돕습니다. 또한 학습 몰입도를 높이고 즉각적인 피드백을 제공하며, 능동적인 학습을 지원합니다.")
st.caption("🇫🇷 French: Les applications de codage conçues par les enseignants offrent une expérience d'apprentissage personnalisée, rendant les concepts complexes plus faciles à comprendre grâce à des outils interactifs et adaptatifs. Elles améliorent l'engagement, fournissent un retour immédiat et soutiennent l'apprentissage actif.")
st.caption("🇷🇺 Russian: Созданные учителями кодированные приложения предлагают персонализированный опыт обучения, упрощая понимание сложных концепций с помощью интерактивных и адаптивных инструментов. Они повышают вовлеченность, предоставляют мгновенную обратную связь и поддерживают активное обучение.")
st.caption("🇨🇳 Chinese: 由教师设计的编程应用程序为学习者提供个性化的学习体验，通过互动和适应性工具使复杂的概念更容易理解。它们增强学习参与度，提供即时反馈，并支持主动学习。")
st.caption("🇯🇵 Japanese: 教師が設計したコーディングアプリケーションは、学習者のニーズに合わせた学習体験を提供し、複雑な概念をインタラクティブで適応性のあるツールを通じて理解しやすくします。また、学習への集中力を高め、即時フィードバックを提供し、主体的な学習をサポートします。")

```

#### 2. requirements.txt

+ A requirements.txt file is a simple text file that lists the Python packages needed for your app or project to run properly. When the app is deployed, the platform reads this file and installs the required libraries automatically.

+ In other words, this file tells the system, “These are the packages my code depends on.”

+ For example, if a Streamlit app uses Streamlit and Google Text-to-Speech, the requirements.txt file may look like this:

🌀 Code to copy

```
streamlit
gTTS
```

#### 3. More codes
[demo app](https://textreading.streamlit.app/)
##### <Ideas>
+ App Design Description: This app can be described through the following functional components:

1. Text input module:  
The app begins with a text box where the user pastes a passage. This serves as the main input area for all later processing.

2. Sentence segmentation module:  
After the text is entered, the app divides the passage into sentence units based on sentence-final punctuation. This allows the text to be handled not only as a whole passage but also as smaller selectable parts.

3. Sentence selection interface:  
The segmented sentences are presented in a dropdown menu. Each item is labeled with a sentence number and a short preview based on the first few words, making navigation simple and efficient.

4. Audio generation module:  
When a sentence is selected, the app converts that sentence into speech using a text-to-speech engine. This module provides immediate audio output for the chosen segment.

5. Passage display module:  
The full original passage is shown below the selection area so that the user can continue to view the text in its complete form.

6. Highlighting function:  
Within the full passage, the selected sentence is visually highlighted. This helps the user identify the exact location of the sentence in context.

7. Language selection option:  
The app includes a language selection feature for text-to-speech output. This allows the same interface to support multiple languages.

##### Compact summary

In design terms, the app consists of:

+ text input → sentence segmentation → dropdown selection → audio playback → full-text display → contextual highlighting

This structure makes the app easy to describe as a modular, interactive reading and listening support tool.

🌀 Code to copy

```
import streamlit as st
import re
import io
import html
from gtts import gTTS

st.set_page_config(page_title="Sentence TTS Highlighter", layout="wide")

st.title("Sentence TTS Highlighter")
st.caption("Paste a passage, select a sentence, play its audio, and see where it appears in the full text.")

# ---------- Functions ----------
def split_into_sentences(text: str):
    text = text.strip()
    if not text:
        return []

    # Split by sentence-ending punctuation while keeping the punctuation
    parts = re.split(r'(?<=[.!?])\s+', text)
    sentences = [p.strip() for p in parts if p.strip()]
    return sentences

def make_label(idx: int, sentence: str, max_words: int = 5):
    words = sentence.split()
    preview = " ".join(words[:max_words])
    if len(words) > max_words:
        preview += " ..."
    return f"{idx + 1}. {preview}"

def highlight_selected_sentence(full_text: str, selected_sentence: str):
    escaped_full = html.escape(full_text)
    escaped_selected = html.escape(selected_sentence)

    highlighted = escaped_full.replace(
        escaped_selected,
        f"<mark style='background-color: #fff3a3; padding: 0.1em 0.2em; border-radius: 4px;'>{escaped_selected}</mark>",
        1
    )

    highlighted = highlighted.replace("\n", "<br>")
    return highlighted

def generate_tts_bytes(text: str, lang: str = "en", tld: str = "com"):
    audio_buffer = io.BytesIO()
    tts = gTTS(text=text, lang=lang, tld=tld, slow=False)
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer.getvalue()

# ---------- Input ----------
text_input = st.text_area(
    "Paste your text here:",
    height=220,
    placeholder="Paste a passage here. The app will split it into sentences."
)

col1, col2 = st.columns([2, 1])

with col2:
    language_option = st.selectbox(
        "TTS language",
        ["English (American)", "English (British)", "Korean", "French", "Spanish", "Japanese"]
    )

lang_settings = {
    "English (American)": ("en", "com"),
    "English (British)": ("en", "co.uk"),
    "Korean": ("ko", None),
    "French": ("fr", None),
    "Spanish": ("es", None),
    "Japanese": ("ja", None),
}

# ---------- Main ----------
if text_input.strip():
    sentences = split_into_sentences(text_input)

    if sentences:
        labels = [make_label(i, s) for i, s in enumerate(sentences)]
        label_to_sentence = dict(zip(labels, sentences))

        with col1:
            selected_label = st.selectbox(
                "Select a sentence:",
                labels
            )

        selected_sentence = label_to_sentence[selected_label]

        st.markdown("### Selected sentence")
        st.write(selected_sentence)

        lang_code, tld = lang_settings[language_option]

        try:
            if tld:
                audio_bytes = generate_tts_bytes(selected_sentence, lang=lang_code, tld=tld)
            else:
                audio_bytes = generate_tts_bytes(selected_sentence, lang=lang_code)

            st.audio(audio_bytes, format="audio/mp3")
        except Exception as e:
            st.error(f"Audio generation failed: {e}")

        st.markdown("### Full passage")
        highlighted_html = highlight_selected_sentence(text_input, selected_sentence)
        st.markdown(
            f"""
            <div style="
                border: 1px solid #ddd;
                padding: 16px;
                border-radius: 10px;
                line-height: 1.8;
                font-size: 1.05rem;
                background-color: #fafafa;">
                {highlighted_html}
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.expander("Show sentence list"):
            for i, s in enumerate(sentences, start=1):
                st.write(f"{i}. {s}")

    else:
        st.warning("No sentences were detected. Please check the text.")
else:
    st.info("Paste a passage above to begin.")
```
