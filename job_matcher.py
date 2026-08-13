import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from config import JOB_ROLES_PATH, WEIGHT_TFIDF, WEIGHT_SKILLS
from text_cleaner import get_cleaned_string

class JobMatcher:
    def __init__(self, roles_path: str = str(JOB_ROLES_PATH)):
        self.roles_path = roles_path
        self.roles_df = self._load_job_roles()

    def _load_job_roles(self) -> pd.DataFrame:
        """
        Loads pre-defined job profiles. Fallback to minimal dataframe if not found.
        """
        if Path(self.roles_path).exists():
            try:
                return pd.read_csv(self.roles_path)
            except Exception as e:
                print(f"Error loading job roles: {e}")
                
        # In-memory fallback
        fallback_data = {
            "Role": ["Data Analyst", "Machine Learning Engineer", "Software Engineer"],
            "Required Skills": ["SQL, Python, Pandas, Tableau", "Python, Scikit-learn, TensorFlow, PyTorch", "Python, Java, Git, SQL, React"],
            "Experience": ["0-2 years", "1-3 years", "0-3 years"],
            "Projects": ["Dashboard", "Classifier", "Task Manager"],
            "Education": ["Bachelor's", "Bachelor's/Master's", "Bachelor's"],
            "Difficulty": ["Easy", "Hard", "Medium"],
            "Learning Path": ["SQL -> Python -> Analytics", "Python -> ML -> DL", "DS & Algo -> OOP -> FullStack"]
        }
        return pd.DataFrame(fallback_data)

    def compute_matches(self, resume_text: str, extracted_skills: list) -> list:
        """
        Matches resume details against all jobs.
        Returns sorted list of match profiles.
        """
        matches = []
        if not resume_text:
            return matches

        # Preprocess resume text for TF-IDF
        cleaned_resume = get_cleaned_string(resume_text)
        
        # Prepare job text contents for TF-IDF (Role, Required Skills, Projects, Learning Path)
        job_texts = []
        for _, row in self.roles_df.iterrows():
            combined_text = f"{row['Role']} {row['Required Skills']} {row['Projects']} {row['Learning Path']}"
            job_texts.append(get_cleaned_string(combined_text))

        # TF-IDF calculation
        all_texts = [cleaned_resume] + job_texts
        vectorizer = TfidfVectorizer()
        try:
            tfidf_matrix = vectorizer.fit_transform(all_texts)
            # Cosine similarity of resume (index 0) against all job roles (indices 1 to N)
            cosine_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()
        except Exception as e:
            print(f"TF-IDF failed: {e}")
            cosine_scores = np.zeros(len(self.roles_df))

        # Skills overlap matching
        resume_skills_set = {s.lower().strip() for s in extracted_skills}

        for idx, row in self.roles_df.iterrows():
            role_name = row['Role']
            required_skills_str = row['Required Skills']
            
            # Parse required skills
            req_skills = [s.strip() for s in required_skills_str.split(',') if s.strip()]
            req_skills_set = {s.lower() for s in req_skills}
            
            # Overlap score
            matched_skills = []
            missing_skills = []
            for skill in req_skills:
                if skill.lower() in resume_skills_set:
                    matched_skills.append(skill)
                else:
                    missing_skills.append(skill)
            
            if req_skills_set:
                skills_overlap_score = len(matched_skills) / len(req_skills_set)
            else:
                skills_overlap_score = 0.0

            # Combined weighted score
            tfidf_score = cosine_scores[idx]
            combined_score = (WEIGHT_TFIDF * tfidf_score) + (WEIGHT_SKILLS * skills_overlap_score)
            
            # Format combined score as percentage
            match_percentage = round(float(combined_score) * 100, 2)
            # Clamp percentage between 0 and 100
            match_percentage = max(0.0, min(100.0, match_percentage))

            matches.append({
                "role": role_name,
                "match_score": match_percentage,
                "tfidf_score": round(float(tfidf_score) * 100, 2),
                "skills_score": round(float(skills_overlap_score) * 100, 2),
                "matched_skills": sorted(matched_skills),
                "missing_skills": sorted(missing_skills),
                "experience_required": row['Experience'],
                "projects_recommended": row['Projects'],
                "education_required": row['Education'],
                "difficulty": row['Difficulty'],
                "learning_path": row['Learning Path']
            })

        # Sort matches by match_score descending
        matches = sorted(matches, key=lambda x: x['match_score'], reverse=True)
        return matches
