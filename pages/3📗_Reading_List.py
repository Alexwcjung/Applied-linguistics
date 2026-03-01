import streamlit as st

# Set the page title
st.set_page_config(page_title="Readings and in-class discussion")

# st.title("Project Dashboard")
st.caption("Readings and discussions")

# 1. Define the tab names
tab_labels = ["🏠 Reading list", "📂 Discussions", "⚙️ In-class presentation"]

# 2. Create the tabs
tab1, tab2, tab3 = st.tabs(tab_labels)

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
    st.header("Discussions")
    st.info("This is where your GitHub repositories will be listed.")

with tab3:
    st.header("In-class presentation")
    st.caption("Fetching the latest documentation from Github 'Collaboration26'.")

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


