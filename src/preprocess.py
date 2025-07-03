from pathlib import Path
from PyPDF2 import PdfReader
import re
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_pdf(file_path):
    reader = PdfReader(r"C:\Users\Admin\Desktop\project1\AI_Assignment_Rohit_Garg_Fresher.pdf")
    raw_text = ""
    for page in reader.pages:
        raw_text += page.extract_text() + "\n"
    return raw_text

def clean_text(text):
    return re.sub(r"\s+", " ", text).strip()

def chunk_text(text, chunk_size=1000, chunk_overlap=100):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", ".", " "],
    )
    return splitter.split_text(text)

def save_chunks(chunks, output_dir="chunks"):
    Path(output_dir).mkdir(exist_ok=True)
    for i, chunk in enumerate(chunks):
        with open(f"{output_dir}/chunk_{i}.txt", "w", encoding="utf-8") as f:
            f.write(chunk)

if __name__ == "__main__":
    text = load_pdf("data/AI_Training_Document.pdf")
    text = clean_text(text)
    chunks = chunk_text(text)
    save_chunks(chunks)
    print(f" {len(chunks)} chunks saved to /chunks")
