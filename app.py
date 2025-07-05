
import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from backend.pdf_parser import parse_pdf
from backend.embeddings import EmbeddingsIndex

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

st.set_page_config(page_title="📄 Chat with Your Notes", layout="wide")
st.title("📄 Chat with Your Notes 🤖")
st.write(
    "Upload your **PDF notes** and chat with them using Gemini!"
)

with st.sidebar:
    st.markdown("## 💡 How to Use")
    st.info(
        """
        1️⃣ Upload your PDF notes  
        2️⃣ Ask questions in the chat box  
        3️⃣ Gemini will answer using relevant sections  
        """
    )
    st.markdown("----")
    st.caption("Built with ❤️ using Streamlit + Gemini")

uploaded_file = st.file_uploader("📎 Upload a PDF", type=["pdf"], key="fileupload")

if uploaded_file:
    with st.spinner("📝 Parsing your PDF..."):
        chunks = parse_pdf(uploaded_file)
    st.success(f"✅ Extracted {len(chunks)} chunks from **{uploaded_file.name}**")

    if "history" not in st.session_state:
        st.session_state["history"] = []

    if "index" not in st.session_state:
        progress = st.progress(0, text="Building semantic index...")
        index = EmbeddingsIndex()
        index.build_index(chunks)
        st.session_state["index"] = index
        st.session_state["chunks"] = chunks
        progress.empty()
    else:
        index = st.session_state["index"]

    with st.expander("🔍 Preview first 3 extracted chunks"):
        for i, chunk in enumerate(chunks[:3]):
            st.write(f"**Chunk {i+1}:** {chunk[:300]}...")

    chat_container = st.container()
    with chat_container:
        for chat in st.session_state["history"]:
            if chat["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(f"**🧑‍💻 You:** {chat['content']}")
            else:
                with st.chat_message("assistant"):
                    st.markdown(f"**🤖 Gemini:** {chat['content']}")

    question = st.chat_input(
        "Type your question and press Enter to ask Gemini..."
    )

    if question:
        st.session_state["history"].append({"role": "user", "content": question})

        with st.chat_message("user"):
            st.markdown(f"**🧑‍💻 You:** {question}")

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            with st.spinner("🤖 Gemini is thinking..."):
                top_chunks = index.search(question)
                context = "\n\n".join(top_chunks)
                prompt = f"""
                Use these notes to answer the question in a helpful way:

                Notes:
                {context}

                Question:
                {question}
                """
                response = model.generate_content(prompt)
                answer = response.text
                message_placeholder.markdown(f"**🤖 Gemini:** {answer}")

        st.session_state["history"].append({"role": "assistant", "content": answer})
