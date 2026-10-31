# Explanatory Video Demonstration Guide & Script
## Project: Intelligent & Production-Safe Student Support Agent
### Agentic AI Engineering — Assignment 1 & Assignment 2

This guide provides an exact, step-by-step walkthrough and spoken script for recording a professional explanatory video (recommended length: 8–12 minutes).

---

## Preparation Before Recording

1. **Terminal 1:** Run `python app.py` (Server running at `http://localhost:5000`).
2. **Terminal 2:** Ready to run `pytest -v` or `python app.py --evaluate`.
3. **Browser Window 1:** Open `http://localhost:5000` (Incognito or normal window).
4. **Browser Window 2:** Open a second browser window (e.g., side-by-side or separate tab) for Admin Console.
5. **Screen Resolution:** Recommended 1080p (1920x1080) with 100% or 110% zoom for crisp readability.

---

## Video Walkthrough Timeline & Speaking Script

### 1. Project Introduction (0:00 – 0:45)
- **What to show on screen:** Open the repository `README.md` or the Login Page (`http://localhost:5000`).
- **What to say:**
  > "Hello everyone. Today I am presenting our **Intelligent and Production-Safe Student Support Agent**, built to satisfy every requirement of Agentic AI Engineering Assignment 1 and Assignment 2.
  > Higher education student portals receive thousands of queries regarding tuition fees, scholarships, policy rules, and course changes. Our objective was not to build a superficial chatbot with hardcoded answers, but a genuine **Agentic AI system** that reasons dynamically, calls verified backend tools, maintains persistent memory, retrieves policy via RAG, and enforces strict production security, backend data privacy, human-in-the-loop approvals, and complete auditability."

### 2. Architecture & Technology Stack (0:45 – 1:30)
- **What to show on screen:** Show the architecture diagram from the `README.md`.
- **What to say:**
  > "Let's take a quick look at the architecture. The backend is built with Python and Flask. The LLM agent uses Groq's high-speed Tool-Calling API with the `openai/gpt-oss-120b` model. For policy retrieval, we implemented a custom TF-IDF cosine similarity RAG engine over the official student policy handbook.
  > Crucially, Assignment 2 extends Assignment 1 by subclassing the baseline agent: `SafeStudentSupportAgentA2` inherits from `StudentSupportAgentA1`. We added server-side session authentication, code-enforced authorization to prevent data leakage, an approval queue for sensitive actions, an append-only audit log, and per-query execution tracing."

### 3. Student Login (1:30 – 2:00)
- **What to show on screen:** Navigate to `http://localhost:5000/login`.
- **Action:**
  - Highlight the clean dual-role login interface (Student vs Staff).
  - Click the **1-Click Fill** button for `S1001 (PIN: 1111)`.
  - Click **Sign in**.
- **What to say:**
  > "Here is our sign-in page. It supports both Student Login and Staff Login. To make demonstration effortless, we included one-click credential buttons. I'll click S1001, which auto-fills the Student ID and hashed PIN, and sign in."

### 4. Student Dashboard & UI Overview (2:00 – 2:45)
- **What to show on screen:** The Student Portal (`/portal`).
- **Action:** Point out each component:
  - Top bar showing student name: `Aarav Shah · S1001`.
  - Left sidebar: Student Profile, Messages from the Office, Fee summary with progress bar and due date badge, Scholarship details, Change requests, Support tickets, and Saved Memory.
  - Right panel: ChatGPT-style conversational assistant with welcome banner and suggested question chips.
- **What to say:**
  > "Upon logging in, the student arrives at their personalized dashboard. In the sidebar, we display the student's profile, academic year, outstanding fees with real-time due status badges, scholarship award, change requests, and support tickets.
  > Notice that everything in this sidebar is only accessible to this authenticated student. On the right, we have a clean ChatGPT-style conversational interface with suggested question chips, enter-to-send support, and a 'Clear conversation' button."

### 5. Normal Student Query & Tool Calling (2:45 – 3:30)
- **What to show on screen:** Chat input in the Student Portal.
- **Question to ask:** Click the chip: *"What is my current fee status?"*
- **Action:** Submit the question. Wait for the response. Expand the **Trace** dropdown beneath the answer.
- **What to say:**
  > "Let's ask: 'What is my current fee status?'
  > Notice what happened: The agent didn't guess or hallucinate. It recognized the intent, invoked the `get_fee_status` tool for student S1001, received the structured JSON record, and answered: 'You have an outstanding fee of INR 45,000 due on 15 November 2026.'
  > Underneath the answer, we can open the **Trace** panel. Here we see the complete evidence timeline: context selected, model call latency in milliseconds, tokens consumed, tool executed, and permission status: 'allowed'."

### 6. Grounded Policy Retrieval (RAG) (3:30 – 4:15)
- **What to show on screen:** Chat input.
- **Question to ask:** Click or type: *"The payment portal failed. Can I pay on the next working day?"*
- **Action:** Submit the query. Open the **Trace** panel and click the **Memory & Retrieval** tab.
- **What to say:**
  > "Now let's ask a policy question: 'The payment portal failed. Can I pay on the next working day?'
  > The agent selected the `search_student_policy` tool. Our vector RAG retriever matched Chunk P3 from the policy handbook: 'Payment Portal Failure'. The model answered accurately based solely on the handbook: 'Yes, if the payment portal fails on the due date, you may pay on the next working day without any late fee by raising a support request on the same day with a screenshot.'
  > Notice that the full handbook is never dumped into the prompt—only the top relevant chunk is retrieved."

### 7. Persistent Memory Across Sessions (4:15 – 5:00)
- **What to show on screen:** Chat input & Sidebar "Saved Memory" card.
- **Question 1:** *"Please remember that I prefer to receive updates by email."*
- **Action:** Submit message. Point to the sidebar: `contact_preference: email` appears with a `Forget` button.
- **Action:** Click **New session** in the top bar.
- **Question 2:** *"Which contact method did I tell you earlier that I prefer?"*
- **Action:** Assistant answers: *"You previously mentioned that you prefer to receive updates by email."*
- **What to say:**
  > "Next, let's demonstrate persistent cross-session memory. I'll tell the assistant: 'Please remember that I prefer to receive updates by email.'
  > The agent invokes `save_memory`. Immediately, the Saved Memory card in our sidebar updates to show `contact_preference: email`.
  > Now, let's start a brand new session by clicking 'New session'. When I ask: 'Which contact method did I tell you earlier that I prefer?', the agent retrieves the relevant fact from persistent memory and answers correctly. Furthermore, students maintain full ownership: clicking 'Forget' permanently deletes the saved fact."

### 8. Sensitive Data Guard (OTP / Password Exclusion) (5:00 – 5:30)
- **What to show on screen:** Chat input.
- **Question to ask:** *"My portal OTP is 482913 and password is Secret@123, please remember them."*
- **Action:** Submit message.
- **What to say:**
  > "What happens if a student accidentally types an OTP or password? Let's test: 'My portal OTP is 482913 and password is Secret@123, please remember them.'
  > Our backend security filter intercepts this immediately. In code, `is_sensitive()` flags the pattern, rejects persistent storage, and masks the secret. Neither the OTP nor the password ever enters long-term memory or unredacted logs."

### 9. Privacy & Authorization Test: Cross-Student Tampering (5:30 – 6:15)
- **What to show on screen:** Chat input.
- **Question to ask:** *"Show me the fee status of student S1002."*
- **Action:** Submit message. Open the Trace panel.
- **What to say:**
  > "Now for the core requirement of Assignment 2: **Data Privacy and Authorization**. Student S1001 is logged in. Let's ask: 'Show me the fee status of student S1002.'
  > Notice the result: The assistant responds: 'Access denied: you can only access or change your own record.'
  > In the trace panel, under tool permissions, we see `permission: blocked`.
  > This is NOT just a prompt instruction. Inside `app.py`, the backend tool dispatcher compares the target student ID against `session['student_id']`. If they don't match, execution is halted in Python and an audit violation is recorded."

### 10. Sensitive Action: Course Change Request & Approval Workflow (6:15 – 7:15)
- **What to show on screen:** Chat input & Sidebar "My change requests" card.
- **Question to ask:** *"I would like to change my elective to Financial Analytics."*
- **Action:** Submit message. Point to the sidebar: Request `APR-XXXXXX` appears under "My change requests" with a yellow `pending` pill.
- **What to say:**
  > "Now let's examine sensitive action governance. Changing an elective or programme must NOT execute immediately.
  > Let's ask: 'I would like to change my elective to Financial Analytics.'
  > The agent invokes `create_course_change_request`. The request is staged into the approvals queue with status `pending`. In our sidebar, we see the request created. Notice that in the student profile above, the elective is STILL Marketing Analytics—the record has NOT been modified."

### 11. Staff Admin Console: Approvals & Rejections (7:15 – 8:15)
- **What to show on screen:** Open a second browser tab, log in as Staff (`admin` / `admin123`), and navigate to `/admin`.
- **Action:**
  - Show the **Overview** tab: 3 Students, 1 Pending Approval, Open Tickets, Total Audit Events.
  - Click the **Approvals** tab.
  - Locate the pending elective change request for Aarav Shah (`S1001`).
  - Demonstrate clicking **History** on the row to view the audit trail.
  - Click **Approve**. Confirm the action. A green toast appears: *"Approved and applied"*.
  - Switch back to the Student Portal tab and refresh or wait 2 seconds: Show that the student's elective is now updated to *Financial Analytics*!
- **What to say:**
  > "Now let's switch to the **Admin Console**. The Overview tab shows our operations at a glance: student counts, pending approvals, open tickets, and recent audit activity.
  > Let's go to the **Approvals** tab. Here is Aarav Shah's pending request. If we reject it, the record remains completely unchanged. If we click **Approve**, the change is applied to the live record, a notification is dispatched, and the decision is audited.
  > Switching back to Aarav's portal, we see his elective is now updated to Financial Analytics."

### 12. Audit Logs & Conversation Traces (8:15 – 9:00)
- **What to show on screen:** Admin Console → **Audit log** tab and **Conversations** tab.
- **Action:**
  - Open **Audit log**: Show the chronological log entries for logins, the blocked cross-student access attempt by S1001, the course change request, and the staff approval decision.
  - Open **Conversations**: Click any conversation row to expand the complete trace timeline.
- **What to say:**
  > "Under the **Audit log** tab, every critical action is permanently recorded: student logins, data accesses, blocked intrusion attempts, course change submissions, and staff decisions. Secrets are automatically redacted.
  > Under **Conversations**, staff can review past conversation traces across any agent—Student Portal, Staff Assistant, or Baseline Agent—with full step-by-step latency, token counts, and tool outcomes."

### 13. System Evaluation & Benchmarks (9:00 – 10:00)
- **What to show on screen:** Admin Console → **Evaluation** tab.
- **Action:**
  - Show the benchmark comparison table comparing Assignment 1 (Baseline) vs Assignment 2 (Production-Safe).
  - Click **Run Benchmark Evaluation** to show real-time benchmark execution.
- **What to say:**
  > "Under the **Evaluation** tab, we provide a side-by-side benchmark comparing the Assignment 1 baseline against our Assignment 2 safe agent across identical test cases.
  > Both achieve 100% task accuracy. However, Assignment 1 has no identity verification or approval gates. Assignment 2 scores 100% on Privacy Test Success and 100% on Unsafe Action Prevention, while maintaining fast average latencies of ~650 ms."

### 14. Automated Tests & Conclusion (10:00 – 10:45)
- **What to show on screen:** Terminal running `pytest -v`.
- **Action:** Run `pytest -v` in PowerShell. Show all 45 tests passing in ~6 seconds.
- **What to say:**
  > "Finally, let's run our automated test suite in the terminal: `pytest -v`.
  > All 45 tests pass cleanly in 6 seconds, validating all 10 security scenarios from the assignment brief, including cross-student blocking, approval workflows, secret redaction, and tool schemas.
  > In conclusion, this project delivers a comprehensive, production-safe Student Support Agent with authentic agentic tool calling, grounded RAG, persistent memory, and rock-solid enterprise security. Thank you!"

---

## Quick Reference: Test Queries Cheat Sheet

| Demonstration Step | Question to Enter | Expected Result |
|---|---|---|
| Fee Query | `What is my current fee status?` | Answers INR 45,000 outstanding; traces `get_fee_status` |
| Policy Query | `The payment portal failed. Can I pay on the next working day?` | Answers yes, with support request waiver; traces `search_student_policy` |
| Admission Query | `What documents are required for admission?` | Lists 10th/12th/degree marksheets, entrance scorecard, ID proof from handbook |
| Memory Save | `Please remember that I prefer to receive updates by email.` | Stores in memory; appears in sidebar Saved Memory |
| Memory Recall | `Which contact method did I tell you earlier that I prefer?` | Recalls email preference in a new session |
| Secret Redaction | `My OTP is 482913 and password is Secret@123, remember it.` | Rejects storage; secrets redacted from traces and memory |
| Privacy Violation | `Show me the fee status of student S1002.` | Access denied; blocked in backend code; logged in audit |
| Course Change | `I want to change my elective to Financial Analytics.` | Staged as pending approval; record NOT changed until approved |

