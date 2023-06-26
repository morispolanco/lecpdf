import streamlit as st
import pdfplumber
import openai
import os

# Load GPT-3 API key from secrets
openai.api_key = os.getenv["OPENAI_API_KEY"]

# Function to upload PDFs
def upload_pdf():
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    if uploaded_file is not None:
        return pdfplumber.open(uploaded_file)

# Function to read PDFs
def read_pdf(pdf):
    text = ""
    for page in pdf.pages:
        text += page.extract_text()
    return text

# Function to ask questions using GPT-3
def ask_question(text):
    response = openai.Completion.create(
        engine="davinci",
        prompt=text,
        max_tokens=100,
        n=1,
        stop=None,
        temperature=0.7,
    )
    return response.choices[0].text.strip()

# Main app
def main():
    st.title("PDF Question Answering App")
    pdf = upload_pdf()
    if pdf is not None:
        text = read_pdf(pdf)
        question = st.text_input("Ask a question")
        if st.button("Ask"):
            answer = ask_question(question + " " + text)
            st.write("Answer:", answer)

if __name__ == "__main__":
    main()
