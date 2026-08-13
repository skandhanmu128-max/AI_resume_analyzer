# 🎥 AI Resume Analyzer Demonstration Video Script

**Duration**: 5 Minutes  
**Objective**: Guide the academic panel through project introduction, technical implementation, code architecture, and live application execution.

---

## 🕒 Timeline breakdown

| Section | Timeline | Focus |
|---|---|---|
| **1. Intro & Concept** | 0:00 - 1:00 | Self introduction, problem statement, project scope. |
| **2. Architecture & Code** | 1:00 - 2:30 | Walkthrough of text cleaning, parsing, matching math, and roadmaps. |
| **3. Streamlit Walkthrough** | 2:30 - 4:15 | Uploading a resume, visual gauge metrics, roadmap timeline, and downloads. |
| **4. Conclusion & Summary** | 4:15 - 5:00 | LMS submission overview, future scope, and final wrap-up. |

---

## 🎙️ Spoken script

### 1. Introduction & Concept (0:00 - 1:00)

**[Visual: Title Slide of Presentation or Streamlit Dashboard Home Page]**

> "Good morning, respected members of the evaluation panel. I am Skandhan M U, and today I am excited to present my project: **AI Resume Analyzer and Job Recommendation System using Natural Language Processing**.
> 
> In today's digital landscape, recruitment is highly bottlenecked. Recruiters receive hundreds of resumes daily, leading to screening fatigue and selection bias. On the other hand, candidates often apply blindly without knowing what skills they lack for a target job role. 
> 
> To solve this double-ended problem, I designed this intelligent pipeline. It parses document contents, extracts competencies using precise dictionary boundaries, ranks job matches using a hybrid scoring algorithm, and dynamically compiles personalized weekly learning roadmaps to help candidates upskill."

---

### 2. Technical Architecture & Code Demonstration (1:00 - 2:30)

**[Visual: Split Screen showing code editor with `resume_parser.py` and `job_matcher.py`]**

> "Let us look at the code execution structure:
> 
> - First, the system utilizes **`resume_parser.py`** to extract plain text from both PDF and DOCX formats. It then segments the text into sections like Experience, Education, and Projects.
> - Next, **`text_cleaner.py`** cleans raw text by filtering out emails, phone numbers, and URLs using regular expressions, before tokenizing and lemmatizing the words using **spaCy**.
> - In **`skill_extractor.py`**, we match the text against a structured dictionary of over 150 categorized skills. Crucially, I implemented exact word boundary checking to avoid false collisions, ensuring we don't accidentally match 'C' inside words like 'Cloud'.
> - Finally, **`job_matcher.py`** executes a hybrid matching formula:
>   $$\text{Match Score} = (40\% \times \text{TF-IDF Cosine Similarity}) + (60\% \times \text{Skill Overlap Ratio})$$
>   This balances overall context matching with the strict checklist of required technical skills."

---

### 3. Live Streamlit Application Demo (2:30 - 4:15)

**[Visual: Screen recording or live display of the Streamlit application interface]**

> "Now, let us run the Streamlit dashboard by executing `streamlit run app.py`. As you can see, we are greeted with a premium glassmorphic UI.
> 
> Let's upload a sample resume. In this case, I will upload our generated `ML_Engineer_Resume.docx` from the sidebar. 
> 
> Instantly, the system parses the resume and shows:
> 1. An **AI Resume Summary** outlining the candidate's core strengths.
> 2. The **Top Recommended Roles** ranked by fit. The candidate matches the **Machine Learning Engineer** profile with a score of **92%**.
> 3. In the **Advanced Analytics** tab, we see interactive bar charts showing the breakdown of skills across programming languages, ML, and databases.
> 4. In the **Upskilling Roadmap** tab, the system identifies the candidate's missing skills. It compiles a step-by-step weekly study schedule, complete with direct links to official docs, GitHub search, Coursera, and YouTube."

---

### 4. Output Explanation & Conclusion (4:15 - 5:00)

**[Visual: Showing the "Academic Deliverables" tab and downloading report PDFs]**

> "Lastly, the **Academic Deliverables** section allows users to compile and download all documentation. On a single click, the application dynamically generates the **6-Page Project Report PDF**, the **One-Page LMS Summary PDF**, and a **15-slide PowerPoint deck** matching all college submission requirements.
> 
> In conclusion, this project provides a highly interactive, scalable, and modular solution for recruiting and career counseling. In the future, we plan to support real-time job scraping and deep semantic sentence transformers.
> 
> Thank you for your time. I am open to any questions."
