"""
job_provider.py
---------------
Live job search integration using the Adzuna Jobs API.

The application works even when Adzuna credentials are not configured.
In that case, the Live Jobs page shows a clear configuration message
instead of crashing.
"""

import os
import re

import requests


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

DEFAULT_COUNTRY = os.getenv("ADZUNA_COUNTRY", "in")

ADZUNA_BASE_URL = (
    "https://api.adzuna.com/v1/api/jobs"
)


# -------------------------------------------------------------------
# Helpers
# -------------------------------------------------------------------

def clean_html(text):
    """Remove HTML tags and normalize whitespace."""

    if not text:
        return ""

    text = str(text)

    # Remove HTML tags.
    text = re.sub(r"<[^>]+>", " ", text)

    # Decode common HTML entities without requiring extra packages.
    replacements = {
        "&amp;": "&",
        "&lt;": "<",
        "&gt;": ">",
        "&quot;": '"',
        "&#39;": "'",
        "&nbsp;": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# Backward-compatible alias.
re_clean = clean_html


def get_adzuna_config():
    """
    Return Adzuna configuration from environment variables.
    """

    return {
        "app_id": os.getenv(
            "ADZUNA_APP_ID",
            ""
        ).strip(),

        "app_key": os.getenv(
            "ADZUNA_APP_KEY",
            ""
        ).strip(),

        "country": os.getenv(
            "ADZUNA_COUNTRY",
            DEFAULT_COUNTRY
        ).strip().lower(),
    }


def is_jobs_configured():
    """Return True when Adzuna credentials are available."""

    config = get_adzuna_config()

    return bool(
        config["app_id"]
        and config["app_key"]
    )


def get_job_provider_status():
    """
    Return the current live-job provider status.
    """

    config = get_adzuna_config()

    configured = bool(
        config["app_id"]
        and config["app_key"]
    )

    return {
        "provider": "Adzuna",
        "configured": configured,
        "country": config["country"],
        "message": (
            "Live jobs are ready."
            if configured
            else (
                "Adzuna API credentials are not configured. "
                "Add ADZUNA_APP_ID and ADZUNA_APP_KEY to your .env file."
            )
        ),
    }


# -------------------------------------------------------------------
# Job normalization
# -------------------------------------------------------------------

def _extract_company(job):
    """Extract company name from an Adzuna job."""

    company = job.get("company")

    if isinstance(company, dict):
        return (
            company.get("display_name")
            or company.get("name")
            or ""
        )

    if company:
        return str(company)

    return "Company not specified"


def _extract_location(job):
    """Extract a readable location from an Adzuna job."""

    location = job.get("location")

    if isinstance(location, dict):
        display_name = location.get("display_name")

        if display_name:
            return str(display_name)

        area = location.get("area")

        if isinstance(area, list):
            return ", ".join(
                str(item)
                for item in area
                if item
            )

    if location:
        return str(location)

    return "Location not specified"


def _extract_category(job):
    """Extract category information."""

    category = job.get("category")

    if isinstance(category, dict):
        return (
            category.get("label")
            or category.get("tag")
            or ""
        )

    if category:
        return str(category)

    return ""


def _extract_salary(job):
    """Create a readable salary string."""

    minimum = job.get("salary_min")
    maximum = job.get("salary_max")

    if minimum and maximum:
        return f"{minimum} - {maximum}"

    if minimum:
        return str(minimum)

    if maximum:
        return str(maximum)

    return "Salary not specified"


def normalize_job(job):
    """
    Convert an Adzuna response item into the application's
    standard job structure.
    """

    return {
        "title": (
            job.get("title")
            or "Untitled Job"
        ),

        "company": _extract_company(job),

        "location": _extract_location(job),

        "description": clean_html(
            job.get("description", "")
        ),

        "url": (
            job.get("redirect_url")
            or job.get("url")
            or ""
        ),

        "created": (
            job.get("created")
            or ""
        ),

        "category": _extract_category(job),

        "salary": _extract_salary(job),

        "contract_type": (
            job.get("contract_type")
            or ""
        ),

        "contract_time": (
            job.get("contract_time")
            or ""
        ),

        "latitude": job.get("latitude"),

        "longitude": job.get("longitude"),
    }


# -------------------------------------------------------------------
# API request
# -------------------------------------------------------------------

def _build_search_url(country):
    """Build the Adzuna search endpoint."""

    country = country or DEFAULT_COUNTRY

    return (
        f"{ADZUNA_BASE_URL}/"
        f"{country}/search/1"
    )


def search_live_jobs(
    query="",
    location="",
    results_per_page=20,
):
    """
    Search live jobs through Adzuna.

    Parameters
    ----------
    query:
        Job title, skill, or keyword.

    location:
        Location such as Kerala, Thrissur, Kochi, etc.

    results_per_page:
        Number of jobs to request.

    Returns
    -------
    dict
        {
            "success": bool,
            "configured": bool,
            "jobs": list,
            "total": int,
            "message": str
        }
    """

    config = get_adzuna_config()

    # ---------------------------------------------------------------
    # Check credentials
    # ---------------------------------------------------------------

    if not config["app_id"] or not config["app_key"]:
        return {
            "success": False,
            "configured": False,
            "jobs": [],
            "total": 0,
            "message": (
                "Live jobs are not configured yet. "
                "Add ADZUNA_APP_ID and ADZUNA_APP_KEY "
                "to your .env file."
            ),
        }

    # ---------------------------------------------------------------
    # Clean parameters
    # ---------------------------------------------------------------

    query = str(query or "").strip()
    location = str(location or "").strip()

    try:
        results_per_page = int(results_per_page)
    except (TypeError, ValueError):
        results_per_page = 20

    results_per_page = max(
        1,
        min(results_per_page, 50)
    )

    # ---------------------------------------------------------------
    # API parameters
    # ---------------------------------------------------------------

    params = {
        "app_id": config["app_id"],
        "app_key": config["app_key"],
        "results_per_page": results_per_page,
        "sort_by": "date",
    }

    if query:
        params["what"] = query

    if location and location.lower() not in {
        "all",
        "all kerala",
        "kerala",
    }:
        params["where"] = location

    # ---------------------------------------------------------------
    # Request
    # ---------------------------------------------------------------

    url = _build_search_url(
        config["country"]
    )

    try:
        response = requests.get(
            url,
            params=params,
            timeout=15,
            headers={
                "User-Agent": (
                    "AI-Powered-Career-Skill-Gap-Analyzer/1.0"
                )
            },
        )

    except requests.exceptions.Timeout:
        return {
            "success": False,
            "configured": True,
            "jobs": [],
            "total": 0,
            "message": (
                "The live jobs service took too long to respond. "
                "Please try again."
            ),
        }

    except requests.exceptions.ConnectionError:
        return {
            "success": False,
            "configured": True,
            "jobs": [],
            "total": 0,
            "message": (
                "Could not connect to the live jobs service. "
                "Check your internet connection and try again."
            ),
        }

    except requests.exceptions.RequestException as exc:
        return {
            "success": False,
            "configured": True,
            "jobs": [],
            "total": 0,
            "message": (
                f"Live jobs request failed: {exc}"
            ),
        }

    # ---------------------------------------------------------------
    # HTTP errors
    # ---------------------------------------------------------------

    if response.status_code in {401, 403}:
        return {
            "success": False,
            "configured": True,
            "jobs": [],
            "total": 0,
            "message": (
                "Adzuna rejected the API credentials. "
                "Check ADZUNA_APP_ID and ADZUNA_APP_KEY."
            ),
        }

    if response.status_code == 429:
        return {
            "success": False,
            "configured": True,
            "jobs": [],
            "total": 0,
            "message": (
                "The live jobs API rate limit was reached. "
                "Please try again later."
            ),
        }

    if not response.ok:
        return {
            "success": False,
            "configured": True,
            "jobs": [],
            "total": 0,
            "message": (
                f"Live jobs service returned HTTP "
                f"{response.status_code}."
            ),
        }

    # ---------------------------------------------------------------
    # Parse JSON
    # ---------------------------------------------------------------

    try:
        data = response.json()

    except ValueError:
        return {
            "success": False,
            "configured": True,
            "jobs": [],
            "total": 0,
            "message": (
                "The live jobs service returned an invalid response."
            ),
        }

    # ---------------------------------------------------------------
    # Extract jobs
    # ---------------------------------------------------------------

    raw_jobs = data.get("results", [])

    if not isinstance(raw_jobs, list):
        raw_jobs = []

    jobs = [
        normalize_job(job)
        for job in raw_jobs
        if isinstance(job, dict)
    ]

    total = data.get(
        "count",
        len(jobs)
    )

    try:
        total = int(total)
    except (TypeError, ValueError):
        total = len(jobs)

    return {
        "success": True,
        "configured": True,
        "jobs": jobs,
        "total": total,
        "message": (
            f"Found {len(jobs)} live job"
            + ("" if len(jobs) == 1 else "s")
            + "."
        ),
    }


# -------------------------------------------------------------------
# Search jobs using skills
# -------------------------------------------------------------------

def search_jobs_for_skills(
    skills,
    location="",
    results_per_page=20,
):
    """
    Search jobs using a list of skills.

    Example:
        ["Python", "SQL", "Machine Learning"]

    The skills are combined into one search query.
    """

    if isinstance(skills, str):
        skills = [skills]

    skills = skills or []

    cleaned_skills = []

    for skill in skills:
        skill = str(skill or "").strip()

        if skill and skill not in cleaned_skills:
            cleaned_skills.append(skill)

    query = " ".join(
        cleaned_skills[:5]
    )

    return search_live_jobs(
        query=query,
        location=location,
        results_per_page=results_per_page,
    )


# -------------------------------------------------------------------
# Convenience function
# -------------------------------------------------------------------

def search_jobs(
    query="",
    location="",
    results_per_page=20,
):
    """
    Compatibility wrapper.

    Allows the application to use either:
        search_live_jobs()
    or:
        search_jobs()
    """

    return search_live_jobs(
        query=query,
        location=location,
        results_per_page=results_per_page,
    )


# -------------------------------------------------------------------
# Direct test
# -------------------------------------------------------------------

if __name__ == "__main__":
    status = get_job_provider_status()

    print("=" * 60)
    print("Live Job Provider")
    print("=" * 60)

    print(
        f"Provider   : {status['provider']}"
    )

    print(
        f"Configured : {status['configured']}"
    )

    print(
        f"Country    : {status['country']}"
    )

    print(
        f"Message    : {status['message']}"
    )

    print("=" * 60)

    if status["configured"]:
        result = search_live_jobs(
            query="Python",
            location="Kerala",
        )

        print(
            f"Success    : {result['success']}"
        )

        print(
            f"Total jobs : {result['total']}"
        )

        for job in result["jobs"][:5]:
            print(
                f"- {job['title']} | "
                f"{job['company']} | "
                f"{job['location']}"
            )
    else:
        print(
            "Add Adzuna credentials to .env "
            "to test live job searching."
        )