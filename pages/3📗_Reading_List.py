import streamlit as st
import requests

# Set the page title
st.set_page_config(page_title="Readings and in-class discussion")

# st.title("Project Dashboard")
# st.caption("Readings and discussions")

# 1. Define the tab names
tab_labels = ["🏠 Reading list", "Core idea", "💦 In-class presentation", "🖼️ Infographics", ]

# 2. Create the tabs
tab1, tab2, tab3, tab4 = st.tabs(tab_labels)

# 3. Add placeholders for content
with tab1:
    st.markdown("### 🔖 Reading list")
    st.caption("To be updated continuously")
    st.markdown("""
      
      + Reading #1: Translanguaging [Li, Wei (2018)](https://www.researchgate.net/publication/323720294_Translanguaging_as_a_Practical_Theory_of_Language)
      + Reading #2: Alignment issues [Curry et al. (2025)](https://github.com/MK316/Applied-linguistics/raw/main/readings/02_Curry_etal_2025.pdf)
      + Reading #3: [Jacob, S. R. & M. Warschauer](https://www.researchgate.net/publication/327217492_Computational_Thinking_and_Literacy) (2018). Computational Thinking and Literacy. _Journal of Computer Science Integration_, 1(1).
      + Reading #4: [UNESCO](https://www.unesco.org/en/digital-education/artificial-intelligence) (2025) _AI in education_.
      + Reading #5: [Zawacki-Richter et al. (2019)](https://www.researchgate.net/publication/336846972_Systematic_review_of_research_on_artificial_intelligence_applications_in_higher_education_-where_are_the_educators) Zawacki-Richter, O., Marín, V. I., Bond, M., & Gouverneur, F. (2019). Systematic review of research on artificial intelligence applications in higher education. _International Journal of Educational Technology in Higher Education_, 16(1), 1–27. https://doi.org/10.1186/s41239-019-0171-0
      + Reading #6: [Jeon et al.](https://www.researchgate.net/publication/394128596_Generative_AI_and_its_dilemmas_Exploring_AI_from_a_translanguaging_perspective) (2025). Generative AI and its dilemmas: exploring AI from a translanguaging perspective. _Applied Linguistics_, 46, 709-717.
      + Reading #7: [Mishra & Koehler (2006)](https://rediie.cl/wp-content/uploads/Mishra-Koehler.pdf) Mishra, P., & Koehler, M. J. (2006). Technological pedagogical content knowledge: A framework for teacher knowledge. _Teachers College Record_, 108(6), 1017–1054. https://doi.org/10.1111/j.1467-9620.2006.00684.x
    
      📗 Spplementary book: _An Introduction to Applied Linguistics_ (2007; 2nd ed.) by A. Davies, Edinburgh University Press.
      """)
with tab2:
    st.markdown("### Core Idea")
    
    # 1. GitHub Raw URL 설정 (blob 대신 raw.githubusercontent.com 사용)
    # 주의: 링크 주소에서 'blob/'을 삭제하고 도메인을 변경해야 합니다.
    url = "https://raw.githubusercontent.com/MK316/Applied-linguistics/main/mdfiles/Core-idea.md"
    
    try:
        # 2. GitHub로부터 마크다운 내용 가져오기
        response = requests.get(url)
        if response.status_code == 200:
            md_content = response.text
            # 3. 가져온 내용을 Streamlit에 렌더링
            st.markdown(md_content)
        else:
            st.error(f"파일을 불러오지 못했습니다. (Status Code: {response.status_code})")
    except Exception as e:
        st.error(f"오류가 발생했습니다: {e}")

with tab3:
    # st.caption("Fetching the latest documentation from Github [Collaboration26](https://github.com/MK316/Collaboration26).")

    # ✅ Use the RAW URL to get the text content directly
    readme_url = "https://raw.githubusercontent.com/MK316/Collaboration26/main/README.md"

    try:
        response = requests.get(readme_url)
        if response.status_code == 200:
            # Render the fetched text as Markdown
            st.markdown(response.text)
        else:
            st.error(f"Failed to load the README file. (HTTP {response.status_code})")
            st.info("Check if the repository is public and the URL is correct.")
    except Exception as e:
        st.error(f"An error occurred while fetching the file: {e}")

with tab4:
    # st.header("🖼️ Infographics")
    # st.write("Select an image from the repository to view it.")

    # 1. Define your images (Replace these with your actual filenames and raw links)
    # Format: "Display Name": "Raw GitHub URL"
    image_options = {
        "Select an image...": None,
        "Supplementary book Chapter 1": "https://raw.githubusercontent.com/MK316/Collaboration26/main/infographic/CH01_infographic.png",
        "Reading #1": "https://raw.githubusercontent.com/MK316/Collaboration26/main/infographic/Reading01_infographic.png",
        "Reading #2": "https://raw.githubusercontent.com/MK316/Collaboration26/main/infographic/Reading02_infographic.png",
        "Reading #3": "https://raw.githubusercontent.com/MK316/Collaboration26/main/infographic/Reading03_infographic.png",
        "Reading #4": "https://raw.githubusercontent.com/MK316/Collaboration26/main/infographic/Reading04_infographic.png",
        "Reading #5": "https://raw.githubusercontent.com/MK316/Collaboration26/main/infographic/Reading05_infographic.png",
        "Reading #6": "https://raw.githubusercontent.com/MK316/Collaboration26/main/infographic/Reading06_infographic.png",
    }

    # 2. Create the dropdown box
    selected_image_name = st.selectbox("Choose an image to display:", options=list(image_options.keys()))

    # 3. Display the selected image
    if selected_image_name and image_options[selected_image_name]:
        image_url = image_options[selected_image_name]
        
        st.divider()
        st.subheader(f"Viewing: {selected_image_name}")
        
        # use_container_width=True makes the image fit the tab width automatically
        st.image(image_url, caption=f"Source: {selected_image_name}", use_container_width=True)
        
        # Optional: Add a download link or direct link
        st.caption(f"[Open original image in new tab]({image_url})")
    else:
        st.info("Please select an image from the dropdown menu above.")
