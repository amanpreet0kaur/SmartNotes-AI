from flask import Flask, request, jsonify, render_template
from google.api_core.client_options import ClientOptions
from google.cloud import documentai_v1
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import textwrap
import requests
import tempfile
import os

app = Flask(__name__)

# Document AI config
project_id = "wise-env-461717-t5"
processor_id = "86a7eec52bbb9616"
location = "us"

opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")
client = documentai_v1.DocumentProcessorServiceClient(client_options=opts)
full_processor_name = client.processor_path(project_id, location, processor_id)

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

GROQ_API_KEY = "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"

text_chunks = []
index = None

def chunk_text(text, max_chars=500):
    return textwrap.wrap(text, max_chars)

def extract_text_with_documentai(file_path):
    with open(file_path, "rb") as f:
        content = f.read()
    raw_document = documentai_v1.RawDocument(content=content, mime_type="application/pdf")
    request = documentai_v1.ProcessRequest(name=full_processor_name, raw_document=raw_document)
    result = client.process_document(request=request)
    document = result.document
    return document.text

def build_index(text):
    global index, text_chunks
    text_chunks = chunk_text(text)
    embeddings = embed_model.encode(text_chunks)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings))

def retrieve_context(query, top_k=5):
    query_embed = embed_model.encode([query])
    distances, indices = index.search(np.array(query_embed), top_k)
    return [text_chunks[i] for i in indices[0]]

def ask_groq_agent(query, context):
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
    )
    return response.json()["choices"][0]["message"]["content"]

@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")

@app.route("/upload", methods=["POST"])
def upload_pdf():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    if not file.filename.lower().endswith(".pdf"):
        return jsonify({"error": "Only PDF files are supported"}), 400

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        file.save(tmp_file.name)
        temp_path = tmp_file.name

    try:
        text = extract_text_with_documentai(temp_path)
        build_index(text)
    except Exception as e:
        os.unlink(temp_path)
        return jsonify({"error": f"Failed processing file: {str(e)}"}), 500

    os.unlink(temp_path)
    return jsonify({"message": "File processed and index built successfully"})

@app.route("/ask", methods=["POST"])
def qa_agent():
    global index
    if index is None:
        return jsonify({"error": "No index found. Please upload a PDF first via /upload"}), 400

    data = request.json
    question = data.get("question")
    if not question:
        return jsonify({"error": "Missing 'question' in request"}), 400

    context = "\n\n".join(retrieve_context(question))
    answer = ask_groq_agent(question, context)
    return jsonify({"question": question, "answer": answer})

def get_summary(text):
    prompt = f"Please provide a concise summary of the following document:\n\n{text[:4000]}"
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3
        }
    )
    return response.json()["choices"][0]["message"]["content"]
@app.route("/summary", methods=["GET"])
def summary():
    global text_chunks
    if not text_chunks:
        return jsonify({"error": "No text found. Please upload a PDF first."}), 400
    combined_text = " ".join(text_chunks)
    summary = get_summary(combined_text)
    return jsonify({"summary": summary})

@app.route("/flashcards", methods=["GET"])
def generate_flashcards():
    global text_chunks
    if not text_chunks:
        return jsonify({"error": "No document available. Upload first."}), 400

    joined_text = "\n".join(text_chunks)
    prompt = (
        "Generate 5 helpful flashcards from the following content. "
        "Use the format exactly like this:\n\n"
        "Q: What is ...?\nA: ...\n\nQ: How does ...?\nA: ...\n\n"
        "Text:\n" + joined_text
    )
    
    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
        json={
            "model": "llama3-70b-8192",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.5
        }
    )

    if response.status_code != 200:
        return jsonify({"error": "Groq API error"}), 500

    content = response.json()["choices"][0]["message"]["content"]

    # Split by question/answer blocks
    lines = content.strip().splitlines()
    flashcards = []
    question = None
    for line in lines:
        line = line.strip()
        if line.lower().startswith("q:"):
            question = line[2:].strip()
        elif line.lower().startswith("a:") and question:
            answer = line[2:].strip()
            flashcards.append({"question": question, "answer": answer})
            question = None

    return jsonify({"flashcards": flashcards})
@app.route("/summary_page")
def summary_page():
    return render_template("summary.html")

@app.route("/flashcards_page")
def flashcards_page():
    return render_template("flashcards.html")

@app.route("/qa_page")
def qa_page():
    return render_template("qa.html")



if __name__ == "__main__":
    app.run(debug=True)
