# ============================================================
# AI-POWERED CAREER SKILL GAP ANALYZER
# skills_data.py
# ============================================================

job_skills = {

    # ========================================================
    # DATA ANALYST
    # ========================================================

    "Data Analyst": [
        "Python",
        "SQL",
        "Excel",
        "Pandas",
        "Data Visualization",
        "Statistics",
    ],


    # ========================================================
    # JUNIOR DATA ANALYST
    # ========================================================

    "Junior Data Analyst": [
        "Excel",
        "SQL",
        "Pandas",
        "Data Visualization",
        "Statistics",
    ],


    # ========================================================
    # BUSINESS INTELLIGENCE ANALYST
    # ========================================================

    "Business Intelligence Analyst": [
        "SQL",
        "Excel",
        "Data Visualization",
        "Statistics",
        "Python",
    ],


    # ========================================================
    # DATA SCIENTIST
    # ========================================================

    "Data Scientist": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Machine Learning",
        "Statistics",
        "Data Visualization",
    ],


    # ========================================================
    # JUNIOR DATA SCIENTIST
    # ========================================================

    "Junior Data Scientist": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Statistics",
        "Machine Learning",
    ],


    # ========================================================
    # MACHINE LEARNING ENGINEER
    # ========================================================

    "Machine Learning Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "SQL",
        "Docker",
        "MLOps",
    ],


    # ========================================================
    # JUNIOR MACHINE LEARNING ENGINEER
    # ========================================================

    "Junior Machine Learning Engineer": [
        "Python",
        "Machine Learning",
        "SQL",
        "Pandas",
        "NumPy",
        "Git",
    ],


    # ========================================================
    # AI ENGINEER
    # ========================================================

    "AI Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "LLMs",
        "Docker",
        "MLOps",
    ],


    # ========================================================
    # DEEP LEARNING ENGINEER
    # ========================================================

    "Deep Learning Engineer": [
        "Python",
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "NumPy",
        "Docker",
    ],


    # ========================================================
    # DATA ENGINEER
    # ========================================================

    "Data Engineer": [
        "Python",
        "SQL",
        "Pandas",
        "Git",
        "Docker",
    ],


    # ========================================================
    # PYTHON DEVELOPER
    # ========================================================

    "Python Developer": [
        "Python",
        "OOP",
        "SQL",
        "Git",
        "Django",
        "Flask",
    ],


    # ========================================================
    # DATA SCIENCE INTERN
    # ========================================================

    "Data Science Intern": [
        "Python",
        "SQL",
        "Pandas",
        "NumPy",
        "Statistics",
        "Data Visualization",
    ],


    # ========================================================
    # MACHINE LEARNING INTERN
    # ========================================================

    "Machine Learning Intern": [
        "Python",
        "Machine Learning",
        "Pandas",
        "NumPy",
        "SQL",
    ],
}


# ============================================================
# ALL AVAILABLE SKILLS
# ============================================================

all_skills = sorted(
    {
        skill
        for skills in job_skills.values()
        for skill in skills
    },
    key=str.lower,
)


# ============================================================
# SKILL CATEGORIES
# ============================================================

skill_categories = {

    "Programming": [
        "Python",
        "Java",
        "JavaScript",
        "C++",
    ],

    "Data Analysis": [
        "SQL",
        "Excel",
        "Pandas",
        "NumPy",
        "Statistics",
        "Data Visualization",
    ],

    "Machine Learning": [
        "Machine Learning",
        "Deep Learning",
        "TensorFlow",
        "LLMs",
    ],

    "Development": [
        "Django",
        "Flask",
        "OOP",
        "Git",
    ],

    "Deployment & MLOps": [
        "Docker",
        "MLOps",
    ],
}


# ============================================================
# SKILL ALIASES
# ============================================================

skill_aliases = {

    "Python": [
        "python",
        "python3",
    ],

    "SQL": [
        "sql",
        "mysql",
        "postgresql",
        "postgres",
    ],

    "Excel": [
        "excel",
        "microsoft excel",
        "ms excel",
    ],

    "Pandas": [
        "pandas",
    ],

    "NumPy": [
        "numpy",
    ],

    "Machine Learning": [
        "machine learning",
        "machine-learning",
        "ml",
    ],

    "Deep Learning": [
        "deep learning",
        "deep-learning",
        "dl",
    ],

    "TensorFlow": [
        "tensorflow",
        "tensor flow",
    ],

    "LLMs": [
        "llm",
        "llms",
        "large language model",
        "large language models",
        "generative ai",
        "genai",
    ],

    "Data Visualization": [
        "data visualization",
        "data visualisation",
        "data viz",
    ],

    "Statistics": [
        "statistics",
        "statistical analysis",
    ],

    "Git": [
        "git",
        "github",
        "gitlab",
    ],

    "Docker": [
        "docker",
    ],

    "MLOps": [
        "mlops",
        "ml ops",
        "machine learning operations",
    ],

    "Django": [
        "django",
    ],

    "Flask": [
        "flask",
    ],

    "OOP": [
        "oop",
        "object oriented programming",
        "object-oriented programming",
    ],

    "Java": [
        "java",
    ],

    "JavaScript": [
        "javascript",
        "java script",
        "js",
    ],

    "C++": [
        "c++",
        "cpp",
    ],
}


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_skills_for_job(job):
    """
    Return the required skills for a particular job.
    """

    if not job:
        return []

    if job in job_skills:
        return job_skills[job]

    job_lower = job.strip().lower()

    for job_name, skills in job_skills.items():

        if job_name.lower() == job_lower:
            return skills

    return []


def get_all_skills():
    """
    Return all unique skills.
    """

    return list(all_skills)


def get_skill_aliases(skill):
    """
    Return aliases for a skill.
    """

    if skill in skill_aliases:
        return skill_aliases[skill]

    skill_lower = skill.strip().lower()

    for name, aliases in skill_aliases.items():

        if name.lower() == skill_lower:
            return aliases

    return [skill]


def get_skills_by_category(category):
    """
    Return skills belonging to a category.
    """

    return skill_categories.get(
        category,
        [],
    )


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

SKILL_ALIASES = skill_aliases
SKILL_CATEGORIES = skill_categories
ALL_SKILLS = all_skills
JOB_SKILLS = job_skills