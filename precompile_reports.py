from report_generator import PDFReportGenerator, PresentationGenerator
from config import REPORTS_DIR

if __name__ == "__main__":
    print("Pre-compiling academic documents...")
    
    pdf_gen = PDFReportGenerator()
    ppt_gen = PresentationGenerator()
    
    # 1. 6-Page College Project Report
    report_path = pdf_gen.generate_college_report("college_project_report.pdf")
    print(f"Generated 6-Page Project Report at: {report_path}")
    
    # 2. One-Page Project Summary
    summary_path = pdf_gen.generate_one_page_summary("one_page_summary.pdf")
    print(f"Generated One-Page Summary at: {summary_path}")
    
    # 3. 15-Slide PPT Presentation
    presentation_path = ppt_gen.generate_presentation("presentation.pptx")
    print(f"Generated 15-Slide Presentation at: {presentation_path}")
    
    print("All deliverables pre-compiled successfully!")
