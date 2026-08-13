import unittest
from text_cleaner import clean_text_basic, preprocess_text, get_cleaned_string
from resume_parser import ResumeParser
from skill_extractor import SkillExtractor
from job_matcher import JobMatcher
from roadmap_generator import RoadmapGenerator

class TestResumeAnalyzer(unittest.TestCase):
    
    # --- Text Cleaner Tests (6 cases) ---
    def test_clean_text_basic_removes_emails(self):
        text = "Contact me at test.user@gmail.com for details."
        self.assertNotIn("test.user@gmail.com", clean_text_basic(text))

    def test_clean_text_basic_removes_urls(self):
        text = "Check out https://github.com/profile for details."
        self.assertNotIn("https://github.com/profile", clean_text_basic(text))

    def test_clean_text_basic_removes_phones(self):
        text = "Call me at +1 (555) 019-2834."
        self.assertNotIn("555", clean_text_basic(text))

    def test_clean_text_basic_lowercases(self):
        text = "PYTHON PYTHON"
        self.assertEqual(clean_text_basic(text), "python python")

    def test_preprocess_text_removes_stopwords(self):
        text = "this is a python developer resume"
        tokens = preprocess_text(text)
        self.assertNotIn("this", tokens)
        self.assertNotIn("is", tokens)
        self.assertIn("python", tokens)

    def test_get_cleaned_string_empty(self):
        self.assertEqual(get_cleaned_string(""), "")

    # --- Resume Parser Tests (4 cases) ---
    def test_extract_sections_default_fallback(self):
        text = "Hello world"
        sections = ResumeParser.extract_sections(text)
        self.assertEqual(sections["Contact Info"], "Hello world")

    def test_extract_sections_segments_education(self):
        text = "John Doe\nEducation\nB.Tech in CS\nExperience\nGoogle Software Engineer"
        sections = ResumeParser.extract_sections(text)
        self.assertEqual(sections["Education"], "B.Tech in CS")
        self.assertEqual(sections["Experience"], "Google Software Engineer")

    def test_extract_sections_ignores_headers_in_sentences(self):
        text = "I gained my core experience during summer projects."
        sections = ResumeParser.extract_sections(text)
        # "experience" is inside a long line, so it shouldn't split it as a header
        self.assertEqual(sections["Contact Info"], text.strip())

    def test_parse_resume_handles_missing_file(self):
        # Should gracefully return empty sections dictionary rather than crashing
        res = ResumeParser.parse_resume("non_existent_file.pdf")
        self.assertEqual(res["raw_text"], "")

    # --- Skill Extractor Tests (5 cases) ---
    def test_skill_extractor_matches_exact_skills(self):
        extractor = SkillExtractor()
        res = extractor.extract_skills("Experienced Python developer.")
        self.assertIn("Python", res["skills"])

    def test_skill_extractor_avoids_substring_collisions(self):
        extractor = SkillExtractor()
        # "Java" should match but it shouldn't match "C" inside "Cloud"
        res = extractor.extract_skills("Java developer working on cloud projects.")
        self.assertIn("Java", res["skills"])
        self.assertNotIn("C", res["skills"])

    def test_skill_extractor_matches_multi_word_skills(self):
        extractor = SkillExtractor()
        res = extractor.extract_skills("Specialized in Machine Learning and Deep Learning.")
        self.assertIn("Machine Learning", res["skills"])
        self.assertIn("Deep Learning", res["skills"])

    def test_skill_extractor_categorizes_skills(self):
        extractor = SkillExtractor()
        res = extractor.extract_skills("Skilled in Python and SQL.")
        self.assertIn("Programming", res["by_category"])
        self.assertIn("Database", res["by_category"])

    def test_skill_extractor_handles_special_characters(self):
        extractor = SkillExtractor()
        # Should match C++ and C# correctly
        res = extractor.extract_skills("Expert in C++ and C# developer.")
        self.assertIn("C++", res["skills"])
        self.assertIn("C#", res["skills"])

    # --- Job Matcher Tests (3 cases) ---
    def test_job_matcher_returns_all_roles(self):
        matcher = JobMatcher()
        matches = matcher.compute_matches("Python developer with SQL experience", ["Python", "SQL"])
        self.assertGreater(len(matches), 0)

    def test_job_matcher_ranks_matching_profiles(self):
        matcher = JobMatcher()
        # This text should match Python Developer very highly
        matches = matcher.compute_matches("Python Developer working on FastAPI and Django backends", ["Python", "Django", "FastAPI"])
        self.assertEqual(matches[0]["role"], "Python Developer")

    def test_job_matcher_computes_overlap_scores(self):
        matcher = JobMatcher()
        matches = matcher.compute_matches("Simple Text", [])
        self.assertEqual(matches[0]["skills_score"], 0.0)

    # --- Roadmap Generator Tests (2 cases) ---
    def test_roadmap_generator_handles_no_missing_skills(self):
        res = RoadmapGenerator.generate_roadmap([], "Software Engineer")
        self.assertEqual(res["weeks"], 0)
        self.assertIn("already possess", res["general_advice"])

    def test_roadmap_generator_compiles_study_timeline(self):
        res = RoadmapGenerator.generate_roadmap(["Docker", "AWS"], "Cloud Engineer")
        self.assertGreater(res["weeks"], 0)
        self.assertEqual(len(res["schedule"]), 2)
        self.assertEqual(res["schedule"][0]["skill"], "Docker")

if __name__ == '__main__':
    unittest.main()
