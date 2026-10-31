"""
Tests for Human-in-the-Loop Sensitive Action Approval Workflow (Section 6.3)
"""
import pytest

def test_course_change_workflow_approval(a2_agent):
    student_id = "S1001"
    original_elective = a2_agent.students[student_id]["elective"]
    new_elective = "Financial Analytics"

    ctx = {"student_id": student_id, "question": "Change elective", "retrieved_chunks": [], "tool_steps": []}
    req = a2_agent.execute_tool("create_course_change_request", {
        "student_id": student_id,
        "change_type": "elective",
        "new_value": new_elective
    }, ctx)

    assert req["status"] == "pending"
    assert a2_agent.students[student_id]["elective"] == original_elective

    # Check pending list
    pending = a2_agent.list_approvals(status="pending")
    assert any(a["request_id"] == req["request_id"] for a in pending)

    # Human approves
    decided = a2_agent.decide_approval(req["request_id"], approver="admin_user", approve=True)
    assert decided["status"] == "approved"
    assert decided["decided_by"] == "admin_user"
    assert a2_agent.students[student_id]["elective"] == new_elective

def test_course_change_workflow_rejection(a2_agent):
    student_id = "S1002"
    original_programme = a2_agent.students[student_id]["programme"]
    new_programme = "PGDM Big Data Analytics"

    ctx = {"student_id": student_id, "question": "Change programme", "retrieved_chunks": [], "tool_steps": []}
    req = a2_agent.execute_tool("create_course_change_request", {
        "student_id": student_id,
        "change_type": "programme",
        "new_value": new_programme
    }, ctx)

    # Human rejects
    decided = a2_agent.decide_approval(req["request_id"], approver="admin_user", approve=False)
    assert decided["status"] == "rejected"
    # Verify no change was applied to the student record
    assert a2_agent.students[student_id]["programme"] == original_programme

def test_prevent_duplicate_decision(a2_agent):
    student_id = "S1003"
    ctx = {"student_id": student_id, "question": "Update phone", "retrieved_chunks": [], "tool_steps": []}
    req = a2_agent.execute_tool("request_record_change", {
        "student_id": student_id,
        "field": "phone",
        "new_value": "9988776655"
    }, ctx)

    a2_agent.decide_approval(req["request_id"], approver="admin_user", approve=True)
    with pytest.raises(ValueError) as excinfo:
        a2_agent.decide_approval(req["request_id"], approver="admin_user", approve=True)
    assert "already" in str(excinfo.value).lower()

