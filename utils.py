import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Configure Google Gemini API
api_key = os.getenv("GEMINI_API_KEY")
gemini_available = False

if api_key:
    try:
        genai.configure(api_key=api_key)
        gemini_available = True
    except Exception as e:
        print(f"Failed to configure Gemini API: {e}")

def get_gemini_response(prompt: str) -> str:
    """
    Queries Gemini API with the given prompt.
    """
    if not gemini_available:
        return ""
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini generation error: {e}")
        return ""

def generate_resume_summary(raw_text: str) -> str:
    """
    Generates a professional 3-4 sentence summary of the resume.
    """
    prompt = (
        f"You are an expert recruiter. Summarize the following resume text in 3-4 professional, "
        f"impactful sentences, highlighting core strengths and experience:\n\n{raw_text[:4000]}"
    )
    response = get_gemini_response(prompt)
    if response:
        return response.strip()
    
    # Clean fallback summary
    return (
        "Experienced software professional with demonstrated competencies in technical design, "
        "problem solving, and application development. Passionate about leveraging cutting-edge tools "
        "and frameworks to build scalable systems. Possesses strong collaborative skills and a "
        "track record of successful project execution."
    )

def generate_career_advice(skills: list, top_roles: list) -> str:
    """
    Provides career advice based on the candidate's skills and matched top roles.
    """
    skills_str = ", ".join(skills)
    roles_str = ", ".join(top_roles)
    prompt = (
        f"Candidate possesses skills: {skills_str}. Top matched roles are: {roles_str}.\n"
        f"Provide 3 actionable career advice tips for this candidate as they seek to transition into these roles."
    )
    response = get_gemini_response(prompt)
    if response:
        return response.strip()
    
    # Recruiter-like fallback advice
    return (
        "### 💡 Career Recommendations:\n\n"
        "1. **Double Down on Strengths:** Your skills in " + (skills[0] if skills else "core programming") + " are highly valued. Focus on advanced applications of these skills.\n"
        "2. **Build Portfolio Highlights:** Create open-source github repositories demonstrating solutions for " + (top_roles[0] if top_roles else "your targeted role") + ".\n"
        "3. **Network in Targeted Domain:** Engage with professionals on LinkedIn working as " + (top_roles[0] if top_roles else "specialists") + " to learn about industry demands."
    )

def generate_resume_improvements(raw_text: str) -> str:
    """
    Analyzes resume text and recommends specific improvements.
    """
    prompt = (
        f"Critique this resume text and list 3-4 specific structural, semantic, or keyword improvements "
        f"to make it stand out to recruiters and ATS systems:\n\n{raw_text[:4000]}"
    )
    response = get_gemini_response(prompt)
    if response:
        return response.strip()
    
    # Fallback recommendations
    return (
        "### 📈 Suggested Resume Improvements:\n\n"
        "1. **Quantify Achievements:** Use metric-driven bullet points (e.g., 'Optimized query latency by 35%') instead of passive statements.\n"
        "2. **ATS Keyword Optimization:** Inject missing skill keywords naturally into your project and experience descriptions.\n"
        "3. **Strong Action Verbs:** Start your experience descriptions with powerful verbs like *Spearheaded*, *Architected*, or *Automated*."
    )

def generate_interview_questions(role: str, skills: list) -> str:
    """
    Generates tailored interview questions (Technical and HR) for a specific role.
    """
    skills_str = ", ".join(skills[:5])
    prompt = (
        f"Generate 3 technical interview questions and 2 behavioral (HR) interview questions "
        f"for a candidate interviewing for the role of '{role}' with skills: {skills_str}. "
        f"Also provide brief model answers or hints for each."
    )
    response = get_gemini_response(prompt)
    if response:
        return response.strip()
    
    # Fallback questions
    return (
        f"### ❓ Simulated Interview Questions for {role}:\n\n"
        f"**1. Technical:** Explain how you would implement a scalable pipeline using {skills[0] if skills else 'your primary language'}. What are the primary bottlenecks?\n"
        f"*Hint: Talk about asynchronous execution, caching layer, and clean database index schema.*\n\n"
        f"**2. Technical:** How do you handle unstructured data or errors during parsing tasks?\n"
        f"*Hint: Emphasize validation models, try-except blocks, logging utilities, and exception handling patterns.*\n\n"
        f"**3. Behavioral:** Describe a time you had to learn a complex technology quickly to meet a project deadline. How did you organize your time?\n"
        f"*Hint: Use the STAR methodology (Situation, Task, Action, Result) to structure your response.*"
    )

def generate_job_prep_tips(role: str) -> str:
    """
    Generates preparation tips for a target job role.
    """
    prompt = f"Provide 3 tailored job preparation tips for someone seeking a job as a '{role}'."
    response = get_gemini_response(prompt)
    if response:
        return response.strip()
    
    # Fallback prep tips
    return (
        f"### 🎯 Job Preparation Strategy for {role}:\n\n"
        f"1. **Standardize Coding Practice:** Practice coding challenges focusing on system design and core algorithms on platforms like LeetCode or HackerRank.\n"
        f"2. **Understand Deployment Cycles:** Learn how pipelines work (e.g., Docker, GitHub Actions, AWS environments).\n"
        f"3. **Study Common Architectural Patterns:** Understand how data flows between backend services, caches, and databases."
    )

def generate_cover_letter(raw_text: str, target_role: str) -> str:
    """
    Generates a personalized cover letter based on the user's resume and a target job role.
    """
    prompt = (
        f"You are an expert career coach. Write a compelling, highly professional cover letter "
        f"for a candidate applying for the '{target_role}' role based on the following resume text. "
        f"Keep it concise, engaging, and highlight the most relevant skills from the resume that match the role. "
        f"Use a modern, ATS-friendly format.\n\nResume Text:\n{raw_text[:4000]}"
    )
    response = get_gemini_response(prompt)
    if response:
        return response.strip()
    
    # Fallback response
    return (
        f"Dear Hiring Manager,\n\n"
        f"I am writing to express my strong interest in the {target_role} position. "
        f"With my background and expertise, I am confident in my ability to contribute effectively to your team. "
        f"My enclosed resume details my technical skills and professional accomplishments.\n\n"
        f"I look forward to the opportunity to discuss how my qualifications align with your needs.\n\n"
        f"Sincerely,\n[Your Name]"
    )
