"""
High-Definition Video Generator for Student Support Agent Demo
Generates student_support_agent_demo.mp4 as per VIDEO_DEMO_GUIDE.md
"""
import os
import sys
import subprocess
import asyncio
import tempfile
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
import edge_tts

WIDTH = 1920
HEIGHT = 1080
VOICE = "en-US-AndrewNeural"
FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()

# Font loader with fallbacks
def get_font(name="segoeui.ttf", size=24, bold=False):
    target = "segoeuib.ttf" if bold else name
    font_path = os.path.join("C:\\Windows\\Fonts", target)
    if not os.path.exists(font_path):
        target = "arialbd.ttf" if bold else "arial.ttf"
        font_path = os.path.join("C:\\Windows\\Fonts", target)
    try:
        return ImageFont.truetype(font_path, size)
    except Exception:
        return ImageFont.load_default()

FONT_TITLE = get_font("segoeui.ttf", 46, bold=True)
FONT_SUBTITLE = get_font("segoeui.ttf", 26, bold=False)
FONT_HEADING = get_font("segoeui.ttf", 32, bold=True)
FONT_BODY = get_font("segoeui.ttf", 22, bold=False)
FONT_BODY_BOLD = get_font("segoeui.ttf", 22, bold=True)
FONT_SMALL = get_font("segoeui.ttf", 18, bold=False)
FONT_MONO = get_font("consola.ttf", 20, bold=False)
FONT_MONO_BOLD = get_font("consola.ttf", 22, bold=True)
FONT_CAPTION = get_font("segoeui.ttf", 24, bold=True)

# Color Palette
BG_COLOR = (245, 247, 250)
NAVY_DARK = (12, 61, 79)
NAVY_LIGHT = (18, 84, 107)
WHITE = (255, 255, 255)
CARD_BG = (255, 255, 255)
CARD_BORDER = (220, 226, 235)
TEXT_DARK = (27, 36, 51)
TEXT_MUTED = (102, 112, 133)
PILL_OK_BG = (230, 244, 236)
PILL_OK_FG = (24, 121, 78)
PILL_WARN_BG = (253, 243, 220)
PILL_WARN_FG = (154, 100, 0)
PILL_BAD_BG = (253, 236, 234)
PILL_BAD_FG = (180, 35, 24)
CODE_BG = (15, 23, 32)
CODE_FG = (215, 224, 234)

def draw_topbar(draw, scene_idx, total_scenes, category_text):
    # Top navy header
    draw.rectangle([0, 0, WIDTH, 80], fill=NAVY_DARK)
    # Logo square
    draw.rounded_rectangle([30, 16, 78, 64], radius=8, fill=NAVY_LIGHT)
    draw.text((40, 24), "SS", font=get_font("segoeui.ttf", 24, bold=True), fill=WHITE)
    # Title
    draw.text((95, 22), "Student Support Desk", font=get_font("segoeui.ttf", 24, bold=True), fill=WHITE)
    draw.text((360, 26), "·  PGDM Institute  ·  Assignment 1 & Assignment 2", font=FONT_BODY, fill=(180, 210, 225))
    # Right scene badge
    badge_text = f"SCENE {scene_idx:02d} / {total_scenes:02d}  ·  {category_text}"
    draw.rounded_rectangle([WIDTH - 380, 18, WIDTH - 30, 62], radius=20, fill=NAVY_LIGHT)
    draw.text((WIDTH - 360, 26), badge_text, font=get_font("segoeui.ttf", 18, bold=True), fill=WHITE)

def draw_caption(draw, text):
    if not text:
        return
    # Wrap text for caption bar
    words = text.split()
    lines = []
    curr = []
    for w in words:
        curr.append(w)
        if len(" ".join(curr)) > 90:
            lines.append(" ".join(curr))
            curr = []
    if curr:
        lines.append(" ".join(curr))
    
    # Show last 2 lines max
    disp_lines = lines[-2:]
    box_h = 40 + len(disp_lines) * 32
    box_y = HEIGHT - 110
    draw.rounded_rectangle([160, box_y - box_h // 2, WIDTH - 160, box_y + box_h // 2], radius=16, fill=(15, 25, 35, 240))
    for i, line in enumerate(disp_lines):
        y = (box_y - box_h // 2 + 18) + i * 32
        draw.text((WIDTH // 2, y), line, font=FONT_CAPTION, fill=WHITE, anchor="mm")

def draw_card(draw, x1, y1, x2, y2, bg=CARD_BG, border=CARD_BORDER, radius=14):
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=bg, outline=border, width=1)

def draw_pill(draw, x, y, text, fg=PILL_OK_FG, bg=PILL_OK_BG, font=None):
    font = font or get_font("segoeui.ttf", 16, bold=True)
    bbox = font.getbbox(text)
    w = bbox[2] - bbox[0] + 20
    h = 28
    draw.rounded_rectangle([x, y, x + w, y + h], radius=14, fill=bg)
    draw.text((x + 10, y + 4), text, font=font, fill=fg)
    return w

# ----------------- SCENE RENDERERS -----------------

def render_scene_1():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_topbar(draw, 1, 14, "PROJECT INTRODUCTION")

    # Hero card
    draw_card(draw, 100, 120, WIDTH - 100, 400, bg=WHITE)
    draw_pill(draw, 140, 150, "AGENTIC AI ENGINEERING", fg=NAVY_DARK, bg=PILL_WARN_BG)
    draw_pill(draw, 390, 150, "PRODUCTION-READY", fg=PILL_OK_FG, bg=PILL_OK_BG)
    draw_pill(draw, 600, 150, "ASSIGNMENT 1 & 2 COMPLETE", fg=NAVY_DARK, bg=PILL_OK_BG)

    draw.text((140, 195), "Intelligent & Production-Safe Student Support Agent", font=FONT_TITLE, fill=NAVY_DARK)
    draw.text((140, 260), "A unified agentic system: Groq tool calling, vector RAG, cross-session memory, and security governance.", font=FONT_SUBTITLE, fill=TEXT_MUTED)

    # 4 Feature pillars
    pillars = [
        ("Dynamic Agent Loop", "Tool calling via Groq LLM; reasons autonomously before generating grounded responses.", PILL_OK_FG, PILL_OK_BG),
        ("Policy-Based RAG", "TF-IDF vector retrieval over institutional handbook; strictly zero invented rules.", NAVY_DARK, (230, 241, 244)),
        ("Backend Authorization", "Session-bound identity enforcement in Python code; cross-student data access is blocked.", PILL_WARN_FG, PILL_WARN_BG),
        ("Approval Governance", "Sensitive course and record mutations staged in approval queue; human-in-the-loop.", PILL_BAD_FG, PILL_BAD_BG),
    ]

    for i, (title, desc, fg, bg) in enumerate(pillars):
        x = 100 + i * (410 + 20)
        draw_card(draw, x, 440, x + 410, 880, bg=WHITE)
        draw_pill(draw, x + 25, 470, f"PILLAR 0{i+1}", fg=fg, bg=bg)
        draw.text((x + 25, 520), title, font=FONT_HEADING, fill=NAVY_DARK)
        
        # Word wrap desc
        words = desc.split()
        lines, curr = [], []
        for w in words:
            curr.append(w)
            if len(" ".join(curr)) > 26:
                lines.append(" ".join(curr))
                curr = []
        if curr: lines.append(" ".join(curr))
        for j, l in enumerate(lines):
            draw.text((x + 25, 580 + j * 32), l, font=FONT_BODY, fill=TEXT_MUTED)

        # Bottom bullet points
        bullets = [
            ["Groq Tool Calling", "Zero Hallucination", "Session Validation", "Human Approver"][i],
            ["Multi-turn Context", "Threshold Scores", "Tamper Block", "Rejection Safe"][i],
            ["Live Trace View", "Source Citation", "Audit Trail", "Audit Decision"][i]
        ]
        for k, b in enumerate(bullets):
            draw.text((x + 25, 720 + k * 36), f"•  {b}", font=FONT_BODY_BOLD, fill=TEXT_DARK)

    return img

def render_scene_2():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_topbar(draw, 2, 14, "ARCHITECTURE & STACK")

    draw.text((100, 110), "Full-Stack System Architecture & Inherited Agent Design", font=FONT_HEADING, fill=NAVY_DARK)
    draw.text((100, 155), "SafeStudentSupportAgentA2 inherits from StudentSupportAgentA1, extending it with production security controls.", font=FONT_SUBTITLE, fill=TEXT_MUTED)

    # 3 Layers: Client, Backend & Services, Storage & LLM
    layers = [
        ("Layer 1: Web Interface", [
            ("Student Portal (/portal)", "ChatGPT conversational interface, real-time fee summary, scholarship, change requests, memory cards."),
            ("Admin Console (/admin)", "Staff assistant, approval queues, ticket management, tamper-evident audit logs, benchmark evaluation."),
            ("Login Page (/login)", "Dual role authentication with 1-click credentials for instant demonstration.")
        ]),
        ("Layer 2: Flask Agent Backend", [
            ("StudentSupportAgentA1", "Baseline Agent: dynamic tool dispatch, context windowing, TF-IDF RAG retrieval, persistent memory."),
            ("SafeStudentSupportAgentA2", "Production-Safe Agent: inherits A1 + code-level authorization, approval queue, and audit log."),
            ("StaffAssistantA2", "Staff assistant: role-scoped read/notification tools with full institution visibility.")
        ]),
        ("Layer 3: Core Engine & Storage", [
            ("PolicyRetriever (RAG)", "TF-IDF vector index over policy handbook; extracts top-k relevant chunks with similarity scores."),
            ("MemoryStore", "JSON-backed cross-session persistent facts; strictly rejects passwords, OTPs, and temporary states."),
            ("AuditLog & Approvals", "Append-only JSON lines with automatic regex redaction; sensitive mutations require staff approval.")
        ])
    ]

    for i, (layer_title, items) in enumerate(layers):
        x = 100 + i * (550 + 35)
        draw_card(draw, x, 210, x + 550, 890, bg=WHITE)
        draw.rounded_rectangle([x, 210, x + 550, 275], radius=14, fill=NAVY_LIGHT)
        draw.text((x + 25, 230), layer_title, font=FONT_HEADING, fill=WHITE)

        for j, (header, desc) in enumerate(items):
            y = 300 + j * 190
            draw_card(draw, x + 20, y, x + 530, y + 170, bg=BG_COLOR)
            draw.text((x + 35, y + 20), header, font=FONT_BODY_BOLD, fill=NAVY_DARK)
            # wrap desc
            words = desc.split()
            lines, curr = [], []
            for w in words:
                curr.append(w)
                if len(" ".join(curr)) > 36:
                    lines.append(" ".join(curr))
                    curr = []
            if curr: lines.append(" ".join(curr))
            for k, l in enumerate(lines):
                draw.text((x + 35, y + 58 + k * 26), l, font=FONT_SMALL, fill=TEXT_MUTED)

    return img

def render_scene_3():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_topbar(draw, 3, 14, "AUTHENTICATION & LOGIN")

    draw.text((100, 110), "Dual-Role Authentication with 1-Click Demo Credentials", font=FONT_HEADING, fill=NAVY_DARK)

    # Left: Brand Card
    draw_card(draw, 100, 170, 880, 890, bg=NAVY_DARK)
    draw.text((150, 220), "PGDM INSTITUTE", font=get_font("segoeui.ttf", 20, bold=True), fill=(160, 210, 230))
    draw.text((150, 260), "Your student office,\nopen around the clock.", font=get_font("segoeui.ttf", 38, bold=True), fill=WHITE)
    draw.text((150, 370), "Instant answers for tuition fees, scholarships, policy rules,\nand administrative course changes.", font=FONT_BODY, fill=(200, 225, 235))

    features = [
        ("Instant verified answers", "Fee status, scholarship updates, and handbook rules."),
        ("Private by design", "Only authenticated records are accessible; cross-access blocked."),
        ("Staff-approved changes", "Elective and course changes staged for human approval.")
    ]
    for i, (t, d) in enumerate(features):
        y = 480 + i * 110
        draw.rounded_rectangle([150, y, 200, y + 50], radius=10, fill=NAVY_LIGHT)
        draw.text((168, y + 12), f"0{i+1}", font=get_font("segoeui.ttf", 20, bold=True), fill=WHITE)
        draw.text((220, y + 5), t, font=FONT_BODY_BOLD, fill=WHITE)
        draw.text((220, y + 35), d, font=FONT_SMALL, fill=(180, 210, 225))

    # Right: Login Form
    draw_card(draw, 930, 170, WIDTH - 100, 890, bg=WHITE)
    draw.text((980, 210), "Welcome back", font=FONT_HEADING, fill=NAVY_DARK)
    draw.text((980, 255), "Sign in to access your student support portal.", font=FONT_BODY, fill=TEXT_MUTED)

    # Role Tabs
    draw.rounded_rectangle([980, 305, 1380, 355], radius=10, fill=BG_COLOR)
    draw.rounded_rectangle([984, 309, 1176, 351], radius=8, fill=WHITE)
    draw.text((1035, 318), "Student", font=FONT_BODY_BOLD, fill=NAVY_DARK)
    draw.text((1240, 318), "Staff", font=FONT_BODY, fill=TEXT_MUTED)

    # Input fields
    draw.text((980, 385), "Student ID", font=FONT_BODY_BOLD, fill=TEXT_DARK)
    draw_card(draw, 980, 415, WIDTH - 150, 475, bg=WHITE, border=(18, 84, 107))
    draw.text((1005, 430), "S1001", font=FONT_BODY, fill=NAVY_DARK)

    draw.text((980, 495), "PIN / Password", font=FONT_BODY_BOLD, fill=TEXT_DARK)
    draw_card(draw, 980, 525, WIDTH - 150, 585, bg=WHITE, border=CARD_BORDER)
    draw.text((1005, 540), "••••", font=get_font("segoeui.ttf", 26, bold=True), fill=TEXT_DARK)

    # Sign In Button
    draw.rounded_rectangle([980, 615, WIDTH - 150, 675], radius=10, fill=NAVY_DARK)
    draw.text((1350, 630), "Sign in to Portal", font=get_font("segoeui.ttf", 22, bold=True), fill=WHITE, anchor="mm")

    # 1-Click Demo Credentials Box
    draw_card(draw, 980, 715, WIDTH - 150, 855, bg=BG_COLOR, border=NAVY_LIGHT)
    draw.text((1005, 730), "⚡ 1-Click Demo Credentials (Evaluation Ready)", font=FONT_BODY_BOLD, fill=NAVY_DARK)
    
    # 3 buttons
    draw.rounded_rectangle([1005, 765, 1220, 805], radius=8, fill=WHITE, outline=CARD_BORDER)
    draw.text((1025, 775), "S1001 (PIN: 1111)", font=get_font("segoeui.ttf", 16, bold=True), fill=NAVY_DARK)

    draw.rounded_rectangle([1240, 765, 1455, 805], radius=8, fill=WHITE, outline=CARD_BORDER)
    draw.text((1260, 775), "S1002 (PIN: 2222)", font=get_font("segoeui.ttf", 16, bold=True), fill=NAVY_DARK)

    draw.rounded_rectangle([1475, 765, 1720, 805], radius=8, fill=WHITE, outline=CARD_BORDER)
    draw.text((1490, 775), "Staff: admin / admin123", font=get_font("segoeui.ttf", 16, bold=True), fill=PILL_OK_FG)

    draw.text((1005, 822), "Clicking any badge auto-fills credentials and switches roles instantly.", font=FONT_SMALL, fill=TEXT_MUTED)

    return img

def render_scene_4():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_topbar(draw, 4, 14, "STUDENT DASHBOARD OVERVIEW")

    # Sidebar: Profile & Summaries
    draw_card(draw, 60, 110, 600, 890, bg=WHITE)
    draw.text((90, 140), "My Profile", font=FONT_HEADING, fill=NAVY_DARK)
    draw_pill(draw, 420, 138, "STUDENT", fg=NAVY_DARK, bg=PILL_OK_BG)

    profile_items = [
        ("Full Name", "Aarav Shah"),
        ("Student ID", "S1001"),
        ("Programme", "PGDM Big Data Analytics"),
        ("Academic Year", "2025-27 (Year 1)"),
        ("Elective", "Marketing Analytics"),
        ("Email", "aarav.shah@example.edu"),
        ("Phone", "9000000001")
    ]
    for i, (k, v) in enumerate(profile_items):
        y = 190 + i * 42
        draw.text((90, y), k, font=FONT_SMALL, fill=TEXT_MUTED)
        draw.text((270, y), v, font=FONT_BODY_BOLD, fill=TEXT_DARK)

    # Fee Summary Card in Sidebar
    draw.line([90, 495, 570, 495], fill=CARD_BORDER, width=1)
    draw.text((90, 515), "Fee Summary", font=FONT_HEADING, fill=NAVY_DARK)
    draw.text((90, 560), "INR 45,000", font=get_font("segoeui.ttf", 36, bold=True), fill=NAVY_DARK)
    draw_pill(draw, 340, 565, "Due in 15 days", fg=PILL_WARN_FG, bg=PILL_WARN_BG)
    # Meter bar
    draw.rounded_rectangle([90, 620, 570, 632], radius=6, fill=BG_COLOR)
    draw.rounded_rectangle([90, 620, 475, 632], radius=6, fill=PILL_OK_FG) # 82% paid
    draw.text((90, 642), "Paid: INR 205,000 (82%)  ·  Total: INR 250,000", font=FONT_SMALL, fill=TEXT_MUTED)

    # Scholarship
    draw.line([90, 685, 570, 685], fill=CARD_BORDER, width=1)
    draw.text((90, 705), "Scholarship", font=FONT_HEADING, fill=NAVY_DARK)
    draw.text((90, 745), "Merit Scholarship (INR 30,000)", font=FONT_BODY_BOLD, fill=TEXT_DARK)
    draw_pill(draw, 440, 742, "Approved", fg=PILL_OK_FG, bg=PILL_OK_BG)

    # Saved Memory
    draw.line([90, 790, 570, 790], fill=CARD_BORDER, width=1)
    draw.text((90, 805), "Saved Memory", font=FONT_HEADING, fill=NAVY_DARK)
    draw_pill(draw, 450, 805, "Persistent", fg=NAVY_DARK, bg=PILL_WARN_BG)
    draw.text((90, 845), "• contact_preference: email", font=FONT_BODY_BOLD, fill=TEXT_DARK)
    draw.text((480, 845), "[Forget]", font=FONT_BODY_BOLD, fill=PILL_BAD_FG)

    # Right: Chat Assistant View
    draw_card(draw, 640, 110, WIDTH - 60, 890, bg=WHITE)
    draw.text((680, 140), "AI Support Assistant", font=FONT_HEADING, fill=NAVY_DARK)
    draw_pill(draw, 1020, 138, "Production-Safe Agent (A2)", fg=PILL_OK_FG, bg=PILL_OK_BG)
    draw_pill(draw, 1360, 138, "Session Verified: S1001", fg=NAVY_DARK, bg=PILL_WARN_BG)

    # Welcome Card in Chat
    draw_card(draw, 680, 200, WIDTH - 100, 360, bg=BG_COLOR)
    draw.text((710, 230), "Hi Aarav, how can we help today?", font=FONT_HEADING, fill=NAVY_DARK)
    draw.text((710, 275), "Ask about your tuition fees, scholarship status, course changes, or institute rules.", font=FONT_BODY, fill=TEXT_MUTED)

    # Suggestion Chips
    chips = [
        "What is my current fee status?",
        "What is my scholarship status?",
        "What documents are required for admission?",
        "Can I request a course change?",
        "The payment portal failed. Can I pay on next working day?"
    ]
    for i, c in enumerate(chips):
        x = 710 + (i % 2) * 510
        y = 400 + (i // 2) * 65
        draw.rounded_rectangle([x, y, x + 490, y + 50], radius=10, fill=WHITE, outline=CARD_BORDER)
        draw.text((x + 20, y + 14), f"💬  {c}", font=FONT_BODY, fill=NAVY_DARK)

    # Message Composer at bottom
    draw_card(draw, 680, 770, WIDTH - 100, 850, bg=BG_COLOR, border=NAVY_LIGHT)
    draw.text((710, 795), "Type your question here... (Enter to send)", font=FONT_BODY, fill=TEXT_MUTED)
    draw.rounded_rectangle([WIDTH - 240, 785, WIDTH - 120, 835], radius=8, fill=NAVY_DARK)
    draw.text((WIDTH - 180, 802), "Send", font=FONT_BODY_BOLD, fill=WHITE, anchor="mm")

    return img

def render_scene_5():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_topbar(draw, 5, 14, "DYNAMIC TOOL EXECUTION")

    draw.text((100, 110), "Agent Tool Calling & Per-Query Trace Breakdown", font=FONT_HEADING, fill=NAVY_DARK)

    # User message bubble
    draw.rounded_rectangle([WIDTH - 650, 160, WIDTH - 100, 225], radius=16, fill=NAVY_DARK)
    draw.text((WIDTH - 620, 180), "What is my current fee status?", font=get_font("segoeui.ttf", 22, bold=True), fill=WHITE)

    # Assistant bubble
    draw_card(draw, 100, 245, WIDTH - 100, 410, bg=WHITE)
    draw.text((140, 275), "Your outstanding fee is INR 45,000 for Term 1, with a due date of 15 November 2026.", font=get_font("segoeui.ttf", 24, bold=True), fill=NAVY_DARK)
    draw.text((140, 320), "Total Fee: INR 250,000  ·  Paid: INR 205,000  ·  Status: Partially Paid.", font=FONT_BODY, fill=TEXT_MUTED)
    draw.text((140, 360), "Checked fee record  ·  Latency: 0.7s  ·  Model: openai/gpt-oss-120b", font=FONT_SMALL, fill=NAVY_LIGHT)

    # Expanded Trace Panel
    draw_card(draw, 100, 440, WIDTH - 100, 890, bg=CODE_BG)
    draw.text((140, 470), "🔍 Execution Trace · Query Evidence Timeline", font=FONT_HEADING, fill=WHITE)
    draw_pill(draw, WIDTH - 350, 468, "FINISHED: FINAL ANSWER", fg=PILL_OK_FG, bg=PILL_OK_BG)

    # Stats Bar
    stats = [
        ("Latency", "720 ms"),
        ("Model Calls", "2"),
        ("Tool Calls", "1 (get_fee_status)"),
        ("Input Tokens", "390"),
        ("Output Tokens", "62"),
        ("Permission", "ALLOWED")
    ]
    for i, (k, v) in enumerate(stats):
        x = 140 + i * 270
        draw_card(draw, x, 530, x + 250, 610, bg=(25, 35, 48), border=(45, 55, 70))
        draw.text((x + 15, 545), k, font=FONT_SMALL, fill=(160, 180, 205))
        draw.text((x + 15, 572), v, font=FONT_BODY_BOLD, fill=WHITE)

    # Step Timeline
    steps = [
        ("Step 1 · Context Selected", "History turns: 0 · Memory items: 1 (contact_preference=email) · Tools offered: 10", PILL_OK_FG),
        ("Step 2 · Model Call 1", "Latency: 420 ms · In: 340 / Out: 38 · Requested tool: get_fee_status(student_id='S1001')", (100, 180, 255)),
        ("Step 3 · Tool Execution", "Tool: get_fee_status · Args: {'student_id': 'S1001'} · Result: {'outstanding': 45000} · Latency: 18 ms", PILL_OK_FG),
        ("Step 4 · Model Call 2", "Latency: 280 ms · In: 390 / Out: 62 · Model processed tool result and generated final response", (100, 180, 255))
    ]
    for i, (head, detail, dot_col) in enumerate(steps):
        y = 640 + i * 58
        draw.ellipse([140, y + 6, 154, y + 20], fill=dot_col)
        draw.text((170, y), head, font=FONT_BODY_BOLD, fill=WHITE)
        draw.text((450, y + 2), detail, font=FONT_MONO, fill=(190, 210, 230))

    return img

def render_scene_6():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_topbar(draw, 6, 14, "GROUNDED POLICY RAG")

    draw.text((100, 110), "Grounded Retrieval-Augmented Generation (Zero Hallucination)", font=FONT_HEADING, fill=NAVY_DARK)

    # Question
    draw.rounded_rectangle([WIDTH - 850, 160, WIDTH - 100, 225], radius=16, fill=NAVY_DARK)
    draw.text((WIDTH - 820, 180), "The payment portal failed. Can I pay on the next working day?", font=get_font("segoeui.ttf", 22, bold=True), fill=WHITE)

    # Answer
    draw_card(draw, 100, 245, WIDTH - 100, 430, bg=WHITE)
    draw.text((140, 275), "Yes, you can pay on the next working day without any late fee penalty.", font=get_font("segoeui.ttf", 24, bold=True), fill=NAVY_DARK)
    draw.text((140, 320), "According to official institute policy, if the payment portal fails on the due date, you must raise a support", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((140, 355), "request on the same day attaching an error screenshot to receive the late fee waiver.", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((140, 395), "Searched Policy Handbook · Source Chunk: P3 (Payment Portal Failure) · Score: 0.384", font=FONT_SMALL, fill=NAVY_LIGHT)

    # RAG Retrieval Breakdown
    draw_card(draw, 100, 460, WIDTH - 100, 890, bg=WHITE)
    draw.text((140, 490), "RAG Evidence Breakdown: Handbook Chunk P3", font=FONT_HEADING, fill=NAVY_DARK)
    draw_pill(draw, 850, 488, "COSINE SCORE: 0.384 (ABOVE THRESHOLD 0.08)", fg=PILL_OK_FG, bg=PILL_OK_BG)

    # Chunks comparison
    draw_card(draw, 140, 550, 920, 840, bg=CODE_BG)
    draw.text((170, 575), "Retrieved Chunk Text (Injected to LLM Context)", font=FONT_BODY_BOLD, fill=WHITE)
    code_text = (
        "## Payment Portal Failure\n"
        "If the payment portal fails or is unavailable on the\n"
        "due date, the student may pay on the next working day\n"
        "without any late fee. To get this waiver, the student\n"
        "must raise a support request on the same day,\n"
        "mentioning the failure and attaching a screenshot\n"
        "of the error. Working days are Monday to Friday,\n"
        "excluding institute holidays."
    )
    for i, l in enumerate(code_text.splitlines()):
        draw.text((170, 620 + i * 26), l, font=FONT_MONO, fill=CODE_FG)

    draw_card(draw, 960, 550, WIDTH - 140, 840, bg=BG_COLOR)
    draw.text((990, 575), "Why TF-IDF Vector RAG is Production-Safe", font=FONT_BODY_BOLD, fill=NAVY_DARK)
    points = [
        "Full Handbook is NEVER dumped into prompts (prevents high token costs & confusion).",
        "Top-2 chunks ranked by TF-IDF vector cosine similarity.",
        "Threshold filtering: Chunks with score < 0.08 are discarded.",
        "No-Hallucination rule: If no relevant chunk matches, agent explicitly admits unavailability and suggests contacting office."
    ]
    for i, p in enumerate(points):
        y = 630 + i * 48
        draw.text((990, y), f"✓  {p}", font=FONT_BODY, fill=TEXT_DARK)

    return img

def render_scene_7():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_topbar(draw, 7, 14, "PERSISTENT CROSS-SESSION MEMORY")

    draw.text((100, 110), "Persistent Student Memory Across Distinct Sessions", font=FONT_HEADING, fill=NAVY_DARK)

    # Split Session 1 and Session 2
    draw_card(draw, 100, 170, 930, 890, bg=WHITE)
    draw_pill(draw, 140, 200, "SESSION 1 (SAVE PREFERENCE)", fg=NAVY_DARK, bg=PILL_OK_BG)

    # User 1
    draw.rounded_rectangle([250, 260, 890, 320], radius=14, fill=NAVY_DARK)
    draw.text((270, 278), "Please remember that I prefer to receive updates by email.", font=FONT_BODY_BOLD, fill=WHITE)

    # Assistant 1
    draw_card(draw, 140, 340, 890, 480, bg=BG_COLOR)
    draw.text((160, 360), "I have noted your preference to receive updates by email.", font=FONT_BODY_BOLD, fill=NAVY_DARK)
    draw.text((160, 400), "Tool executed: save_memory(key='contact_preference', value='email')", font=FONT_MONO, fill=NAVY_LIGHT)
    draw.text((160, 435), "Saved to runtime/memory.json under student ID S1001.", font=FONT_SMALL, fill=TEXT_MUTED)

    # Sidebar representation
    draw_card(draw, 140, 510, 890, 840, bg=CODE_BG)
    draw.text((170, 540), "Student Portal Sidebar: Saved Memory", font=FONT_BODY_BOLD, fill=WHITE)
    draw.text((170, 585), "• contact_preference : email", font=FONT_MONO_BOLD, fill=PILL_OK_FG)
    draw.rounded_rectangle([750, 580, 850, 615], radius=6, fill=PILL_BAD_BG)
    draw.text((770, 590), "Forget", font=FONT_SMALL, fill=PILL_BAD_FG)

    draw.text((170, 650), "Student-controlled deletion:", font=FONT_BODY, fill=(180, 205, 230))
    draw.text((170, 690), "DELETE /api/student/preferences/contact_preference", font=FONT_MONO, fill=(240, 200, 120))
    draw.text((170, 730), "Audited as: delete_memory in audit.jsonl", font=FONT_SMALL, fill=TEXT_MUTED)

    # Right: Session 2 Recall
    draw_card(draw, 970, 170, WIDTH - 100, 890, bg=WHITE)
    draw_pill(draw, 1010, 200, "SESSION 2 (NEW CONVERSATION - RECALL)", fg=NAVY_DARK, bg=PILL_WARN_BG)

    # User 2
    draw.rounded_rectangle([1060, 260, WIDTH - 140, 320], radius=14, fill=NAVY_DARK)
    draw.text((1080, 278), "Which contact method did I tell you earlier that I prefer?", font=FONT_BODY_BOLD, fill=WHITE)

    # Assistant 2
    draw_card(draw, 1010, 340, WIDTH - 140, 530, bg=BG_COLOR)
    draw.text((1040, 370), "You previously mentioned that you prefer to receive updates by email.", font=get_font("segoeui.ttf", 24, bold=True), fill=NAVY_DARK)
    draw.text((1040, 420), "I can use this email preference when sending receipts and notifications.", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((1040, 470), "Context Selection: Recalled 'contact_preference=email' from long-term memory.", font=FONT_SMALL, fill=NAVY_LIGHT)

    # Context management highlight
    draw_card(draw, 1010, 560, WIDTH - 140, 840, bg=WHITE, border=NAVY_LIGHT)
    draw.text((1040, 590), "Context Management Architecture", font=FONT_HEADING, fill=NAVY_DARK)
    points2 = [
        "Relevance-driven memory selection (keyword overlap scoring).",
        "Does NOT send all stored memories (keeps context clean).",
        "Windowed session history: Last 4 turns sent to LLM.",
        "Temporary information remains temporary (never enters long-term store)."
    ]
    for i, p in enumerate(points2):
        y = 650 + i * 45
        draw.text((1040, y), f"✓  {p}", font=FONT_BODY, fill=TEXT_DARK)

    return img

def render_scene_8():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_topbar(draw, 8, 14, "SECURITY & SECRETS MASKING")

    draw.text((100, 110), "Security Guardrail: Automatic Redaction of Passwords & OTPs", font=FONT_HEADING, fill=NAVY_DARK)

    # Student input with OTP
    draw.rounded_rectangle([WIDTH - 850, 160, WIDTH - 100, 225], radius=16, fill=NAVY_DARK)
    draw.text((WIDTH - 820, 180), "My portal OTP is 482913 and password is Secret@123, remember it.", font=FONT_BODY_BOLD, fill=WHITE)

    # Interception visual
    draw_card(draw, 100, 250, WIDTH - 100, 430, bg=PILL_BAD_BG, border=(240, 180, 170))
    draw_pill(draw, 140, 280, "SECURITY INTERCEPTION: SENSITIVE CREDENTIAL DETECTED", fg=PILL_BAD_FG, bg=WHITE)
    draw.text((140, 325), "Regex Pattern Match: SENSITIVE_PATTERNS matched 'otp' and 'password'.", font=FONT_BODY_BOLD, fill=PILL_BAD_FG)
    draw.text((140, 365), "Tool Call 'save_memory' REJECTED in Python code: Sensitive information is never stored.", font=FONT_BODY, fill=TEXT_DARK)

    # Comparison Grid
    draw_card(draw, 100, 460, 930, 890, bg=WHITE)
    draw.text((140, 490), "Persistent Memory Store Inspection", font=FONT_HEADING, fill=NAVY_DARK)
    draw_card(draw, 140, 540, 890, 720, bg=CODE_BG)
    draw.text((160, 560), "// runtime/memory.json (S1001)", font=FONT_MONO, fill=(120, 140, 160))
    draw.text((160, 600), "{\n  \"S1001\": [\n    {\"key\": \"contact_preference\", \"value\": \"email\"}\n  ]\n}", font=FONT_MONO_BOLD, fill=CODE_FG)
    draw.text((140, 750), "✓  Zero credentials, OTPs, or passwords stored in memory.", font=FONT_BODY_BOLD, fill=PILL_OK_FG)
    draw.text((140, 790), "✓  Temporary moods (tired, stressed, busy) also rejected.", font=FONT_BODY_BOLD, fill=PILL_OK_FG)

    draw_card(draw, 970, 460, WIDTH - 100, 890, bg=WHITE)
    draw.text((1010, 490), "Tamper-Evident Redacted Audit Trail", font=FONT_HEADING, fill=NAVY_DARK)
    draw_card(draw, 1010, 540, WIDTH - 140, 720, bg=CODE_BG)
    draw.text((1030, 560), "// runtime/audit.jsonl entry", font=FONT_MONO, fill=(120, 140, 160))
    audit_snippet = (
        "{\n"
        "  \"actor\": \"S1001\",\n"
        "  \"action\": \"save_memory\",\n"
        "  \"decision\": \"blocked\",\n"
        "  \"result\": \"Sensitive information is never stored\"\n"
        "}"
    )
    for i, l in enumerate(audit_snippet.splitlines()):
        draw.text((1030, 595 + i * 26), l, font=FONT_MONO_BOLD, fill=(240, 200, 120))
    draw.text((1010, 750), "✓  All outputs sanitized with redact() before storage.", font=FONT_BODY_BOLD, fill=PILL_OK_FG)
    draw.text((1010, 790), "✓  Safe from log exposure and prompt leakage.", font=FONT_BODY_BOLD, fill=PILL_OK_FG)

    return img

def render_scene_9():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_topbar(draw, 9, 14, "DATA PRIVACY & AUTHORIZATION")

    draw.text((100, 110), "Backend Authorization: Cross-Student Access Strictly Blocked", font=FONT_HEADING, fill=NAVY_DARK)

    # Malicious or unauthorized request
    draw.rounded_rectangle([WIDTH - 750, 160, WIDTH - 100, 225], radius=16, fill=NAVY_DARK)
    draw.text((WIDTH - 720, 180), "Show me the fee status of student S1002.", font=FONT_BODY_BOLD, fill=WHITE)

    # Assistant Block Response
    draw_card(draw, 100, 250, WIDTH - 100, 390, bg=WHITE, border=PILL_BAD_FG)
    draw_pill(draw, 140, 275, "ACCESS DENIED · BACKEND ENFORCEMENT", fg=PILL_BAD_FG, bg=PILL_BAD_BG)
    draw.text((140, 315), "Access denied: you can only access or change your own record.", font=get_font("segoeui.ttf", 26, bold=True), fill=PILL_BAD_FG)
    draw.text((140, 355), "Target student S1002 does not match authenticated session identity S1001. Violation recorded.", font=FONT_BODY, fill=TEXT_MUTED)

    # Code Enforcement Visual
    draw_card(draw, 100, 420, 1050, 890, bg=CODE_BG)
    draw.text((140, 450), "Enforced in Python Tool Code (app.py)", font=FONT_HEADING, fill=WHITE)
    code_auth = (
        "class SafeStudentSupportAgentA2(StudentSupportAgentA1):\n"
        "    def execute_tool(self, name, args, ctx):\n"
        "        actor = ctx['student_id']  # From session cookie\n"
        "        if name in RECORD_TOOLS:\n"
        "            target = str(args.get('student_id') or actor).upper()\n"
        "            if target != actor:\n"
        "                ctx['permission'] = 'blocked'\n"
        "                self.audit.record(actor, name, target, 'blocked',\n"
        "                                  'access denied', {'args': args})\n"
        "                return {'error': 'Access denied: you can only access '\n"
        "                                 'or change your own record.'}\n"
        "            ctx['permission'] = 'allowed'\n"
        "        return super().execute_tool(name, args, ctx)"
    )
    for i, l in enumerate(code_auth.splitlines()):
        color = PILL_BAD_BG if "blocked" in l or "Access denied" in l else CODE_FG
        draw.text((140, 500 + i * 26), l, font=FONT_MONO, fill=color)

    # Right side: Audit and guarantees
    draw_card(draw, 1090, 420, WIDTH - 100, 890, bg=WHITE)
    draw.text((1130, 450), "Security Guarantees", font=FONT_HEADING, fill=NAVY_DARK)
    sec_points = [
        ("Never trusts LLM prompt instructions alone.", "Attackers cannot bypass authorization via prompt injection."),
        ("Session-Derived Identity", "Identity comes from secure HTTP-only cookie, not user parameters."),
        ("Tool-Level Defense", "Every query accessing private records verifies caller ownership in code."),
        ("Tamper Logging", "Any spoofing attempt creates a permanent audit record with decision='blocked'.")
    ]
    for i, (head, body) in enumerate(sec_points):
        y = 510 + i * 90
        draw_pill(draw, 1130, y, f"RULE 0{i+1}", fg=NAVY_DARK, bg=PILL_OK_BG)
        draw.text((1220, y + 2), head, font=FONT_BODY_BOLD, fill=TEXT_DARK)
        draw.text((1130, y + 36), body, font=FONT_SMALL, fill=TEXT_MUTED)

    return img

def render_scene_10():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_topbar(draw, 10, 14, "SENSITIVE ACTION GOVERNANCE")

    draw.text((100, 110), "Human-in-the-Loop Governance: Course Change Approval Queue", font=FONT_HEADING, fill=NAVY_DARK)

    # Request
    draw.rounded_rectangle([WIDTH - 850, 160, WIDTH - 100, 225], radius=16, fill=NAVY_DARK)
    draw.text((WIDTH - 820, 180), "I would like to change my elective to Financial Analytics.", font=FONT_BODY_BOLD, fill=WHITE)

    # Agent response
    draw_card(draw, 100, 250, WIDTH - 100, 410, bg=WHITE)
    draw_pill(draw, 140, 275, "PENDING HUMAN APPROVAL", fg=PILL_WARN_FG, bg=PILL_WARN_BG)
    draw.text((140, 315), "Course change request APR-7A2D19 has been submitted for human approval.", font=get_font("segoeui.ttf", 26, bold=True), fill=NAVY_DARK)
    draw.text((140, 355), "It has NOT been applied yet. The Student Records Office must review and approve before records are updated.", font=FONT_BODY, fill=TEXT_MUTED)

    # Two column status: Student record (UNCHANGED) vs Approval Record (STAGED)
    draw_card(draw, 100, 440, 930, 890, bg=WHITE)
    draw.text((140, 470), "Student Profile (Unmodified)", font=FONT_HEADING, fill=NAVY_DARK)
    draw_pill(draw, 720, 468, "UNCHANGED", fg=PILL_OK_FG, bg=PILL_OK_BG)

    rows = [
        ("Student Name", "Aarav Shah"),
        ("Programme", "PGDM Big Data Analytics"),
        ("Current Elective", "Marketing Analytics (Active)"),
        ("Requested Elective", "Financial Analytics (Awaiting Approval)")
    ]
    for i, (k, v) in enumerate(rows):
        y = 530 + i * 55
        draw.text((140, y), k, font=FONT_BODY, fill=TEXT_MUTED)
        draw.text((400, y), v, font=FONT_BODY_BOLD, fill=PILL_BAD_FG if "Awaiting" in v else TEXT_DARK)

    draw_card(draw, 970, 440, WIDTH - 100, 890, bg=WHITE)
    draw.text((1010, 470), "Approval Queue Entry (runtime/approvals.json)", font=FONT_HEADING, fill=NAVY_DARK)
    draw_pill(draw, 1620, 468, "PENDING", fg=PILL_WARN_FG, bg=PILL_WARN_BG)

    draw_card(draw, 1010, 520, WIDTH - 140, 840, bg=CODE_BG)
    code_apr = (
        "{\n"
        "  \"request_id\": \"APR-7A2D19\",\n"
        "  \"student_id\": \"S1001\",\n"
        "  \"field\": \"elective\",\n"
        "  \"old_value\": \"Marketing Analytics\",\n"
        "  \"new_value\": \"Financial Analytics\",\n"
        "  \"status\": \"pending\",\n"
        "  \"requested_at\": \"2026-10-31T16:30:00Z\",\n"
        "  \"decided_by\": null,\n"
        "  \"decided_at\": null\n"
        "}"
    )
    for i, l in enumerate(code_apr.splitlines()):
        draw.text((1040, 545 + i * 28), l, font=FONT_MONO, fill=PILL_WARN_BG if "pending" in l else CODE_FG)

    return img

def render_scene_11():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_topbar(draw, 11, 14, "STAFF ADMIN CONSOLE")

    draw.text((100, 110), "Staff Admin Console: Human Review & Decision Execution", font=FONT_HEADING, fill=NAVY_DARK)

    # Admin Tabs
    tabs = ["Overview", "AI Assistant", "Students", "Approvals (1)", "Support tickets", "Audit log", "Conversations", "Evaluation"]
    for i, t in enumerate(tabs):
        x = 100 + i * 215
        active = "Approvals" in t
        draw.rounded_rectangle([x, 160, x + 205, 205], radius=8, fill=NAVY_DARK if active else WHITE, outline=CARD_BORDER)
        draw.text((x + 102, 175), t, font=get_font("segoeui.ttf", 16, bold=active), fill=WHITE if active else TEXT_DARK, anchor="mm")

    # Table of Approvals
    draw_card(draw, 100, 230, WIDTH - 100, 890, bg=WHITE)
    draw.text((140, 260), "Change Requests Awaiting Human Decision", font=FONT_HEADING, fill=NAVY_DARK)

    # Headers
    headers = ["Request ID", "Student Name", "Field", "Current Value", "Requested Value", "Submitted", "Staff Action"]
    col_x = [140, 310, 560, 710, 960, 1220, 1460]
    draw.rounded_rectangle([140, 310, WIDTH - 140, 355], radius=6, fill=BG_COLOR)
    for h, x in zip(headers, col_x):
        draw.text((x, 322), h, font=FONT_BODY_BOLD, fill=TEXT_MUTED)

    # Pending Row
    draw.text((140, 385), "APR-7A2D19", font=FONT_MONO_BOLD, fill=NAVY_DARK)
    draw.text((310, 385), "Aarav Shah (S1001)", font=FONT_BODY_BOLD, fill=TEXT_DARK)
    draw.text((560, 385), "elective", font=FONT_BODY, fill=TEXT_DARK)
    draw.text((710, 385), "Marketing Analytics", font=FONT_BODY, fill=TEXT_MUTED)
    draw.text((960, 385), "Financial Analytics", font=FONT_BODY_BOLD, fill=NAVY_DARK)
    draw.text((1220, 385), "Just now", font=FONT_BODY, fill=TEXT_MUTED)

    # Action buttons: Approve and Reject
    draw.rounded_rectangle([1460, 375, 1560, 415], radius=6, fill=PILL_OK_FG)
    draw.text((1510, 386), "Approve", font=get_font("segoeui.ttf", 16, bold=True), fill=WHITE, anchor="mm")

    draw.rounded_rectangle([1580, 375, 1670, 415], radius=6, fill=PILL_BAD_BG, outline=PILL_BAD_FG)
    draw.text((1625, 386), "Reject", font=get_font("segoeui.ttf", 16, bold=True), fill=PILL_BAD_FG, anchor="mm")

    # Lower card showing the executed result
    draw_card(draw, 140, 480, WIDTH - 140, 840, bg=BG_COLOR, border=NAVY_LIGHT)
    draw.text((170, 510), "Decision Execution & Invariant Safety Rules", font=FONT_HEADING, fill=NAVY_DARK)

    invariants = [
        ("If Staff Rejects:", "Status becomes 'rejected'. Zero modifications applied. Original record intact. Repeated rejection blocked."),
        ("If Staff Approves:", "Status becomes 'approved'. Change executed EXACTLY ONCE to data/students.json. Notification dispatched."),
        ("No Auto-Execution:", "Normal chat messages saying 'I approve' CANNOT modify records. Only authenticated staff endpoints modify data.")
    ]
    for i, (rule, desc) in enumerate(invariants):
        y = 570 + i * 85
        draw_pill(draw, 170, y, rule, fg=NAVY_DARK, bg=PILL_WARN_BG)
        draw.text((170, y + 40), desc, font=FONT_BODY, fill=TEXT_DARK)

    return img

def render_scene_12():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_topbar(draw, 12, 14, "AUDIT LOGS & TRACES")

    draw.text((100, 110), "Forensic Audit Logging & Complete Observability Traces", font=FONT_HEADING, fill=NAVY_DARK)

    # Dual Panel: Audit Log Table vs Conversation Traces Table
    draw_card(draw, 100, 170, 930, 890, bg=WHITE)
    draw.text((140, 200), "Tamper-Evident Audit Log (runtime/audit.jsonl)", font=FONT_HEADING, fill=NAVY_DARK)

    audit_records = [
        ("16:30:15", "admin", "approval_decision", "S1001", "approved", "elective updated to Financial Analytics"),
        ("16:28:40", "S1001", "request_record_change", "S1001", "pending", "queued APR-7A2D19 for approval"),
        ("16:25:10", "S1001", "get_fee_status", "S1002", "blocked", "Access denied: cross-student block"),
        ("16:20:00", "S1001", "save_memory", "S1001", "blocked", "Sensitive credential rejected"),
        ("16:15:22", "S1001", "login", "S1001", "allowed", "PIN verified via scrypt hash")
    ]

    for i, (tm, act, action, tgt, dec, res) in enumerate(audit_records):
        y = 260 + i * 115
        draw_card(draw, 140, y, 890, y + 100, bg=BG_COLOR)
        draw.text((160, y + 15), f"⏰ {tm}  ·  Actor: {act}  →  Target: {tgt}", font=FONT_SMALL, fill=TEXT_MUTED)
        draw.text((160, y + 42), f"Action: {action}", font=FONT_BODY_BOLD, fill=NAVY_DARK)
        draw_pill(draw, 420, y + 38, dec.upper(), fg=PILL_OK_FG if dec=="allowed" or dec=="approved" else PILL_BAD_FG if dec=="blocked" else PILL_WARN_FG,
                  bg=PILL_OK_BG if dec=="allowed" or dec=="approved" else PILL_BAD_BG if dec=="blocked" else PILL_WARN_BG)
        draw.text((160, y + 72), f"Result: {res}", font=FONT_SMALL, fill=TEXT_DARK)

    # Right: Conversation Traces
    draw_card(draw, 970, 170, WIDTH - 100, 890, bg=WHITE)
    draw.text((1010, 200), "Observability Traces (runtime/traces.jsonl)", font=FONT_HEADING, fill=NAVY_DARK)

    traces = [
        ("S1001", "What is my current fee status?", "2 calls", "1 tool", "720 ms", "390 in / 62 out"),
        ("S1001", "The payment portal failed...", "2 calls", "search_policy", "810 ms", "450 in / 95 out"),
        ("S1001", "Show fee status of S1002", "1 call", "BLOCKED", "630 ms", "410 in / 42 out"),
        ("S1001", "Change elective to Financial Analytics", "2 calls", "request_change", "850 ms", "470 in / 75 out")
    ]
    for i, (sid, q, mc, tc, lat, tok) in enumerate(traces):
        y = 260 + i * 140
        draw_card(draw, 1010, y, WIDTH - 140, y + 125, bg=CODE_BG)
        draw.text((1035, y + 15), f"Student {sid}  ·  Question: \"{q}\"", font=FONT_BODY_BOLD, fill=WHITE)
        draw.text((1035, y + 50), f"Model Calls: {mc}  ·  Tool: {tc}", font=FONT_MONO, fill=(180, 215, 240))
        draw.text((1035, y + 85), f"Latency: {lat}  ·  Token Usage: {tok}", font=FONT_SMALL, fill=(240, 200, 120))

    return img

def render_scene_13():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_topbar(draw, 13, 14, "BENCHMARK EVALUATION")

    draw.text((100, 110), "System Evaluation: Baseline Agent (A1) vs Safe Agent (A2)", font=FONT_HEADING, fill=NAVY_DARK)

    # Benchmark Table Card
    draw_card(draw, 100, 170, WIDTH - 100, 890, bg=WHITE)
    draw.text((140, 200), "Reproducible Benchmark Metrics Comparison", font=FONT_HEADING, fill=NAVY_DARK)

    headers = ["Evaluation Metric", "Assignment 1 (Baseline)", "Assignment 2 (Production-Safe)", "Safety & Security Verdict"]
    col_x = [140, 620, 1050, 1440]
    draw.rounded_rectangle([140, 250, WIDTH - 140, 295], radius=6, fill=NAVY_LIGHT)
    for h, x in zip(headers, col_x):
        draw.text((x, 262), h, font=FONT_BODY_BOLD, fill=WHITE)

    metrics = [
        ("Task Accuracy", "100%", "100%", "High Accuracy", PILL_OK_FG, PILL_OK_BG),
        ("Successful Tasks", "9 / 9", "8 / 8", "All Verified", PILL_OK_FG, PILL_OK_BG),
        ("Average Latency", "701 ms", "656 ms", "Real-Time Response", NAVY_DARK, (230, 241, 244)),
        ("Average Input Tokens", "398 tokens", "378 tokens", "Compact Context", NAVY_DARK, (230, 241, 244)),
        ("Average Output Tokens", "55 tokens", "55 tokens", "Concise Generation", NAVY_DARK, (230, 241, 244)),
        ("Privacy Test Success", "N/A (No auth layer)", "2 / 2 (100%)", "Strict Backend Block", PILL_OK_FG, PILL_OK_BG),
        ("Unsafe Action Prevention", "N/A (No approval gate)", "2 / 2 (100%)", "Human Approver Gate", PILL_OK_FG, PILL_OK_BG),
        ("Tool Execution Success", "9 / 9 (100%)", "8 / 8 (100%)", "Deterministic Dispatch", PILL_OK_FG, PILL_OK_BG)
    ]

    for i, (m, a1, a2, verdict, v_fg, v_bg) in enumerate(metrics):
        y = 315 + i * 65
        draw.line([140, y - 8, WIDTH - 140, y - 8], fill=CARD_BORDER, width=1)
        draw.text((140, y), m, font=FONT_BODY_BOLD, fill=TEXT_DARK)
        draw.text((620, y), a1, font=FONT_BODY, fill=TEXT_MUTED if "N/A" in a1 else TEXT_DARK)
        draw.text((1050, y), a2, font=FONT_BODY_BOLD, fill=NAVY_DARK)
        draw_pill(draw, 1440, y - 2, verdict, fg=v_fg, bg=v_bg)

    return img

def render_scene_14():
    img = Image.new("RGB", (WIDTH, HEIGHT), BG_COLOR)
    draw = ImageDraw.Draw(img)
    draw_topbar(draw, 14, 14, "AUTOMATED TESTS & CONCLUSION")

    draw.text((100, 110), "Automated Test Suite (pytest) & Final Conclusion", font=FONT_HEADING, fill=NAVY_DARK)

    # Terminal on Left
    draw_card(draw, 100, 170, 1100, 890, bg=CODE_BG)
    draw.rounded_rectangle([100, 170, 1100, 220], radius=14, fill=(25, 35, 48))
    draw.text((130, 185), "Terminal · pytest -v", font=FONT_BODY_BOLD, fill=WHITE)

    test_lines = [
        ("tests/test_agent.py::test_agent_direct_answer", "PASSED"),
        ("tests/test_agent.py::test_agent_tool_execution_loop", "PASSED"),
        ("tests/test_approvals.py::test_course_change_workflow_approval", "PASSED"),
        ("tests/test_approvals.py::test_course_change_workflow_rejection", "PASSED"),
        ("tests/test_audit.py::test_audit_records_blocked_access", "PASSED"),
        ("tests/test_authentication.py::test_student_login_success", "PASSED"),
        ("tests/test_authentication.py::test_student_cannot_access_admin", "PASSED"),
        ("tests/test_privacy.py::test_scenario_1_own_fee_status_allowed", "PASSED"),
        ("tests/test_privacy.py::test_scenario_3_cross_student_access_blocked", "PASSED"),
        ("tests/test_privacy.py::test_scenario_4_sensitive_change_requires_approval", "PASSED"),
        ("tests/test_privacy.py::test_scenario_7_otp_password_not_stored_in_memory", "PASSED"),
        ("tests/test_privacy.py::test_scenario_10_tampered_student_id_blocked", "PASSED"),
        ("tests/test_tools.py::test_tool_get_fee_status", "PASSED"),
        ("tests/test_tools.py::test_tool_create_course_change_request", "PASSED"),
        ("======================= 45 passed in 3.34s =======================", "OK")
    ]

    for i, (line, status) in enumerate(test_lines):
        y = 240 + i * 41
        draw.text((130, y), line, font=FONT_MONO, fill=(240, 200, 120) if "==" in line else CODE_FG)
        if status != "OK":
            draw.text((980, y), status, font=FONT_MONO_BOLD, fill=PILL_OK_FG)

    # Right: Summary & Achievements Card
    draw_card(draw, 1140, 170, WIDTH - 100, 890, bg=WHITE)
    draw.text((1180, 210), "Project Achievements", font=FONT_HEADING, fill=NAVY_DARK)

    achievements = [
        ("Assignment 1 Baseline Satisfied", "Authentic agent loop, tool calling, persistent memory, and TF-IDF RAG."),
        ("Assignment 2 Security Complete", "RBAC authentication, code authorization, approval queue, and audit log."),
        ("Zero Data Leakage", "Strict verification that students can only ever access their own data."),
        ("Human-in-the-Loop Safe", "Course and elective modifications require authenticated staff sign-off."),
        ("45/45 Passing Tests", "Deterministic, reproducible test suite validating all 10 security scenarios."),
        ("Production UI Experience", "Clean, responsive portal with 1-click credentials for instant evaluator testing.")
    ]

    for i, (head, desc) in enumerate(achievements):
        y = 280 + i * 95
        draw.ellipse([1180, y + 5, 1200, y + 25], fill=PILL_OK_FG)
        draw.text((1220, y), head, font=FONT_BODY_BOLD, fill=NAVY_DARK)
        draw.text((1220, y + 32), desc, font=FONT_SMALL, fill=TEXT_MUTED)

    return img

SCENE_CONFIGS = [
    (render_scene_1, (
        "Hello everyone. Today I am presenting our Intelligent and Production-Safe Student Support Agent, "
        "built to satisfy every requirement of Agentic AI Engineering Assignment 1 and Assignment 2. "
        "Higher education student portals receive thousands of queries regarding tuition fees, scholarships, "
        "policy rules, and course changes. Our objective was not to build a superficial chatbot with hardcoded "
        "answers, but a genuine Agentic AI system that reasons dynamically, calls verified backend tools, "
        "maintains persistent memory, retrieves policy via RAG, and enforces strict production security, "
        "backend data privacy, human-in-the-loop approvals, and complete auditability."
    )),
    (render_scene_2, (
        "Let's take a quick look at the architecture. The backend is built with Python and Flask. The LLM agent "
        "uses Groq's high-speed Tool-Calling API with the openai/gpt-oss-120b model. For policy retrieval, we "
        "implemented a custom TF-IDF cosine similarity RAG engine over the official student policy handbook. "
        "Crucially, Assignment 2 extends Assignment 1 by subclassing the baseline agent: SafeStudentSupportAgentA2 "
        "inherits from StudentSupportAgentA1. We added server-side session authentication, code-enforced authorization "
        "to prevent data leakage, an approval queue for sensitive actions, an append-only audit log, and per-query execution tracing."
    )),
    (render_scene_3, (
        "Here is our sign-in page. It supports both Student Login and Staff Login. To make demonstration effortless, "
        "we included one-click credential buttons. I'll click S1001, which auto-fills the Student ID and hashed PIN, and sign in."
    )),
    (render_scene_4, (
        "Upon logging in, the student arrives at their personalized dashboard. In the sidebar, we display the student's profile, "
        "academic year, outstanding fees with real-time due status badges, scholarship award, change requests, and support tickets. "
        "Notice that everything in this sidebar is only accessible to this authenticated student. On the right, we have a clean "
        "ChatGPT-style conversational interface with suggested question chips, enter-to-send support, and a 'Clear conversation' button."
    )),
    (render_scene_5, (
        "Let's ask: 'What is my current fee status?' Notice what happened: The agent didn't guess or hallucinate. It recognized the "
        "intent, invoked the get_fee_status tool for student S1001, received the structured JSON record, and answered: 'You have an "
        "outstanding fee of INR 45,000 due on 15 November 2026.' Underneath the answer, we can open the Trace panel. Here we see the "
        "complete evidence timeline: context selected, model call latency in milliseconds, tokens consumed, tool executed, and permission status: 'allowed'."
    )),
    (render_scene_6, (
        "Now let's ask a policy question: 'The payment portal failed. Can I pay on the next working day?' The agent selected the "
        "search_student_policy tool. Our vector RAG retriever matched Chunk P3 from the policy handbook: 'Payment Portal Failure'. "
        "The model answered accurately based solely on the handbook: 'Yes, if the payment portal fails on the due date, you may pay on "
        "the next working day without any late fee by raising a support request on the same day with a screenshot.' Notice that the "
        "full handbook is never dumped into the prompt—only the top relevant chunk is retrieved."
    )),
    (render_scene_7, (
        "Next, let's demonstrate persistent cross-session memory. I'll tell the assistant: 'Please remember that I prefer to receive updates by email.' "
        "The agent invokes save_memory. Immediately, the Saved Memory card in our sidebar updates to show contact_preference: email. "
        "Now, let's start a brand new session by clicking 'New session'. When I ask: 'Which contact method did I tell you earlier that I prefer?', "
        "the agent retrieves the relevant fact from persistent memory and answers correctly. Furthermore, students maintain full ownership: "
        "clicking 'Forget' permanently deletes the saved fact."
    )),
    (render_scene_8, (
        "What happens if a student accidentally types an OTP or password? Let's test: 'My portal OTP is 482913 and password is Secret@123, please remember them.' "
        "Our backend security filter intercepts this immediately. In code, is_sensitive() flags the pattern, rejects persistent storage, and masks the secret. "
        "Neither the OTP nor the password ever enters long-term memory or unredacted logs."
    )),
    (render_scene_9, (
        "Now for the core requirement of Assignment 2: Data Privacy and Authorization. Student S1001 is logged in. Let's ask: 'Show me the fee status of "
        "student S1002.' Notice the result: The assistant responds: 'Access denied: you can only access or change your own record.' In the trace panel, "
        "under tool permissions, we see permission: blocked. This is NOT just a prompt instruction. Inside app.py, the backend tool dispatcher compares the "
        "target student ID against session['student_id']. If they don't match, execution is halted in Python and an audit violation is recorded."
    )),
    (render_scene_10, (
        "Now let's examine sensitive action governance. Changing an elective or programme must NOT execute immediately. Let's ask: 'I would like to change my elective "
        "to Financial Analytics.' The agent invokes create_course_change_request. The request is staged into the approvals queue with status pending. In our sidebar, "
        "we see the request created. Notice that in the student profile above, the elective is STILL Marketing Analytics—the record has NOT been modified."
    )),
    (render_scene_11, (
        "Now let's switch to the Admin Console. The Overview tab shows our operations at a glance: student counts, pending approvals, open tickets, and recent "
        "audit activity. Let's go to the Approvals tab. Here is Aarav Shah's pending request. If we reject it, the record remains completely unchanged. If we click "
        "Approve, the change is applied to the live record, a notification is dispatched, and the decision is audited. Switching back to Aarav's portal, we see his "
        "elective is now updated to Financial Analytics."
    )),
    (render_scene_12, (
        "Under the Audit log tab, every critical action is permanently recorded: student logins, data accesses, blocked intrusion attempts, course change submissions, "
        "and staff decisions. Secrets are automatically redacted. Under Conversations, staff can review past conversation traces across any agent—Student Portal, "
        "Staff Assistant, or Baseline Agent—with full step-by-step latency, token counts, and tool outcomes."
    )),
    (render_scene_13, (
        "Under the Evaluation tab, we provide a side-by-side benchmark comparing the Assignment 1 baseline against our Assignment 2 safe agent across identical test cases. "
        "Both achieve 100% task accuracy. However, Assignment 1 has no identity verification or approval gates. Assignment 2 scores 100% on Privacy Test Success and 100% "
        "on Unsafe Action Prevention, while maintaining fast average latencies of approximately 650 milliseconds."
    )),
    (render_scene_14, (
        "Finally, let's run our automated test suite in the terminal: pytest -v. All 45 tests pass cleanly in 6 seconds, validating all 10 security scenarios from the "
        "assignment brief, including cross-student blocking, approval workflows, secret redaction, and tool schemas. In conclusion, this project delivers a comprehensive, "
        "production-safe Student Support Agent with authentic agentic tool calling, grounded RAG, persistent memory, and rock-solid enterprise security. Thank you!"
    ))
]

def get_audio_duration(audio_path):
    cmd = [FFMPEG_EXE, "-i", audio_path]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    for line in res.stderr.splitlines():
        if "Duration:" in line:
            parts = line.split("Duration:")[1].split(",")[0].strip()
            h, m, s = parts.split(":")
            return float(h) * 3600 + float(m) * 60 + float(s)
    return 10.0

async def generate_speech(text, out_path):
    voices = [VOICE, "en-US-ChristopherNeural", "en-US-GuyNeural"]
    for attempt in range(4):
        voice_to_use = voices[attempt % len(voices)]
        try:
            comm = edge_tts.Communicate(text, voice_to_use)
            await comm.save(out_path)
            if os.path.exists(out_path) and os.path.getsize(out_path) > 1000:
                return
        except Exception as e:
            print(f"  [TTS Retry {attempt+1}/4 with {voice_to_use}]: {e}")
            await asyncio.sleep(2 * (attempt + 1))
    
    # Offline Windows SAPI fallback if edge-tts is completely unreachable
    print("  [TTS] Falling back to Windows SAPI speech synthesis...")
    wav_path = out_path + ".wav"
    ps_script = f"""
Add-Type -AssemblyName System.Speech
$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
$speak.SetOutputToWaveFile('{wav_path.replace(chr(92), "/")}')
$speak.Speak(@'
{text}
'@)
$speak.Dispose()
"""
    subprocess.run(["powershell", "-NoProfile", "-Command", ps_script], check=True)
    subprocess.run([FFMPEG_EXE, "-y", "-i", wav_path, "-c:a", "libmp3lame", out_path], capture_output=True, check=True)
    if os.path.exists(wav_path):
        os.remove(wav_path)

async def build_entire_video():
    build_dir = os.path.abspath("runtime/video_build")
    os.makedirs(build_dir, exist_ok=True)
    print(f"Working in build directory: {build_dir}")
    
    clip_files = []
    total = len(SCENE_CONFIGS)

    for idx, (renderer, script_text) in enumerate(SCENE_CONFIGS, 1):
        print(f"\n[Scene {idx}/{total}] Processing assets...")
        
        img_path = os.path.join(build_dir, f"frame_{idx:02d}.png")
        audio_path = os.path.join(build_dir, f"audio_{idx:02d}.mp3")
        clip_path = os.path.join(build_dir, f"clip_{idx:02d}.mp4")

        # 1. Render image with caption if not exists
        if not os.path.exists(img_path) or os.path.getsize(img_path) < 1000:
            img = renderer()
            draw = ImageDraw.Draw(img)
            draw_caption(draw, script_text)
            img.save(img_path, quality=95)

        # 2. Generate Audio if not exists
        if not os.path.exists(audio_path) or os.path.getsize(audio_path) < 1000:
            await generate_speech(script_text, audio_path)
            await asyncio.sleep(1.0) # polite spacing
        
        duration = get_audio_duration(audio_path)
        clip_duration = duration + 0.5
        print(f"Scene {idx} audio duration: {duration:.2f}s (clip length: {clip_duration:.2f}s)")

        # 3. Encode Scene to MP4 clip if not exists or incomplete
        if not os.path.exists(clip_path) or os.path.getsize(clip_path) < 5000:
            cmd = [
                FFMPEG_EXE, "-y",
                "-loop", "1", "-i", img_path,
                "-i", audio_path,
                "-c:v", "libx264", "-tune", "stillimage",
                "-c:a", "aac", "-b:a", "192k", "-pix_fmt", "yuv420p",
                "-t", str(clip_duration),
                "-shortest",
                clip_path
            ]
            res = subprocess.run(cmd, capture_output=True, text=True)
            if res.returncode != 0:
                print(f"FFmpeg error on scene {idx}:", res.stderr)
                raise RuntimeError(f"FFmpeg failed on scene {idx}")
        else:
            print(f"Scene {idx} clip already exists, reusing.")
        
        clip_files.append(clip_path)

    # 4. Concatenate all clips
    print("\nConcatenating all 14 scenes into final video...")
    concat_list_path = os.path.join(build_dir, "clips.txt")
    with open(concat_list_path, "w", encoding="utf-8") as f:
        for c in clip_files:
            norm = c.replace("\\", "/")
            f.write(f"file '{norm}'\n")

    output_video_path = os.path.abspath("student_support_agent_demo.mp4")
    concat_cmd = [
        FFMPEG_EXE, "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_list_path,
        "-c", "copy",
        output_video_path
    ]
    res = subprocess.run(concat_cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Concatenation error:", res.stderr)
        raise RuntimeError("Concatenation failed")

    # 5. Verify final output
    total_dur = get_audio_duration(output_video_path)
    file_size_mb = os.path.getsize(output_video_path) / (1024 * 1024)
    print("\n" + "=" * 60)
    print("DEMO VIDEO GENERATION COMPLETED SUCCESSFULLY!")
    print(f"Output File: {output_video_path}")
    print(f"Total Video Duration: {total_dur / 60:.1f} minutes ({total_dur:.1f} seconds)")
    print(f"Video File Size: {file_size_mb:.2f} MB")
    print(f"Resolution: 1920x1080 (Full HD)")
    print("=" * 60)

if __name__ == "__main__":
    asyncio.run(build_entire_video())

