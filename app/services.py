from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
import json
import os

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError(
        "AI API key not found. Set GROQ_API_KEY in project/.env and restart the server."
    )

client = OpenAI(
    api_key=api_key,
    # base_url="https://api.ilmu.ai/v1"
    base_url="https://api.groq.com/openai/v1"
)


def ai_brain(user_text, score):
    system_prompt = f"""
    You are an AI architect that extracts 
    structured student data and generates intelligent study workflows. 
    Always return valid JSON only.
    User Message: "{user_text}"
    Predicted Score: "{score}"

    Task: 
    - Based on this score generate a study workflow and extract study data from user messages. 
    - Generate a study workflow on how to improve the exam result or maintain the result.
    - Determine problem analysis, weak areas, step-by-step improvement plan, daily schedule, motivation.
    Required JSON format:
        {{
        "subject": "string",
        "daily_study_hours": float,
        "attendance_percentage":float,
        "sleep_hours":float,
        "screen_time":float,
        "analysis":[
            {{
                "step": 1, 
                "title":"string",
                "explanation": "string"
            }}],

        "weakness_analysis": [
            "string"],

        "improvement_target": {{
            "target_score":90,
            "actions":["string"]
            }},

        "summary": "string"
        }}
    Rules:
    - If user input is empty, return: {{
        "error": "empty_input"}}.
    - Generate 3 to 8 steps depending on user situation.
    - Set improvement_target based on the predicted score (lower score = improvement focus, higher score = maintenance or optimization).
    - Do NOT limit number of steps.
    - Ensure all numeric fields are valid numbers (not strings).
    - If the valeu are missing, estimate them based on context.
    - The 'analysis' must be a multi-step workflow tailored to the user's specific situation.
    - RETURN ONLY JSON.

    """
    response = client.chat.completions.create(
        # model="ilmu-glm-5.1",
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an AI architect. Return only valid JSON in the response. "
                    "Do not wrap the JSON in markdown code fences like ```json ... ```."
                ),
            },
            {"role": "user", "content": system_prompt},
        ],
    )
    content = response.choices[0].message.content
    if not content or not content.strip():
        raise RuntimeError(
            f"Empty AI response; raw response object: {repr(response)}"
        )
    content = content.strip()
    if content.startswith("```json") or content.startswith("```json\n"):
        content = content.split("```", 1)[1].strip()
        if content.endswith("```"):
            content = content[: -3].strip()
    elif content.startswith("```") and content.endswith("```"):
        content = content[3:-3].strip()
    try:
        return json.loads(content)
    except json.JSONDecodeError as decode_err:
        raise RuntimeError(
            f"Invalid JSON from AI. Cleaned content={repr(content)} Error={decode_err}"
        ) from decode_err
