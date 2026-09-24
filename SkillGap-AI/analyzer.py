from skills_data import job_skills

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Similar skill names
skill_aliases = {
    "ml": "machine learning",
    "machine learning": "machine learning",

    "dl": "deep learning",
    "deep learning": "deep learning",

    "python programming": "python",
    "python": "python",

    "structured query language": "sql",
    "sql": "sql",

    "object oriented programming": "oop",
    "oop": "oop",

    "tensorflow": "tensorflow",

    "numpy": "numpy",
    "pandas": "pandas",

    "data viz": "data visualization",
    "data visualization": "data visualization"
}


# Skill priority
skill_priority = {
    "Python": "High",
    "Machine Learning": "High",
    "SQL": "High",
    "Deep Learning": "High",
    "OOP": "High",

    "Pandas": "Medium",
    "NumPy": "Medium",
    "TensorFlow": "Medium",
    "Statistics": "Medium",
    "Git": "Medium",
    "Flask": "Medium",
    "Django": "Medium",
    "Data Visualization": "Medium",

    "Docker": "Low",
    "MLOps": "Low",
    "Excel": "Low"
}


# Priority weights
priority_weights = {
    "High": 3,
    "Medium": 2,
    "Low": 1
}


# Learning recommendations
skill_resources = {

    "Python":
        "Learn Python fundamentals, functions, data structures and OOP.",

    "SQL":
        "Learn SQL queries, joins, filtering and database concepts.",

    "Machine Learning":
        "Learn supervised learning, unsupervised learning and model evaluation.",

    "Deep Learning":
        "Learn neural networks, activation functions and deep learning models.",

    "TensorFlow":
        "Learn TensorFlow and use Keras to build machine learning models.",

    "Pandas":
        "Learn DataFrames, data cleaning and data analysis.",

    "NumPy":
        "Learn arrays, numerical operations and matrix calculations.",

    "Statistics":
        "Learn probability, distributions, mean, median and hypothesis testing.",

    "Docker":
        "Learn containers, images and how to deploy applications.",

    "MLOps":
        "Learn model deployment, pipelines, monitoring and ML workflows.",

    "Git":
        "Learn version control, commits, branches and GitHub.",

    "Flask":
        "Learn how to build Python web applications using Flask.",

    "Django":
        "Learn how to build full-stack web applications using Django.",

    "Excel":
        "Learn formulas, functions, charts and data analysis.",

    "OOP":
        "Learn classes, objects, inheritance and polymorphism.",

    "Data Visualization":
        "Learn how to create charts and visualize data."
}


# Free structured courses
course_links = {

    "Python":
        "https://www.kaggle.com/learn/python",

    "SQL":
        "https://www.kaggle.com/learn/intro-to-sql",

    "Machine Learning":
        "https://www.kaggle.com/learn/intro-to-machine-learning",

    "Deep Learning":
        "https://www.kaggle.com/learn/intro-to-deep-learning",

    "TensorFlow":
        "https://www.tensorflow.org/tutorials",

    "Pandas":
        "https://www.kaggle.com/learn/pandas",

    "NumPy":
        "https://www.w3schools.com/python/numpy/",

    "Statistics":
        "https://www.khanacademy.org/math/statistics-probability",

    "Docker":
        "https://docs.docker.com/get-started/",

    "MLOps":
        "https://www.tensorflow.org/tfx",

    "Git":
        "https://git-scm.com/book/en/v2",

    "Flask":
        "https://flask.palletsprojects.com/en/stable/tutorial/",

    "Django":
        "https://docs.djangoproject.com/en/stable/intro/tutorial01/",

    "Excel":
        "https://www.w3schools.com/excel/",

    "OOP":
        "https://docs.python.org/3/tutorial/classes.html",

    "Data Visualization":
        "https://www.kaggle.com/learn/data-visualization"
}


# Easy explanation links
easy_explanation_links = {

    "Python":
        "https://www.w3schools.com/python/",

    "SQL":
        "https://www.w3schools.com/sql/",

    "Machine Learning":
        "https://www.w3schools.com/python/python_ml_getting_started.asp",

    "Deep Learning":
        "https://www.tensorflow.org/tutorials",

    "TensorFlow":
        "https://www.tensorflow.org/learn",

    "Pandas":
        "https://www.w3schools.com/python/pandas/",

    "NumPy":
        "https://www.w3schools.com/python/numpy/",

    "Statistics":
        "https://www.w3schools.com/statistics/",

    "Docker":
        "https://www.docker.com/101-tutorial/",

    "MLOps":
        "https://www.tensorflow.org/tfx/guide",

    "Git":
        "https://www.w3schools.com/git/",

    "Flask":
        "https://www.w3schools.com/python/python_web_flask.asp",

    "Django":
        "https://www.w3schools.com/django/",

    "Excel":
        "https://www.w3schools.com/excel/",

    "OOP":
        "https://www.w3schools.com/python/python_classes.asp",

    "Data Visualization":
        "https://www.w3schools.com/python/matplotlib_intro.asp"
}


# YouTube learning links
youtube_links = {

    "Python":
        "https://www.youtube.com/results?search_query=Python+full+course+for+beginners",

    "SQL":
        "https://www.youtube.com/results?search_query=SQL+full+course+for+beginners",

    "Machine Learning":
        "https://www.youtube.com/results?search_query=Machine+Learning+full+course+for+beginners",

    "Deep Learning":
        "https://www.youtube.com/results?search_query=Deep+Learning+full+course+for+beginners",

    "TensorFlow":
        "https://www.youtube.com/results?search_query=TensorFlow+full+course+for+beginners",

    "Pandas":
        "https://www.youtube.com/results?search_query=Pandas+tutorial+for+beginners",

    "NumPy":
        "https://www.youtube.com/results?search_query=NumPy+tutorial+for+beginners",

    "Statistics":
        "https://www.youtube.com/results?search_query=Statistics+for+Data+Science+beginners",

    "Docker":
        "https://www.youtube.com/results?search_query=Docker+tutorial+for+beginners",

    "MLOps":
        "https://www.youtube.com/results?search_query=MLOps+tutorial+for+beginners",

    "Git":
        "https://www.youtube.com/results?search_query=Git+and+GitHub+tutorial+for+beginners",

    "Flask":
        "https://www.youtube.com/results?search_query=Flask+full+course+for+beginners",

    "Django":
        "https://www.youtube.com/results?search_query=Django+full+course+for+beginners",

    "Excel":
        "https://www.youtube.com/results?search_query=Excel+full+course+for+beginners",

    "OOP":
        "https://www.youtube.com/results?search_query=Python+OOP+tutorial+for+beginners",

    "Data Visualization":
        "https://www.youtube.com/results?search_query=Data+Visualization+Python+tutorial"
}


def normalize_skill(skill):

    skill = skill.strip().lower()

    if skill in skill_aliases:
        return skill_aliases[skill]

    return skill


def get_similarity(skill1, skill2):

    documents = [
        skill1.lower(),
        skill2.lower()
    ]

    vectorizer = TfidfVectorizer()

    tfidf_matrix = vectorizer.fit_transform(documents)

    similarity = cosine_similarity(
        tfidf_matrix[0],
        tfidf_matrix[1]
    )

    return similarity[0][0]


def get_readiness_level(score):

    if score < 40:
        return "Beginner"

    elif score < 60:
        return "Developing"

    elif score < 80:
        return "Intermediate"

    else:
        return "Job Ready"


def analyze_skills(user_skills, target_job):

    required_skills = job_skills[target_job]

    normalized_user_skills = []

    for skill in user_skills:
        normalized_user_skills.append(
            normalize_skill(skill)
        )


    matching_skills = []
    missing_skills = []


    for required_skill in required_skills:

        normalized_required_skill = normalize_skill(
            required_skill
        )

        found_match = False


        for user_skill in normalized_user_skills:

            if normalized_required_skill == user_skill:

                found_match = True
                break


            similarity = get_similarity(
                normalized_required_skill,
                user_skill
            )


            if similarity >= 0.7:

                found_match = True
                break


        if found_match:

            matching_skills.append(required_skill)

        else:

            missing_skills.append(required_skill)


    # Weighted readiness score
    total_weight = 0
    matched_weight = 0


    for skill in required_skills:

        priority = skill_priority.get(
            skill,
            "Medium"
        )

        weight = priority_weights[priority]

        total_weight += weight


        if skill in matching_skills:

            matched_weight += weight


    readiness_score = (
        matched_weight / total_weight
    ) * 100


    readiness_level = get_readiness_level(
        readiness_score
    )


    # Learning path
    learning_path = []


    for skill in missing_skills:

        priority = skill_priority.get(
            skill,
            "Medium"
        )


        resource = skill_resources.get(
            skill,
            "Learn the fundamentals and practice this skill."
        )


        course_link = course_links.get(
            skill,
            "https://www.kaggle.com/learn"
        )


        easy_link = easy_explanation_links.get(
            skill,
            "https://www.w3schools.com/"
        )


        youtube_link = youtube_links.get(
            skill,
            "https://www.youtube.com/"
        )


        learning_path.append({

            "skill": skill,

            "priority": priority,

            "resource": resource,

            "course_link": course_link,

            "easy_link": easy_link,

            "youtube_link": youtube_link

        })


    # Sort by priority
    priority_order = {
        "High": 1,
        "Medium": 2,
        "Low": 3
    }


    learning_path.sort(
        key=lambda item:
        priority_order[item["priority"]]
    )


    return (
        matching_skills,
        missing_skills,
        readiness_score,
        readiness_level,
        learning_path
    )