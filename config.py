import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
REPORTS_DIR = BASE_DIR / "reports"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
DIAGRAMS_DIR = BASE_DIR / "diagrams"
TESTS_DIR = BASE_DIR / "tests"
SAMPLE_RESUMES_DIR = BASE_DIR / "sample_resumes"

# Ensure directories exist
for directory in [DATA_DIR, REPORTS_DIR, SCREENSHOTS_DIR, DIAGRAMS_DIR, TESTS_DIR, SAMPLE_RESUMES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

SKILL_DICT_PATH = DATA_DIR / "skill_dictionary.csv"
JOB_ROLES_PATH = DATA_DIR / "job_roles.csv"

# NLP Configuration
SPACY_MODEL = "en_core_web_sm"

# Matching Settings
SIMILARITY_THRESHOLD = 0.3
WEIGHT_TFIDF = 0.4
WEIGHT_SKILLS = 0.6  # Skills overlap receives higher weight for practical role recommendations

# Streamlit UI Themes & Styles
UI_TITLE = "AI Resume Analyzer & Job Recommendation System"
UI_THEMES = {
    "Dark Mode": {
        "bg_color": "#0E1117",
        "card_bg": "rgba(255, 255, 255, 0.05)",
        "text_color": "#FAFAFA",
        "accent_color": "#FF4B4B",
        "border_color": "rgba(255, 255, 255, 0.1)",
        "gradient": "linear-gradient(135deg, #1f4068, #162447, #0f1a1c)"
    },
    "Light Mode": {
        "bg_color": "#F0F2F6",
        "card_bg": "rgba(0, 0, 0, 0.03)",
        "text_color": "#31333F",
        "accent_color": "#FF4B4B",
        "border_color": "rgba(0, 0, 0, 0.1)",
        "gradient": "linear-gradient(135deg, #e0f2fe, #bae6fd, #f0f9ff)"
    }
}
