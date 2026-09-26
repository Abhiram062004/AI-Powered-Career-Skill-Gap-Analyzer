# 🎯 AI-Powered Career Skill Gap Analyzer

A Flask web application that analyzes a resume against a target career, identifies matched and missing skills, calculates an ATS/readiness score, and helps users close their skill gaps — with optional AI-powered analysis, AI resume rewriting, and live job search for Kerala, India.

## ✨ Features

- **Resume Upload & Parsing** — Supports PDF, DOCX, PNG, JPG, and JPEG resumes, with OCR fallback for scanned documents (Tesseract).
- **Skill Gap Analysis** — Deterministic rule-based analyzer that matches resume content against required skills for a chosen career.
- **ATS & Readiness Scoring** — Quantifies how well a resume aligns with a target role.
- **Optional AI Analysis** — Uses OpenAI (if configured) to generate strengths, gaps, recommendations, and interview focus areas, with a rule-based fallback when no API key is set.
- **AI Resume Rewriting** — Rewrites resume content for a target role without fabricating experience or skills.
- **Live Job Search** — Integrates with the Adzuna Jobs API to search current openings across Kerala districts.
- **Careers & Learning Resources** — Browse career profiles with required skills and curated learning resources.
- **User Accounts & History** — Register/login and keep a history of past analyses (SQLite database).

## 🛠️ Tech Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **Resume Parsing:** PyPDF2, python-docx, Pillow, pytesseract, pdf2image
- **AI:** OpenAI API (optional)
- **Live Jobs:** Adzuna Jobs API (optional)
- **Auth:** Werkzeug password hashing

## 📁 Project Structure

```
.
├── app.py                # Main Flask application & routes
├── analyzer.py            # Deterministic skill-gap / ATS analysis engine
├── career_data.py         # Career profiles & learning resource links
├── database.py             # SQLite setup, users & analysis history
├── job_provider.py         # Adzuna live job search integration
├── llm_analyzer.py         # Optional OpenAI-powered analysis & resume rewriting
├── resume_utils.py         # Resume text extraction (PDF/DOCX/Image + OCR)
├── skills_data.py          # Job-to-skill mappings, categories & aliases
├── requirements.txt
├── .env.example             # Example environment configuration
└── .gitignore
```

## ⚙️ Prerequisites

- Python 3.10+
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) installed on your system (for scanned PDF / image resumes)
- [Poppler](https://poppler.freedesktop.org/) installed (required by `pdf2image` for scanned PDF OCR)

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/<your-username>/<your-repo>.git
   cd <your-repo>
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   Then edit `.env` and fill in the values (see [Environment Variables](#-environment-variables) below).

5. **Run the application**
   ```bash
   python app.py
   ```
   The app will be available at `http://127.0.0.1:5000`.

## 🔐 Environment Variables

Create a `.env` file in the project root (use `.env.example` as a template):

| Variable | Required | Description |
|---|---|---|
| `FLASK_SECRET_KEY` | Recommended | Secret key for session security. Use a long random string. |
| `OPENAI_API_KEY` | Optional | Enables AI-powered analysis and resume rewriting. Falls back to the rule-based analyzer if empty. |
| `OPENAI_MODEL` | Optional | OpenAI model name to use (defaults to a preset value). |
| `ADZUNA_APP_ID` | Optional | Enables the Live Jobs feature via the Adzuna API. |
| `ADZUNA_APP_KEY` | Optional | Adzuna API key, used together with `ADZUNA_APP_ID`. |
| `ADZUNA_COUNTRY` | Optional | Country code for Adzuna search (defaults to `in` for India). |

> The app works fully without `OPENAI_API_KEY` or Adzuna credentials — those features simply show a "not configured" message instead of crashing.

## 📌 Notes

- `career_analyzer.db` is the local SQLite database. It's included here for convenience but is typically excluded from version control (see `.gitignore`) so each deployment starts fresh — delete it locally if you want a clean database, it will be recreated automatically on first run.
- Never commit your real `.env` file or API keys — only `.env.example` should be tracked in git.

👨‍💻 Author

Abhiram P S
B.Tech – Artificial Intelligence and Machine Learning
