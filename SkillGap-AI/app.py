"""
app.py
------
Main Flask application for the
AI-Powered Career Skill Gap Analyzer.
"""

import os
from pathlib import Path

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash,
)
from werkzeug.utils import secure_filename

from analyzer import analyze_profile
from career_data import (
    CAREER_DATA,
    RESOURCE_LINKS,
    build_career_items,
    get_career_data,
    get_career_resources,
)
from database import (
    create_user,
    get_history,
    get_user_by_email,
    init_db,
    save_analysis,
)
from job_provider import (
    get_job_provider_status,
    search_live_jobs,
)
from llm_analyzer import (
    analyze_with_ai,
    get_ai_status,
    rewrite_resume_with_ai,
)
from resume_utils import (
    allowed_resume,
    extract_resume_text,
)
from skills_data import (
    get_all_skills,
    get_skills_for_job,
)


# ============================================================
# ENVIRONMENT LOADER
# ============================================================

BASE_DIR = Path(__file__).resolve().parent


def load_env_file(path=None):
    """
    Load simple KEY=VALUE entries from .env.

    python-dotenv is not required.
    """

    if path is None:
        path = BASE_DIR / ".env"

    path = Path(path)

    if not path.exists():
        return

    try:
        with path.open(
            "r",
            encoding="utf-8",
        ) as file:

            for raw_line in file:
                line = raw_line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                if "=" not in line:
                    continue

                key, value = line.split(
                    "=",
                    1,
                )

                key = key.strip()
                value = value.strip()

                if (
                    len(value) >= 2
                    and value[0] == value[-1]
                    and value[0] in {
                        '"',
                        "'",
                    }
                ):
                    value = value[1:-1]

                if key and key not in os.environ:
                    os.environ[key] = value

    except OSError:
        pass


# IMPORTANT:
# Environment must be loaded BEFORE importing/using
# AI and job-provider configuration.
load_env_file()


# ============================================================
# FLASK APPLICATION
# ============================================================

app = Flask(
    __name__,
)

app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "change-this-secret-key",
)

app.config["MAX_CONTENT_LENGTH"] = (
    10 * 1024 * 1024
)

UPLOAD_FOLDER = BASE_DIR / "uploads"

UPLOAD_FOLDER.mkdir(
    parents=True,
    exist_ok=True,
)

app.config["UPLOAD_FOLDER"] = str(
    UPLOAD_FOLDER
)


# ============================================================
# DATABASE
# ============================================================

init_db()


# ============================================================
# GLOBAL DATA
# ============================================================

CAREERS = CAREER_DATA

CAREER_ITEMS = build_career_items()

ALL_SKILLS = get_all_skills()

AI_STATUS = get_ai_status()

JOB_PROVIDER_STATUS = (
    get_job_provider_status()
)


# ============================================================
# KERALA DISTRICTS
# ============================================================

KERALA_DISTRICTS = [
    "Alappuzha",
    "Ernakulam",
    "Idukki",
    "Kannur",
    "Kasaragod",
    "Kollam",
    "Kottayam",
    "Kozhikode",
    "Malappuram",
    "Palakkad",
    "Pathanamthitta",
    "Thiruvananthapuram",
    "Thrissur",
    "Wayanad",
]


# ============================================================
# USER HELPERS
# ============================================================

def current_user():
    """Return the currently logged-in user."""

    return session.get(
        "user"
    )


def is_logged_in():
    """Return True when a user is logged in."""

    return current_user() is not None


# ============================================================
# SIMPLE AI FALLBACK
# ============================================================

def build_fallback_ai_analysis(
    matched_skills,
    missing_skills,
):
    """
    Provide useful analysis when OpenAI is unavailable.
    """

    matched_skills = matched_skills or []
    missing_skills = missing_skills or []

    return {
        "summary": (
            f"The resume matches "
            f"{len(matched_skills)} of "
            f"{len(matched_skills) + len(missing_skills)} "
            "identified role skills."
        ),

        "strengths": matched_skills[:6],

        "gaps": missing_skills[:8],

        "recommendations": [
            (
                f"Add genuine project or work evidence "
                f"for {skill} if you have experience with it."
            )
            for skill in missing_skills[:6]
        ],

        "resume_improvements": [
            "Use clear achievement-focused bullet points.",
            "Highlight relevant technical projects.",
            "Keep important role-specific skills visible.",
        ],

        "interview_focus": missing_skills[:6],
    }


# ============================================================
# TEMPLATE GLOBALS
# ============================================================

@app.context_processor
def inject_globals():
    """Make common data available to every template."""

    return {
        "project_name": (
            "AI-Powered Career Skill Gap Analyzer"
        ),

        "user": current_user(),

        "kerala_districts": (
            KERALA_DISTRICTS
        ),

        "ai_status": AI_STATUS,

        "job_provider_status": (
            JOB_PROVIDER_STATUS
        ),

        "all_skills": ALL_SKILLS,

        "careers": CAREERS,

        "career_items": CAREER_ITEMS,
    }


# ============================================================
# HOME
# ============================================================

@app.route("/")
def home():
    """Home page."""

    return render_template(
        "index.html",
        page="home",
        careers=CAREERS,
        career_items=CAREER_ITEMS,
    )


# ============================================================
# REGISTER
# ============================================================

@app.route(
    "/register",
    methods=["GET", "POST"],
)
def register():
    """Create a new account."""

    if request.method == "POST":

        name = request.form.get(
            "name",
            "",
        ).strip()

        email = request.form.get(
            "email",
            "",
        ).strip().lower()

        password = request.form.get(
            "password",
            "",
        )

        if not name:
            flash(
                "Please enter your name.",
                "error",
            )

            return redirect(
                url_for("register")
            )

        if not email:
            flash(
                "Please enter your email.",
                "error",
            )

            return redirect(
                url_for("register")
            )

        if len(password) < 6:
            flash(
                "Password must contain at least 6 characters.",
                "error",
            )

            return redirect(
                url_for("register")
            )

        existing_user = (
            get_user_by_email(email)
        )

        if existing_user:
            flash(
                "An account with this email already exists.",
                "error",
            )

            return redirect(
                url_for("login")
            )

        password_hash = (
            generate_password_hash(
                password
            )
        )

        user_id = create_user(
            name,
            email,
            password_hash,
        )

        if not user_id:
            flash(
                "Could not create the account.",
                "error",
            )

            return redirect(
                url_for("register")
            )

        session["user"] = {
            "id": user_id,
            "name": name,
            "email": email,
        }

        flash(
            "Account created successfully.",
            "success",
        )

        return redirect(
            url_for("home")
        )

    return render_template(
        "index.html",
        page="register",
        careers=CAREERS,
    )


# ============================================================
# LOGIN
# ============================================================

@app.route(
    "/login",
    methods=["GET", "POST"],
)
def login():
    """Log an existing user in."""

    if request.method == "POST":

        email = request.form.get(
            "email",
            "",
        ).strip().lower()

        password = request.form.get(
            "password",
            "",
        )

        user = get_user_by_email(
            email
        )

        if (
            not user
            or not check_password_hash(
                user["password_hash"],
                password,
            )
        ):
            flash(
                "Invalid email or password.",
                "error",
            )

            return redirect(
                url_for("login")
            )

        session["user"] = {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
        }

        flash(
            "Welcome back!",
            "success",
        )

        return redirect(
            url_for("home")
        )

    return render_template(
        "index.html",
        page="login",
        careers=CAREERS,
    )


# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
def logout():
    """Log the current user out."""

    session.pop(
        "user",
        None,
    )

    flash(
        "You have been logged out.",
        "success",
    )

    return redirect(
        url_for("home")
    )


# ============================================================
# SKILL ANALYZER
# ============================================================

@app.route(
    "/analyzer",
    methods=["GET", "POST"],
)
def analyzer_page():
    """
    Skill Analyzer page.

    This is the analyzer that works without uploading a resume.
    """

    result = None
    error = None

    selected_skills = []

    if request.method == "POST":

        target_job = request.form.get(
            "job",
            "",
        ).strip()

        selected_skills = request.form.getlist(
            "skills"
        )

        additional_skills = request.form.get(
            "additional_skills",
            "",
        ).strip()

        if additional_skills:

            selected_skills.extend(
                item.strip()
                for item in additional_skills.split(",")
                if item.strip()
            )

        if target_job not in CAREERS:

            error = (
                "Please select a valid career."
            )

        else:

            result = analyze_profile(
                resume_text="",
                target_job=target_job,
                selected_skills=selected_skills,
                additional_skills=additional_skills,
            )

    return render_template(
        "index.html",
        page="analyzer",
        careers=CAREERS,
        all_skills=ALL_SKILLS,
        result=result,
        error=error,
        selected_skills=selected_skills,
    )


# ============================================================
# RESUME ANALYZER
# ============================================================

@app.route(
    "/resume-analyzer",
    methods=["GET", "POST"],
)
def resume_analyzer():
    """Upload and analyze a resume."""

    result = None
    error = None

    selected_skills = []

    if request.method == "POST":

        target_job = request.form.get(
            "job",
            "",
        ).strip()

        job_description = request.form.get(
            "job_description",
            "",
        ).strip()

        selected_skills = request.form.getlist(
            "skills"
        )

        additional_skills = request.form.get(
            "additional_skills",
            "",
        ).strip()

        resume = request.files.get(
            "resume"
        )

        # --------------------------------------------------------
        # Validation
        # --------------------------------------------------------

        if target_job not in CAREERS:

            error = (
                "Please select a target career."
            )

        elif not resume or not resume.filename:

            error = (
                "Please upload a resume."
            )

        elif not allowed_resume(
            resume.filename
        ):

            error = (
                "Supported formats: "
                "PDF, DOCX, PNG, JPG and JPEG."
            )

        else:

            safe_filename = secure_filename(
                resume.filename
            )

            if not safe_filename:
                safe_filename = (
                    "uploaded_resume"
                )

            filepath = (
                UPLOAD_FOLDER
                / safe_filename
            )

            try:

                # ------------------------------------------------
                # Save file
                # ------------------------------------------------

                resume.save(
                    str(filepath)
                )

                # ------------------------------------------------
                # Extract text
                # ------------------------------------------------

                with filepath.open(
                    "rb"
                ) as file:

                    resume_text = (
                        extract_resume_text(
                            file,
                            safe_filename,
                        )
                    )

                if not resume_text.strip():

                    raise ValueError(
                        "No readable text was found in the resume. "
                        "For scanned PDFs/images, make sure "
                        "Tesseract OCR and Poppler are installed."
                    )

                # ------------------------------------------------
                # Rule-based analysis
                # ------------------------------------------------

                base_result = analyze_profile(
                    resume_text=resume_text,
                    target_job=target_job,
                    job_description=job_description,
                    selected_skills=selected_skills,
                    additional_skills=additional_skills,
                )

                # ------------------------------------------------
                # AI analysis
                # ------------------------------------------------

                ai_result = analyze_with_ai(
                    resume_text=resume_text,
                    target_job=target_job,
                    job_description=job_description,
                    matched_skills=(
                        base_result.get(
                            "matched_skills",
                            [],
                        )
                    ),
                    missing_skills=(
                        base_result.get(
                            "missing_skills",
                            [],
                        )
                    ),
                    ats_score=(
                        base_result.get(
                            "ats_score",
                            0,
                        )
                    ),
                    readiness_score=(
                        base_result.get(
                            "readiness_score",
                            0,
                        )
                    ),
                )

                if not ai_result:

                    ai_result = (
                        build_fallback_ai_analysis(
                            base_result.get(
                                "matched_skills",
                                [],
                            ),
                            base_result.get(
                                "missing_skills",
                                [],
                            ),
                        )
                    )

                    ai_status = (
                        "Rule-based fallback"
                    )

                else:

                    ai_status = (
                        "AI-powered"
                    )

                # ------------------------------------------------
                # Final result
                # ------------------------------------------------

                result = {
                    **base_result,

                    "ai": ai_result,

                    "ai_status": ai_status,

                    "resume_text": (
                        resume_text[:20000]
                    ),

                    "word_count": len(
                        resume_text.split()
                    ),

                    "filename": safe_filename,
                }

                # ------------------------------------------------
                # Save history
                # ------------------------------------------------

                if current_user():

                    save_analysis(
                        user_id=current_user()["id"],
                        filename=safe_filename,
                        target_job=target_job,
                        job_description=job_description,
                        result=result,
                    )

            except Exception as exc:

                error = (
                    f"Resume analysis failed: {exc}"
                )

    return render_template(
        "index.html",
        page="resume_analyzer",
        careers=CAREERS,
        all_skills=ALL_SKILLS,
        result=result,
        error=error,
        selected_skills=selected_skills,
    )


# ============================================================
# AI RESUME REWRITE
# ============================================================

@app.route(
    "/rewrite",
    methods=["POST"],
)
def rewrite_resume():
    """Generate an AI-improved resume."""

    data = (
        request.get_json(
            silent=True
        )
        or {}
    )

    resume_text = str(
        data.get(
            "resume_text",
            "",
        )
    ).strip()

    target_job = str(
        data.get(
            "target_job",
            "",
        )
    ).strip()

    job_description = str(
        data.get(
            "job_description",
            "",
        )
    ).strip()

    if not resume_text:

        return jsonify(
            {
                "error": (
                    "Resume text is required."
                )
            }
        ), 400

    if target_job not in CAREERS:

        return jsonify(
            {
                "error": (
                    "Please select a valid target career."
                )
            }
        ), 400

    result = rewrite_resume_with_ai(
        resume_text=resume_text,
        target_job=target_job,
        job_description=job_description,
    )

    if not result:

        return jsonify(
            {
                "error": (
                    "AI resume rewriting is not available. "
                    "Please configure OPENAI_API_KEY in your .env file."
                )
            }
        ), 503

    return jsonify(
        result
    )


# ============================================================
# CAREERS & RESOURCES
# ============================================================

@app.route("/careers")
def career_list():
    """Compatibility route."""

    return redirect(
        url_for(
            "careers_resources"
        )
    )


@app.route("/careers-resources")
def careers_resources():
    """Combined careers and learning resources page."""

    career_resources = {}

    for career_name in CAREERS:

        career_resources[
            career_name
        ] = get_career_resources(
            career_name
        )

    return render_template(
        "index.html",
        page="careers_resources",
        careers=CAREERS,
        career_items=CAREER_ITEMS,
        career_resources=career_resources,
    )


@app.route(
    "/career/<path:job>"
)
def career_details(job):
    """Show detailed information for one career."""

    if job not in CAREERS:

        return render_template(
            "index.html",
            page="404",
            careers=CAREERS,
        ), 404

    career = get_career_data(
        job
    )

    resources = get_career_resources(
        job
    )

    return render_template(
        "index.html",
        page="career_details",
        careers=CAREERS,
        job=job,
        career=career,
        career_resources=resources,
    )


@app.route("/resources")
def learning_resources():
    """Compatibility route for the old Resources URL."""

    return redirect(
        url_for(
            "careers_resources"
        )
    )


# ============================================================
# LIVE JOBS
# ============================================================

@app.route("/jobs")
def live_jobs():
    """Search live jobs using Adzuna."""

    query = request.args.get(
        "q",
        "",
    ).strip()

    location = request.args.get(
        "location",
        "",
    ).strip()

    jobs = []

    message = ""

    job_status = (
        get_job_provider_status()
    )

    if query:

        provider_location = location

        if location.lower() in {
            "",
            "all",
            "all kerala",
            "kerala",
        }:
            provider_location = ""

        response = search_live_jobs(
            query=query,
            location=provider_location,
        )

        jobs = response.get(
            "jobs",
            []
        )

        message = response.get(
            "message",
            "",
        )

    else:

        message = (
            "Select a job title or skill "
            "and a Kerala location, then "
            "click Search Jobs."
        )

    return render_template(
        "index.html",
        page="jobs",
        careers=CAREERS,
        jobs=jobs,
        jobs_message=message,
        query=query,
        location=location,
        job_provider_status=job_status,
    )


# ============================================================
# HISTORY
# ============================================================

@app.route("/history")
def history():
    """Show logged-in user's analysis history."""

    if not current_user():

        flash(
            "Please log in to view your analysis history.",
            "error",
        )

        return redirect(
            url_for("login")
        )

    records = get_history(
        current_user()["id"]
    )

    return render_template(
        "index.html",
        page="history",
        careers=CAREERS,
        history=records,
    )


# ============================================================
# ABOUT
# ============================================================

@app.route("/about")
def about():
    """About page."""

    return render_template(
        "index.html",
        page="about",
        careers=CAREERS,
    )


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(413)
def file_too_large(_error):
    """Handle files larger than 10 MB."""

    return render_template(
        "index.html",
        page="home",
        careers=CAREERS,
        error=(
            "The uploaded file is too large. "
            "Maximum allowed size is 10 MB."
        ),
    ), 413


@app.errorhandler(404)
def page_not_found(_error):
    """Handle missing pages."""

    return render_template(
        "index.html",
        page="404",
        careers=CAREERS,
    ), 404


@app.errorhandler(500)
def internal_server_error(_error):
    """Handle unexpected server errors."""

    return render_template(
        "index.html",
        page="500",
        careers=CAREERS,
        error=(
            "An unexpected server error occurred."
        ),
    ), 500


# ============================================================
# APPLICATION START
# ============================================================

if __name__ == "__main__":

    print(
        "=============================================="
    )

    print(
        " AI-Powered Career Skill Gap Analyzer"
    )

    print(
        "=============================================="
    )

    print(
        f"AI available: "
        f"{get_ai_status()['available']}"
    )

    print(
        f"AI model: "
        f"{get_ai_status()['model']}"
    )

    print(
        f"Live jobs configured: "
        f"{get_job_provider_status()['configured']}"
    )

    print(
        "Server: http://127.0.0.1:5000"
    )

    print(
        "=============================================="
    )

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000,
    )