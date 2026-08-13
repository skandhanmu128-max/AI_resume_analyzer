# AI Resume Analyzer and Job Recommendation System using NLP

An intelligent, end-to-end recruitment screening and career advising platform. It extracts structured info from PDF and DOCX CVs, matches them against multiple job roles using TF-IDF text mining and skill set-overlaps, builds multi-week learning roadmaps for missing competencies, and acts as an AI Career Advisor powered by Google Gemini.

---

## 🚀 Features

- **Document Parser**: Ingests PDF and DOCX documents to extract clean textual content.
- **Section Segmentation**: Gracefully splits resumes into Contact Info, Education, Experience, Projects, and Certifications.
- **Skill Extractor**: Matches terms against a custom dictionary of 150+ skills using regex word boundaries to avoid false positives (e.g. distinguishing "C" from "Cloud").
- **Hybrid Matching Engine**: Scores profiles using a weighted average of TF-IDF Cosine Similarity and Set-based Skill Overlaps.
- **Dynamic Learning Roadmap**: Identifies missing skills and compiles a weekly learning schedule with direct links to official documentation, GitHub repositories, Coursera, Udemy, and YouTube.
- **AI Career Counselor**: Generates tailored ATS improvement plans, resume summaries, and simulated technical & behavioral interview questions using Google Gemini.
- **Streamlit Dashboard**: A modern web interface with glassmorphic visuals, interactive Plotly metrics, and instant PDF/PowerPoint report compilers.

---

## 📂 Project Structure

```text
AI_Resume_Analyzer/
│── app.py                  # Streamlit dashboard
│── resume_parser.py        # PDF/DOCX Parsing logic
│── text_cleaner.py         # NLP text sanitization
│── skill_extractor.py      # Category-based skill matcher
│── job_matcher.py          # TF-IDF & Cosine Similarity match engine
│── roadmap_generator.py    # Study timeline compiler
│── report_generator.py     # PDF & Slide document compiler
│── config.py               # Settings and themes
│── utils.py                # Gemini integration & mock fallbacks
│── requirements.txt        # Package dependencies
│── LICENSE                 # MIT License
│── .env.example            # Environment variables template
│── .gitignore              # Git Ignore configuration
│
├── data/
│      job_roles.csv        # Predefined job profiles
│      skill_dictionary.csv # 150+ skill mapping
│
├── sample_resumes/         # Pre-made resume test files
│
├── notebooks/
│      AI_Resume_Analyzer.ipynb  # Google Colab Notebook
│
└── tests/
       test_cases.py        # 20+ Unit test suite
```

---

## 🛠️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/AI_Resume_Analyzer.git
   cd AI_Resume_Analyzer
   ```

2. **Install requirements**:
   Make sure you have Python 3.9+ installed, then run:
   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Configure Environment Variables**:
   Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```
   Provide your **Gemini API Key** in the `.env` file:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```
   *(If no API key is provided, the application will automatically activate standard simulated mock advisor profiles so that all features remain functional).*

---

## 💻 How to Run

1. **Generate Sample Resumes & Reports**:
   Run the sample generation utility to populate the test directory:
   ```bash
   python generate_samples.py
   ```

2. **Start the Dashboard**:
   ```bash
   streamlit run app.py
   ```

3. **Run Unit Tests**:
   Ensure all core NLP systems pass:
   ```bash
   python -m unittest tests/test_cases.py
   ```

---

## 🧬 Methodology & Algorithms

1. **Sanitization**: Regular expressions strip phone markers, emails, and web URLs. Words are then tokenized and lemmatized via `spaCy`'s English vocabulary core.
2. **Feature Array**: The text is converted into frequency arrays using **TF-IDF Vectorization**.
3. **Similarity**: Cosine Similarity yields a score representing textual correspondence between the resume and the job role specifications:
   $$\text{Cosine Similarity}(A, B) = \frac{A \cdot B}{\|A\| \|B\|}$$
4. **Weighted Combined Index**: 
   $$\text{Final Index} = (0.4 \times \text{TF-IDF Score}) + (0.6 \times \text{Skill Overlap Ratio})$$

---

## 🎓 Academic Presentation Slide Deck Details

The program compiles a professional **15-slide PowerPoint deck** containing:
- Problem Statement & Lit Survey
- System Architecture Workflow
- NLP Processing Details
- TF-IDF and Hybrid Matching math
- Study Roadmaps and AI Integration
- Conclusion & Future Scope

---

## 📄 License

Distributed under the MIT License. See [LICENSE](file:///c:/Users/Skandhan%20M%20U/OneDrive/Desktop/AI_resume_analyzer/LICENSE) for more information.
