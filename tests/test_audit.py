"""
Tests for Audit Logging & Redaction (Section 6.4)
"""
import json
from app import redact, is_sensitive

def test_audit_records_login(a2_agent):
    a2_agent.verify_login("S1001", "1111")
    logs = [e for e in a2_agent.audit.all() if e["action"] == "login"]
    assert len(logs) > 0
    assert logs[-1]["target_student"] == "S1001"
    assert logs[-1]["decision"] == "allowed"

def test_audit_records_failed_login(a2_agent):
    a2_agent.verify_login("S1001", "wrong_pin")
    logs = [e for e in a2_agent.audit.all() if e["action"] == "login"]
    assert len(logs) > 0
    assert logs[-1]["decision"] == "blocked"

def test_audit_records_blocked_access(a2_agent):
    ctx = {"student_id": "S1001", "question": "Peek at S1002"}
    a2_agent.execute_tool("get_fee_status", {"student_id": "S1002"}, ctx)
    logs = [e for e in a2_agent.audit.all() if e["decision"] == "blocked"]
    assert any(e["actor"] == "S1001" and e["target_student"] == "S1002" for e in logs)

def test_audit_records_approvals(a2_agent):
    ctx = {"student_id": "S1001", "question": "Change email"}
    req = a2_agent.execute_tool("request_record_change", {"student_id": "S1001", "field": "email", "new_value": "new@edu.com"}, ctx)
    a2_agent.decide_approval(req["request_id"], approver="admin", approve=True)

    dec_logs = [e for e in a2_agent.audit.all() if e["action"] == "approval_decision"]
    assert len(dec_logs) > 0
    assert dec_logs[-1]["actor"] == "admin"
    assert dec_logs[-1]["decision"] == "approved"

def test_redaction_secrets():
    text_with_otp = "My OTP is 928374 please verify"
    assert is_sensitive(text_with_otp)
    redacted = redact(text_with_otp)
    assert "928374" not in redacted
    assert "[REDACTED]" in redacted

def test_redaction_password():
    text_with_pwd = "my password is Secret@123"
    assert is_sensitive(text_with_pwd)
    redacted = redact(text_with_pwd)
    assert "Secret@123" not in redacted
    assert "[REDACTED]" in redacted

