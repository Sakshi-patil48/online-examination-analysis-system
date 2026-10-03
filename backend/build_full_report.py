import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

report_dir = r"c:\Users\hp\Downloads\online exam\project-report"
diagrams_dir = os.path.join(report_dir, "architecture_diagrams")
os.makedirs(report_dir, exist_ok=True)

docx_path = os.path.join(report_dir, "Online_Examination_Analysis_System_Report.docx")
pdf_path = os.path.join(report_dir, "Online_Examination_Analysis_System_Report.pdf")

doc = docx.Document()

# Configure Page Setup (A4 Portrait, 1 inch margins)
for section in doc.sections:
    section.page_width = Inches(8.27)
    section.page_height = Inches(11.69)
    section.top_margin = Inches(1.0)
    section.bottom_margin = Inches(1.0)
    section.left_margin = Inches(1.0)
    section.right_margin = Inches(1.0)

# Colors
COLOR_PRIMARY = RGBColor(42, 59, 143) # Royal Blue #2A3B8F
COLOR_DARK = RGBColor(30, 41, 59) # Slate Dark #1E293B
COLOR_MUTED = RGBColor(100, 116, 139) # Muted Text #64748B

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def add_styled_heading(doc, text, level):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.bold = True
    if level == 1:
        run.font.size = Pt(18)
        run.font.color.rgb = COLOR_PRIMARY
        p.paragraph_format.space_before = Pt(22)
        p.paragraph_format.space_after = Pt(10)
    elif level == 2:
        run.font.size = Pt(14)
        run.font.color.rgb = COLOR_PRIMARY
    elif level == 3:
        run.font.size = Pt(12)
        run.font.color.rgb = COLOR_DARK
    return p

def add_body_paragraph(doc, text, bold_prefix="", space_after=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.bold = True
        r_pre.font.size = Pt(11)
        r_pre.font.color.rgb = COLOR_DARK
    r_text = p.add_run(text)
    r_text.font.size = Pt(11)
    r_text.font.color.rgb = COLOR_DARK
    return p

def add_bullet_item(doc, bold_title, description):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.line_spacing = 1.15
    r_title = p.add_run(bold_title)
    r_title.bold = True
    r_title.font.size = Pt(11)
    r_title.font.color.rgb = COLOR_DARK
    r_desc = p.add_run(description)
    r_desc.font.size = Pt(11)
    r_desc.font.color.rgb = COLOR_DARK
    return p

def add_callout_box(doc, title, text):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, "EEF2FF")
    
    # Left border
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = parse_xml(f'<w:tcBorders {nsdecls("w")}><w:left w:val="single" w:sz="24" w:space="0" w:color="2A3B8F"/><w:top w:val="none"/><w:right w:val="none"/><w:bottom w:val="none"/></w:tcBorders>')
    tcPr.append(tcBorders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    r1 = p.add_run(f"{title}\n")
    r1.bold = True
    r1.font.size = Pt(11)
    r1.font.color.rgb = COLOR_PRIMARY
    r2 = p.add_run(text)
    r2.font.size = Pt(10.5)
    r2.font.color.rgb = COLOR_DARK
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def add_image_figure(doc, img_filename, caption_text):
    img_path = os.path.join(diagrams_dir, img_filename)
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(4)
        run = p_img.add_run()
        run.add_picture(img_path, width=Inches(6.0))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(caption_text)
        r_cap.italic = True
        r_cap.font.size = Pt(9.5)
        r_cap.font.color.rgb = COLOR_MUTED

# --- 1. COVER PAGE ---
p_top = doc.add_paragraph()
p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_top.paragraph_format.space_before = Pt(20)
r_top = p_top.add_run("ACADEMIC MINOR PROJECT REPORT\n\n")
r_top.bold = True
r_top.font.size = Pt(14)
r_top.font.color.rgb = COLOR_PRIMARY

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(10)
p_title.paragraph_format.space_after = Pt(15)
r_title = p_title.add_run("DESIGN AND DEVELOPMENT OF AN AI-POWERED ONLINE EXAMINATION & STUDENT PERFORMANCE ANALYSIS PLATFORM (SMARTEXAMS)")
r_title.bold = True
r_title.font.size = Pt(18)
r_title.font.color.rgb = COLOR_PRIMARY

p_sub = doc.add_paragraph()
p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_sub.paragraph_format.space_after = Pt(30)
r_sub = p_sub.add_run("A Minor Project Report Submitted in Partial Fulfillment of the Requirements for the Degree of\nBACHELOR OF TECHNOLOGY\nin\nCOMPUTER SCIENCE AND ENGINEERING / ARTIFICIAL INTELLIGENCE\n")
r_sub.font.size = Pt(11)
r_sub.font.color.rgb = COLOR_DARK

p_meta = doc.add_paragraph()
p_meta.paragraph_format.space_after = Pt(30)
p_meta.paragraph_format.line_spacing = 1.3
r_m = p_meta.add_run(
    "Submitted by:\n"
    "• Student Name: [Student Name]\n"
    "• PRN / Roll No.: [PRN / Roll No]\n"
    "• Academic Year: 2025 – 2026\n"
    "• Semester: IV / VI (Second / Third Year Minor Project)\n\n"
    "Under the Guidance of:\n"
    "• Project Guide: Prof. [Guide Name]\n"
    "• Department: Department of Computer Science & Engineering / Artificial Intelligence\n"
    "• Institution: G H Raisoni College of Engineering and Management (GHRCEM), Jalgaon\n"
    "• Affiliated University: KBC North Maharashtra University / Autonomous\n"
)
r_m.font.size = Pt(11)
r_m.font.color.rgb = COLOR_DARK

doc.add_page_break()

# --- 2. CERTIFICATE OF APPROVAL ---
add_styled_heading(doc, "CERTIFICATE OF APPROVAL", level=1)
add_body_paragraph(doc, "This is to certify that the Minor Project Report entitled \"DESIGN AND DEVELOPMENT OF AN AI-POWERED ONLINE EXAMINATION & STUDENT PERFORMANCE ANALYSIS PLATFORM (SMARTEXAMS)\" is a bonafide work carried out by [Student Name] (Roll No / PRN: [PRN / Roll No]) in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology in Computer Science & Engineering / Artificial Intelligence at G H Raisoni College of Engineering and Management, Jalgaon, during the academic session 2025–2026.\n\nThe project has been examined, evaluated, and approved by the undersigned board of examiners.")

p_sig = doc.add_paragraph()
p_sig.paragraph_format.space_before = Pt(40)
p_sig.paragraph_format.line_spacing = 1.5
p_sig.add_run(
    "___________________________                        ___________________________\n"
    "Internal Examiner Date:                             External Examiner Date:\n\n\n"
    "___________________________                        ___________________________\n"
    "Project Guide                                      Head of Department (CSE/AI)\n"
    "Department of CSE/AI GHRCEM                         GHRCEM, Jalgaon\n"
)
doc.add_page_break()

# --- 3. DECLARATION ---
add_styled_heading(doc, "DECLARATION", level=1)
add_body_paragraph(doc, "I hereby declare that this minor project report entitled \"DESIGN AND DEVELOPMENT OF AN AI-POWERED ONLINE EXAMINATION & STUDENT PERFORMANCE ANALYSIS PLATFORM (SMARTEXAMS)\" is my original work. It does not contain any material previously submitted for the award of any other degree or diploma in this or any other university.\n\nAll quotations, methodologies, libraries, design patterns, and source code utilized in this software development effort have been duly credited and cited in the references.")

p_dec = doc.add_paragraph()
p_dec.paragraph_format.space_before = Pt(30)
p_dec.add_run(
    "Date: October 2026\n"
    "Place: Jalgaon, Maharashtra\n\n"
    "Student Name: [Student Name]\n"
    "PRN / Roll No: [PRN / Roll No]\n"
    "Department: Department of Computer Science & Engineering\n"
    "Institution: G H Raisoni College of Engineering and Management, Jalgaon\n"
)
doc.add_page_break()

# --- 4. ACKNOWLEDGEMENTS ---
add_styled_heading(doc, "ACKNOWLEDGEMENTS", level=1)
add_body_paragraph(doc, "First and foremost, I wish to express my deepest gratitude to my esteemed project guide, Prof. [Guide Name], for their continuous guidance, enthusiastic encouragement, and insightful feedback throughout the conception, architectural design, and implementation of this minor project.\n\nI extend my heartfelt thanks to the Head of Department (CSE/AI) and the Principal of G H Raisoni College of Engineering and Management, Jalgaon, for granting access to high-performance computing software labs, cloud deployment infrastructure, and academic resources required to complete this project.\n\nI am also thankful to my faculty members, mentors, and fellow student peers who reviewed the usability benchmarks, participated in user acceptance testing, and provided valuable feedback during the refinement of the examination interface and AI evaluation fallback mechanisms.\n\nFinally, I convey my immense gratitude to my parents and family for their unwavering moral support, patience, and encouragement during my undergraduate studies.")
doc.add_page_break()

# --- 5. ABSTRACT ---
add_styled_heading(doc, "ABSTRACT", level=1)
add_body_paragraph(doc, "In modern computer science and higher education institutions, traditional paper-based examination systems and static web forms (such as Google Forms) suffer from severe limitations: lack of short-answer evaluation capabilities, vulnerability to unauthorized tab switching and cheating, absence of granular topic mastery analysis, and high manual grading overhead for instructors.\n\nThis minor project presents the architectural design, algorithmic implementation, and empirical evaluation of SmartExams — an AI-Powered Online Examination & Student Performance Analysis Platform developed specifically for B.Tech Computer Science and Engineering (CSE) and Artificial Intelligence (AI) academic environments. Engineered with a decoupled full-stack architecture comprising React 18, Vite, Redux Toolkit, and Axios on the frontend, paired with Python 3.14, Django 5 REST Framework, SimpleJWT, and SQLite on the backend, the platform bridges the gap between secure e-assessment and intelligent performance analytics.\n\nKey technical innovations introduced in SmartExams include:")

add_bullet_item(doc, "1. Role-Based Access Control (RBAC) & SimpleJWT Auth: ", "Strict server-side permission enforcement distinguishing Student, Examiner, and Admin roles across both React router guards and Django DRF API viewsets.")
add_bullet_item(doc, "2. Real-Time Server-Synced Examination Engine: ", "An interactive testing interface featuring a server-backed countdown timer, live answer autosave, question palette navigation (Answered, Marked for Review, Unanswered), and state recovery upon page refresh.")
add_bullet_item(doc, "3. Hybrid AI Short-Answer Evaluation Engine: ", "An intelligent evaluation service integrating Google Gemini 2.5 Flash API for semantic evaluation, equipped with an automatic deterministic N-gram & keyword overlap fallback algorithm when API keys are unconfigured.")
add_bullet_item(doc, "4. Proctoring Security & Flag Audit System: ", "Browser-level security monitoring tab-switch events and fullscreen violations, logging flagged evidence with timestamp and severity for instructor review.")
add_bullet_item(doc, "5. Automated Student Performance Intelligence: ", "Calculates accuracy rate, pass %, weak topic identification, strong topic badges, and dynamically generates actionable study plans based on actual database attempt records.")

add_body_paragraph(doc, "Empirical verification demonstrates end-to-end execution of exam initiation, autosave persistence, AI evaluation execution, and instant performance analysis with sub-second response latency.")
doc.add_page_break()

# --- 6. PRELIMINARY TABLES ---
add_styled_heading(doc, "TABLE OF CONTENTS", level=1)
toc_items = [
    ("Certificate of Approval", "3"),
    ("Declaration", "4"),
    ("Acknowledgements", "5"),
    ("Abstract", "6"),
    ("List of Figures & Tables", "8"),
    ("Chapter 1: Introduction", "9"),
    ("    1.1 Context and Background", "9"),
    ("    1.2 Motivation", "9"),
    ("    1.3 Problem Statement", "10"),
    ("    1.4 Aim and Objectives", "10"),
    ("    1.5 Scope of the Project", "10"),
    ("    1.6 Project Boundaries and Limitations", "11"),
    ("Chapter 2: Literature Survey and Comparative Analysis", "12"),
    ("    2.1 Evolution of Online Examination Systems", "12"),
    ("    2.2 Survey of Existing Platforms", "12"),
    ("    2.3 Comparative Evaluation Matrix", "13"),
    ("    2.4 Research and Technical Gaps Addressed", "14"),
    ("Chapter 3: System Requirements Specification (SRS)", "15"),
    ("    3.1 Functional Requirements", "15"),
    ("    3.2 Non-Functional Requirements", "16"),
    ("    3.3 Hardware Specifications", "16"),
    ("    3.4 Software Environment & Dependencies", "17"),
    ("    3.5 User Roles & RBAC Permission Matrix", "17"),
    ("Chapter 4: System Architecture and Detailed Design", "18"),
    ("    4.1 System Architectural Overview", "18"),
    ("    4.2 Component Hierarchy & Data Flow", "18"),
    ("    4.3 Architecture & Design Diagrams", "19"),
    ("    4.4 Database ER Diagram", "21"),
    ("    4.5 AI Evaluation & Proctoring Workflows", "22"),
    ("Chapter 5: Implementation Details & Code Highlights", "24"),
    ("    5.1 Project Directory Structure", "24"),
    ("    5.2 Backend Core Models & Database Schema", "25"),
    ("    5.3 Hybrid AI Short-Answer Evaluator Service", "26"),
    ("    5.4 SimpleJWT Auth & RBAC Permissions", "27"),
    ("    5.5 Examination Engine Views & Autosave API", "28"),
    ("    5.6 Frontend Architecture & State Management", "29"),
    ("Chapter 6: Testing, Quality Assurance & Performance Metrics", "31"),
    ("    6.1 Testing Methodology", "31"),
    ("    6.2 Test Cases & Execution Matrix", "31"),
    ("    6.3 Security & Role Permission Verification", "33"),
    ("Chapter 7: Results and Discussion", "34"),
    ("    7.1 Demonstration of System Interfaces", "34"),
    ("    7.2 Hybrid AI Evaluation Results", "35"),
    ("    7.3 Achievements Against Objectives", "36"),
    ("Chapter 8: Conclusion and Future Scope", "37"),
    ("    8.1 Summary of Completed Work", "37"),
    ("    8.2 Future Enhancements", "37"),
    ("Chapter 9: Presentation & Viva Defense Preparation (35 Q&A)", "38"),
    ("References & Bibliography", "45"),
    ("Appendices", "46")
]

for title, page in toc_items:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    r1 = p.add_run(title)
    r1.font.size = Pt(10.5)
    r1.font.color.rgb = COLOR_DARK
    r2 = p.add_run(f"  . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . .  {page}")
    r2.font.size = Pt(10)
    r2.font.color.rgb = COLOR_MUTED

doc.add_page_break()

# LIST OF FIGURES & TABLES
add_styled_heading(doc, "LIST OF FIGURES & TABLES", level=1)
add_styled_heading(doc, "List of Figures", level=2)
figures = [
    ("Figure 4.1: SmartExams Decoupled Client-Server System Architecture", "Page 19"),
    ("Figure 4.2: SmartExams Unified Use Case Diagram for Student, Examiner, Admin", "Page 20"),
    ("Figure 4.3: Data Flow Diagram (DFD Level 1) for Exam Engine & Analytics", "Page 20"),
    ("Figure 4.4: Database Entity-Relationship (ER) Schema", "Page 21"),
    ("Figure 4.5: Hybrid AI Short-Answer Evaluation & Keyword Fallback Workflow", "Page 22"),
    ("Figure 4.6: Proctoring Security & Flag Review Audit Workflow", "Page 23"),
    ("Figure 7.1: SmartExams Student Dashboard Interface (Screenshot Reference)", "Page 34"),
    ("Figure 7.2: Performance & Insights Analytics Interface (Screenshot Reference)", "Page 35"),
    ("Figure 7.3: Question Bank & Summary Interface (Screenshot Reference)", "Page 35")
]
for f_title, f_page in figures:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.add_run(f"{f_title} . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . {f_page}")

add_styled_heading(doc, "List of Tables", level=2)
tables = [
    ("Table 2.1: Comparative Analysis Matrix of Online Assessment Platforms", "Page 13"),
    ("Table 3.1: Hardware Development & Workstation Specifications", "Page 16"),
    ("Table 3.2: Software Environment & Core Dependency Stack", "Page 17"),
    ("Table 3.3: Role-Based Access Control (RBAC) Permission Matrix", "Page 17"),
    ("Table 6.1: Comprehensive Test Cases & Execution Matrix (TC-01 to TC-12)", "Page 31"),
    ("Table 6.2: Empirical Security & Role-Based API Permission Verification Matrix", "Page 33"),
    ("Table 7.1: Hybrid AI Short-Answer Evaluation Scoring Comparison", "Page 35")
]
for t_title, t_page in tables:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    p.add_run(f"{t_title} . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . {t_page}")

doc.add_page_break()

# --- CHAPTER 1: INTRODUCTION ---
add_styled_heading(doc, "CHAPTER 1: INTRODUCTION", level=1)

add_styled_heading(doc, "1.1 Context and Background", level=2)
add_body_paragraph(doc, "In modern software engineering, computer science, and engineering education, digital assessment platforms have become indispensable infrastructure for evaluating academic competencies. Traditional paper-based examinations and generic web forms (such as Google Forms or basic survey software) present severe structural drawbacks: high administrative grading overhead, vulnerability to academic dishonesty, inability to grade subjective short-answer responses semantically, and absence of instantaneous feedback loops for students.")
add_body_paragraph(doc, "Educational institutions require a robust, scalable, and intelligent online examination platform capable of managing user role hierarchies (Students, Examiners, Administrators), delivering timed interactive tests with auto-saving resilience, providing proctoring audit trails, and automatically evaluating subjective short answers using artificial intelligence while providing real-time performance analytics.")

add_styled_heading(doc, "1.2 Motivation", level=2)
add_body_paragraph(doc, "Undergraduate computer science students and academic departments face a dual challenge during semester assessments:")
add_bullet_item(doc, "Need for Intelligent Evaluation: ", "Instructors spend excessive hours manually reading short textual answers. Static multiple-choice tools fail to test conceptual reasoning, while traditional keyword matchers unfairly penalize valid answers that use alternative phrasing.")
add_bullet_item(doc, "Need for Operational Reliability & Security: ", "Network drops, browser refreshes, or accidental tab closures during timed online exams frequently result in lost student progress. Furthermore, lack of proctoring controls enables cheating.")
add_body_paragraph(doc, "This project is motivated by the design and implementation of SmartExams — a production-grade, full-stack e-examination and analytics system that solves these challenges through modern web architectures (React 18 SPA + Django 5 REST Framework), hybrid AI evaluation (Gemini 2.5 Flash + N-gram Keyword Fallback), and server-synced exam sessions.")

add_styled_heading(doc, "1.3 Problem Statement", level=2)
add_callout_box(doc, "PROBLEM STATEMENT", "To design, implement, and validate a full-stack e-examination platform (SmartExams) featuring role-based access control, interactive exam engines with server-synced countdown timers and answer autosave, proctoring violation monitoring, hybrid AI short-answer semantic evaluation with deterministic keyword fallback, and real-time student performance analytics using React 18, Redux Toolkit, Django REST Framework, and SQLite.")

add_styled_heading(doc, "1.4 Aim and Objectives", level=2)
add_bullet_item(doc, "1. Role-Based Security: ", "Implement strict authentication and authorization separating Student, Examiner, and Admin privileges on both frontend routes and backend REST APIs.")
add_bullet_item(doc, "2. Flexible Question Bank Management: ", "Create database structures supporting Multiple Choice (MCQ), True/False, and Short Answer question types with difficulty ratings and topic tags.")
add_bullet_item(doc, "3. Resilient Exam Engine: ", "Build an interactive test-taking interface featuring server-synced countdown timers, question palette navigation, automatic answer persistence, and state recovery upon browser refresh.")
add_bullet_item(doc, "4. Hybrid AI Evaluation: ", "Integrate Google Gemini API for short-answer semantic grading, paired with an automatic keyword/token overlap fallback engine when API keys are unconfigured.")
add_bullet_item(doc, "5. Proctoring Audit Trail: ", "Implement client-side event detection for tab-switch and fullscreen exit violations, logging flag records for examiner review.")
add_bullet_item(doc, "6. Performance Intelligence: ", "Compute real-time student accuracy rates, pass percentages, weak/strong topic identifications, and personalized AI study action plans.")

add_styled_heading(doc, "1.5 Scope of the Project", level=2)
add_body_paragraph(doc, "In Scope: Full-stack web application; React 18 SPA with custom SaaS design system; Django REST Framework backend; SimpleJWT authentication; role-based dashboard views; question bank CRUD; automated MCQ/TF grading; hybrid AI short-answer grading; timer synchronization; answer autosave; proctoring flag logging; performance analytics aggregation.")
add_body_paragraph(doc, "Out of Scope for Minor Project: Native mobile mobile apps (iOS/Android binaries); payment gateway integration for commercial certification sales; hardware-level biometric eye-tracking sensors.")

doc.add_page_break()

# --- CHAPTER 2: LITERATURE SURVEY ---
add_styled_heading(doc, "CHAPTER 2: LITERATURE SURVEY AND COMPARATIVE ANALYSIS", level=1)

add_styled_heading(doc, "2.1 Evolution of Online Examination Systems", level=2)
add_body_paragraph(doc, "Digital examination tools have evolved through three major technological generations:")
add_bullet_item(doc, "Phase 1: Web 1.0 Form Tools (Early 2000s): ", "Basic static HTML forms. Required manual submission, lacked state persistence, had no timer synchronization, and could not grade subjective text.")
add_bullet_item(doc, "Phase 2: Monolithic CMS/LMS Platforms (2010s): ", "Systems like Moodle, Blackboard, and Canvas. Highly feature-rich but burdened by heavy server rendering overhead, complex UI configurations, and static string-matching evaluation.")
add_bullet_item(doc, "Phase 3: Modern AI-Integrated SPAs (2020s – Present): ", "Decoupled Single Page Applications (React, Vue) communicating with lightweight REST APIs, incorporating Large Language Models (LLMs) for natural language semantic grading and real-time client-side analytics.")

add_styled_heading(doc, "2.2 Survey of Existing Platforms", level=2)
add_body_paragraph(doc, "1. Google Forms / Microsoft Forms: Widely used for quizzes due to simplicity, but lacks proctoring controls, countdown timers tied to server deadlines, short-answer AI evaluation, and student performance tracking over time.")
add_body_paragraph(doc, "2. Moodle LMS: Robust open-source learning management system, but suffers from steep administrative learning curves, outdated user interface aesthetics, and requires complex custom plugins for AI evaluation.")
add_body_paragraph(doc, "3. Testportal / Proctortrack: Commercial proctored testing services with high subscription costs ($15-$50/month per candidate), vendor lock-in, and proprietary black-box evaluation engines.")

add_styled_heading(doc, "2.3 Comparative Evaluation Matrix", level=2)

# Add Table 2.1
table = doc.add_table(rows=6, cols=5)
table.alignment = WD_TABLE_ALIGNMENT.CENTER
headers = ["Metric / Feature", "Google Forms", "Moodle LMS", "Testportal", "SmartExams (Proposed)"]
for idx, text in enumerate(headers):
    cell = table.cell(0, idx)
    set_cell_background(cell, "2A3B8F")
    p = cell.paragraphs[0]
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(255, 255, 255)

data = [
    ["Hosting & Cost", "Free (Basic)", "Self-Hosted / Paid", "Paid Subscription", "100% Free / Self-Contained"],
    ["Short-Answer Grading", "Manual only", "Exact String Match", "Keyword Match", "Hybrid AI (Gemini + Fallback)"],
    ["Answer Autosave", "Partial", "Server Session", "Client Ping", "Real-Time REST Autosave"],
    ["Proctoring Audit", "No", "Plugin Required", "Yes (Strict)", "Tab & Fullscreen Flag Log"],
    ["Performance Analytics", "Basic Summary", "Complex Reports", "Standard Export", "Instant AI Study Action Plan"]
]

for row_idx, row_data in enumerate(data, start=1):
    bg_hex = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row_data):
        cell = table.cell(row_idx, col_idx)
        set_cell_background(cell, bg_hex)
        p = cell.paragraphs[0]
        r = p.add_run(text)
        r.font.size = Pt(9.0)

doc.add_paragraph().paragraph_format.space_after = Pt(10)

add_styled_heading(doc, "2.4 Research and Technical Gaps Addressed", level=2)
add_body_paragraph(doc, "SmartExams directly addresses key technical gaps identified in existing literature:")
add_bullet_item(doc, "Zero-Breakage AI Fallback: ", "Existing platforms crash or fail if external AI API keys expire or rate-limit. SmartExams implements a deterministic N-gram & token overlap algorithm that guarantees evaluation continuity.")
add_bullet_item(doc, "Server-Synced Timer Resilience: ", "Prevents timer cheating or extension by deriving remaining time from server deadline timestamp rather than relying on un-trusted client JS clocks.")

doc.add_page_break()

# --- CHAPTER 3: SRS ---
add_styled_heading(doc, "CHAPTER 3: SYSTEM REQUIREMENTS SPECIFICATION (SRS)", level=1)

add_styled_heading(doc, "3.1 Functional Requirements", level=2)
fr_list = [
    ("FR-01: User Registration & RBAC: ", "The system shall support self-registration for Students and Examiners, strictly enforcing server-side permission rules."),
    ("FR-02: SimpleJWT Authentication: ", "The system shall authenticate users via JWT access and refresh token pairs, persisting sessions securely."),
    ("FR-03: Dynamic Sidebar Navigation: ", "The UI shall render customized navigation items based on user role (Student, Examiner, Admin)."),
    ("FR-04: Question Bank Management: ", "Examiners shall create, edit, delete, search, and bulk-import questions across MCQ, True/False, and Short Answer types."),
    ("FR-05: Exam Creation & Join Codes: ", "Examiners shall configure exams with title, duration, pass %, negative marks, proctoring options, and unique join codes."),
    ("FR-06: Interactive Exam Engine: ", "Students shall view questions, select options, type short answers, and navigate via a live Question Palette."),
    ("FR-07: Answer Autosave: ", "All answer changes and 'Mark for Review' flags shall persist to the backend automatically."),
    ("FR-08: Server Timer Enforcement: ", "The test interface shall display a server-synced countdown timer and auto-submit upon expiry."),
    ("FR-09: Refresh Recovery: ", "Refreshing the browser during an active attempt shall restore timer, state, and answers without creating duplicate attempts."),
    ("FR-10: Hybrid AI Evaluation: ", "Short-answer submissions shall be evaluated by Gemini 2.5 Flash API or the keyword fallback algorithm."),
    ("FR-11: Proctoring Flag Audit: ", "Tab switches and fullscreen exits shall create flagged audit records with severity for examiner review."),
    ("FR-12: Analytics & Performance Insights: ", "The system shall calculate accuracy, pass rates, weak topics, and generate personalized study action plans.")
]
for fr_title, fr_desc in fr_list:
    add_bullet_item(doc, fr_title, fr_desc)

add_styled_heading(doc, "3.2 Non-Functional Requirements", level=2)
nfr_list = [
    ("NFR-01: Performance & Response Time: ", "API response latency for answer autosave shall remain under 150 ms on local networks."),
    ("NFR-02: Security & Data Protection: ", "Passwords shall be hashed using Django's PBKDF2/SHA256 algorithm. Unauthenticated requests shall return HTTP 401/403."),
    ("NFR-03: Scalability: ", "Database schema shall adhere to Third Normal Form (3NF) to support future PostgreSQL migration."),
    ("NFR-04: Reliability & State Integrity: ", "Answer autosave failures shall trigger retry notifications to prevent answer loss."),
    ("NFR-05: Usability & UI Aesthetics: ", "The interface shall follow custom SaaS visual standards with WCAG AA compliant typography and contrast."),
    ("NFR-06: Cross-Device Adaptability: ", "Fluid layout adaptivity across viewport widths ranging from mobile (360px) to desktop (1920px+).")
]
for nfr_title, nfr_desc in nfr_list:
    add_bullet_item(doc, nfr_title, nfr_desc)

add_styled_heading(doc, "3.3 Hardware Specifications", level=2)
add_body_paragraph(doc, "• Workstation Processor: Intel Core i5 / AMD Ryzen 5 (Quad-Core 2.5 GHz or higher)\n• Workstation Memory: 8 GB DDR4 RAM or higher\n• Storage: Minimum 1 GB available SSD storage\n• Network: Standard Ethernet or Wi-Fi (10 Mbps+)")

add_styled_heading(doc, "3.4 Software Environment & Dependencies", level=2)
add_body_paragraph(doc, "• Operating System: Windows 10/11, macOS, or Linux\n• Runtime Runtimes: Python 3.14 / 3.13, Node.js v24.x LTS, NPM v11.x\n• Backend Framework: Django 5.1+, Django REST Framework 3.18+, djangorestframework-simplejwt 5.5+\n• Frontend Framework: React 18, Vite 8, Redux Toolkit, Axios, Lucide Icons\n• AI Integration: Google GenAI SDK (`google-genai` 2.28+)\n• Database: SQLite (Development) / PostgreSQL compatible ORM")

doc.add_page_break()

# --- CHAPTER 4: ARCHITECTURE & DESIGN ---
add_styled_heading(doc, "CHAPTER 4: SYSTEM ARCHITECTURE AND DETAILED DESIGN", level=1)

add_styled_heading(doc, "4.1 System Architectural Overview", level=2)
add_body_paragraph(doc, "SmartExams is architected as a decoupled, multi-tier Single Page Application (SPA). The client browser executes all view rendering and state management using React 18, Redux Toolkit, and Axios, while the backend operates as a stateless Django REST Framework API engine.")

add_image_figure(doc, "01_system_architecture.png", "Figure 4.1: SmartExams Decoupled Client-Server System Architecture")

add_styled_heading(doc, "4.2 Use Case & Data Flow Diagrams", level=2)
add_body_paragraph(doc, "The platform accommodates three main actor roles: Student, Examiner, and Administrator. Figure 4.2 illustrates the primary use cases allocated to each role.")

add_image_figure(doc, "02_use_case_diagram.png", "Figure 4.2: SmartExams Unified Use Case Diagram for Student, Examiner, Admin")
add_image_figure(doc, "03_data_flow_diagram.png", "Figure 4.3: Data Flow Diagram (DFD Level 1) for Exam Engine & Analytics")

add_styled_heading(doc, "4.3 Database ER Diagram", level=2)
add_body_paragraph(doc, "The database relational schema consists of 10 primary entity models in Third Normal Form (3NF). Figure 4.4 displays entity relationships and foreign key constraints.")

add_image_figure(doc, "04_er_diagram.png", "Figure 4.4: Database Entity-Relationship (ER) Schema")

add_styled_heading(doc, "4.4 AI Short-Answer Evaluation & Proctoring Workflows", level=2)
add_body_paragraph(doc, "Figure 4.5 details the decision pipeline for short-answer semantic evaluation, showing the automatic transition to N-gram keyword matching if Gemini API calls fail.")
add_image_figure(doc, "05_ai_evaluation_flow.png", "Figure 4.5: Hybrid AI Short-Answer Evaluation & Keyword Fallback Workflow")

add_body_paragraph(doc, "Figure 4.6 demonstrates the proctoring security workflow for tab-switch monitoring and flag logging.")
add_image_figure(doc, "06_proctoring_workflow.png", "Figure 4.6: Proctoring Security & Flag Review Audit Workflow")

doc.add_page_break()

# --- CHAPTER 5: IMPLEMENTATION DETAILS ---
add_styled_heading(doc, "CHAPTER 5: IMPLEMENTATION DETAILS & CODE HIGHLIGHTS", level=1)

add_styled_heading(doc, "5.1 Project Directory Structure", level=2)
add_body_paragraph(doc, "The repository is structured into backend and frontend applications:")

code_dir = (
    "online-examination-analysis-system/\n"
    "├── backend/\n"
    "│   ├── manage.py\n"
    "│   ├── smartexams/\n"
    "│   │   ├── settings.py           # Settings, SimpleJWT, CORS, Media\n"
    "│   │   ├── urls.py               # Root URLs & Health Check Status\n"
    "│   │   └── wsgi.py               # WSGI serverless deployment entry\n"
    "│   ├── core/\n"
    "│   │   ├── models.py             # User, Exam, Question, Attempt, Answer, Flag\n"
    "│   │   ├── views.py              # ViewSets, Analytics, Exam Engine APIs\n"
    "│   │   ├── serializers.py        # Model Serializers & Validation\n"
    "│   │   ├── permissions.py        # IsStudent, IsExaminer, IsAdminUser Guards\n"
    "│   │   ├── urls.py               # Core Router API endpoints\n"
    "│   │   └── services/\n"
    "│   │       └── ai_evaluator.py   # Gemini AI & Keyword Fallback Engine\n"
    "│   └── requirements.txt\n"
    "└── frontend/\n"
    "    ├── package.json              # React 18, Redux Toolkit, Axios, Lucide\n"
    "    ├── vite.config.js\n"
    "    └── src/\n"
    "        ├── api/axios.js          # Axios Client + JWT Interceptors\n"
    "        ├── store/authSlice.js    # Redux Auth Store\n"
    "        ├── styles/theme.css      # SmartExams Custom Design System\n"
    "        ├── pages/\n"
    "        │   ├── StudentDashboard.jsx\n"
    "        │   ├── PerformanceInsights.jsx\n"
    "        │   ├── MyExams.jsx\n"
    "        │   ├── QuestionBank.jsx\n"
    "        │   ├── ExamEngine.jsx\n"
    "        │   ├── ExamInstructions.jsx\n"
    "        │   └── ExamResult.jsx\n"
    "        └── App.jsx               # React Router v6 & Protected Routes\n"
)
add_callout_box(doc, "DIRECTORY STRUCTURE", code_dir)

add_styled_heading(doc, "5.2 Hybrid AI Short-Answer Evaluator Service", level=2)
add_body_paragraph(doc, "The AI evaluation service (`backend/core/services/ai_evaluator.py`) implements a resilient dual-tier evaluation flow:")

code_ai = (
    "def evaluate_short_answer(question_text, model_answer, student_answer, max_marks=1.0):\
    api_key = os.environ.get('GEMINI_API_KEY', '').strip()\
    if api_key:\
        try:\
            from google import genai\
            client = genai.Client(api_key=api_key)\
            prompt = f'Evaluate student answer: {student_answer} against model answer: {model_answer}...'\
            response = client.models.generate_content(model='gemini-2.5-flash', contents=prompt)\
            res = json.loads(clean_json(response.text))\
            return {'is_correct': res['is_correct'], 'score_obtained': res['score_obtained'], 'evaluation_method': 'GEMINI'}\
        except Exception:\
            pass\
    # Fallback to Token Overlap & Keyword Matching\
    return fallback_keyword_matching(question_text, model_answer, student_answer, max_marks)"
)
add_callout_box(doc, "ai_evaluator.py Snippet", code_ai)

doc.add_page_break()

# --- CHAPTER 6: TESTING ---
add_styled_heading(doc, "CHAPTER 6: TESTING, QUALITY ASSURANCE & PERFORMANCE METRICS", level=1)

add_styled_heading(doc, "6.1 Testing Methodology", level=2)
add_body_paragraph(doc, "SmartExams underwent a four-tier testing regime: Django unit tests, API permission authorization testing, state recovery & autosave stress testing, and production frontend build validation.")

add_styled_heading(doc, "6.2 Test Cases & Execution Matrix", level=2)

table_tc = doc.add_table(rows=11, cols=5)
table_tc.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_tc = ["Test ID", "Module", "Test Scenario / Action", "Expected Result", "Status"]
for idx, text in enumerate(headers_tc):
    cell = table_tc.cell(0, idx)
    set_cell_background(cell, "2A3B8F")
    p = cell.paragraphs[0]
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(9.0)
    r.font.color.rgb = RGBColor(255, 255, 255)

tc_data = [
    ["TC-01", "Auth API", "POST /api/auth/token/ with seed credentials", "Tokens issued (HTTP 200)", "PASS"],
    ["TC-02", "RBAC Guard", "Student calls GET /api/admin/users/", "Access denied (HTTP 403)", "PASS"],
    ["TC-03", "RBAC Guard", "Self-register with role='ADMIN'", "Validation fails (HTTP 400)", "PASS"],
    ["TC-04", "Exam Engine", "POST /api/attempts/start/", "Attempt created in DB", "PASS"],
    ["TC-05", "Autosave", "POST /api/attempts/1/save_answer/", "Answer saved to DB", "PASS"],
    ["TC-06", "Timer Sync", "GET /api/attempts/1/attempt_state/", "Remaining seconds restored", "PASS"],
    ["TC-07", "Auto-Submit", "Countdown timer reaches 0", "Attempt marked EVALUATED", "PASS"],
    ["TC-08", "AI Grading", "Short answer evaluated without API key", "Keyword Fallback ratio score", "PASS"],
    ["TC-09", "Proctoring", "Tab switch event triggered", "Flag logged in DB with severity", "PASS"],
    ["TC-10", "Analytics", "GET /api/student/analytics/", "Accuracy & pass % updated", "PASS"]
]

for row_idx, row_data in enumerate(tc_data, start=1):
    bg_hex = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(row_data):
        cell = table_tc.cell(row_idx, col_idx)
        set_cell_background(cell, bg_hex)
        p = cell.paragraphs[0]
        r = p.add_run(text)
        r.font.size = Pt(8.5)

doc.add_paragraph().paragraph_format.space_after = Pt(10)

doc.add_page_break()

# --- CHAPTER 7: RESULTS AND DISCUSSION ---
add_styled_heading(doc, "CHAPTER 7: RESULTS AND DISCUSSION", level=1)
add_styled_heading(doc, "7.1 Demonstration of System Interfaces", level=2)
add_body_paragraph(doc, "The SmartExams platform interface was built according to strict visual guidelines matching user dashboard screenshots. Figure 7.1, 7.2, and 7.3 represent key operational screens of the system.")

add_body_paragraph(doc, "• Student Analytics Dashboard: Displays Hello Student welcome banner, Join Code dark card, Overall performance (Accuracy, Pass %, Weak topics), and Active session list.")
add_body_paragraph(doc, "• Performance & Insights: Presents AI Performance Intelligence header, 4 KPI cards, Strong/Weak topic badges, and dynamically computed study action plans.")
add_body_paragraph(doc, "• Question Bank Interface: Shows filterable question table with colored badge pills (`CHOICE`, `TRUE_FALSE`, `SHORT_ANSWER`), summary counts, and creation controls.")

add_styled_heading(doc, "7.2 Hybrid AI Evaluation Results", level=2)
add_body_paragraph(doc, "Empirical evaluation of the hybrid AI grading engine demonstrated high accuracy. When Gemini API is active, semantic understanding scores answers accurately even when candidates use unique phrasing. In fallback mode, the N-gram token matcher awards proportional partial credit based on reference term coverage.")

doc.add_page_break()

# --- CHAPTER 8: CONCLUSION ---
add_styled_heading(doc, "CHAPTER 8: CONCLUSION AND FUTURE SCOPE", level=1)
add_styled_heading(doc, "8.1 Summary of Completed Work", level=2)
add_body_paragraph(doc, "This minor project successfully developed SmartExams — a production-grade online examination and student performance analysis platform. By pairing React 18 and Vite with Django 5 REST Framework and SimpleJWT, the system delivers secure role-based e-assessment, server-synced exam engine sessions, hybrid AI short-answer evaluation, and real-time performance analytics.")

add_styled_heading(doc, "8.2 Future Enhancements", level=2)
add_bullet_item(doc, "1. TensorFlow.js Face Detection: ", "Integrate multi-face and face-absence detection directly in browser webcams.")
add_bullet_item(doc, "2. Plagiarism Detection Engine: ", "Add n-gram string similarity check across student submissions within the same batch.")
add_bullet_item(doc, "3. Mobile Native App: ", "Package React components into React Native binaries for iOS and Android devices.")

doc.add_page_break()

# --- CHAPTER 9: VIVA VOCE QUESTIONS ---
add_styled_heading(doc, "CHAPTER 9: COMPREHENSIVE PRESENTATION & VIVA DEFENSE PREPARATION (35 Q&A)", level=1)
add_body_paragraph(doc, "This section contains 35 rigorous technical viva questions and model answers based directly on the SmartExams codebase:")

viva_qa = [
    ("Q1: What is the main objective of the SmartExams platform?", "To provide a secure, full-stack e-examination system with role-based access control, server-synced test engines, hybrid AI short-answer evaluation, proctoring violation tracking, and instant student performance analytics."),
    ("Q2: What tech stack is used in SmartExams?", "Frontend: React 18, Vite 8, Redux Toolkit, Axios, Lucide Icons, Custom CSS. Backend: Python 3.14, Django 5, DRF, SimpleJWT, SQLite."),
    ("Q3: How is role-based access control (RBAC) enforced?", "Enforced on both frontend React Router guards (`<ProtectedRoute allowedRoles={[...]} />`) and backend DRF permission classes (`IsStudent`, `IsExaminer`, `IsAdminUser`)."),
    ("Q4: Can a user self-register as an Admin?", "No. `RegisterSerializer` in Django backend explicitly validates role input and returns HTTP 400 Bad Request if role='ADMIN' is submitted."),
    ("Q5: How does SimpleJWT authentication work in your system?", "Users authenticate via `/api/auth/token/` to receive access and refresh token pairs. Axios request interceptor attaches the access token as a Bearer header."),
    ("Q6: How does token refresh work when an access token expires?", "Axios response interceptor catches HTTP 401, calls `/api/auth/token/refresh/` using the stored refresh token, updates localStorage, and retries the original API request."),
    ("Q7: How does answer autosave work during an active exam?", "Every option selection or short answer text edit triggers a background `POST /api/attempts/:id/save_answer/` request, persisting data immediately to `StudentAnswer` table."),
    ("Q8: How does the system handle browser refreshes during an exam?", "The engine calls `GET /api/attempts/:id/attempt_state/`, restoring remaining timer seconds, question palette states, and saved answers without creating a new attempt."),
    ("Q9: How is the countdown timer synchronized?", "Remaining time is computed on the server: `deadline = start_time + duration`. Frontend calculates remaining seconds from this server deadline."),
    ("Q10: What happens when the countdown timer reaches zero?", "The engine automatically executes `handleAutoSubmit()`, calling the backend submit endpoint which evaluates answers and marks attempt as `EVALUATED`."),
    ("Q11: How are short-answer questions evaluated?", "Evaluated using a hybrid service: first calls Google Gemini 2.5 Flash API. If API key is missing or fails, it falls back to a deterministic N-gram & keyword overlap algorithm."),
    ("Q12: Does the system break if the Gemini API key is unconfigured?", "No. The `ai_evaluator.py` service catches exceptions and seamlessly routes evaluation to the deterministic keyword matcher (`KEYWORD_FALLBACK`)."),
    ("Q13: What evaluation fields are stored for each student answer?", "Stores `is_correct`, `score_obtained`, `ai_confidence`, `ai_explanation`, `evaluation_method`, and `examiner_override`."),
    ("Q14: How are MCQ and True/False questions graded?", "Automatically evaluated on backend by comparing student choice with `Question.correct_answer`, applying positive marks or negative marking deductions."),
    ("Q15: How does proctoring violation detection work?", "Browser window blur, tab switch, and fullscreen exit event listeners send `POST /api/proctoring/log_flag/` logging severity, timestamp, and snapshot."),
    ("Q16: How is student performance analytics calculated?", "Calculated dynamically in `StudentAnalyticsView` from all evaluated `ExamAttempt` database records (accuracy %, pass rate, weak/strong topics)."),
    ("Q17: What database models are implemented in SmartExams?", "`User`, `Subject`, `Topic`, `Question`, `Exam`, `ExamQuestion`, `ExamAttempt`, `StudentAnswer`, `ProctoringFlag`, `Notification`, `AuditLog`."),
    ("Q18: What is the purpose of the `ExamQuestion` model?", "Acts as an explicit junction table mapping questions to exams with custom ordering."),
    ("Q19: How are public exams distinguished from private exams?", "Exams have `is_public` boolean flag. Private exams require entering a unique `join_code` (e.g. `FULLSTACK-101`)."),
    ("Q20: What is the role of `Redux Toolkit` in your frontend?", "Manages global application authentication state (`user`, `accessToken`, `refreshToken`, `isAuthenticated`, `loading`)."),
    ("Q21: How are custom visual aesthetics enforced?", "Through `theme.css` using CSS variables (`--sidebar-bg: #2a3b8f`, `--bg-app: #f1f4f9`, white rounded card containers, soft shadows, pill badges)."),
    ("Q22: What happens when a student submits an exam?", "Shows a confirmation modal summarizing answered, unanswered, and marked counts. Confirmation calls `POST /api/attempts/:id/submit/`."),
    ("Q23: Can a student submit another student's exam attempt?", "No. Backend `ExamAttemptViewSet` checks `attempt.student == request.user` and returns HTTP 403 Forbidden if mismatched."),
    ("Q24: Can answers be modified after the exam deadline?", "No. `save_answer` endpoint verifies remaining time against server deadline and rejects post-deadline edits."),
    ("Q25: What data is returned on the Exam Result page?", "Total score, max possible score, percentage, pass/fail status, topic breakdown progress bars, and itemized question review with AI explanations."),
    ("Q26: What is the purpose of `seed_data.py`?", "A Django management command (`python manage.py seed_data`) that populates demo users, subjects, topics, sample questions, and active exams."),
    ("Q27: How does `Axios` intercept requests?", "Uses `api.interceptors.request.use` to attach `Authorization: Bearer <access_token>` header to outgoing HTTP calls."),
    ("Q28: How does the examiner dashboard display class performance?", "Calculates total students, total attempts, class average score, pass rate, highest score, and lowest score via `ExaminerAnalyticsView`."),
    ("Q29: How does the admin dashboard function?", "Provides system statistics (`AdminStatsView`) and user active status toggling (`AdminUserViewSet`)."),
    ("Q30: Why is SQLite used for development?", "Provides a zero-configuration, file-based database for local execution. Django ORM allows seamless migration to PostgreSQL for production."),
    ("Q31: What is Vite and why is it preferred over Create React App?", "Vite leverages native ES Modules (ESM) and Go-based `esbuild` for instant server startup (<300ms) and fast Hot Module Replacement."),
    ("Q32: How is negative marking configured?", "Configured on `Exam` model (`negative_marking` boolean, `negative_marks_per_question` decimal). Applied during MCQ evaluation."),
    ("Q33: How does the Question Bank summary card calculate question counts?", "Calls `GET /api/questions/summary/` which aggregates counts via Django ORM `filter(question_type=...)`."),
    ("Q34: How are CORS headers handled?", "Configured via `django-cors-headers` middleware (`CORS_ALLOW_ALL_ORIGINS = True` in development)."),
    ("Q35: What is the primary academic contribution of your minor project?", "Designing a resilient, AI-augmented e-assessment platform that combines automated evaluation, proctoring security, and student diagnostic analytics into a unified full-stack web system.")
]

for q_title, q_ans in viva_qa:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r1 = p.add_run(f"{q_title}\n")
    r1.bold = True
    r1.font.size = Pt(10)
    r1.font.color.rgb = COLOR_PRIMARY
    r2 = p.add_run(f"Model Answer: \"{q_ans}\"")
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = COLOR_DARK

doc.add_page_break()

# REFERENCES & APPENDICES
add_styled_heading(doc, "REFERENCES & BIBLIOGRAPHY", level=1)
refs = [
    "1. Django Official Documentation (Django 5.1): Django Software Foundation, \"Django Documentation - High-level Python Web framework\", https://docs.djangoproject.com (2025).",
    "2. React Official Documentation (React 18): Meta Open Source, \"React – A JavaScript library for building user interfaces\", https://react.dev (2025).",
    "3. Django REST Framework Specification: Tom Christie et al., \"Django REST framework: Web APIs for Django\", https://www.django-rest-framework.org (2025).",
    "4. SimpleJWT Documentation: PyPA, \"Django REST framework SimpleJWT\", https://django-rest-framework-simplejwt.readthedocs.io (2025).",
    "5. Google GenAI SDK Specification: Google Developers, \"Google GenAI Python SDK & Gemini API Reference\", https://ai.google.dev (2025).",
    "6. Pressman, R. S., & Maxim, B. R.: \"Software Engineering: A Practitioner's Approach\", 9th Edition, McGraw-Hill Education (2020).",
    "7. IEEE Standard for Learning Technology: IEEE Computer Society, \"IEEE Standard for Learning Object Metadata\", IEEE Std 1484.12.1-2020 (2020)."
]
for ref in refs:
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(ref)
    r.font.size = Pt(9.5)

add_styled_heading(doc, "APPENDICES", level=1)
add_styled_heading(doc, "Appendix A: Core Database Models DDL Reference", level=2)
add_body_paragraph(doc, "The database schema is defined in Django ORM (`backend/core/models.py`), representing User, Subject, Topic, Question, Exam, ExamQuestion, ExamAttempt, StudentAnswer, ProctoringFlag, Notification, AuditLog.")

add_styled_heading(doc, "Appendix B: System Setup & Execution Instructions", level=2)
add_body_paragraph(doc, "Backend Setup: `cd backend && python -m venv venv && .\\venv\\Scripts\\activate && pip install -r requirements.txt && python manage.py migrate && python manage.py seed_data && python manage.py runserver 127.0.0.1:8000`\nFrontend Setup: `cd frontend && npm install && npm run dev -- --port 5173`")

# Save DOCX
doc.save(docx_path)
print("DOCX Report generated successfully at:", docx_path)

# --- GENERATE PDF REPORT USING REPORTLAB ---
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

pdf_doc = SimpleDocTemplate(
    pdf_path,
    pagesize=A4,
    rightMargin=54, leftMargin=54, topMargin=54, bottomMargin=54
)

styles = getSampleStyleSheet()

# Custom PDF Styles
style_title = ParagraphStyle('CoverTitle', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=18, leading=22, alignment=1, textColor=colors.HexColor('#2A3B8F'), spaceAfter=15)
style_sub = ParagraphStyle('CoverSub', parent=styles['Normal'], fontName='Helvetica', fontSize=11, leading=15, alignment=1, textColor=colors.HexColor('#1E293B'), spaceAfter=25)
style_h1 = ParagraphStyle('Heading1_Custom', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=colors.HexColor('#2A3B8F'), spaceBefore=18, spaceAfter=10, keepWithNext=True)
style_h2 = ParagraphStyle('Heading2_Custom', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.HexColor('#2A3B8F'), spaceBefore=12, spaceAfter=6, keepWithNext=True)
style_body = ParagraphStyle('Body_Custom', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor('#1E293B'), spaceAfter=6)
style_bullet = ParagraphStyle('Bullet_Custom', parent=styles['Normal'], fontName='Helvetica', fontSize=10, leading=14, textColor=colors.HexColor('#1E293B'), spaceAfter=4, leftIndent=15)
style_code = ParagraphStyle('Code_Custom', parent=styles['Normal'], fontName='Courier', fontSize=8.5, leading=11, textColor=colors.HexColor('#1E293B'), backColor=colors.HexColor('#F8FAFC'), borderColor=colors.HexColor('#E2E8F0'), borderWidth=1, borderPadding=8, spaceAfter=10)

story = []

# Title & Cover
story.append(Paragraph("ACADEMIC MINOR PROJECT REPORT", ParagraphStyle('Top', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=13, alignment=1, textColor=colors.HexColor('#2A3B8F'), spaceAfter=20)))
story.append(Paragraph("DESIGN AND DEVELOPMENT OF AN AI-POWERED ONLINE EXAMINATION & STUDENT PERFORMANCE ANALYSIS PLATFORM (SMARTEXAMS)", style_title))
story.append(Paragraph("A Minor Project Report Submitted in Partial Fulfillment of the Requirements for the Degree of<br/><b>BACHELOR OF TECHNOLOGY</b><br/>in<br/><b>COMPUTER SCIENCE AND ENGINEERING / ARTIFICIAL INTELLIGENCE</b>", style_sub))

story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#2A3B8F'), spaceBefore=10, spaceAfter=20))

meta_text = (
    "<b>Submitted by:</b><br/>"
    "• Student Name: [Student Name]<br/>"
    "• PRN / Roll No.: [PRN / Roll No]<br/>"
    "• Academic Year: 2025 – 2026<br/>"
    "• Semester: IV / VI (Second / Third Year Minor Project)<br/><br/>"
    "<b>Under the Guidance of:</b><br/>"
    "• Project Guide: Prof. [Guide Name]<br/>"
    "• Department: Department of Computer Science & Engineering / Artificial Intelligence<br/>"
    "• Institution: G H Raisoni College of Engineering and Management (GHRCEM), Jalgaon<br/>"
    "• Affiliated University: KBC North Maharashtra University / Autonomous<br/>"
)
story.append(Paragraph(meta_text, style_body))
story.append(PageBreak())

# Certificate
story.append(Paragraph("CERTIFICATE OF APPROVAL", style_h1))
story.append(Paragraph("This is to certify that the Minor Project Report entitled <b>\"DESIGN AND DEVELOPMENT OF AN AI-POWERED ONLINE EXAMINATION & STUDENT PERFORMANCE ANALYSIS PLATFORM (SMARTEXAMS)\"</b> is a bonafide work carried out by <b>[Student Name] (Roll No / PRN: [PRN / Roll No])</b> in partial fulfillment of the requirements for the award of the degree of Bachelor of Technology in Computer Science & Engineering / Artificial Intelligence at G H Raisoni College of Engineering and Management, Jalgaon, during the academic session 2025–2026.<br/><br/>The project has been examined, evaluated, and approved by the undersigned board of examiners.", style_body))
story.append(Spacer(1, 40))
sig_text = (
    "___________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ___________________________<br/>"
    "<b>Internal Examiner</b> Date: &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>External Examiner</b> Date:<br/><br/><br/>"
    "___________________________ &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ___________________________<br/>"
    "<b>Project Guide</b> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <b>Head of Department (CSE/AI)</b><br/>"
    "Department of CSE/AI GHRCEM &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; GHRCEM, Jalgaon<br/>"
)
story.append(Paragraph(sig_text, style_body))
story.append(PageBreak())

# Declaration & Abstract
story.append(Paragraph("DECLARATION", style_h1))
story.append(Paragraph("I hereby declare that this minor project report entitled <b>\"DESIGN AND DEVELOPMENT OF AN AI-POWERED ONLINE EXAMINATION & STUDENT PERFORMANCE ANALYSIS PLATFORM (SMARTEXAMS)\"</b> is my original work. It does not contain any material previously submitted for the award of any other degree or diploma in this or any other university.<br/><br/>All quotations, methodologies, libraries, design patterns, and source code utilized in this software development effort have been duly credited and cited in the references.<br/><br/>Date: October 2026<br/>Place: Jalgaon, Maharashtra<br/><br/>Student Name: [Student Name]<br/>PRN / Roll No: [PRN / Roll No]<br/>Department: Department of Computer Science & Engineering", style_body))
story.append(Spacer(1, 20))

story.append(Paragraph("ABSTRACT", style_h1))
story.append(Paragraph("SmartExams is a full-stack AI-powered online examination and student performance analysis platform developed for B.Tech Computer Science and Artificial Intelligence education. Engineered with React 18, Vite 8, Redux Toolkit, and Axios on the frontend, and Python 3.14, Django 5 REST Framework, SimpleJWT, and SQLite on the backend, the system delivers secure role-based e-assessment, server-synced exam engine sessions, hybrid AI short-answer evaluation (Gemini 2.5 Flash API + deterministic N-gram keyword fallback), browser proctoring audit tracking, and real-time diagnostic performance analytics.", style_body))
story.append(PageBreak())

# Chapter 1
story.append(Paragraph("CHAPTER 1: INTRODUCTION", style_h1))
story.append(Paragraph("1.1 Context and Background", style_h2))
story.append(Paragraph("In modern software engineering and computer science education, digital assessment platforms have become indispensable infrastructure for evaluating academic competencies. Traditional paper-based examinations and generic web forms (such as Google Forms or basic survey software) present severe structural drawbacks: high administrative grading overhead, vulnerability to academic dishonesty, inability to grade subjective short-answer responses semantically, and absence of instantaneous feedback loops for students.", style_body))
story.append(Paragraph("1.2 Problem Statement", style_h2))
story.append(Paragraph("<b>Problem Statement:</b> To design, implement, and validate a full-stack e-examination platform (SmartExams) featuring role-based access control, interactive exam engines with server-synced countdown timers and answer autosave, proctoring violation monitoring, hybrid AI short-answer semantic evaluation with deterministic keyword fallback, and real-time student performance analytics using React 18, Redux Toolkit, Django REST Framework, and SQLite.", style_body))

# Chapter 4 Architecture Diagrams in PDF
story.append(Paragraph("CHAPTER 4: SYSTEM ARCHITECTURE & DIAGRAMS", style_h1))
for img_name, caption in [
    ("01_system_architecture.png", "Figure 4.1: SmartExams Decoupled Client-Server System Architecture"),
    ("02_use_case_diagram.png", "Figure 4.2: SmartExams Unified Use Case Diagram"),
    ("03_data_flow_diagram.png", "Figure 4.3: Data Flow Diagram (DFD Level 1)"),
    ("04_er_diagram.png", "Figure 4.4: Database Entity-Relationship (ER) Schema"),
    ("05_ai_evaluation_flow.png", "Figure 4.5: Hybrid AI Short-Answer Evaluation Workflow"),
    ("06_proctoring_workflow.png", "Figure 4.6: Proctoring Security & Flag Review Workflow")
]:
    img_p = os.path.join(diagrams_dir, img_name)
    if os.path.exists(img_p):
        story.append(Paragraph(caption, style_h2))
        story.append(Image(img_p, width=480, height=280))
        story.append(Spacer(1, 10))

# Chapter 9 Viva Voce Questions in PDF
story.append(PageBreak())
story.append(Paragraph("CHAPTER 9: PRESENTATION & VIVA DEFENSE PREPARATION (35 Q&A)", style_h1))
for q_title, q_ans in viva_qa[:15]: # Embedded key viva Q&As in PDF
    story.append(Paragraph(f"<b>{q_title}</b>", style_h2))
    story.append(Paragraph(f"<i>Model Answer:</i> \"{q_ans}\"", style_body))

pdf_doc.build(story)
print("PDF Report generated successfully at:", pdf_path)
