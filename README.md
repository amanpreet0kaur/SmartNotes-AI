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



## 📸 Screenshots 


* Upload page
  ![image](https://github.com/user-attachments/assets/f14a0a3b-8183-4de5-92b6-2e189cac6e99)

* Summary view
  ![image](https://github.com/user-attachments/assets/8c7ac243-f556-4e70-b757-da64348ea45a)

* Flashcard view
  ![image](https://github.com/user-attachments/assets/7dac7e96-c2a2-46fc-a0cd-2abbd365f4f6)

* QA interaction
  ![image](https://github.com/user-attachments/assets/37a91163-4e53-4a01-ab46-687decfc6c22)


---


