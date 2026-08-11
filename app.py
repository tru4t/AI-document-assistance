import streamlit as st
from pypdf import PdfReader
import google.generativeai as genai

# Configure API key
api_key = st.secrets["GOOGLE_API_KEY"]
genai.configure(api_key=api_key)

# Initialize model
model = genai.GenerativeModel("models/gemini-3.5-flash")

st.title("📄 AI Document Assistant")

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text() or ""
    
    st.success("PDF uploaded and extracted successfully!")
    col1, col2 = st.columns(2)

    # Summarize Document
    with col1:
        if st.button("Summarize Document"):
            response = model.generate_content(
                f"Summarize the following document accurately:\n\n{pdf_text}"
            )
            st.write(response.text)
            
    # Generate Interview Questions
    with col2:
        if st.button("Generate Interview Questions"):
            response = model.generate_content(
                f"Generate 5 interview questions based on this document:\n\n{pdf_text}"
            )
            st.write(response.text)
            
    st.divider()
    
    # Custom Question
    user_question = st.text_input("Ask a question about the PDF:")
    if st.button("Submit Question"):
        if user_question:
            prompt = f"Answer the user's question using ONLY the context provided below.\n\nContext:\n{pdf_text}\n\nQuestion: {user_question}"
            response = model.generate_content(prompt)
            st.subheader("Answer:")
            st.write(response.text)
