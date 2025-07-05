from PyPDF2 import PdfReader
from utils.helpers import chunk_text_by_tokens

def parse_pdf(uploaded_file, chunk_size=200, overlap=50):
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    chunks = chunk_text_by_tokens(text, chunk_size, overlap)
    return chunks
