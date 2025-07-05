from typing import List
import tiktoken

def chunk_text_by_tokens(text: str, chunk_size: 200, overlap: 50) -> List[str]:
    enc = tiktoken.get_encoding("gpt2") 
    tokens = enc.encode(text)
    
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk = tokens[start:end]
        chunk_text = enc.decode(chunk)
        chunks.append(chunk_text)
        start += chunk_size - overlap 
    return chunks

