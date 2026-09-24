from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os
import re
import PyPDF2


app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf"}

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# =========================================================
# CAREER DATA
# =========================================================

careers = {

    "Data Scientist": {
        "description": "Analyze data and build machine learning solutions to solve real-world business problems.",
        "skills": [
            "Python",
            "SQL",
            "Machine Learning",
            "Statistics",
            "Pandas",
            "NumPy",
            "Data Visualization",
            "Scikit-learn",
            "Deep Learning"
        ],
        "salary": "₹6 LPA - ₹20 LPA",
        "companies": [
            "Google",
            "Microsoft",
            "Amazon",
            "IBM",
            "Accenture"
        ]
    },

    "Machine Learning Engineer": {
        "description": "Build, train, evaluate and deploy machine learning models.",
        "skills": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow",
            "PyTorch",
            "Scikit-learn",
            "SQL",
            "Docker",
            "Git",
            "MLOps"
        ],
        "salary": "₹7 LPA - ₹25 LPA",
        "companies": [
            "Google",
            "Microsoft",
            "Amazon",
            "NVIDIA",
            "IBM"
        ]
    },

    "Data Analyst": {
        "description": "Analyze datasets and communicate insights that support business decisions.",
        "skills": [
            "Python",
            "SQL",
            "Excel",
            "Pandas",
            "Statistics",
            "Power BI",
            "Tableau",
            "Data Visualization"
        ],
        "salary": "₹4 LPA - ₹12 LPA",
        "companies": [
            "Deloitte",
            "Accenture",
            "TCS",
            "Infosys",
            "Amazon"
        ]
    },

    "Python Developer": {
        "description": "Build backend applications, APIs and software solutions using Python.",
        "skills": [
            "Python",
            "OOP",
            "Flask",
            "Django",
            "SQL",
            "Git",
            "REST API",
            "Data Structures"
        ],
        "salary": "₹4 LPA - ₹15 LPA",
        "companies": [
            "Google",
            "Amazon",
            "Infosys",
            "TCS",
            "Wipro"
        ]
    },

    "Full Stack Developer": {
        "description": "Develop complete web applications using frontend and backend technologies.",
        "skills": [
            "HTML",
            "CSS",
            "JavaScript",
            "React",
            "Python",
            "Flask",
            "SQL",
            "Git",
            "REST API"
        ],
        "salary": "₹5 LPA - ₹18 LPA",
        "companies": [
            "Google",
            "Microsoft",
            "Amazon",
            "Infosys",
            "TCS"
        ]
    },

    "Software Engineer": {
        "description": "Design, develop, test and maintain software applications.",
        "skills": [
            "Python",
            "Java",
            "C++",
            "Data Structures",
            "Algorithms",
            "OOP",
            "Git",
            "SQL"
        ],
        "salary": "₹5 LPA - ₹25 LPA",
        "companies": [
            "Google",
            "Microsoft",
            "Amazon",
            "Meta",
            "Apple"
        ]
    },

    "AI Engineer": {
        "description": "Develop artificial intelligence applications using machine learning and deep learning.",
        "skills": [
            "Python",
            "Machine Learning",
            "Deep Learning",
            "TensorFlow",
            "PyTorch",
            "NLP",
            "Computer Vision",
            "Git"
        ],
        "salary": "₹8 LPA - ₹30 LPA",
        "companies": [
            "Google",
            "Microsoft",
            "NVIDIA",
            "Amazon",
            "IBM"
        ]
    }
}


# =========================================================
# RESOURCES
# =========================================================

resources = {

    "Python": {
        "youtube": "https://www.youtube.com/results?search_query=python+tutorial+for+beginners",
        "course": "https://www.w3schools.com/python/"
    },

    "SQL": {
        "youtube": "https://www.youtube.com/results?search_query=sql+tutorial+for+beginners",
        "course": "https://www.w3schools.com/sql/"
    },

    "Machine Learning": {
        "youtube": "https://www.youtube.com/results?search_query=machine+learning+tutorial+for+beginners",
        "course": "https://www.coursera.org/learn/machine-learning"
    },

    "Deep Learning": {
        "youtube": "https://www.youtube.com/results?search_query=deep+learning+tutorial",
        "course": "https://www.deeplearning.ai/"
    },

    "TensorFlow": {
        "youtube": "https://www.youtube.com/results?search_query=tensorflow+tutorial",
        "course": "https://www.tensorflow.org/tutorials"
    },

    "PyTorch": {
        "youtube": "https://www.youtube.com/results?search_query=pytorch+tutorial",
        "course": "https://pytorch.org/tutorials/"
    },

    "Pandas": {
        "youtube": "https://www.youtube.com/results?search_query=pandas+python+tutorial",
        "course": "https://www.w3schools.com/python/pandas/"
    },

    "NumPy": {
        "youtube": "https://www.youtube.com/results?search_query=numpy+tutorial",
        "course": "https://www.w3schools.com/python/numpy/"
    },

    "Statistics": {
        "youtube": "https://www.youtube.com/results?search_query=statistics+for+data+science",
        "course": "https://www.khanacademy.org/math/statistics-probability"
    },

    "Data Visualization": {
        "youtube": "https://www.youtube.com/results?search_query=data+visualization+tutorial",
        "course": "https://www.tableau.com/learn/training"
    },

    "Scikit-learn": {
        "youtube": "https://www.youtube.com/results?search_query=scikit+learn+tutorial",
        "course": "https://scikit-learn.org/stable/tutorial/"
    },

    "Docker": {
        "youtube": "https://www.youtube.com/results?search_query=docker+tutorial",
        "course": "https://docs.docker.com/get-started/"
    },

    "Git": {
        "youtube": "https://www.youtube.com/results?search_query=git+github+tutorial",
        "course": "https://www.w3schools.com/git/"
    },

    "MLOps": {
        "youtube": "https://www.youtube.com/results?search_query=mlops+tutorial",
        "course": "https://ml-ops.org/"
    },

    "Excel": {
        "youtube": "https://www.youtube.com/results?search_query=excel+tutorial",
        "course": "https://support.microsoft.com/excel"
    },

    "Power BI": {
        "youtube": "https://www.youtube.com/results?search_query=power+bi+tutorial",
        "course": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi/"
    },

    "Tableau": {
        "youtube": "https://www.youtube.com/results?search_query=tableau+tutorial",
        "course": "https://www.tableau.com/learn/training"
    },

    "HTML": {
        "youtube": "https://www.youtube.com/results?search_query=html+tutorial",
        "course": "https://www.w3schools.com/html/"
    },

    "CSS": {
        "youtube": "https://www.youtube.com/results?search_query=css+tutorial",
        "course": "https://www.w3schools.com/css/"
    },

    "JavaScript": {
        "youtube": "https://www.youtube.com/results?search_query=javascript+tutorial",
        "course": "https://www.w3schools.com/js/"
    },

    "React": {
        "youtube": "https://www.youtube.com/results?search_query=react+tutorial",
        "course": "https://react.dev/learn"
    },

    "Flask": {
        "youtube": "https://www.youtube.com/results?search_query=flask+python+tutorial",
        "course": "https://flask.palletsprojects.com/"
    },

    "Django": {
        "youtube": "https://www.youtube.com/results?search_query=django+tutorial",
        "course": "https://docs.djangoproject.com/"
    },

    "REST API": {
        "youtube": "https://www.youtube.com/results?search_query=rest+api+tutorial",
        "course": "https://developer.mozilla.org/en-US/docs/Glossary/REST"
    },

    "Data Structures": {
        "youtube": "https://www.youtube.com/results?search_query=data+structures+tutorial",
        "course": "https://www.geeksforgeeks.org/data-structures/"
    },

    "Algorithms": {
        "youtube": "https://www.youtube.com/results?search_query=algorithms+tutorial",
        "course": "https://www.geeksforgeeks.org/fundamentals-of-algorithms/"
    },

    "Java": {
        "youtube": "https://www.youtube.com/results?search_query=java+tutorial",
        "course": "https://www.w3schools.com/java/"
    },

    "C++": {
        "youtube": "https://www.youtube.com/results?search_query=c%2B%2B+tutorial",
        "course": "https://www.w3schools.com/cpp/"
    },

    "OOP": {
        "youtube": "https://www.youtube.com/results?search_query=object+oriented+programming+tutorial",
        "course": "https://www.w3schools.com/python/python_classes.asp"
    },

    "NLP": {
        "youtube": "https://www.youtube.com/results?search_query=natural+language+processing+tutorial",
        "course": "https://www.coursera.org/learn/language-processing"
    },

    "Computer Vision": {
        "youtube": "https://www.youtube.com/results?search_query=computer+vision+tutorial",
        "course": "https://opencv.org/"
    }
}


# =========================================================
# ALL SKILLS
# =========================================================

all_skills = sorted(
    set(
        skill
        for career in careers.values()
        for skill in career["skills"]
    )
)


# =========================================================
# PDF
# =========================================================

def allowed_file(filename):

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in ALLOWED_EXTENSIONS
    )


def extract_pdf_text(filepath):

    text = ""

    try:

        with open(filepath, "rb") as file:

            reader = PyPDF2.PdfReader(file)

            for page in reader.pages:

                content = page.extract_text()

                if content:
                    text += content + "\n"

    except Exception as error:

        print("PDF ERROR:", error)

    return text


# =========================================================
# SKILL DETECTION
# =========================================================

def detect_skills(text):

    text_lower = text.lower()

    found = []

    for skill in all_skills:

        pattern = r"\b" + re.escape(skill.lower()) + r"\b"

        if re.search(pattern, text_lower):

            found.append(skill)

    return found


# =========================================================
# SKILL EVIDENCE
# =========================================================

def get_skill_evidence(text, skills):

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    evidence = {}

    for skill in skills:

        matched_line = ""

        for line in lines:

            if skill.lower() in line.lower():

                matched_line = line[:220]

                break

        if matched_line:

            evidence[skill] = matched_line

        else:

            evidence[skill] = "Skill listed without detailed evidence."

    return evidence


# =========================================================
# ATS SCORE
# =========================================================

def calculate_ats_score(
    resume_text,
    required_skills,
    matched_skills,
    job_description=""
):

    score = 0

    # Skill match: 50
    if required_skills:

        score += (
            len(matched_skills)
            / len(required_skills)
        ) * 50

    text_lower = resume_text.lower()

    # Important resume sections: 20

    sections = [
        "summary",
        "experience",
        "education",
        "skills",
        "projects"
    ]

    section_count = sum(
        1
        for section in sections
        if section in text_lower
    )

    score += (
        section_count / len(sections)
    ) * 20

    # Job description keyword matching: 20

    if job_description:

        jd_words = set(
            re.findall(
                r"\b[a-zA-Z]{4,}\b",
                job_description.lower()
            )
        )

        resume_words = set(
            re.findall(
                r"\b[a-zA-Z]{4,}\b",
                text_lower
            )
        )

        common = jd_words.intersection(
            resume_words
        )

        if jd_words:

            score += min(
                len(common) / len(jd_words) * 20,
                20
            )

    else:

        score += 10

    # Resume completeness: 10

    word_count = len(
        resume_text.split()
    )

    if word_count >= 300:

        score += 10

    elif word_count >= 180:

        score += 7

    elif word_count >= 100:

        score += 4

    return min(round(score), 100)


# =========================================================
# SUITABILITY
# =========================================================

def suitability(score):

    if score >= 85:
        return "Excellent Match"

    if score >= 70:
        return "Strong Match"

    if score >= 55:
        return "Moderate Match"

    return "Needs Improvement"


# =========================================================
# RESUME SUGGESTIONS
# =========================================================

def resume_suggestions(
    resume_text,
    missing_skills,
    job_description
):

    text_lower = resume_text.lower()

    suggestions = []

    if missing_skills:

        suggestions.append(
            "Add relevant missing job skills after gaining genuine experience with them."
        )

    if "summary" not in text_lower:

        suggestions.append(
            "Add a concise professional summary containing your target role and strongest skills."
        )

    if "projects" not in text_lower:

        suggestions.append(
            "Add 2 to 3 relevant projects with technologies, responsibilities and measurable results."
        )

    if "experience" not in text_lower:

        suggestions.append(
            "Add internships, training or practical experience related to the target position."
        )

    if "education" not in text_lower:

        suggestions.append(
            "Clearly include your education, degree and relevant academic information."
        )

    if job_description:

        suggestions.append(
            "Use important keywords from the job description naturally where they accurately describe your experience."
        )

    suggestions.append(
        "Replace generic statements with measurable achievements whenever possible."
    )

    suggestions.append(
        "Keep section headings simple and use an ATS-friendly structure."
    )

    return suggestions


# =========================================================
# ROADMAP
# =========================================================

def create_roadmap(
    required_skills,
    matched_skills,
    missing_skills
):

    roadmap = []

    number = 1

    for skill in matched_skills:

        roadmap.append({
            "step": number,
            "skill": skill,
            "status": "Completed",
            "priority": "Current Strength"
        })

        number += 1

    for skill in missing_skills:

        priority = "High"

        if len(roadmap) > len(required_skills) * 0.6:
            priority = "Medium"

        roadmap.append({
            "step": number,
            "skill": skill,
            "status": "Learn Next",
            "priority": priority
        })

        number += 1

    return roadmap


# =========================================================
# WHAT IF SIMULATOR
# =========================================================

def calculate_simulated_scores(
    required_skills,
    matched_skills,
    missing_skills
):

    current = round(
        len(matched_skills)
        / len(required_skills)
        * 100
    )

    simulations = []

    score = current

    for skill in missing_skills:

        score = min(
            score + round(
                100 / len(required_skills)
            ),
            100
        )

        simulations.append({
            "skill": skill,
            "score": score
        })

    return current, simulations


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html",
        page="home",
        careers=careers
    )


# =========================================================
# CAREER ANALYZER
# =========================================================

@app.route(
    "/analyzer",
    methods=["GET", "POST"]
)
def analyzer():

    result = None

    if request.method == "POST":

        job = request.form.get("job")

        selected_skills = request.form.getlist(
            "skills"
        )

        additional = request.form.get(
            "additional_skills",
            ""
        )

        if additional:

            selected_skills += [
                skill.strip()
                for skill in additional.split(",")
                if skill.strip()
            ]

        required = careers[job]["skills"]

        matched = []

        for skill in required:

            if any(
                skill.lower()
                == user_skill.lower()
                for user_skill in selected_skills
            ):

                matched.append(skill)

        missing = [
            skill
            for skill in required
            if skill not in matched
        ]

        score = round(
            len(matched)
            / len(required)
            * 100
        )

        result = {

            "job": job,

            "available_skills": matched,

            "missing_skills": missing,

            "readiness_score": score,

            "resources": {
                skill: resources[skill]
                for skill in missing
                if skill in resources
            }

        }

    return render_template(
        "index.html",
        page="analyzer",
        careers=careers,
        all_skills=all_skills,
        result=result
    )


# =========================================================
# RESUME ANALYZER
# =========================================================

@app.route(
    "/resume-analyzer",
    methods=["GET", "POST"]
)
def resume_analyzer():

    result = None
    error = None

    if request.method == "POST":

        job = request.form.get("job")

        file = request.files.get("resume")

        job_description = request.form.get(
            "job_description",
            ""
        )

        if not file or file.filename == "":

            error = "Please upload a PDF resume."

        elif not allowed_file(file.filename):

            error = "Only PDF files are supported."

        else:

            filename = secure_filename(
                file.filename
            )

            filepath = os.path.join(
                app.config["UPLOAD_FOLDER"],
                filename
            )

            file.save(filepath)

            resume_text = extract_pdf_text(
                filepath
            )

            if not resume_text.strip():

                error = (
                    "No readable text was found in the PDF. "
                    "Please upload a text-based PDF."
                )

            else:

                required = careers[job]["skills"]

                resume_skills = detect_skills(
                    resume_text
                )

                matched = [
                    skill
                    for skill in required
                    if skill in resume_skills
                ]

                missing = [
                    skill
                    for skill in required
                    if skill not in matched
                ]

                evidence = get_skill_evidence(
                    resume_text,
                    matched
                )

                ats = calculate_ats_score(
                    resume_text,
                    required,
                    matched,
                    job_description
                )

                fit = suitability(ats)

                suggestions = resume_suggestions(
                    resume_text,
                    missing,
                    job_description
                )

                roadmap = create_roadmap(
                    required,
                    matched,
                    missing
                )

                current_score, simulations = (
                    calculate_simulated_scores(
                        required,
                        matched,
                        missing
                    )
                )

                result = {

                    "job": job,

                    "ats_score": ats,

                    "suitability": fit,

                    "matched_skills": matched,

                    "missing_skills": missing,

                    "evidence": evidence,

                    "suggestions": suggestions,

                    "roadmap": roadmap,

                    "simulations": simulations,

                    "word_count": len(
                        resume_text.split()
                    )

                }

    return render_template(
        "index.html",
        page="resume_analyzer",
        careers=careers,
        result=result,
        error=error
    )


# =========================================================
# CAREERS
# =========================================================

@app.route("/careers")
def career_list():

    return render_template(
        "index.html",
        page="careers",
        careers=careers
    )


# =========================================================
# CAREER DETAILS
# =========================================================

@app.route("/career/<job>")
def career_details(job):

    if job not in careers:

        return "Career not found", 404

    return render_template(
        "index.html",
        page="career_details",
        job=job,
        career=careers[job],
        careers=careers
    )


# =========================================================
# RESOURCES
# =========================================================

@app.route("/resources")
def learning_resources():

    return render_template(
        "index.html",
        page="resources",
        resources=resources,
        careers=careers
    )


# =========================================================
# ABOUT
# =========================================================

@app.route("/about")
def about():

    return render_template(
        "index.html",
        page="about",
        careers=careers
    )


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )