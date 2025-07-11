
# 🎙️ Audio/Video to Article Generator (AI-Powered Workflow)

This project transforms your audio or video files into polished, publish-ready articles using a modular AI pipeline that includes transcription, article generation, style enforcement, and scoring.

--------------------------------------------------------------------------------------------------------

## 🚀 Features

- 🎧 **Audio/Video Input** (`.mp3`, `.wav`, `.mp4`, `.mkv`)
- 📝 **Automatic Transcription** using Whisper or AssemblyAI
- ✍️ **Article Draft Generation** using Google Gemini LLM
- 📐 **Style Enforcer** to apply tone/clarity rules
- 📊 **BERT-based Scoring** to evaluate writing quality
- 🌐 **Streamlit Web Interface** for easy use

--------------------------------------------------------------------------------------------------------

## 🧠 Project Workflow

```mermaid
graph LR
A[Audio/Video Upload] --> B[Transcription (Whisper/AssemblyAI)]
B --> C[Article Generator (Gemini)]
C --> D[Style Enforcer]
D --> E[BERT-based Scoring]
E --> F[Publish-Ready Article]
```

--------------------------------------------------------------------------------------------------------

## 📦 Installation

### 1. Clone the repo
```bash
git clone https://github.com/your-username/audio-to-article-generator.git
cd audio-to-article-generator
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

--------------------------------------------------------------------------------------------------------

## 📁 Project Structure

```
├── app.py                      # Streamlit frontend
├── transcription/
│   └── assembly_ai.py         # AssemblyAI transcription logic
├── generation/
│   └── gemini_generator.py    # Article generation using Gemini
├── style_check/
│   └── style_enforcer.py      # Style rule enforcement
├── scoring/
│   └── bert_scorer.py         # BERT-based scoring module
├── utils/
│   └── helpers.py             # File type handlers, audio extraction
├── .env                       # Store API keys securely
├── README.md
└── requirements.txt
```

--------------------------------------------------------------------------------------------------------

## 🔐 Environment Setup

Create a `.env` file with the following:

```env
GEMINI_API_KEY=your_google_gemini_api_key
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
```

--------------------------------------------------------------------------------------------------------

## ▶️ Usage

Start the Streamlit app:

```bash
streamlit run app.py
```

1. Upload your audio or video file.
2. Watch as the app transcribes, drafts, styles, and scores your article.
3. Download or copy the final publish-ready version.

--------------------------------------------------------------------------------------------------------

## 🛠️ Tech Stack

- Python
- Streamlit
- Whisper / AssemblyAI (Speech-to-text)
- Gemini (LLM for article generation)
- BERT (Scoring)
- MoviePy (audio extraction)

--------------------------------------------------------------------------------------------------------

## ✨ Future Enhancements

- 📷 Auto image generation based on article context
- 🌍 Multilingual support
- 🔗 Direct publishing to Notion, Medium, or LinkedIn

--------------------------------------------------------------------------------------------------------

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first to discuss what you’d like to change.

--------------------------------------------------------------------------------------------------------

## 📄 License

[MIT License](LICENSE)

--------------------------------------------------------------------------------------------------------

## 💬 Connect

Feel free to reach out or connect on [LinkedIn](https://www.linkedin.com/in/prathap-elumalai-8abaa3250).
