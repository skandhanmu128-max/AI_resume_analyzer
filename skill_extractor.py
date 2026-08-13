import pandas as pd
import re
from pathlib import Path
from config import SKILL_DICT_PATH

class SkillExtractor:
    def __init__(self, dictionary_path: str = str(SKILL_DICT_PATH)):
        self.dictionary_path = dictionary_path
        self.skills_df = self._load_dictionary()
        self.skill_map = self._build_skill_map()

    def _load_dictionary(self) -> pd.DataFrame:
        """
        Loads the skill dictionary csv. Fallback to a hardcoded minimal dataset if file doesn't exist.
        """
        if Path(self.dictionary_path).exists():
            try:
                return pd.read_csv(self.dictionary_path)
            except Exception as e:
                print(f"Error loading skill dictionary: {e}")
        
        # In-memory fallback
        fallback_data = {
            "Skill": ["Python", "SQL", "Java", "C++", "HTML", "CSS", "Docker", "Kubernetes", "AWS", "Machine Learning", "Communication"],
            "Category": ["Programming", "Database", "Programming", "Programming", "Web", "Web", "DevOps", "DevOps", "Cloud", "AI", "Soft Skills"]
        }
        return pd.DataFrame(fallback_data)

    def _build_skill_map(self) -> dict:
        """
        Creates a mapping of lowercase skill name to its original casing and category.
        """
        skill_map = {}
        for _, row in self.skills_df.iterrows():
            skill_name = str(row['Skill']).strip()
            category = str(row['Category']).strip()
            if skill_name:
                skill_map[skill_name.lower()] = {
                    "original": skill_name,
                    "category": category
                }
        return skill_map

    def extract_skills(self, text: str) -> dict:
        """
        Extracts skills from text based on the skill map.
        Uses boundary checking to avoid false substring matches.
        """
        if not text:
            return {"skills": [], "by_category": {}}

        text_lower = text.lower()
        extracted_skills = set()
        
        # Sort skills by length in descending order to match multi-word skills first 
        # (e.g. "deep learning" before "learning")
        sorted_skills = sorted(self.skill_map.keys(), key=len, reverse=True)
        
        # To avoid double-matching sub-phrases, we keep track of matched spans
        matched_indices = []

        for skill in sorted_skills:
            # Create regex with word boundaries
            # Handle special characters in skills like C++, C#, .NET
            escaped_skill = re.escape(skill)
            
            # Special word boundary rules for skills containing trailing symbols like ++, #, .net
            if escaped_skill.endswith(r'\+\+') or escaped_skill.endswith(r'\#'):
                pattern = r'\b' + escaped_skill + r'(?!\w)'
            elif escaped_skill.startswith(r'\.'):
                pattern = r'(?<!\w)' + escaped_skill + r'\b'
            else:
                pattern = r'\b' + escaped_skill + r'\b'
                
            for match in re.finditer(pattern, text_lower):
                start, end = match.span()
                # Check if this span overlaps with any already matched span
                overlap = False
                for m_start, m_end in matched_indices:
                    if not (end <= m_start or start >= m_end):
                        overlap = True
                        break
                
                if not overlap:
                    extracted_skills.add(self.skill_map[skill]["original"])
                    matched_indices.append((start, end))

        # Categorize
        by_category = {}
        for skill_name in extracted_skills:
            info = self.skill_map[skill_name.lower()]
            category = info["category"]
            if category not in by_category:
                by_category[category] = []
            by_category[category].append(skill_name)
            
        return {
            "skills": sorted(list(extracted_skills)),
            "by_category": by_category
        }
