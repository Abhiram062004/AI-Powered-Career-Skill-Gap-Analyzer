"""
llm_analyzer.py
---------------
Optional AI analysis and AI resume rewriting.

If OPENAI_API_KEY is not configured, the application continues
working using the deterministic analyzer in analyzer.py.
"""

import json
import os
import re


# -------------------------------------------------------------------
# Optional OpenAI import
# -------------------------------------------------------------------

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

DEFAULT_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.6-luna",
)


# -------------------------------------------------------------------
# OpenAI client
# -------------------------------------------------------------------

def get_client():
    """
    Create an OpenAI client when the SDK and API key are available.
    """

    if OpenAI is None:
        return None

    api_key = os.getenv(
        "OPENAI_API_KEY",
        ""
    ).strip()

    if not api_key:
        return None

    try:
        return OpenAI(
            api_key=api_key
        )
    except Exception:
        return None


# -------------------------------------------------------------------
# JSON helpers
# -------------------------------------------------------------------

def _extract_json(text):
    """
    Extract JSON from an AI response.

    Handles:
    - normal JSON
    - ```json ... ```
    - extra text around JSON
    """

    if not text:
        return {}

    text = str(text).strip()

    # ---------------------------------------------------------------
    # Direct JSON
    # ---------------------------------------------------------------

    try:
        data = json.loads(text)

        if isinstance(data, dict):
            return data

    except (TypeError, ValueError, json.JSONDecodeError):
        pass

    # ---------------------------------------------------------------
    # Markdown code block
    # ---------------------------------------------------------------

    code_match = re.search(
        r"```(?:json)?\s*(.*?)\s*```",
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    if code_match:
        candidate = code_match.group(1).strip()

        try:
            data = json.loads(candidate)

            if isinstance(data, dict):
                return data

        except (
            TypeError,
            ValueError,
            json.JSONDecodeError,
        ):
            pass

    # ---------------------------------------------------------------
    # Find first JSON object
    # ---------------------------------------------------------------

    start = text.find("{")
    end = text.rfind("}")

    if start != -1 and end > start:
        candidate = text[start:end + 1]

        try:
            data = json.loads(candidate)

            if isinstance(data, dict):
                return data

        except (
            TypeError,
            ValueError,
            json.JSONDecodeError,
        ):
            pass

    return {}


# -------------------------------------------------------------------
# Generic LLM call
# -------------------------------------------------------------------

def call_llm(
    instructions,
    input_text,
    model=None,
):
    """
    Send a request to the configured OpenAI model.

    Returns:
        parsed dictionary
        or None if the request fails.
    """

    client = get_client()

    if client is None:
        return None

    model = model or DEFAULT_MODEL

    try:
        response = client.responses.create(
            model=model,
            instructions=instructions,
            input=input_text,
            text={
                "format": {
                    "type": "json_object"
                }
            },
        )

        output_text = getattr(
            response,
            "output_text",
            ""
        )

        if not output_text:
            return None

        return _extract_json(
            output_text
        )

    except Exception as exc:
        print(
            f"[AI] Request failed: {exc}"
        )

        return None


# -------------------------------------------------------------------
# AI career analysis
# -------------------------------------------------------------------

def analyze_with_ai(
    resume_text,
    target_job="",
    job_description="",
    matched_skills=None,
    missing_skills=None,
    ats_score=0,
    readiness_score=0,
):
    """
    Perform optional AI-powered analysis of a resume.

    The AI is instructed to use only information actually present
    in the resume and supplied analysis data.
    """

    matched_skills = matched_skills or []
    missing_skills = missing_skills or []

    instructions = """
You are an AI career and resume analysis assistant.

Analyze the candidate's resume for the specified target career.

IMPORTANT RULES:
1. Never invent education, employment, internships, projects,
   certifications, technologies, achievements, or experience.
2. Only use facts explicitly present in the supplied resume.
3. Clearly distinguish resume evidence from recommendations.
4. Missing skills are not proof that the candidate does not know them.
5. Give practical and concise recommendations.
6. Return ONLY valid JSON.
7. Do not use markdown inside the JSON values.

Return exactly this structure:

{
  "summary": "short professional summary",
  "strengths": ["strength 1", "strength 2"],
  "gaps": ["gap 1", "gap 2"],
  "recommendations": ["recommendation 1", "recommendation 2"],
  "resume_improvements": ["improvement 1", "improvement 2"],
  "interview_focus": ["topic 1", "topic 2"]
}
"""

    user_input = f"""
TARGET CAREER:
{target_job or "Not specified"}

JOB DESCRIPTION:
{job_description or "Not provided"}

DETERMINISTIC READINESS SCORE:
{readiness_score}

DETERMINISTIC ATS SCORE:
{ats_score}

MATCHED SKILLS:
{json.dumps(matched_skills, ensure_ascii=False)}

MISSING SKILLS:
{json.dumps(missing_skills, ensure_ascii=False)}

RESUME:
{resume_text}
"""

    return call_llm(
        instructions=instructions,
        input_text=user_input,
    )


# -------------------------------------------------------------------
# AI resume rewriting
# -------------------------------------------------------------------

def rewrite_resume_with_ai(
    resume_text,
    target_job="",
    job_description="",
    missing_skills=None,
):
    """
    Rewrite and improve resume content using AI.

    The AI must not fabricate experience or qualifications.
    """

    missing_skills = missing_skills or []

    instructions = """
You are a professional resume editor.

Rewrite the supplied resume for the specified target career.

STRICT RULES:
1. Never invent facts.
2. Never add fake employment.
3. Never add fake internships.
4. Never add fake projects.
5. Never add fake certifications.
6. Never add fake skills.
7. Never invent metrics or percentages.
8. Preserve the candidate's actual education and experience.
9. Improve wording, structure, clarity, and ATS keyword alignment.
10. Missing skills may be mentioned only as recommended skills to learn;
    do not claim the candidate already has them.
11. Keep the result professional and concise.
12. Return ONLY valid JSON.
13. Do not use markdown inside JSON values.

Return:

{
  "professional_summary": "rewritten summary",
  "skills": ["skill 1", "skill 2"],
  "experience": [
    {
      "role": "role name",
      "company": "company name",
      "bullets": [
        "improved bullet"
      ]
    }
  ],
  "projects": [
    {
      "name": "project name",
      "bullets": [
        "improved project bullet"
      ]
    }
  ],
  "education": [
    {
      "degree": "degree",
      "institution": "institution",
      "details": "details"
    }
  ],
  "certifications": [],
  "additional_sections": []
}

If a section does not exist in the original resume, return an empty
array or an empty string rather than inventing content.
"""

    user_input = f"""
TARGET CAREER:
{target_job or "Not specified"}

JOB DESCRIPTION:
{job_description or "Not provided"}

SKILLS THAT MAY BE MISSING:
{json.dumps(missing_skills, ensure_ascii=False)}

ORIGINAL RESUME:
{resume_text}
"""

    return call_llm(
        instructions=instructions,
        input_text=user_input,
    )


# -------------------------------------------------------------------
# AI status
# -------------------------------------------------------------------

def is_ai_available():
    """Return whether AI analysis can currently be used."""

    return get_client() is not None


def get_model_name():
    """Return the configured model name."""

    return DEFAULT_MODEL


def get_ai_status():
    """Return useful AI configuration information."""

    available = is_ai_available()

    return {
        "available": available,
        "model": DEFAULT_MODEL,
        "provider": "OpenAI",
        "message": (
            f"AI analysis is available using {DEFAULT_MODEL}."
            if available
            else (
                "AI analysis is not configured. "
                "Add OPENAI_API_KEY to the .env file."
            )
        ),
    }


# -------------------------------------------------------------------
# Merge AI results into deterministic analysis
# -------------------------------------------------------------------

def merge_ai_analysis(
    analysis_result,
    ai_result,
):
    """
    Merge AI-generated insights into an existing analyzer result.

    Deterministic scores and skill matching remain unchanged.
    """

    if not isinstance(
        analysis_result,
        dict,
    ):
        analysis_result = {}

    if not isinstance(
        ai_result,
        dict,
    ):
        return analysis_result

    summary = ai_result.get(
        "summary",
        ""
    )

    strengths = ai_result.get(
        "strengths",
        []
    )

    gaps = ai_result.get(
        "gaps",
        []
    )

    recommendations = ai_result.get(
        "recommendations",
        []
    )

    improvements = ai_result.get(
        "resume_improvements",
        []
    )

    interview_focus = ai_result.get(
        "interview_focus",
        []
    )

    if not isinstance(strengths, list):
        strengths = [str(strengths)]

    if not isinstance(gaps, list):
        gaps = [str(gaps)]

    if not isinstance(recommendations, list):
        recommendations = [str(recommendations)]

    if not isinstance(improvements, list):
        improvements = [str(improvements)]

    if not isinstance(interview_focus, list):
        interview_focus = [str(interview_focus)]

    analysis_result["ai_available"] = True

    if summary:
        analysis_result["ai_summary"] = str(
            summary
        )

    if strengths:
        analysis_result["ai_strengths"] = strengths

    if gaps:
        analysis_result["ai_gaps"] = gaps

    if recommendations:
        analysis_result[
            "ai_recommendations"
        ] = recommendations

    analysis_result[
        "ai_resume_improvements"
    ] = improvements

    analysis_result[
        "ai_interview_focus"
    ] = interview_focus

    return analysis_result


# -------------------------------------------------------------------
# Direct test
# -------------------------------------------------------------------

if __name__ == "__main__":
    status = get_ai_status()

    print("=" * 60)
    print("AI Analyzer")
    print("=" * 60)

    print(
        f"Provider : {status['provider']}"
    )

    print(
        f"Model    : {status['model']}"
    )

    print(
        f"Available: {status['available']}"
    )

    print(
        f"Message  : {status['message']}"
    )

    print("=" * 60)