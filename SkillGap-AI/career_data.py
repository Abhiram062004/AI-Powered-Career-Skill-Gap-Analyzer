"""
career_data.py
--------------
Career information, required skills, salary ranges, career paths,
and learning resources for the AI-Powered Career Skill Gap Analyzer.
"""

from skills_data import get_skills_for_job


CAREER_DATA = {
    "Data Analyst": {
        "title": "Data Analyst",
        "description": (
            "Analyze data, identify trends, create reports and dashboards, "
            "and support data-driven business decisions."
        ),
        "salary": "₹3.5 LPA – ₹10 LPA",
        "companies": [
            "TCS",
            "Infosys",
            "Accenture",
            "Deloitte",
            "EY",
            "Wipro",
        ],
        "career_path": [
            "Junior Data Analyst",
            "Data Analyst",
            "Senior Data Analyst",
            "Lead Data Analyst",
            "Analytics Manager",
        ],
    },

    "Junior Data Analyst": {
        "title": "Junior Data Analyst",
        "description": (
            "Work with datasets, prepare reports, perform basic analysis, "
            "and support senior analysts."
        ),
        "salary": "₹2.5 LPA – ₹6 LPA",
        "companies": [
            "TCS",
            "Infosys",
            "Wipro",
            "Cognizant",
            "Accenture",
        ],
        "career_path": [
            "Junior Data Analyst",
            "Data Analyst",
            "Senior Data Analyst",
            "Analytics Lead",
        ],
    },

    "Business Intelligence Analyst": {
        "title": "Business Intelligence Analyst",
        "description": (
            "Transform business data into dashboards, reports, and "
            "actionable insights."
        ),
        "salary": "₹4 LPA – ₹12 LPA",
        "companies": [
            "Microsoft",
            "Deloitte",
            "Accenture",
            "IBM",
            "TCS",
        ],
        "career_path": [
            "BI Analyst",
            "Senior BI Analyst",
            "BI Developer",
            "BI Manager",
        ],
    },

    "Data Scientist": {
        "title": "Data Scientist",
        "description": (
            "Use statistics, machine learning, and programming to extract "
            "insights and build predictive models."
        ),
        "salary": "₹5 LPA – ₹18 LPA",
        "companies": [
            "Amazon",
            "Google",
            "Microsoft",
            "Flipkart",
            "Walmart",
            "TCS",
        ],
        "career_path": [
            "Data Science Intern",
            "Junior Data Scientist",
            "Data Scientist",
            "Senior Data Scientist",
            "Lead Data Scientist",
        ],
    },

    "Junior Data Scientist": {
        "title": "Junior Data Scientist",
        "description": (
            "Assist in data preparation, exploratory analysis, feature "
            "engineering, and machine learning model development."
        ),
        "salary": "₹4 LPA – ₹9 LPA",
        "companies": [
            "TCS",
            "Infosys",
            "Accenture",
            "Cognizant",
            "Wipro",
        ],
        "career_path": [
            "Junior Data Scientist",
            "Data Scientist",
            "Senior Data Scientist",
            "Lead Data Scientist",
        ],
    },

    "Machine Learning Engineer": {
        "title": "Machine Learning Engineer",
        "description": (
            "Develop, train, evaluate, and deploy machine learning models "
            "for real-world applications."
        ),
        "salary": "₹5 LPA – ₹20 LPA",
        "companies": [
            "Google",
            "Microsoft",
            "Amazon",
            "NVIDIA",
            "Intel",
            "Adobe",
        ],
        "career_path": [
            "ML Intern",
            "Junior ML Engineer",
            "Machine Learning Engineer",
            "Senior ML Engineer",
            "ML Architect",
        ],
    },

    "Junior Machine Learning Engineer": {
        "title": "Junior Machine Learning Engineer",
        "description": (
            "Support machine learning projects through data preparation, "
            "model training, testing, and deployment."
        ),
        "salary": "₹4 LPA – ₹10 LPA",
        "companies": [
            "TCS",
            "Infosys",
            "Accenture",
            "Cognizant",
            "IBM",
        ],
        "career_path": [
            "ML Intern",
            "Junior ML Engineer",
            "ML Engineer",
            "Senior ML Engineer",
        ],
    },

    "AI Engineer": {
        "title": "AI Engineer",
        "description": (
            "Build AI-powered applications using machine learning, deep "
            "learning, natural language processing, computer vision, and "
            "modern generative AI techniques."
        ),
        "salary": "₹5 LPA – ₹22 LPA",
        "companies": [
            "Microsoft",
            "Google",
            "Amazon",
            "OpenAI",
            "NVIDIA",
            "IBM",
        ],
        "career_path": [
            "AI Intern",
            "Junior AI Engineer",
            "AI Engineer",
            "Senior AI Engineer",
            "AI Architect",
        ],
    },

    "Deep Learning Engineer": {
        "title": "Deep Learning Engineer",
        "description": (
            "Design and train neural networks for computer vision, NLP, "
            "speech processing, and other AI applications."
        ),
        "salary": "₹5 LPA – ₹20 LPA",
        "companies": [
            "NVIDIA",
            "Google",
            "Microsoft",
            "Meta",
            "Amazon",
        ],
        "career_path": [
            "AI/ML Intern",
            "Junior Deep Learning Engineer",
            "Deep Learning Engineer",
            "Senior Deep Learning Engineer",
            "AI Research Engineer",
        ],
    },

    "Data Engineer": {
        "title": "Data Engineer",
        "description": (
            "Build and maintain data pipelines, databases, ETL processes, "
            "and data infrastructure."
        ),
        "salary": "₹4 LPA – ₹16 LPA",
        "companies": [
            "Amazon",
            "Microsoft",
            "Google",
            "Deloitte",
            "Accenture",
            "TCS",
        ],
        "career_path": [
            "Data Engineering Intern",
            "Junior Data Engineer",
            "Data Engineer",
            "Senior Data Engineer",
            "Data Architect",
        ],
    },

    "Python Developer": {
        "title": "Python Developer",
        "description": (
            "Develop applications, APIs, automation tools, and backend "
            "systems using Python."
        ),
        "salary": "₹3 LPA – ₹12 LPA",
        "companies": [
            "TCS",
            "Infosys",
            "Wipro",
            "Accenture",
            "Zoho",
            "IBM",
        ],
        "career_path": [
            "Python Intern",
            "Junior Python Developer",
            "Python Developer",
            "Senior Python Developer",
            "Backend Lead",
        ],
    },

    "Data Science Intern": {
        "title": "Data Science Intern",
        "description": (
            "Gain practical experience in data cleaning, visualization, "
            "statistics, machine learning, and exploratory data analysis."
        ),
        "salary": "₹10K – ₹35K / month",
        "companies": [
            "Startups",
            "TCS",
            "Infosys",
            "Accenture",
            "Analytics Companies",
        ],
        "career_path": [
            "Data Science Intern",
            "Junior Data Scientist",
            "Data Scientist",
            "Senior Data Scientist",
        ],
    },

    "Machine Learning Intern": {
        "title": "Machine Learning Intern",
        "description": (
            "Work on real-world machine learning projects involving data "
            "preprocessing, model training, evaluation, and experimentation."
        ),
        "salary": "₹10K – ₹40K / month",
        "companies": [
            "AI Startups",
            "TCS",
            "Infosys",
            "Microsoft",
            "Amazon",
        ],
        "career_path": [
            "ML Intern",
            "Junior ML Engineer",
            "Machine Learning Engineer",
            "Senior ML Engineer",
        ],
    },
}


# -------------------------------------------------------------------
# Learning resources
# -------------------------------------------------------------------

RESOURCE_LINKS = {
    "Python": [
        {
            "name": "Python Official Tutorial",
            "url": "https://docs.python.org/3/tutorial/",
            "type": "Free Course",
        },
        {
            "name": "Python Full Course - freeCodeCamp",
            "url": "https://www.youtube.com/watch?v=rfscVS0vtbw",
            "type": "YouTube",
        },
    ],

    "SQL": [
        {
            "name": "SQLBolt",
            "url": "https://sqlbolt.com/",
            "type": "Free Course",
        },
        {
            "name": "SQL Full Course - freeCodeCamp",
            "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY",
            "type": "YouTube",
        },
    ],

    "NumPy": [
        {
            "name": "NumPy Documentation",
            "url": "https://numpy.org/learn/",
            "type": "Free Learning",
        },
        {
            "name": "NumPy Tutorial",
            "url": "https://www.youtube.com/watch?v=QUT1VHiLmmI",
            "type": "YouTube",
        },
    ],

    "Pandas": [
        {
            "name": "Pandas Documentation",
            "url": "https://pandas.pydata.org/docs/",
            "type": "Free Learning",
        },
        {
            "name": "Pandas Tutorial - freeCodeCamp",
            "url": "https://www.youtube.com/watch?v=vmEHCJofslg",
            "type": "YouTube",
        },
    ],

    "Matplotlib": [
        {
            "name": "Matplotlib Documentation",
            "url": "https://matplotlib.org/stable/tutorials/",
            "type": "Free Learning",
        },
        {
            "name": "Matplotlib Tutorial",
            "url": "https://www.youtube.com/watch?v=3Xc3CA655Y4",
            "type": "YouTube",
        },
    ],

    "Statistics": [
        {
            "name": "Khan Academy Statistics",
            "url": "https://www.khanacademy.org/math/statistics-probability",
            "type": "Free Course",
        },
        {
            "name": "Statistics Full Course",
            "url": "https://www.youtube.com/watch?v=xxpc-HPKN28",
            "type": "YouTube",
        },
    ],

    "Machine Learning": [
        {
            "name": "Google Machine Learning Crash Course",
            "url": "https://developers.google.com/machine-learning/crash-course",
            "type": "Free Course",
        },
        {
            "name": "Machine Learning Course - freeCodeCamp",
            "url": "https://www.youtube.com/watch?v=NWONeJKn6kc",
            "type": "YouTube",
        },
    ],

    "Scikit-learn": [
        {
            "name": "Scikit-learn User Guide",
            "url": "https://scikit-learn.org/stable/user_guide.html",
            "type": "Free Learning",
        },
        {
            "name": "Scikit-learn Tutorial",
            "url": "https://www.youtube.com/watch?v=0B5eIE_1vpU",
            "type": "YouTube",
        },
    ],

    "Deep Learning": [
        {
            "name": "Deep Learning Specialization",
            "url": "https://www.deeplearning.ai/courses/deep-learning-specialization/",
            "type": "Course",
        },
        {
            "name": "Deep Learning Course",
            "url": "https://www.youtube.com/watch?v=VyWAvY2CF9c",
            "type": "YouTube",
        },
    ],

    "TensorFlow": [
        {
            "name": "TensorFlow Tutorials",
            "url": "https://www.tensorflow.org/tutorials",
            "type": "Free Learning",
        },
        {
            "name": "TensorFlow Course",
            "url": "https://www.youtube.com/watch?v=tPYj3fFJGjk",
            "type": "YouTube",
        },
    ],

    "PyTorch": [
        {
            "name": "PyTorch Tutorials",
            "url": "https://pytorch.org/tutorials/",
            "type": "Free Learning",
        },
        {
            "name": "PyTorch Course",
            "url": "https://www.youtube.com/watch?v=V_xro1bcAuA",
            "type": "YouTube",
        },
    ],

    "NLP": [
        {
            "name": "Hugging Face NLP Course",
            "url": "https://huggingface.co/learn/nlp-course",
            "type": "Free Course",
        },
        {
            "name": "NLP Course",
            "url": "https://www.youtube.com/watch?v=fLvJ8VdHLA0",
            "type": "YouTube",
        },
    ],

    "Computer Vision": [
        {
            "name": "OpenCV Documentation",
            "url": "https://docs.opencv.org/",
            "type": "Free Learning",
        },
        {
            "name": "Computer Vision Course",
            "url": "https://www.youtube.com/watch?v=01sAkU_NvOY",
            "type": "YouTube",
        },
    ],

    "LLMs": [
        {
            "name": "Hugging Face LLM Course",
            "url": "https://huggingface.co/learn/llm-course",
            "type": "Free Course",
        },
        {
            "name": "LLM Course",
            "url": "https://www.youtube.com/watch?v=zjkBMFhNj_g",
            "type": "YouTube",
        },
    ],

    "Git": [
        {
            "name": "Git Documentation",
            "url": "https://git-scm.com/doc",
            "type": "Free Learning",
        },
        {
            "name": "Git and GitHub Course",
            "url": "https://www.youtube.com/watch?v=RGOj5yH7evk",
            "type": "YouTube",
        },
    ],

    "GitHub": [
        {
            "name": "GitHub Skills",
            "url": "https://skills.github.com/",
            "type": "Free Learning",
        },
        {
            "name": "GitHub Tutorial",
            "url": "https://www.youtube.com/watch?v=RGOj5yH7evk",
            "type": "YouTube",
        },
    ],

    "Power BI": [
        {
            "name": "Microsoft Power BI Learning",
            "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi/",
            "type": "Free Course",
        },
        {
            "name": "Power BI Full Course",
            "url": "https://www.youtube.com/watch?v=0m80Hr5x7Yw",
            "type": "YouTube",
        },
    ],

    "Excel": [
        {
            "name": "Microsoft Excel Training",
            "url": "https://support.microsoft.com/excel",
            "type": "Free Learning",
        },
        {
            "name": "Excel Full Course",
            "url": "https://www.youtube.com/watch?v=Vl0H-qTclOg",
            "type": "YouTube",
        },
    ],

    "ETL": [
        {
            "name": "ETL Concepts",
            "url": "https://www.ibm.com/think/topics/etl",
            "type": "Free Learning",
        },
        {
            "name": "ETL Tutorial",
            "url": "https://www.youtube.com/watch?v=8DvywoWv6fI",
            "type": "YouTube",
        },
    ],

    "Data Structures": [
        {
            "name": "GeeksforGeeks DSA",
            "url": "https://www.geeksforgeeks.org/data-structures/",
            "type": "Free Learning",
        },
        {
            "name": "Data Structures Course",
            "url": "https://www.youtube.com/watch?v=RBSGKlAvoiM",
            "type": "YouTube",
        },
    ],

    "Flask": [
        {
            "name": "Flask Documentation",
            "url": "https://flask.palletsprojects.com/",
            "type": "Free Learning",
        },
        {
            "name": "Flask Tutorial",
            "url": "https://www.youtube.com/watch?v=Z1RJmh_OqeA",
            "type": "YouTube",
        },
    ],

    "Django": [
        {
            "name": "Django Documentation",
            "url": "https://docs.djangoproject.com/",
            "type": "Free Learning",
        },
        {
            "name": "Django Course",
            "url": "https://www.youtube.com/watch?v=F5mRW0jo-U4",
            "type": "YouTube",
        },
    ],

    "Cloud": [
        {
            "name": "AWS Training",
            "url": "https://aws.amazon.com/training/",
            "type": "Free Learning",
        },
        {
            "name": "Cloud Computing Course",
            "url": "https://www.youtube.com/watch?v=2LaAJq1lB1Q",
            "type": "YouTube",
        },
    ],

    "Docker": [
        {
            "name": "Docker Get Started",
            "url": "https://docs.docker.com/get-started/",
            "type": "Free Learning",
        },
        {
            "name": "Docker Course",
            "url": "https://www.youtube.com/watch?v=3c-iBn73dDE",
            "type": "YouTube",
        },
    ],

    "APIs": [
        {
            "name": "Postman API Learning",
            "url": "https://learning.postman.com/",
            "type": "Free Learning",
        },
        {
            "name": "REST API Tutorial",
            "url": "https://www.youtube.com/watch?v=Q-BpqyOT3a8",
            "type": "YouTube",
        },
    ],

    "Java": [
        {
            "name": "Oracle Java Tutorials",
            "url": "https://docs.oracle.com/javase/tutorial/",
            "type": "Free Learning",
        },
        {
            "name": "Java Full Course",
            "url": "https://www.youtube.com/watch?v=xk4_1vDrzzo",
            "type": "YouTube",
        },
    ],

    "C++": [
        {
            "name": "Learn C++",
            "url": "https://www.learncpp.com/",
            "type": "Free Course",
        },
        {
            "name": "C++ Course",
            "url": "https://www.youtube.com/watch?v=vLnPwxZdW4Y",
            "type": "YouTube",
        },
    ],

    "Linux": [
        {
            "name": "Linux Journey",
            "url": "https://linuxjourney.com/",
            "type": "Free Course",
        },
        {
            "name": "Linux Course",
            "url": "https://www.youtube.com/watch?v=sWbUDq4S6Y8",
            "type": "YouTube",
        },
    ],

    "Data Visualization": [
        {
            "name": "Kaggle Data Visualization",
            "url": "https://www.kaggle.com/learn/data-visualization",
            "type": "Free Course",
        },
        {
            "name": "Data Visualization Tutorial",
            "url": "https://www.youtube.com/watch?v=GPVsHOlRBBI",
            "type": "YouTube",
        },
    ],
}


def get_career_data(job_title):
    """Return complete information for a career."""
    return CAREER_DATA.get(job_title)


def get_all_careers():
    """Return all available careers."""
    return list(CAREER_DATA.keys())


def get_career_skills(job_title):
    """Return required skills for a selected career."""
    return get_skills_for_job(job_title)


def get_career_resources(job_title):
    """
    Return resources grouped by the skills required for the career.
    """
    skills = get_career_skills(job_title)

    resources = {}

    for skill in skills:
        if skill in RESOURCE_LINKS:
            resources[skill] = RESOURCE_LINKS[skill]

    return resources


def build_career_items():
    """
    Build the career list used by the Flask templates.
    Each career contains:
        - career information
        - required skills
        - learning resources
    """

    career_items = []

    for job_title, data in CAREER_DATA.items():
        item = dict(data)

        item["skills"] = get_career_skills(job_title)
        item["resources"] = get_career_resources(job_title)

        career_items.append(item)

    return career_items


def get_resource_links():
    """Return all available learning resources."""
    return RESOURCE_LINKS


# Compatibility aliases
CAREERS = CAREER_DATA
RESOURCES = RESOURCE_LINKS