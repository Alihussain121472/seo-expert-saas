# 🚀 SEO Expert SaaS - AI-Powered SEO Management Platform

Welcome to **SEO Expert**, a professional, fully-automated SaaS platform designed to act as your dedicated AI SEO specialist. 

Simply provide a website URL, and our intelligent backend automatically crawls the page, analyzes technical and on-page SEO factors using Google's **Gemini AI**, and builds a prioritized list of actionable recommendations directly on your dashboard.

## ✨ Key Features

- 🤖 **AI SEO Manager:** Chat naturally with the built-in AI agent. It reads your database securely and gives customized advice based on your connected websites.
- 🌐 **Multi-Language Support:** The AI perfectly understands and communicates in **English, Urdu, and Roman Urdu** (e.g., *"Meri website ka SEO kaisa hai?"*).
- 📊 **Automated Audits:** Instantly generates Technical SEO, On-Page SEO, and overall Health Scores completely in the background via FastAPI's background tasks.
- 📱 **Mobile-First UI:** A beautiful, highly responsive dashboard built with Next.js and Tailwind CSS.
- 🔒 **Privacy First:** Your API keys, local databases, and sensitive configuration files are strictly ignored by Git and remain private to your local environment.

## 🛠️ Technology Stack

**Frontend:**
- [Next.js (App Router)](https://nextjs.org/)
- TypeScript
- Tailwind CSS
- React

**Backend:**
- [FastAPI](https://fastapi.tiangolo.com/) (Python)
- [LangChain](https://python.langchain.com/) & Google Gemini Pro (AI Agents)
- SQLAlchemy & PostgreSQL / SQLite
- PyJWT & Passlib (Authentication)
- BeautifulSoup4 (Web Crawler)

**Deployment:**
- Docker & Docker Compose configured for instant SaaS deployment.

## 🚀 How to Run Locally

### 1. Prerequisites
- Node.js (v18+)
- Python (v3.11+)
- A Google Gemini API Key

### 2. Backend Setup
```bash
cd backend
python -m venv venv
# Activate the virtual environment (Windows: .\venv\Scripts\activate, Mac/Linux: source venv/bin/activate)
pip install -r requirements.txt
pip install email-validator langchain-google-genai psycopg2-binary
```
Set your API key in your terminal:
```bash
export GOOGLE_API_KEY="your_gemini_api_key_here" # For Linux/Mac
$env:GOOGLE_API_KEY="your_gemini_api_key_here"   # For Windows PowerShell
```
Start the backend server:
```bash
uvicorn main:app --port 8000 --reload
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Access the App
Open your browser and navigate to **[http://localhost:3000](http://localhost:3000)** to view the dashboard!

## 🔐 Security Notice
This repository is configured with a strict `.gitignore` to ensure **no sensitive files** (such as `.env` files, local `sql_app.db` database files, or `venv` packages) are accidentally published. The core code is open for professional display, while all your proprietary data remains completely private.
