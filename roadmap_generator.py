import urllib.parse

# Comprehensive resource dictionary for common technical skills
RESOURCE_CATALOG = {
    "python": {
        "docs": "https://docs.python.org/3/",
        "github": "https://github.com/python/cpython",
        "coursera": "https://www.coursera.org/specializations/python",
        "udemy": "https://www.udemy.com/course/complete-python-bootcamp/"
    },
    "sql": {
        "docs": "https://www.postgresql.org/docs/ or https://dev.mysql.com/doc/",
        "github": "https://github.com/srnativ/awesome-sql",
        "coursera": "https://www.coursera.org/learn/sql-for-data-science",
        "udemy": "https://www.udemy.com/course/the-complete-sql-bootcamp/"
    },
    "pandas": {
        "docs": "https://pandas.pydata.org/docs/",
        "github": "https://github.com/pandas-dev/pandas",
        "coursera": "https://www.coursera.org/learn/data-analysis-with-python",
        "udemy": "https://www.udemy.com/course/data-analysis-with-pandas/"
    },
    "scikit-learn": {
        "docs": "https://scikit-learn.org/stable/documentation.html",
        "github": "https://github.com/scikit-learn/scikit-learn",
        "coursera": "https://www.coursera.org/learn/machine-learning-with-python",
        "udemy": "https://www.udemy.com/course/machinelearning/"
    },
    "tensorflow": {
        "docs": "https://www.tensorflow.org/api_docs",
        "github": "https://github.com/tensorflow/tensorflow",
        "coursera": "https://www.coursera.org/professional-certificates/tensorflow-in-practice",
        "udemy": "https://www.udemy.com/course/complete-guide-to-tensorflow-for-deep-learning-with-python/"
    },
    "pytorch": {
        "docs": "https://pytorch.org/docs/stable/index.html",
        "github": "https://github.com/pytorch/pytorch",
        "coursera": "https://www.coursera.org/learn/deep-neural-networks-with-pytorch",
        "udemy": "https://www.udemy.com/course/pytorch-for-deep-learning-with-python-bootcamp/"
    },
    "django": {
        "docs": "https://docs.djangoproject.com/en/stable/",
        "github": "https://github.com/django/django",
        "coursera": "https://www.coursera.org/specializations/django",
        "udemy": "https://www.udemy.com/course/python-and-django-full-stack-web-developer-bootcamp/"
    },
    "fastapi": {
        "docs": "https://fastapi.tiangolo.com/",
        "github": "https://github.com/tiangolo/fastapi",
        "coursera": "https://www.coursera.org/learn/fastapi-apis",
        "udemy": "https://www.udemy.com/course/fastapi-the-complete-course/"
    },
    "docker": {
        "docs": "https://docs.docker.com/",
        "github": "https://github.com/veggiemonk/awesome-docker",
        "coursera": "https://www.coursera.org/learn/docker-for-developers",
        "udemy": "https://www.udemy.com/course/docker-mastery/"
    },
    "kubernetes": {
        "docs": "https://kubernetes.io/docs/home/",
        "github": "https://github.com/kubernetes/kubernetes",
        "coursera": "https://www.coursera.org/learn/introduction-to-kubernetes-edx",
        "udemy": "https://www.udemy.com/course/certified-kubernetes-administrator-with-practice-tests/"
    },
    "aws": {
        "docs": "https://docs.aws.amazon.com/",
        "github": "https://github.com/open-guides/og-aws",
        "coursera": "https://www.coursera.org/specializations/aws-fundamentals",
        "udemy": "https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/"
    },
    "spacy": {
        "docs": "https://spacy.io/usage",
        "github": "https://github.com/explosion/spaCy",
        "coursera": "https://www.coursera.org/learn/natural-language-processing-tensorflow",
        "udemy": "https://www.udemy.com/course/natural-language-processing-in-python-spacy/"
    },
    "git": {
        "docs": "https://git-scm.com/doc",
        "github": "https://github.com/github/gitignore",
        "coursera": "https://www.coursera.org/learn/introduction-git-github",
        "udemy": "https://www.udemy.com/course/git-complete/"
    }
}

class RoadmapGenerator:
    @staticmethod
    def generate_roadmap(missing_skills: list, role_name: str) -> dict:
        """
        Creates a structured weekly learning roadmap based on missing skills.
        """
        if not missing_skills:
            return {
                "role": role_name,
                "weeks": 0,
                "schedule": [],
                "general_advice": "You already possess all critical skills for this role! Focus on building high-impact portfolio projects."
            }

        schedule = []
        weeks_per_skill = 2 if len(missing_skills) < 3 else 1
        current_week = 1

        for skill in missing_skills:
            skill_lower = skill.lower().strip()
            
            # Retrieve specific resources or build generic search queries
            if skill_lower in RESOURCE_CATALOG:
                resources = RESOURCE_CATALOG[skill_lower]
            else:
                query = urllib.parse.quote(f"{skill} tutorial for beginners")
                resources = {
                    "docs": f"https://www.google.com/search?q={urllib.parse.quote(skill + ' official documentation')}",
                    "github": f"https://github.com/search?q={urllib.parse.quote(skill)}",
                    "coursera": f"https://www.coursera.org/search?query={urllib.parse.quote(skill)}",
                    "udemy": f"https://www.udemy.com/courses/search/?q={urllib.parse.quote(skill)}"
                }
            
            # YouTube search link
            resources["youtube"] = f"https://www.youtube.com/results?search_query={urllib.parse.quote(skill + ' tutorial')}"

            # Week duration text
            week_text = f"Week {current_week}" if weeks_per_skill == 1 else f"Week {current_week} - {current_week + 1}"
            current_week += weeks_per_skill

            schedule.append({
                "period": week_text,
                "skill": skill,
                "tasks": [
                    f"Understand core syntax, basic components, and execution lifecycle of {skill}.",
                    f"Build a miniature practice module or run scripts exercising {skill}.",
                    f"Integrate {skill} into a repository to showcase on your portfolio."
                ],
                "resources": resources
            })

        total_weeks = current_week - 1
        
        return {
            "role": role_name,
            "weeks": total_weeks,
            "schedule": schedule,
            "general_advice": f"This roadmap is tailored to bridge your skill gap for the {role_name} role. Spend 10-15 hours per week following these steps."
        }
