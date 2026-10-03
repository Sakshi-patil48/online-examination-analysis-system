import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

output_dir = r"c:\Users\hp\Downloads\online exam\project-report\architecture_diagrams"
os.makedirs(output_dir, exist_ok=True)

# Common styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.family'] = 'sans-serif'

# Diagram 1: System Architecture
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

# Title
ax.text(5, 5.7, "SmartExams System Architecture", fontsize=14, fontweight='bold', ha='center', color='#2a3b8f')

# Client Layer
rect_client = patches.FancyBboxPatch((0.5, 3.2), 3.0, 2.0, boxstyle="round,pad=0.1", ec="#324ed8", fc="#eef2ff", lw=2)
ax.add_patch(rect_client)
ax.text(2.0, 4.8, "Client Layer (Frontend)", fontsize=11, fontweight='bold', ha='center', color='#1e293b')
ax.text(2.0, 4.3, "• React 18 SPA & Vite 8\n• Redux Toolkit State\n• Axios API Client + JWT\n• Custom CSS Design System", fontsize=9, ha='center', color='#475569')

# Server Layer
rect_server = patches.FancyBboxPatch((4.2, 3.2), 3.0, 2.0, boxstyle="round,pad=0.1", ec="#2a3b8f", fc="#f1f4f9", lw=2)
ax.add_patch(rect_server)
ax.text(5.7, 4.8, "Server Layer (Backend)", fontsize=11, fontweight='bold', ha='center', color='#1e293b')
ax.text(5.7, 4.3, "• Python 3.14 + Django 5\n• Django REST Framework\n• SimpleJWT & RBAC Guards\n• ViewSets & Serializers", fontsize=9, ha='center', color='#475569')

# Data & AI Layer
rect_db = patches.FancyBboxPatch((7.8, 3.2), 1.8, 2.0, boxstyle="round,pad=0.1", ec="#16a34a", fc="#dcfce7", lw=2)
ax.add_patch(rect_db)
ax.text(8.7, 4.8, "Data Layer", fontsize=11, fontweight='bold', ha='center', color='#15803d')
ax.text(8.7, 4.3, "• Django ORM\n• SQLite (Dev)\n• Audit Logs\n• Media Storage", fontsize=9, ha='center', color='#166534')

# AI & Proctoring Services
rect_services = patches.FancyBboxPatch((2.5, 0.6), 5.0, 1.8, boxstyle="round,pad=0.1", ec="#ca8a04", fc="#fef9c3", lw=2)
ax.add_patch(rect_services)
ax.text(5.0, 2.0, "External & Intelligent Services Layer", fontsize=11, fontweight='bold', ha='center', color='#854d0e')
ax.text(5.0, 1.3, "• Google Gemini 2.5 Flash API (Short Answer Evaluation)\n• Deterministic N-Gram & Keyword Overlap Fallback Engine\n• Browser Webcam & Tab-Switch Proctoring Monitor", fontsize=9, ha='center', color='#713f12')

# Arrows
ax.annotate("", xy=(4.2, 4.2), xytext=(3.5, 4.2), arrowprops=dict(arrowstyle="<->", color="#324ed8", lw=2))
ax.annotate("", xy=(7.8, 4.2), xytext=(7.2, 4.2), arrowprops=dict(arrowstyle="<->", color="#16a34a", lw=2))
ax.annotate("", xy=(5.0, 3.2), xytext=(5.0, 2.4), arrowprops=dict(arrowstyle="<->", color="#ca8a04", lw=2))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "01_system_architecture.png"), dpi=300)
plt.close()

# Diagram 2: Use Case Diagram
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

ax.text(5, 5.7, "SmartExams Use Case Diagram", fontsize=14, fontweight='bold', ha='center', color='#2a3b8f')

# Actors
ax.text(1.0, 4.5, "👤 Student", fontsize=11, fontweight='bold', ha='center', color='#324ed8')
ax.text(1.0, 2.8, "👤 Examiner", fontsize=11, fontweight='bold', ha='center', color='#ca8a04')
ax.text(1.0, 1.1, "👤 Admin", fontsize=11, fontweight='bold', ha='center', color='#dc2626')

# System Boundary Box
rect_sys = patches.Rectangle((2.8, 0.4), 6.5, 5.0, ec="#64748b", fc="#fafbfc", lw=2, ls="--")
ax.add_patch(rect_sys)
ax.text(6.0, 5.1, "SmartExams Platform Boundary", fontsize=10, fontweight='bold', ha='center', color='#64748b')

# Use Cases (Ellipses)
cases = [
    ("Take Exam & Autosave", 4.2, 4.5),
    ("View Performance Insights", 7.5, 4.5),
    ("Question Bank Practice", 4.2, 3.7),
    ("Create & Schedule Exam", 7.5, 3.1),
    ("Manage Question Bank", 4.2, 2.5),
    ("Review Proctoring Audit", 7.5, 1.9),
    ("User & RBAC Management", 4.2, 1.1),
    ("System Audit Logs", 7.5, 0.9)
]

for label, x, y in cases:
    ellipse = patches.Ellipse((x, y), 2.6, 0.6, ec="#2a3b8f", fc="#ffffff", lw=1.5)
    ax.add_patch(ellipse)
    ax.text(x, y, label, fontsize=8.5, fontweight='bold', ha='center', va='center', color='#1e293b')

# Connectors
ax.plot([1.5, 2.9], [4.5, 4.5], color='#324ed8', lw=1.2)
ax.plot([1.5, 6.2], [4.5, 4.5], color='#324ed8', lw=1.2)
ax.plot([1.5, 2.9], [4.5, 3.7], color='#324ed8', lw=1.2)

ax.plot([1.5, 6.2], [2.8, 3.1], color='#ca8a04', lw=1.2)
ax.plot([1.5, 2.9], [2.8, 2.5], color='#ca8a04', lw=1.2)
ax.plot([1.5, 6.2], [2.8, 1.9], color='#ca8a04', lw=1.2)

ax.plot([1.5, 2.9], [1.1, 1.1], color='#dc2626', lw=1.2)
ax.plot([1.5, 6.2], [1.1, 0.9], color='#dc2626', lw=1.2)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "02_use_case_diagram.png"), dpi=300)
plt.close()

# Diagram 3: Data Flow Diagram (DFD Level 1)
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

ax.text(5, 5.7, "Data Flow Diagram (DFD Level 1)", fontsize=14, fontweight='bold', ha='center', color='#2a3b8f')

# External Entities
rect_p1 = patches.Rectangle((0.5, 4.2), 1.8, 0.9, ec="#324ed8", fc="#eef2ff", lw=1.5)
ax.add_patch(rect_p1)
ax.text(1.4, 4.65, "Student", fontsize=10, fontweight='bold', ha='center', color='#1e293b')

# Processes (Circles)
p_nodes = [
    ("1.0 Auth & JWT", 3.8, 4.65),
    ("2.0 Exam Session", 6.8, 4.65),
    ("3.0 Answer Autosave", 6.8, 2.5),
    ("4.0 AI Evaluation", 3.8, 2.5),
    ("5.0 Analytics Engine", 3.8, 0.8)
]

for label, x, y in p_nodes:
    circle = patches.Circle((x, y), 0.75, ec="#2a3b8f", fc="#ffffff", lw=2)
    ax.add_patch(circle)
    ax.text(x, y, label, fontsize=8, fontweight='bold', ha='center', va='center', color='#2a3b8f')

# Data Store
rect_ds = patches.Rectangle((7.8, 0.6), 1.8, 2.6, ec="#16a34a", fc="#dcfce7", lw=1.5)
ax.add_patch(rect_ds)
ax.text(8.7, 2.8, "D1: Database\n(SQLite/PostgreSQL)", fontsize=9, fontweight='bold', ha='center', color='#15803d')
ax.text(8.7, 1.8, "• Users\n• Exams\n• Questions\n• Attempts\n• Answers", fontsize=8, ha='center', color='#166534')

# Flow arrows
ax.annotate("Login Req", xy=(3.05, 4.65), xytext=(2.3, 4.65), arrowprops=dict(arrowstyle="->", color="#324ed8", lw=1.2), fontsize=7.5)
ax.annotate("Token", xy=(6.05, 4.65), xytext=(4.55, 4.65), arrowprops=dict(arrowstyle="->", color="#324ed8", lw=1.2), fontsize=7.5)
ax.annotate("Answer Payload", xy=(6.8, 3.25), xytext=(6.8, 3.9), arrowprops=dict(arrowstyle="->", color="#324ed8", lw=1.2), fontsize=7.5)
ax.annotate("Store Answer", xy=(7.8, 2.5), xytext=(7.55, 2.5), arrowprops=dict(arrowstyle="->", color="#16a34a", lw=1.2), fontsize=7.5)
ax.annotate("Short Ans", xy=(4.55, 2.5), xytext=(6.05, 2.5), arrowprops=dict(arrowstyle="->", color="#ca8a04", lw=1.2), fontsize=7.5)
ax.annotate("Eval Result", xy=(3.8, 1.55), xytext=(3.8, 1.75), arrowprops=dict(arrowstyle="->", color="#16a34a", lw=1.2), fontsize=7.5)

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "03_data_flow_diagram.png"), dpi=300)
plt.close()

# Diagram 4: ER Diagram
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

ax.text(5, 5.7, "Database Entity-Relationship (ER) Diagram", fontsize=14, fontweight='bold', ha='center', color='#2a3b8f')

entities = [
    ("User\n(PK: id, role, email)", 1.2, 4.5, "#eef2ff", "#324ed8"),
    ("Subject / Topic\n(PK: id, code, name)", 5.0, 4.5, "#e0f2fe", "#0284c7"),
    ("Exam\n(PK: id, join_code)", 8.8, 4.5, "#eef2ff", "#324ed8"),
    ("Question\n(PK: id, type, marks)", 5.0, 2.5, "#fef9c3", "#ca8a04"),
    ("ExamAttempt\n(PK: id, score, status)", 8.8, 2.5, "#dcfce7", "#16a34a"),
    ("StudentAnswer\n(PK: id, eval_method)", 5.0, 0.8, "#f3f4f6", "#475569"),
    ("ProctoringFlag\n(PK: id, flag_type)", 8.8, 0.8, "#fee2e2", "#dc2626")
]

for label, x, y, bg, ec in entities:
    r = patches.FancyBboxPatch((x-1.1, y-0.5), 2.2, 1.0, boxstyle="round,pad=0.05", ec=ec, fc=bg, lw=1.5)
    ax.add_patch(r)
    ax.text(x, y, label, fontsize=8.5, fontweight='bold', ha='center', va='center', color='#1e293b')

# Relationships Lines
ax.plot([2.3, 3.9], [4.5, 4.5], color='#64748b', lw=1.2, ls="--") # User creates Subject
ax.plot([6.1, 7.7], [4.5, 4.5], color='#64748b', lw=1.2) # Topic linked to Exam
ax.plot([5.0, 5.0], [4.0, 3.0], color='#64748b', lw=1.2) # Topic has Questions
ax.plot([8.8, 8.8], [4.0, 3.0], color='#64748b', lw=1.2) # Exam has Attempts
ax.plot([6.1, 7.7], [2.5, 2.5], color='#64748b', lw=1.2) # Attempt has Questions
ax.plot([5.0, 5.0], [2.0, 1.3], color='#64748b', lw=1.2) # Answer tied to Question
ax.plot([8.8, 8.8], [2.0, 1.3], color='#64748b', lw=1.2) # Attempt has ProctoringFlags

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "04_er_diagram.png"), dpi=300)
plt.close()

# Diagram 5: AI Evaluation Flow
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

ax.text(5, 5.7, "AI Short-Answer Evaluation & Fallback Flow", fontsize=14, fontweight='bold', ha='center', color='#2a3b8f')

blocks = [
    ("Student Submits Short Answer", 5.0, 4.9, "#eef2ff", "#324ed8"),
    ("Check GEMINI_API_KEY Configured?", 5.0, 3.7, "#fef9c3", "#ca8a04"),
    ("Call Gemini 2.5 Flash API\n(Generate Content & Grade JSON)", 2.3, 2.4, "#dcfce7", "#16a34a"),
    ("Execute N-Gram Keyword Matcher\n(Deterministic Fallback Ratio)", 7.7, 2.4, "#fee2e2", "#dc2626"),
    ("Store Score, AI Confidence & Explanation\n(Set eval_method: GEMINI / KEYWORD_FALLBACK)", 5.0, 1.0, "#e0f2fe", "#0284c7")
]

for label, x, y, bg, ec in blocks:
    r = patches.FancyBboxPatch((x-1.8, y-0.4), 3.6, 0.8, boxstyle="round,pad=0.05", ec=ec, fc=bg, lw=1.5)
    ax.add_patch(r)
    ax.text(x, y, label, fontsize=8.5, fontweight='bold', ha='center', va='center', color='#1e293b')

ax.annotate("", xy=(5.0, 4.1), xytext=(5.0, 4.5), arrowprops=dict(arrowstyle="->", color="#324ed8", lw=1.2))
ax.annotate("Yes (API Key Available)", xy=(3.2, 2.8), xytext=(4.0, 3.4), arrowprops=dict(arrowstyle="->", color="#16a34a", lw=1.2), fontsize=8)
ax.annotate("No / Exception", xy=(6.8, 2.8), xytext=(6.0, 3.4), arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.2), fontsize=8)
ax.annotate("", xy=(4.2, 1.4), xytext=(2.3, 2.0), arrowprops=dict(arrowstyle="->", color="#16a34a", lw=1.2))
ax.annotate("", xy=(5.8, 1.4), xytext=(7.7, 2.0), arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.2))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "05_ai_evaluation_flow.png"), dpi=300)
plt.close()

# Diagram 6: Proctoring Security Workflow
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
ax.set_xlim(0, 10)
ax.set_ylim(0, 6)
ax.axis('off')

ax.text(5, 5.7, "Proctoring Security & Audit Workflow", fontsize=14, fontweight='bold', ha='center', color='#2a3b8f')

p_blocks = [
    ("Active Exam Session Monitored", 1.8, 4.5, "#eef2ff", "#324ed8"),
    ("Detect Event:\nTab Switch / Fullscreen Exit", 5.0, 4.5, "#fef9c3", "#ca8a04"),
    ("Log Flag & Capture Snapshot\n(POST /api/proctoring/log_flag/)", 8.2, 4.5, "#fee2e2", "#dc2626"),
    ("Flag Logged with Severity & Timestamp", 8.2, 2.2, "#e0f2fe", "#0284c7"),
    ("Examiner Review Audit Dashboard\n(Review Flag & Add Notes)", 5.0, 2.2, "#dcfce7", "#16a34a"),
    ("Audit Log Updated / Session Cleared", 1.8, 2.2, "#f3f4f6", "#475569")
]

for label, x, y, bg, ec in p_blocks:
    r = patches.FancyBboxPatch((x-1.3, y-0.45), 2.6, 0.9, boxstyle="round,pad=0.05", ec=ec, fc=bg, lw=1.5)
    ax.add_patch(r)
    ax.text(x, y, label, fontsize=8.5, fontweight='bold', ha='center', va='center', color='#1e293b')

ax.annotate("", xy=(3.7, 4.5), xytext=(3.1, 4.5), arrowprops=dict(arrowstyle="->", color="#324ed8", lw=1.2))
ax.annotate("", xy=(6.9, 4.5), xytext=(6.3, 4.5), arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.2))
ax.annotate("", xy=(8.2, 2.65), xytext=(8.2, 4.05), arrowprops=dict(arrowstyle="->", color="#dc2626", lw=1.2))
ax.annotate("", xy=(6.3, 2.2), xytext=(6.9, 2.2), arrowprops=dict(arrowstyle="->", color="#16a34a", lw=1.2))
ax.annotate("", xy=(3.1, 2.2), xytext=(3.7, 2.2), arrowprops=dict(arrowstyle="->", color="#475569", lw=1.2))

plt.tight_layout()
plt.savefig(os.path.join(output_dir, "06_proctoring_workflow.png"), dpi=300)
plt.close()

print("All 6 architecture diagrams generated successfully in:", output_dir)
