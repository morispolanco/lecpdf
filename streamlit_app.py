import streamlit as st
import pdfplumber
import openai
import os

# Load GPT-3 API key from secrets
openai.api_key = os.getenv("OPENAI_API_KEY")

# Function to read and extract text from PDF
def read_pdf(file):
    with pdfplumber.open(file) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
    return text

# Function to split text into chunks
def split_text(text, chunk_size):
    chunks = []
    for i in range(0, len(text), chunk_size):
        chunks.append(text[i:i+chunk_size])
    return chunks

# Main app
def main():
    st.title("PDF Reader and Question Answering App")
    
    # File upload
    uploaded_file = st.file_uploader("Upload PDF", type="pdf")
    
    if uploaded_file is not None:
        # Read PDF and extract text
        text = read_pdf(uploaded_file)
        
        # Split text into chunks
        chunk_size = 1000
        chunks = split_text(text, chunk_size)
        
        # Question input
        question = st.text_input("Enter your question")
        
        if st.button("Ask"):
            # Use GPT-3 to answer question
            answer = openai.Completion.create(
                engine="davinci",
                prompt=question,
                max_tokens=100,
                temperature=0.7,
                n=1,
                stop=None,
                log_level="info"
            )
            
            st.write("Answer:", answer.choices[0].text)
    
if __name__ == "__main__":
    main()






