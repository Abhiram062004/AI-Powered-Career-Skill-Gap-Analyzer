"""
analyzer.py
-----------
Core resume and career skill-gap analysis engine.

Features:
- Resume skill detection
- Career skill comparison
- Job-description keyword analysis
- ATS score
- Career readiness score
- Matched / missing skills
- Evidence extraction
- Learning roadmap
- Free resources
- Skill analyzer without a resume
- No external ML package required
"""

import re
from collections import Counter

from skills_data import (
    get_all_skills,
    get_skills_for_job,
)


# ============================================================
# SKILL ALIASES
# ============================================================

SKILL_ALIASES = {
    "ml": "machine learning",
    "machine learning": "machine learning",

    "dl": "deep learning",
    "deep learning": "deep learning",

    "python programming": "python",
    "python": "python",

    "structured query language": "sql",
    "sql": "sql",

    "object oriented programming": "oop",
    "object oriented programming language": "oop",
    "oop": "oop",

    "sklearn": "scikit-learn",
    "scikit learn": "scikit-learn",
    "scikit-learn": "scikit-learn",

    "tensorflow": "tensorflow",

    "pytorch": "pytorch",

    "numpy": "numpy",

    "pandas": "pandas",

    "data viz": "data visualization",
    "data visualization": "data visualization",

    "natural language processing": "nlp",
    "nlp": "nlp",

    "large language model": "llms",
    "large language models": "llms",
    "llm": "llms",
    "llms": "llms",

    "powerbi": "power bi",
    "power bi": "power bi",

    "ms excel": "excel",
    "microsoft excel": "excel",
    "excel": "excel",

    "version control": "git",
    "git": "git",

    "containerization": "docker",
    "docker": "docker",

    "machine learning operations": "mlops",
    "ml ops": "mlops",
    "mlops": "mlops",
}


# ============================================================
# SKILL PRIORITY
# ============================================================

SKILL_PRIORITY = {
    "Python": "High",
    "Machine Learning": "High",
    "SQL": "High",
    "Deep Learning": "High",
    "OOP": "High",
    "LLMs": "High",
    "NLP": "High",

    "Pandas": "Medium",
    "NumPy": "Medium",
    "TensorFlow": "Medium",
    "PyTorch": "Medium",
    "Statistics": "Medium",
    "Git": "Medium",
    "Flask": "Medium",
    "Django": "Medium",
    "Data Visualization": "Medium",
    "Power BI": "Medium",
    "Scikit-learn": "Medium",

    "Docker": "Low",
    "MLOps": "Low",
    "Excel": "Low",
}


PRIORITY_WEIGHTS = {
    "High": 3,
    "Medium": 2,
    "Low": 1,
}


# ============================================================
# LEARNING RESOURCES
# ============================================================

FREE_RESOURCES = {

    "Python":
        "https://docs.python.org/3/tutorial/",

    "SQL":
        "https://www.w3schools.com/sql/",

    "Excel":
        "https://support.microsoft.com/excel",

    "Pandas":
        "https://pandas.pydata.org/docs/getting_started/intro_tutorials/",

    "NumPy":
        "https://numpy.org/learn/",

    "Machine Learning":
        "https://developers.google.com/machine-learning/crash-course",

    "Deep Learning":
        "https://www.tensorflow.org/tutorials",

    "TensorFlow":
        "https://www.tensorflow.org/learn",

    "PyTorch":
        "https://pytorch.org/tutorials/",

    "Scikit-learn":
        "https://scikit-learn.org/stable/getting_started.html",

    "Statistics":
        "https://www.khanacademy.org/math/statistics-probability",

    "Data Visualization":
        "https://www.data-to-viz.com/",

    "Power BI":
        "https://learn.microsoft.com/en-us/training/powerplatform/power-bi/",

    "Docker":
        "https://docs.docker.com/get-started/",

    "MLOps":
        "https://ml-ops.org/",

    "Git":
        "https://git-scm.com/book/en/v2",

    "Flask":
        "https://flask.palletsprojects.com/en/stable/tutorial/",

    "Django":
        "https://docs.djangoproject.com/en/stable/intro/tutorial/",

    "OOP":
        "https://docs.python.org/3/tutorial/classes.html",

    "NLP":
        "https://huggingface.co/learn/nlp-course/chapter1/1",

    "LLMs":
        "https://huggingface.co/learn/llm-course/chapter1/1",
}


YOUTUBE_RESOURCES = {

    "Python":
        "https://www.youtube.com/results?search_query=Python+full+course+for+beginners",

    "SQL":
        "https://www.youtube.com/results?search_query=SQL+full+course+for+beginners",

    "Excel":
        "https://www.youtube.com/results?search_query=Excel+full+course+for+beginners",

    "Pandas":
        "https://www.youtube.com/results?search_query=Pandas+tutorial+for+beginners",

    "NumPy":
        "https://www.youtube.com/results?search_query=NumPy+tutorial+for+beginners",

    "Machine Learning":
        "https://www.youtube.com/results?search_query=Machine+Learning+full+course+for+beginners",

    "Deep Learning":
        "https://www.youtube.com/results?search_query=Deep+Learning+full+course+for+beginners",

    "TensorFlow":
        "https://www.youtube.com/results?search_query=TensorFlow+tutorial+for+beginners",

    "PyTorch":
        "https://www.youtube.com/results?search_query=PyTorch+tutorial+for+beginners",

    "Scikit-learn":
        "https://www.youtube.com/results?search_query=Scikit-learn+tutorial+for+beginners",

    "Statistics":
        "https://www.youtube.com/results?search_query=Statistics+for+Data+Science+beginners",

    "Data Visualization":
        "https://www.youtube.com/results?search_query=Data+Visualization+Python+tutorial",

    "Power BI":
        "https://www.youtube.com/results?search_query=Power+BI+full+course+for+beginners",

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

    "OOP":
        "https://www.youtube.com/results?search_query=Python+OOP+tutorial+for+beginners",

    "NLP":
        "https://www.youtube.com/results?search_query=Natural+Language+Processing+NLP+tutorial",

    "LLMs":
        "https://www.youtube.com/results?search_query=Large+Language+Models+LLM+tutorial",
}


# ============================================================
# TEXT HELPERS
# ============================================================

def clean_text(text):
    """Normalize text for analysis."""

    if not text:
        return ""

    text = str(text)

    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    return text.strip()


def normalize_skill(skill):
    """
    Normalize a skill name.

    Example:
        ML -> machine learning
        Python Programming -> python
    """

    if not skill:
        return ""

    skill = str(skill).strip().lower()

    skill = re.sub(
        r"\s+",
        " ",
        skill,
    )

    return SKILL_ALIASES.get(
        skill,
        skill,
    )


def canonical_skill_name(skill):
    """
    Convert normalized skill names back to display names.
    """

    normalized = normalize_skill(
        skill
    )

    mapping = {

        "python": "Python",

        "sql": "SQL",

        "excel": "Excel",

        "pandas": "Pandas",

        "numpy": "NumPy",

        "machine learning":
            "Machine Learning",

        "deep learning":
            "Deep Learning",

        "tensorflow":
            "TensorFlow",

        "pytorch":
            "PyTorch",

        "scikit-learn":
            "Scikit-learn",

        "statistics":
            "Statistics",

        "data visualization":
            "Data Visualization",

        "docker":
            "Docker",

        "mlops":
            "MLOps",

        "git":
            "Git",

        "flask":
            "Flask",

        "django":
            "Django",

        "oop":
            "OOP",

        "nlp":
            "NLP",

        "llms":
            "LLMs",

        "power bi":
            "Power BI",
    }

    return mapping.get(
        normalized,
        str(skill).strip(),
    )


# ============================================================
# SKILL MATCHING
# ============================================================

def skill_present(text, skill):
    """
    Determine whether a skill is present in text.

    Uses phrase matching instead of simple substring matching
    to reduce false positives.
    """

    if not text or not skill:
        return False

    text_lower = text.lower()

    normalized = normalize_skill(
        skill
    )

    # Different possible phrases.
    aliases = [
        normalized,
        str(skill).lower(),
    ]

    if normalized == "machine learning":
        aliases.extend([
            "machine learning",
            "machine-learning",
            "ml",
        ])

    elif normalized == "deep learning":
        aliases.extend([
            "deep learning",
            "deep-learning",
            "dl",
        ])

    elif normalized == "scikit-learn":
        aliases.extend([
            "scikit-learn",
            "scikit learn",
            "sklearn",
        ])

    elif normalized == "llms":
        aliases.extend([
            "llm",
            "llms",
            "large language model",
            "large language models",
        ])

    elif normalized == "nlp":
        aliases.extend([
            "nlp",
            "natural language processing",
        ])

    elif normalized == "power bi":
        aliases.extend([
            "power bi",
            "powerbi",
        ])

    # Remove duplicates.
    aliases = list(
        dict.fromkeys(
            aliases
        )
    )

    for alias in aliases:

        alias = alias.strip()

        if not alias:
            continue

        pattern = (
            r"(?<![a-zA-Z0-9])"
            + re.escape(alias)
            + r"(?![a-zA-Z0-9])"
        )

        if re.search(
            pattern,
            text_lower,
        ):
            return True

    return False


def get_similarity(skill1, skill2):
    """
    Lightweight similarity score between two skill names.

    This avoids requiring scikit-learn.
    """

    a = normalize_skill(skill1)
    b = normalize_skill(skill2)

    if not a or not b:
        return 0.0

    if a == b:
        return 1.0

    a_words = set(a.split())
    b_words = set(b.split())

    if not a_words or not b_words:
        return 0.0

    intersection = len(
        a_words & b_words
    )

    union = len(
        a_words | b_words
    )

    if union == 0:
        return 0.0

    return intersection / union


def skills_match(
    required_skill,
    user_skills,
):
    """
    Check whether a required skill is represented
    in a user's selected skills.
    """

    required_normalized = (
        normalize_skill(
            required_skill
        )
    )

    for user_skill in user_skills:

        user_normalized = (
            normalize_skill(
                user_skill
            )
        )

        if (
            required_normalized
            == user_normalized
        ):
            return True

        if get_similarity(
            required_normalized,
            user_normalized,
        ) >= 0.75:
            return True

    return False


# ============================================================
# RESUME SKILL EXTRACTION
# ============================================================

def extract_skills_from_resume(
    resume_text,
):
    """
    Detect known skills in resume text.
    """

    resume_text = clean_text(
        resume_text
    )

    detected = []

    for skill in get_all_skills():

        if skill_present(
            resume_text,
            skill,
        ):

            detected.append(skill)

    return detected


# ============================================================
# JOB DESCRIPTION
# ============================================================

def extract_job_keywords(
    job_description,
):
    """
    Extract known skills appearing in a job description.
    """

    if not job_description:
        return []

    detected = []

    for skill in get_all_skills():

        if skill_present(
            job_description,
            skill,
        ):

            detected.append(skill)

    return detected


# ============================================================
# READINESS
# ============================================================

def get_readiness_level(score):
    """Convert score to a readable readiness level."""

    if score < 40:
        return "Beginner"

    if score < 60:
        return "Developing"

    if score < 80:
        return "Intermediate"

    return "Job Ready"


def calculate_readiness(
    required_skills,
    matched_skills,
):
    """
    Calculate weighted career readiness.
    """

    if not required_skills:
        return 0

    total_weight = 0
    matched_weight = 0

    matched_normalized = {
        normalize_skill(skill)
        for skill in matched_skills
    }

    for skill in required_skills:

        priority = SKILL_PRIORITY.get(
            skill,
            "Medium",
        )

        weight = PRIORITY_WEIGHTS.get(
            priority,
            2,
        )

        total_weight += weight

        if normalize_skill(skill) in matched_normalized:
            matched_weight += weight

    if total_weight == 0:
        return 0

    score = (
        matched_weight
        / total_weight
    ) * 100

    return round(
        max(0, min(100, score))
    )


# ============================================================
# ATS SCORE
# ============================================================

def calculate_ats_score(
    resume_text,
    required_skills,
    matched_skills,
    job_description="",
):
    """
    Calculate an ATS-style score.

    Components:
    - Required skill coverage
    - Job-description keyword coverage
    - Resume structure indicators
    """

    if not resume_text:
        return 0

    resume_text_lower = (
        resume_text.lower()
    )

    # --------------------------------------------------------
    # Skill coverage
    # --------------------------------------------------------

    if required_skills:

        skill_score = (
            len(matched_skills)
            / len(required_skills)
        ) * 70

    else:

        skill_score = 0


    # --------------------------------------------------------
    # Job-description matching
    # --------------------------------------------------------

    jd_score = 0

    jd_skills = extract_job_keywords(
        job_description
    )

    if jd_skills:

        jd_matched = 0

        for skill in jd_skills:

            if skill_present(
                resume_text,
                skill,
            ):
                jd_matched += 1

        jd_score = (
            jd_matched
            / len(jd_skills)
        ) * 20


    # --------------------------------------------------------
    # Resume structure
    # --------------------------------------------------------

    structure_keywords = [
        "education",
        "experience",
        "skills",
        "projects",
        "certifications",
    ]

    structure_matches = sum(
        1
        for keyword in structure_keywords
        if keyword in resume_text_lower
    )

    structure_score = (
        structure_matches
        / len(structure_keywords)
    ) * 10

    score = (
        skill_score
        + jd_score
        + structure_score
    )

    return round(
        max(0, min(100, score))
    )


# ============================================================
# EVIDENCE
# ============================================================

def extract_skill_evidence(
    resume_text,
    skills,
    max_lines=3,
):
    """
    Find resume lines that provide evidence for each skill.
    """

    evidence = {}

    if not resume_text:
        return evidence

    lines = [
        line.strip()
        for line in resume_text.splitlines()
        if line.strip()
    ]

    for skill in skills:

        matching_lines = []

        for line in lines:

            if skill_present(
                line,
                skill,
            ):

                matching_lines.append(
                    line
                )

            if len(
                matching_lines
            ) >= max_lines:
                break

        if matching_lines:

            evidence[skill] = (
                matching_lines
            )

    return evidence


# ============================================================
# SUGGESTIONS
# ============================================================

def generate_suggestions(
    missing_skills,
    ats_score,
    resume_text,
):
    """
    Generate deterministic resume improvement suggestions.
    """

    suggestions = []

    # --------------------------------------------------------
    # Missing skills
    # --------------------------------------------------------

    if missing_skills:

        important = missing_skills[:6]

        suggestions.append(
            "Build genuine projects or learning evidence "
            "for these missing skills: "
            + ", ".join(important)
            + "."
        )

    # --------------------------------------------------------
    # ATS score
    # --------------------------------------------------------

    if ats_score < 60:

        suggestions.append(
            "Improve ATS alignment by using clear section "
            "headings such as Skills, Projects, Education "
            "and Experience."
        )

    elif ats_score < 80:

        suggestions.append(
            "Improve keyword alignment with the target "
            "career and job description."
        )

    else:

        suggestions.append(
            "Maintain clear, concise and role-specific "
            "resume wording."
        )

    # --------------------------------------------------------
    # Resume length
    # --------------------------------------------------------

    word_count = len(
        resume_text.split()
    )

    if word_count < 250:

        suggestions.append(
            "Your resume appears short. Add relevant "
            "projects, technical skills or achievements "
            "that are genuinely supported by your experience."
        )

    elif word_count > 1200:

        suggestions.append(
            "Consider removing repetitive information "
            "and keeping the resume focused on the target role."
        )

    # --------------------------------------------------------
    # Projects
    # --------------------------------------------------------

    if "project" not in resume_text.lower():

        suggestions.append(
            "Add relevant academic or personal projects "
            "that demonstrate your technical skills."
        )

    return suggestions


# ============================================================
# ROADMAP
# ============================================================

def build_roadmap(
    missing_skills,
):
    """
    Create a learning roadmap from missing skills.
    """

    roadmap = []

    for index, skill in enumerate(
        missing_skills,
        start=1,
    ):

        priority = SKILL_PRIORITY.get(
            skill,
            "Medium",
        )

        if priority == "High":

            description = (
                f"Prioritize {skill}. "
                f"Learn the fundamentals, practice "
                f"with exercises and build at least "
                f"one practical project."
            )

        elif priority == "Medium":

            description = (
                f"Develop working knowledge of {skill} "
                f"through a structured course and a "
                f"small practical project."
            )

        else:

            description = (
                f"Learn the basics of {skill} and "
                f"practice it when working on projects."
            )

        roadmap.append(
            {
                "step": index,
                "title": skill,
                "description": description,
                "priority": priority,
            }
        )

    return roadmap


# ============================================================
# RESOURCES
# ============================================================

def get_resources_for_skills(
    skills,
):
    """
    Return free resources and YouTube resources
    for each skill.
    """

    resources = {}

    for skill in skills:

        free_url = FREE_RESOURCES.get(
            skill
        )

        youtube_url = YOUTUBE_RESOURCES.get(
            skill
        )

        links = []

        if free_url:

            links.append(
                {
                    "name": "Free Course / Documentation",
                    "url": free_url,
                    "type": "free",
                }
            )

        if youtube_url:

            links.append(
                {
                    "name": "YouTube Tutorials",
                    "url": youtube_url,
                    "type": "youtube",
                }
            )

        if links:

            resources[skill] = links

    return resources


# ============================================================
# SKILL ANALYZER
# ============================================================

def analyze_skills(
    user_skills,
    target_job,
):
    """
    Analyze manually selected skills against a career.
    """

    user_skills = user_skills or []

    required_skills = (
        get_skills_for_job(
            target_job
        )
    )

    normalized_user = []

    for skill in user_skills:

        if skill:

            display = canonical_skill_name(
                skill
            )

            if display not in normalized_user:

                normalized_user.append(
                    display
                )

    matched_skills = []
    missing_skills = []

    for required_skill in required_skills:

        if skills_match(
            required_skill,
            normalized_user,
        ):

            matched_skills.append(
                required_skill
            )

        else:

            missing_skills.append(
                required_skill
            )

    readiness_score = calculate_readiness(
        required_skills,
        matched_skills,
    )

    roadmap = build_roadmap(
        missing_skills
    )

    resources = get_resources_for_skills(
        missing_skills
    )

    return {
        "target_job": target_job,

        "required_skills":
            required_skills,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "readiness_score":
            readiness_score,

        "career_readiness_score":
            readiness_score,

        "readiness_level":
            get_readiness_level(
                readiness_score
            ),

        "ats_score":
            0,

        "evidence":
            {},

        "suggestions":
            [
                (
                    f"Learn {skill} and practice it "
                    "through a practical project."
                )
                for skill in missing_skills[:6]
            ],

        "roadmap":
            roadmap,

        "resources":
            resources,
    }


# ============================================================
# MAIN ANALYZER
# ============================================================

def analyze_profile(
    resume_text="",
    target_job="",
    job_description="",
    selected_skills=None,
    additional_skills="",
    **kwargs,
):
    """
    Main analysis function.

    Parameters
    ----------
    resume_text:
        Extracted resume text.

    target_job:
        Career selected by the user.

    job_description:
        Optional job description.

    selected_skills:
        Skills manually selected by the user.

    additional_skills:
        Comma-separated additional skills.

    Returns
    -------
    dict
        Complete analysis result.
    """

    # --------------------------------------------------------
    # Backward compatibility
    # --------------------------------------------------------

    if not resume_text:

        resume_text = kwargs.get(
            "text",
            "",
        )

    if not target_job:

        target_job = kwargs.get(
            "job",
            "",
        )

    if selected_skills is None:

        selected_skills = kwargs.get(
            "skills",
            [],
        )

    resume_text = clean_text(
        resume_text
    )

    job_description = clean_text(
        job_description
    )

    # --------------------------------------------------------
    # Required career skills
    # --------------------------------------------------------

    required_skills = (
        get_skills_for_job(
            target_job
        )
    )

    # --------------------------------------------------------
    # Resume skills
    # --------------------------------------------------------

    resume_skills = (
        extract_skills_from_resume(
            resume_text
        )
    )

    # --------------------------------------------------------
    # Manual skills
    # --------------------------------------------------------

    manual_skills = []

    for skill in (
        selected_skills or []
    ):

        if skill:

            manual_skills.append(
                canonical_skill_name(
                    skill
                )
            )

    if additional_skills:

        if isinstance(
            additional_skills,
            str,
        ):

            additional_list = (
                additional_skills.split(",")
            )

        else:

            additional_list = (
                additional_skills
            )

        for skill in additional_list:

            skill = str(
                skill
            ).strip()

            if skill:

                manual_skills.append(
                    canonical_skill_name(
                        skill
                    )
                )

    # --------------------------------------------------------
    # Combine detected + manual skills
    # --------------------------------------------------------

    all_user_skills = []

    for skill in (
        resume_skills
        + manual_skills
    ):

        if skill not in all_user_skills:

            all_user_skills.append(
                skill
            )

    # --------------------------------------------------------
    # Job description skills
    # --------------------------------------------------------

    job_skills = (
        extract_job_keywords(
            job_description
        )
    )

    # --------------------------------------------------------
    # Determine matched / missing
    # --------------------------------------------------------

    matched_skills = []
    missing_skills = []

    for required_skill in required_skills:

        if skills_match(
            required_skill,
            all_user_skills,
        ):

            matched_skills.append(
                required_skill
            )

        else:

            missing_skills.append(
                required_skill
            )

    # --------------------------------------------------------
    # Job description matching
    # --------------------------------------------------------

    job_matched_skills = []

    for skill in job_skills:

        if skill_present(
            resume_text,
            skill,
        ):

            job_matched_skills.append(
                skill
            )

    # --------------------------------------------------------
    # Readiness
    # --------------------------------------------------------

    readiness_score = calculate_readiness(
        required_skills,
        matched_skills,
    )

    readiness_level = (
        get_readiness_level(
            readiness_score
        )
    )

    # --------------------------------------------------------
    # ATS
    # --------------------------------------------------------

    ats_score = calculate_ats_score(
        resume_text=resume_text,
        required_skills=required_skills,
        matched_skills=matched_skills,
        job_description=job_description,
    )

    # --------------------------------------------------------
    # Evidence
    # --------------------------------------------------------

    evidence = extract_skill_evidence(
        resume_text,
        matched_skills,
    )

    # --------------------------------------------------------
    # Suggestions
    # --------------------------------------------------------

    suggestions = generate_suggestions(
        missing_skills,
        ats_score,
        resume_text,
    )

    # --------------------------------------------------------
    # Roadmap
    # --------------------------------------------------------

    roadmap = build_roadmap(
        missing_skills
    )

    # --------------------------------------------------------
    # Resources
    # --------------------------------------------------------

    resources = get_resources_for_skills(
        missing_skills
    )

    # --------------------------------------------------------
    # Resume statistics
    # --------------------------------------------------------

    word_count = len(
        resume_text.split()
    )

    # --------------------------------------------------------
    # Result
    # --------------------------------------------------------

    return {

        "target_job":
            target_job,

        "required_skills":
            required_skills,

        "matched_skills":
            matched_skills,

        "missing_skills":
            missing_skills,

        "readiness_score":
            readiness_score,

        "career_readiness_score":
            readiness_score,

        "readiness_level":
            readiness_level,

        "ats_score":
            ats_score,

        "evidence":
            evidence,

        "suggestions":
            suggestions,

        "roadmap":
            roadmap,

        "resources":
            resources,

        "resume_skills":
            resume_skills,

        "selected_skills":
            manual_skills,

        "job_description_skills":
            job_skills,

        "job_matched_skills":
            job_matched_skills,

        "word_count":
            word_count,

        "skill_count":
            len(all_user_skills),

        "analysis_summary":
            (
                f"Matched {len(matched_skills)} "
                f"of {len(required_skills)} "
                f"required skills."
            ),
    }


# ============================================================
# COMPATIBILITY HELPERS
# ============================================================

def get_required_skills(target_job):
    """Return required skills for a career."""

    return get_skills_for_job(
        target_job
    )


def get_skill_resources(skill):
    """Return learning resources for one skill."""

    return get_resources_for_skills(
        [skill]
    ).get(
        skill,
        [],
    )


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("AI Career Skill Gap Analyzer")
    print("Analyzer module test")
    print("=" * 60)

    test_result = analyze_profile(
        resume_text=(
            """
            Python developer with experience in SQL,
            Pandas, NumPy and Machine Learning.
            Built machine learning projects using Python.
            """
        ),
        target_job="Machine Learning Engineer",
    )

    print(
        "Target:",
        test_result["target_job"],
    )

    print(
        "Matched:",
        test_result["matched_skills"],
    )

    print(
        "Missing:",
        test_result["missing_skills"],
    )

    print(
        "Readiness:",
        f"{test_result['readiness_score']}%",
    )

    print(
        "ATS:",
        f"{test_result['ats_score']}%",
    )

    print("=" * 60)