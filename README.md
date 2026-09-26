

# AI-Powered Career Skill Gap Analyzer 🚀

An AI-powered web application that helps students and job seekers analyze their resumes, identify career skill gaps, measure ATS and career readiness, and discover personalized learning resources and job opportunities.

---

## 📌 About the Project

The **AI-Powered Career Skill Gap Analyzer** compares a user's existing skills with the skills required for a selected career role.

The application analyzes an uploaded resume, identifies matched and missing skills, calculates an ATS score and career readiness score, and generates a personalized roadmap to help the user prepare for their target career.

The application also provides career-specific learning resources and live job opportunities.

---

## ✨ Key Features

### 📄 Resume Analysis
- Upload resumes in PDF, DOCX, PNG, JPG, or JPEG format.
- Extract resume text automatically.
- Detect technical and career-related skills.
- Compare resume skills with target career requirements.

### 🎯 Skill Gap Analysis
- Select a target career.
- Select specific skills manually.
- Add additional skills.
- Identify matched skills.
- Identify missing skills.
- Highlight evidence found in the resume.

### 📊 ATS Analysis
- Generate an ATS score.
- Analyze resume skill relevance.
- Identify missing skills that may improve career alignment.
- Provide suggestions for improving the resume.

### 🧠 AI-Powered Analysis
When an OpenAI API key is configured, the application can provide:
- AI-based resume insights
- Personalized recommendations
- Career-specific analysis
- AI-assisted resume rewriting

### ✍️ AI Resume Rewriting
Improve resume wording while preserving the original facts.

The AI rewriting feature is designed to:
- Improve clarity
- Improve professional wording
- Strengthen resume descriptions
- Preserve existing information
- Avoid inventing qualifications or experience

### 🗺️ Career Roadmap
Generate a structured learning roadmap based on:
- Current skills
- Missing skills
- Target career
- Skill priorities

### 📚 Careers & Resources
Explore different technology and data-related careers.

Each career includes:
- Required skills
- Skill categories
- Learning resources
- Free learning links
- YouTube resources

### 💼 Live Job Search
Search current job opportunities using the Adzuna Jobs API.

The job search supports:
- Job title selection
- Skill-based search
- Kerala locations
- All Kerala
- Kerala districts
- Company information
- Job descriptions
- Salary information when available
- Direct job links

### 👤 User Accounts
Users can:
- Register
- Log in
- Log out
- Save resume analyses
- View previous analyses
- Delete saved analyses

### 📜 Analysis History
Logged-in users can view previous resume analyses and review their results later.

---

## 🛠️ Technologies Used

### Backend
- Python
- Flask
- SQLite

### AI
- OpenAI API

### Resume Processing
- PyPDF2
- python-docx
- Pillow
- Tesseract OCR
- pdf2image

### Frontend
- HTML5
- CSS3
- JavaScript
- Jinja2

### APIs
- OpenAI API
- Adzuna Jobs API

---

## 🧩 Supported Career Roles

The application currently supports career analysis for roles including:

- Data Analyst
- Junior Data Analyst
- Business Intelligence Analyst
- Data Scientist
- Junior Data Scientist
- Machine Learning Engineer
- Junior Machine Learning Engineer
- AI Engineer
- Deep Learning Engineer
- Data Engineer
- Python Developer
- Data Science Intern
- Machine Learning Intern

---

## 🔄 How It Works

```text
             Resume Upload
                   │
                   ▼
          Resume Text Extraction
                   │
                   ▼
             Skill Detection
                   │
                   ▼
          Select Target Career
                   │
                   ▼
          Compare Required Skills
                   │
          ┌────────┴────────┐
          ▼                 ▼
    Matched Skills     Missing Skills
          │                 │
          └────────┬────────┘
                   ▼
             ATS Analysis
                   │
                   ▼
        Career Readiness Score
                   │
                   ▼
          Personalized Suggestions
                   │
          ┌────────┴────────┐
          ▼                 ▼
   Career Roadmap      Learning Resources
                   │
                   ▼
            Optional AI Analysis
