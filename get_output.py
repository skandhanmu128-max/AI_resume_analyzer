from resume_parser import ResumeParser
from skill_extractor import SkillExtractor
from job_matcher import JobMatcher

print("Analyzing: sample_resumes/ML_Engineer_Resume.docx...\n")

# 1. Parse Resume
parsed = ResumeParser.parse_resume("sample_resumes/ML_Engineer_Resume.docx")

# 2. Extract Skills
extractor = SkillExtractor()
skills_payload = extractor.extract_skills(parsed['raw_text'])

# 3. Match Jobs
matcher = JobMatcher()
matches = matcher.compute_matches(parsed['raw_text'], skills_payload['skills'])

if matches:
    top = matches[0]
    print(f"Target Role: {top['role']}")
    print(f"Resume Match Score: {top['match_score']}%\n")
    
    print("Skills Found:")
    for skill in top['matched_skills']:
        print(f"- {skill}")
        
    print("\nMissing Skills:")
    for skill in top['missing_skills']:
        print(f"- {skill}")
        
    print("\nRecommended Roles:")
    for i, m in enumerate(matches[:3]):
        print(f"{i+1}. {m['role']} - {m['match_score']}%")
else:
    print("No matches found.")
