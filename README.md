# 📄 Chat with Your Notes

A Streamlit-powered web application that lets you upload your PDF notes and interactively ask questions about them using Gemini models, with a retrieval-augmented pipeline for more relevant answers.

---

## 🚀 Features

- Upload a PDF up to 200 MB
- Chunking with token-overlapping to preserve context
- Embeddings-based semantic search
- Gemini generative AI answers
- Chat-like interface with conversation history

---

## 🛠️ Tech Stack

- **Streamlit** (UI)
- **PyPDF2** (PDF parsing)
- **scikit-learn** (TF-IDF embedding search)
- **Google Generative AI (Gemini)** (generative answers)
- **Python** 3.10+ **is required**

---

## ⚙️ Installation

Clone this repository:

```bash
git clone https://github.com/Navkanj/chat-with-your-notes.git
cd chat-with-your-notes
```
Install dependencies:

```bash
pip install -r requirements.txt
```

Create a .env file with your Gemini API key:

```bash
GOOGLE_API_KEY=your_api_key_here
```

🚀 Running the App
```bash
streamlit run app.py
```
