import re
from pathlib import Path
from pypdf import PdfReader
from docx import Document

class ResumeParser:
    @staticmethod
    def extract_text_from_pdf(pdf_path: str) -> str:
        """
        Extracts raw text from a PDF file.
        """
        text = ""
        try:
            reader = PdfReader(pdf_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        except Exception as e:
            print(f"Error reading PDF {pdf_path}: {e}")
        return text

    @staticmethod
    def extract_text_from_docx(docx_path: str) -> str:
        """
        Extracts raw text from a DOCX file.
        """
        text = ""
        try:
            doc = Document(docx_path)
            for para in doc.paragraphs:
                if para.text:
                    text += para.text + "\n"
        except Exception as e:
            print(f"Error reading DOCX {docx_path}: {e}")
        return text

    @classmethod
    def parse_resume(cls, file_path: str) -> dict:
        """
        Main entry point for parsing resumes. Identifies type and returns parsed structure.
        """
        path = Path(file_path)
        raw_text = ""
        if path.suffix.lower() == '.pdf':
            raw_text = cls.extract_text_from_pdf(str(path))
        elif path.suffix.lower() == '.docx':
            raw_text = cls.extract_text_from_docx(str(path))
        else:
            # Try to read as plain text
            try:
                raw_text = path.read_text(encoding='utf-8', errors='ignore')
            except Exception:
                raw_text = ""
        
        parsed_sections = cls.extract_sections(raw_text)
        parsed_sections['raw_text'] = raw_text
        return parsed_sections

    @staticmethod
    def extract_sections(text: str) -> dict:
        """
        Segments the resume text into standard sections using keyword matching.
        """
        sections = {
            "Contact Info": "",
            "Education": "",
            "Experience": "",
            "Projects": "",
            "Certifications": ""
        }
        
        if not text:
            return sections
        
        # Define search headers with boundaries or line-starts
        patterns = {
            "Education": r'\b(?:education|academic background|academic credentials|qualification|degrees)\b',
            "Experience": r'\b(?:experience|work experience|professional experience|employment history|work history)\b',
            "Projects": r'\b(?:projects|academic projects|personal projects|key projects|selected projects)\b',
            "Certifications": r'\b(?:certifications|certification|licenses|courses|credentials)\b'
        }
        
        lines = text.split('\n')
        current_section = "Contact Info"  # Default before any header is matched
        
        section_lines = {key: [] for key in sections.keys()}
        
        for line in lines:
            stripped = line.strip()
            if not stripped:
                continue
            
            # Check if this line is a section header
            matched_header = False
            for section_name, pattern in patterns.items():
                if re.search(pattern, stripped, re.IGNORECASE) and len(stripped) < 40:
                    current_section = section_name
                    matched_header = True
                    break
            
            if not matched_header:
                section_lines[current_section].append(line)
        
        for key in sections.keys():
            sections[key] = "\n".join(section_lines[key]).strip()
            
        return sections
