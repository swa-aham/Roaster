import streamlit as st
from streamlit_extras.add_vertical_space import add_vertical_space
from helper import *

# Heading
st.markdown("""
<style>
    #MainMenu
    {
        visibility: hidden;
    }
</style>
""", unsafe_allow_html=True)
st.markdown("""
Powered by [Resumify](https://resumify-black.vercel.app/)\n
""", unsafe_allow_html=True)
st.title("Roaster 😈")
st.write("Upload you resume & get funny & sarcastic comments. Roast yourself")

# Sidebar
with st.sidebar:
    st.title('Roaster 😈')
    st.markdown('''
    ## About
    Roast your resume.
    Upload your resume and get funny & sarcastic comments.
    
    Part of the [Resumify](https://resumify-black.vercel.app/)
    
    ''')
    add_vertical_space(5)
    st.write('By [Soham](https://www.linkedin.com/in/soham-mandaviya/)')


def main():
    # upload a PDF file
    uploaded_file = st.file_uploader("Choose a PDF", type="pdf")
    lang = st.text_input("Enter language (Optional, default: English)")

    if uploaded_file is not None:
        # Save uploaded file to a temporary location
        with open("uploaded_temp.pdf", "wb") as temp_file:
            temp_file.write(uploaded_file.read())

        # Extract text using the provided function
        extracted_text = read_pdf("uploaded_temp.pdf")

        if extracted_text:
            st.write(get_gemini_response(extracted_text, lang))


if __name__ == '__main__':
    main()
