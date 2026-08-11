import streamlit as st
from pypdf import PdfReader
from google import genai

client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

st.title("📄 AI Document Assistant")

uploaded_file = st.file_uploader("Upload a PDF document", type=["pdf"])

if uploaded_file is not None:
    reader = PdfReader(uploaded_file)
    pdf_text = ""
    for page in reader.pages:
        pdf_text += page.extract_text() or ""
    
    st.success("PDF uploaded and extracted successfully!")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Summarize Document"):
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"Summarize the following document accurately:\n\n{pdf_text}"
            )
            st.write(response.text)
            
    with col2:
        if st.button("Generate Interview Questions"):
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=f"Generate 5 interview questions based on this document:\n\n{pdf_text}"
            )
            st.write(response.text)
            
    st.divider()
    
    user_question = st.text_input("Ask a question about the PDF:")
    if st.button("Submit Question"):
        if user_question:
            # Combine Document Content + User Question
            prompt = f"Answer the user's question using ONLY the context provided below.\n\nContext:\n{pdf_text}\n\nQuestion: {user_question}"
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt
            )
            st.subheader("Answer:")
            st.write(response.text)
