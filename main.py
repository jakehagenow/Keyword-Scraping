import streamlit as st 
from scrape import scrape_website, create_prompt #, clean_body_content #, extract_body_content

def scrape_button():
    st.session_state.scrape = True

if "scrape" not in st.session_state:
    st.session_state.scrape = False

st.title("IE Web Scraper V1")
starting_url = st.text_input("Enter a website URL:")
keywords = st.text_input("Enter keywords to search for separated by ',': ")

st.button("Scrape Site", on_click=scrape_button)
if st.session_state.scrape:
    st.write(f"Scraping the Website: {starting_url}")
    st.write(f"Searching for {keywords}...")
    
    result = scrape_website(starting_url, keywords)
    
    # st.session_state.dom_content = result

    with st.expander("View Site Text"):
        # st.write("Site Text", result["text"])
        st.text_area("Site Text", result["text"], height=300)
    with st.expander("View Site Links"):
        st.write("Site Links", result["links"])
    with st.expander("View Relevant Text and Links"):
        st.write("Relevant Finds:", result['found'])

    print("Attempting to Create Prompt...")
    try:
        prompt_result = create_prompt(result['found'])
        if prompt_result:
            with st.expander("View Prompt"):
                st.text_area("Prompt for LLM", prompt_result, height=600)
    except:
        print("Could not call function...")

# url to test with : https://knocking.wiche.edu/pandemic-ed-pipeline-challenges/


