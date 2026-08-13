import streamlit as st
import os
import pandas as pd
import tempfile
from pathlib import Path
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt

# Import custom modules
from config import UI_TITLE, UI_THEMES
from resume_parser import ResumeParser
from skill_extractor import SkillExtractor
from job_matcher import JobMatcher
from roadmap_generator import RoadmapGenerator
from report_generator import PDFReportGenerator, PresentationGenerator
import utils
from voice_utils import text_to_speech
from streamlit_mic_recorder import mic_recorder

# Set page config
st.set_page_config(
    page_title=UI_TITLE,
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Premium CSS Styling (Glassmorphism & animations)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
    
    /* Background Animation */
    .stApp {
        background: linear-gradient(-45deg, #0f172a, #1e293b, #0f172a, #334155);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
        font-family: 'Outfit', sans-serif;
        color: #f8fafc;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Typography */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #38bdf8, #818cf8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(15, 23, 42, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 28px;
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        margin-bottom: 24px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    }
    .glass-card:hover {
        transform: translateY(-5px) scale(1.02);
        border-color: rgba(56, 189, 248, 0.4);
        box-shadow: 0 15px 40px 0 rgba(56, 189, 248, 0.2);
    }

    /* Buttons */
    div.stButton > button:first-child {
        background: linear-gradient(90deg, #38bdf8 0%, #818cf8 100%);
        color: white;
        border-radius: 30px;
        border: none;
        padding: 12px 28px;
        font-weight: 600;
        letter-spacing: 0.5px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        font-size: 0.9rem;
    }
    div.stButton > button:first-child:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 20px rgba(56, 189, 248, 0.4);
        background: linear-gradient(90deg, #818cf8 0%, #38bdf8 100%);
    }

    /* Metrics */
    .metric-value {
        font-size: 3rem;
        font-weight: 800;
        background: -webkit-linear-gradient(45deg, #fbbf24, #f59e0b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 4px 10px rgba(245, 158, 11, 0.3);
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.8) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
</style>
""", unsafe_allow_html=True)

# App state management
if "parsed_data" not in st.session_state:
    st.session_state.parsed_data = None
if "selected_role_idx" not in st.session_state:
    st.session_state.selected_role_idx = 0

# Sidebar configuration
st.sidebar.image("https://img.icons8.com/clouds/200/resume.png", width=120)
st.sidebar.title("Resume Analyzer 🚀")
st.sidebar.write("Analyze profiles and discover optimized career roadmaps using NLP & GenAI.")

# Theme selector
theme = st.sidebar.selectbox("UI Palette Theme", ["Dark Mode", "Light Mode"])
st.sidebar.markdown("---")

# File Ingestion
st.sidebar.subheader("📄 Upload Resume")
uploaded_file = st.sidebar.file_uploader("Upload PDF or DOCX format", type=["pdf", "docx"])

if uploaded_file:
    # Process uploaded file
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(uploaded_file.name).suffix) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name

    with st.spinner("Parsing resume details..."):
        # Parsing
        parsed_sections = ResumeParser.parse_resume(tmp_file_path)
        
        # Skill extraction
        extractor = SkillExtractor()
        skills_payload = extractor.extract_skills(parsed_sections['raw_text'])
        
        # Recommendation and matches
        matcher = JobMatcher()
        matches = matcher.compute_matches(parsed_sections['raw_text'], skills_payload['skills'])
        
        st.session_state.parsed_data = {
            "sections": parsed_sections,
            "skills": skills_payload['skills'],
            "skills_by_category": skills_payload['by_category'],
            "matches": matches,
            "filename": uploaded_file.name
        }
        
    try:
        os.unlink(tmp_file_path)
    except Exception:
        pass

# Navigation tabs
tabs = ["🏠 Home & Analysis", "📊 Advanced Analytics", "🗺️ Upskilling Roadmap", "💡 AI Career Advisor", "📝 Cover Letter Gen", "🎓 Academic Deliverables"]
selected_tab = st.sidebar.radio("Navigation Menu", tabs)

# Render tab contents
if not st.session_state.parsed_data:
    st.title("🚀 Welcome to AI Resume Analyzer")
    st.markdown("""
    Upload a resume in the sidebar to begin.
    
    ### System Features:
    * **Exact Resume Parsing:** Extracts sections from PDF and DOCX documents automatically.
    * **Automated Skill Classification:** Filters competencies across 150+ categorized targets.
    * **Weighted Similarity Match:** Combines TF-IDF scores with explicit set-overlap.
    * **Upskilling Roadmap:** Details custom study paths complete with Coursera, Udemy, and YouTube links.
    * **AI Advice Engine:** Generates resume critiques, summaries, and mock interview prep questions.
    """)
else:
    data = st.session_state.parsed_data
    matches = data["matches"]
    
    if selected_tab == "🏠 Home & Analysis":
        st.title("🏠 Resume Parsing & Matching Summary")
        
        # Split into columns
        col1, col2 = st.columns([1, 2])
        
        with col1:
            with st.container(border=True):
                st.subheader("🎯 Primary Matches")
                if matches:
                    top_match = matches[0]
                    st.markdown(f"### Top Role Recommended:")
                    st.markdown(f"<span class='metric-value'>{top_match['role']}</span>", unsafe_allow_html=True)
                    st.markdown(f"**Overall Match score:** `{top_match['match_score']}%`")
                    st.markdown(f"**Experience Requirement:** {top_match['experience_required']}")
                    st.markdown(f"**Target Difficulty:** {top_match['difficulty']}")
                else:
                    st.write("No matching profiles found.")
            
            # Match breakdown list
            with st.container(border=True):
                st.subheader("📋 Top Recommended Roles")
                for idx, r in enumerate(matches[:3]):
                    st.markdown(f"**{idx+1}. {r['role']}**")
                    st.progress(r['match_score'] / 100.0)
                    st.write(f"Score: `{r['match_score']}%` | Skills Match: `{r['skills_score']}%`")

        with col2:
            with st.container(border=True):
                st.subheader("🤖 AI Resume Summary")
                # Generate summary on demand
                summary = utils.generate_resume_summary(data['sections']['raw_text'])
                st.write(summary)
                
                # --- TTS Feature ---
                if st.button("🔊 Read Summary aloud"):
                    with st.spinner("Generating audio..."):
                        audio_path = text_to_speech(summary)
                        if audio_path:
                            st.audio(audio_path, format="audio/mp3")
                # -------------------
            
            # --- Unique Feature: ATS Readability & Keyword Density ---
            with st.container(border=True):
                st.subheader("⚡ ATS Readability Score")
                raw_text = data['sections']['raw_text']
                word_count = len(raw_text.split())
                readability_score = min(100, max(0, int((word_count / 400) * 100))) if word_count < 800 else 88
            
                st.metric(label="ATS Parsability Confidence", value=f"{readability_score}%", delta=f"{word_count} total words")
                st.progress(readability_score / 100.0)
            
                if word_count < 200:
                    st.warning("Resume is too short. ATS systems might discard it for lack of detail.")
                elif word_count > 1000:
                    st.warning("Resume is very long. Consider condensing for better human readability.")
                else:
                    st.success("Optimal length for ATS parsing and human readability.")
            # ---------------------------------------------------------
            
            with st.container(border=True):
                st.subheader("🔍 Parsed Resume Sections")
                sec_tabs = st.tabs(["Education", "Experience", "Projects", "Certifications"])
                with sec_tabs[0]:
                    st.write(data['sections']['Education'] or "No explicit education section detected.")
                with sec_tabs[1]:
                    st.write(data['sections']['Experience'] or "No explicit experience section detected.")
                with sec_tabs[2]:
                    st.write(data['sections']['Projects'] or "No explicit projects section detected.")
                with sec_tabs[3]:
                    st.write(data['sections']['Certifications'] or "No explicit certifications section detected.")

    elif selected_tab == "📊 Advanced Analytics":
        st.title("📊 Advanced Competency Analytics")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.container(border=True):
                st.subheader("🧬 Detected Skills Categories")
            
                cat_data = []
                for cat, items in data['skills_by_category'].items():
                    cat_data.append({"Category": cat, "Count": len(items), "Skills": ", ".join(items)})
            
                df_cat = pd.DataFrame(cat_data)
                if not df_cat.empty:
                    fig = px.bar(
                        df_cat,
                        x="Count",
                        y="Category",
                        orientation="h",
                        title="Skill Counts by Category",
                        color="Count",
                        color_continuous_scale="Viridis"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                    # --- Unique Feature: Radar Chart ---
                    st.subheader("Radar Chart: Skill Distribution")
                    fig_radar = px.line_polar(
                        df_cat, 
                        r="Count", 
                        theta="Category", 
                        line_close=True,
                        title="Skill Distribution Radar"
                    )
                    fig_radar.update_traces(fill='toself')
                    st.plotly_chart(fig_radar, use_container_width=True)
                    # -----------------------------------
                
                    st.dataframe(df_cat[["Category", "Skills"]])
                else:
                    st.write("No skills found.")

        with col2:
            with st.container(border=True):
                st.subheader("🎯 Match Score Analysis")
                if matches:
                    # Radial/gauge chart for the top role
                    top_role = matches[0]
                    fig_gauge = go.Figure(go.Indicator(
                        mode="gauge+number",
                        value=top_role['match_score'],
                        title={'text': f"Overall Fit: {top_role['role']}"},
                        gauge={
                            'axis': {'range': [0, 100]},
                            'bar': {'color': "#FF4B4B"},
                            'steps': [
                                {'range': [0, 40], 'color': "rgba(255, 75, 75, 0.1)"},
                                {'range': [40, 75], 'color': "rgba(255, 75, 75, 0.3)"},
                                {'range': [75, 100], 'color': "rgba(255, 75, 75, 0.6)"}
                            ]
                        }
                    ))
                    st.plotly_chart(fig_gauge, use_container_width=True)

    elif selected_tab == "🗺️ Upskilling Roadmap":
        st.title("🗺️ Personalized Weekly Upskilling Roadmap")
        
        # Let user choose which recommended role to generate roadmap for
        roles_list = [r['role'] for r in matches[:3]]
        selected_role_name = st.selectbox("Select Target Job Role", roles_list)
        
        target_role = next(r for r in matches if r['role'] == selected_role_name)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            with st.container(border=True):
                st.subheader("🎯 Role Profile Details")
                st.write(f"**Target Role:** `{target_role['role']}`")
                st.write(f"**Matched Skills:** {len(target_role['matched_skills'])} detected")
                st.write(f"**Missing Skills:** {len(target_role['missing_skills'])} detected")
                st.write(f"**Required Experience:** {target_role['experience_required']}")
                st.write(f"**Education Standard:** {target_role['education_required']}")
                st.write(f"**Standard Projects:** {target_role['projects_recommended']}")
            
            with st.container(border=True):
                st.subheader("⚠️ Missing Skills Checklist")
                for skill in target_role['missing_skills']:
                    st.markdown(f"❌ {skill}")
                if not target_role['missing_skills']:
                    st.success("🎉 You possess all required skills for this job role!")

        with col2:
            with st.container(border=True):
                st.subheader("📅 Weekly Learning Roadmap")
            
                # Generate schedule
                roadmap = RoadmapGenerator.generate_roadmap(target_role['missing_skills'], target_role['role'])
            
                st.write(roadmap["general_advice"])
                st.write(f"**Estimated Duration:** `{roadmap['weeks']} weeks`")
                st.write("---")
            
                for item in roadmap['schedule']:
                    with st.expander(f"📅 {item['period']} - Master: **{item['skill']}**"):
                        st.markdown("##### Target Focus & Tasks:")
                        for t in item['tasks']:
                            st.write(f"✅ {t}")
                        st.markdown("##### Curated Online Resources:")
                        res = item['resources']
                        st.markdown(f"📖 [Official Documentation]({res['docs']})")
                        st.markdown(f"💻 [GitHub Repositories]({res['github']})")
                        st.markdown(f"🎓 [Coursera Search]({res['coursera']})")
                        st.markdown(f"🎥 [YouTube Tutorials]({res['youtube']})")

    elif selected_tab == "💡 AI Career Advisor":
        st.title("💡 Dynamic Career Advisory & Interview Prep")
        
        # Selected target role
        roles_list = [r['role'] for r in matches[:3]]
        selected_role_name = st.selectbox("Select Interview Role", roles_list)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.container(border=True):
                st.subheader("📈 ATS Resume Critique")
                critique = utils.generate_resume_improvements(data['sections']['raw_text'])
                st.markdown(critique)
            
            with st.container(border=True):
                st.subheader("🎯 Job Preparation Tips")
                prep_tips = utils.generate_job_prep_tips(selected_role_name)
                st.markdown(prep_tips)

        with col2:
            with st.container(border=True):
                st.subheader("❓ Tailored Interview Questions & Hints")
                questions = utils.generate_interview_questions(selected_role_name, data['skills'])
                st.markdown(questions)
                
                # --- STT Feature ---
                st.divider()
                st.subheader("🎙️ Practice Answer (Voice)")
                st.write("Record your answer to one of the questions above.")
                audio = mic_recorder(start_prompt="Start Recording", stop_prompt="Stop Recording", key='recorder')
                if audio:
                    st.success("Audio successfully captured!")
                    st.audio(audio['bytes'])
                    st.info("In a full production environment, this would be transcribed and sent to the LLM for feedback.")
                # -------------------

    elif selected_tab == "📝 Cover Letter Gen":
        st.title("📝 AI Cover Letter Generator")
        st.write("Instantly generate a highly personalized, ATS-friendly cover letter based on your extracted resume and target role.")
        
        roles_list = [r['role'] for r in matches[:3]]
        selected_role_name = st.selectbox("Select Target Role for Cover Letter", roles_list)
        
        with st.container(border=True):
            if st.button("Generate Cover Letter", type="primary"):
                with st.spinner("Writing professional cover letter..."):
                    cover_letter = utils.generate_cover_letter(data['sections']['raw_text'], selected_role_name)
                
                    st.subheader("Your AI-Generated Cover Letter")
                    st.text_area("Copy your cover letter here:", value=cover_letter, height=400)
                
                    st.download_button(
                        label="⬇️ Download as Text File",
                        data=cover_letter,
                        file_name="cover_letter.txt",
                        mime="text/plain"
                    )

    elif selected_tab == "🎓 Academic Deliverables":
        st.title("🎓 Complete Academic Artifact Downloads")
        st.write("Automatically compiles academic reports, PowerPoint presentations, and summaries based on your profile.")
        
        # Automatically compile on button trigger
        pdf_gen = PDFReportGenerator()
        ppt_gen = PresentationGenerator()
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            with st.container(border=True):
                st.subheader("📄 Dynamic Reports")
            
                # Target role roadmap compiler data
                if not matches:
                    st.warning("No matches found to generate a report for.")
                    st.stop()
                top_match = matches[0]
                roadmap_data = RoadmapGenerator.generate_roadmap(top_match['missing_skills'], top_match['role'])
            
                payload_data = {
                    "summary": utils.generate_resume_summary(data['sections']['raw_text']),
                    "skills_by_category": data['skills_by_category'],
                    "recommendations": matches,
                    "roadmap": roadmap_data
                }
            
                if st.button("Compile Resume Analysis Report PDF"):
                    report_path = pdf_gen.generate_resume_analysis("resume_analysis_report.pdf", payload_data)
                    with open(report_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download Resume Analysis Report PDF",
                            data=f,
                            file_name="resume_analysis_report.pdf",
                            mime="application/pdf"
                        )
            
                if st.button("Compile College Project Report (6 Pages)"):
                    report_path = pdf_gen.generate_college_report("college_project_report.pdf")
                    with open(report_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download 6-Page Academic Project Report",
                            data=f,
                            file_name="college_project_report.pdf",
                            mime="application/pdf"
                        )
            
                if st.button("Compile One-Page LMS Summary PDF"):
                    report_path = pdf_gen.generate_one_page_summary("one_page_summary.pdf")
                    with open(report_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download One-Page Project Summary",
                            data=f,
                            file_name="one_page_summary.pdf",
                            mime="application/pdf"
                        )

        with col2:
            with st.container(border=True):
                st.subheader("📊 PPT Presentation")
            
                if st.button("Compile 15-Slide PPT Presentation"):
                    ppt_path = ppt_gen.generate_presentation("presentation.pptx")
                    with open(ppt_path, "rb") as f:
                        st.download_button(
                            label="⬇️ Download 15-Slide PowerPoint Deck",
                            data=f,
                            file_name="project_presentation.pptx",
                            mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                        )
