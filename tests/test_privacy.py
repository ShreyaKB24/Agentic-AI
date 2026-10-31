"""
Test Suite for Assignment 2 Security and Privacy Scenarios (Scenarios 1 through 10)
"""
import json

def test_scenario_1_own_fee_status_allowed(a2_agent):
    """Scenario 1: Authenticated student asks for their own fee status. Expected: Allowed."""
    ctx = {"student_id": "S1001", "question": "What is my fee status?", "retrieved_chunks": [], "tool_steps": []}
    result = a2_agent.execute_tool("get_fee_status", {"student_id": "S1001"}, ctx)
    assert ctx.get("permission") == "allowed"
    assert "error" not in result
    assert result["student_id"] == "S1001"
    assert "total_fee" in result
    assert "outstanding" in result

def test_scenario_2_own_scholarship_status_allowed(a2_agent):
    """Scenario 2: Authenticated student asks for their own scholarship status. Expected: Allowed."""
    ctx = {"student_id": "S1001", "question": "What is my scholarship status?", "retrieved_chunks": [], "tool_steps": []}
    result = a2_agent.execute_tool("get_scholarship_status", {"student_id": "S1001"}, ctx)
    assert ctx.get("permission") == "allowed"
    assert "error" not in result
    assert result["student_id"] == "S1001"
    assert "name" in result
    assert "status" in result

def test_scenario_3_cross_student_access_blocked(a2_agent):
    """Scenario 3: Authenticated student attempts to access another student's private data. Expected: Blocked by backend authorization."""
    ctx = {"student_id": "S1001", "question": "Show me the fee status of S1002.", "retrieved_chunks": [], "tool_steps": []}
    result = a2_agent.execute_tool("get_fee_status", {"student_id": "S1002"}, ctx)
    assert ctx.get("permission") == "blocked"
    assert "error" in result
    assert "Access denied" in result["error"]
    # Check that audit recorded this blocked decision
    audit_events = [e for e in a2_agent.audit.all() if e["actor"] == "S1001" and e["target_student"] == "S1002"]
    assert len(audit_events) > 0
    assert audit_events[-1]["decision"] == "blocked"

def test_scenario_4_sensitive_change_requires_approval(a2_agent):
    """Scenario 4: Student requests a sensitive change to their own record. Expected: Approval required. No immediate execution."""
    original_phone = a2_agent.students["S1001"]["phone"]
    ctx = {"student_id": "S1001", "question": "Please update my phone number to 9999988888", "retrieved_chunks": [], "tool_steps": []}
    result = a2_agent.execute_tool("request_record_change", {"student_id": "S1001", "field": "phone", "new_value": "9999988888"}, ctx)
    assert result.get("status") == "pending"
    assert "NOT been applied yet" in result.get("message", "")
    # Record must NOT be modified yet
    assert a2_agent.students["S1001"]["phone"] == original_phone

def test_scenario_5_staff_rejects_change_no_modification(a2_agent):
    """Scenario 5: Staff rejects the request. Expected: No change to the original student record."""
    original_phone = a2_agent.students["S1001"]["phone"]
    ctx = {"student_id": "S1001", "question": "Update phone to 9111122222", "retrieved_chunks": [], "tool_steps": []}
    req = a2_agent.execute_tool("request_record_change", {"student_id": "S1001", "field": "phone", "new_value": "9111122222"}, ctx)
    req_id = req["request_id"]
    
    # Staff rejects
    decided = a2_agent.decide_approval(req_id, approver="admin", approve=False)
    assert decided["status"] == "rejected"
    # Verify student record remains unchanged
    assert a2_agent.students["S1001"]["phone"] == original_phone

def test_scenario_6_staff_approves_change_executed_once(a2_agent):
    """Scenario 6: Staff approves the request. Expected: Change executed exactly once."""
    original_email = a2_agent.students["S1001"]["email"]
    new_email = "aarav.new@example.edu"
    ctx = {"student_id": "S1001", "question": "Change email", "retrieved_chunks": [], "tool_steps": []}
    req = a2_agent.execute_tool("request_record_change", {"student_id": "S1001", "field": "email", "new_value": new_email}, ctx)
    req_id = req["request_id"]

    # Staff approves
    decided = a2_agent.decide_approval(req_id, approver="admin", approve=True)
    assert decided["status"] == "approved"
    assert a2_agent.students["S1001"]["email"] == new_email

    # Attempting to re-decide must raise ValueError
    import pytest
    with pytest.raises(ValueError):
        a2_agent.decide_approval(req_id, approver="admin", approve=True)

def test_scenario_7_otp_password_not_stored_in_memory(a2_agent):
    """Scenario 7: Student supplies an OTP or password in chat. Expected: Sensitive information must not enter persistent memory or traces."""
    ctx = {"student_id": "S1001", "question": "My OTP is 738291 and password is secretPassword123, remember it.", "retrieved_chunks": [], "tool_steps": []}
    result = a2_agent.execute_tool("save_memory", {"key": "login_otp", "value": "738291"}, ctx)
    assert result.get("saved") is False
    assert "Sensitive information" in result.get("reason", "")
    
    # Check that memory for S1001 does not contain the OTP or password
    all_mem = json.dumps(a2_agent.memory.all_items("S1001"))
    assert "738291" not in all_mem
    assert "secretPassword123" not in all_mem

def test_scenario_8_unauthenticated_access_denied(client):
    """Scenario 8: Unauthenticated user attempts to access student or admin endpoints. Expected: Access denied."""
    res_student = client.get("/api/student/profile")
    assert res_student.status_code == 401
    res_admin = client.get("/api/admin/approvals")
    assert res_admin.status_code == 401

def test_scenario_9_student_cannot_access_admin_dashboard(client):
    """Scenario 9: Student attempts to access the admin dashboard. Expected: Access denied."""
    client.post("/api/auth/student-login", json={"student_id": "S1001", "pin": "1111"})
    res_admin_page = client.get("/admin")
    assert res_admin_page.status_code == 302
    res_admin_api = client.get("/api/admin/overview")
    assert res_admin_api.status_code == 401

def test_scenario_10_tampered_student_id_blocked(a2_agent):
    """Scenario 10: Student manipulates a request to change the target student ID. Expected: Backend ownership validation blocks the request."""
    # Student S1001 sends a request spoofing student_id S1002 in arguments
    ctx = {"student_id": "S1001", "question": "Change student details", "retrieved_chunks": [], "tool_steps": []}
    result = a2_agent.execute_tool("create_course_change_request", {"student_id": "S1002", "change_type": "elective", "new_value": "AI Analytics"}, ctx)
    assert ctx.get("permission") == "blocked"
    assert "error" in result
    assert "Access denied" in result["error"]

