# SmartNotes-AI


🧠 Document Insight Assistant
This is a Flask-based web application that allows users to:

Extract text from PDFs using Google Document AI

Ask questions using a Groq-powered LLM QA agent

Generate concise summaries of the uploaded documents

Create flashcards for quick learning and revision

Interact via a simple web interface

🚀 Features
📄 PDF Upload & OCR using Google Document AI

🧠 Semantic Search with FAISS & Sentence Transformers

💬 LLM-Powered QA Agent using llama3-70b-8192 from Groq API

📝 Auto Summary Generator

🎓 Flashcard Creator (Q/A pairs) for study & revision

🌐 Clean web interface built using Flask templates

📁 Folder Structure
css
Copy code
project/
├── app.py                   # Main Flask app
├── templates/
│   ├── home.html
│   ├── qa.html
│   ├── flashcards.html
│   └── summary.html
├── requirements.txt
└── README.md
