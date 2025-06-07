# SmartNotes-AI



---

# 🧠 Document Insight Assistant

This is a Flask-based web application that allows users to:

* Extract text from PDFs using **Google Document AI**
* Ask questions using a **Groq-powered LLM QA agent**
* Generate concise **summaries** of the uploaded documents
* Create **flashcards** for quick learning and revision
* Interact via a simple **web interface**

---

## 🚀 Features

* 📄 **PDF Upload & OCR** using Google Document AI
* 🧠 **Semantic Search** with FAISS & Sentence Transformers
* 💬 **LLM-Powered QA Agent** using `llama3-70b-8192` from Groq API
* 📝 **Auto Summary Generator**
* 🎓 **Flashcard Creator** (Q/A pairs) for study & revision
* 🌐 Clean web interface built using Flask templates

---

## 📁 Folder Structure

```
project/
├── app.py                   # Main Flask app
├── templates/
│   ├── home.html
│   ├── qa.html
│   ├── flashcards.html
│   └── summary.html
├── requirements.txt
└── README.md
```

---

## 🛠️ Setup Instructions

### ✅ Prerequisites

* Python 3.8+
* Google Cloud Project with **Document AI** enabled
* Groq API key


## 💡 How It Works

1. **Upload PDF** → Text is extracted via Google Document AI
2. **Build Embeddings** → Text is chunked and vectorized via SentenceTransformer
3. **Ask Questions** → Query is embedded and matched using FAISS, Groq LLM answers
4. **Summarize** → Groq summarizes document
5. **Flashcards** → Groq generates flashcards from extracted text

---

## 🔍 Available Endpoints

| Method | Endpoint           | Description                            |
| ------ | ------------------ | -------------------------------------- |
| GET    | `/`                | Home page                              |
| POST   | `/upload`          | Upload and process a PDF               |
| POST   | `/ask`             | Ask a question about the document      |
| GET    | `/summary`         | Get a summary of the uploaded document |
| GET    | `/flashcards`      | Generate 5 flashcards from the text    |
| GET    | `/summary_page`    | Summary UI page                        |
| GET    | `/flashcards_page` | Flashcard UI page                      |
| GET    | `/qa_page`         | QA UI page                             |

---

## 📦 Dependencies

```txt
Flask
google-cloud-documentai
sentence-transformers
faiss-cpu
numpy
requests
textwrap
```

---



## 📸 Screenshots (optional)

Include screenshots of:

* Upload page
* Summary view
* Flashcard view
* QA interaction

---


