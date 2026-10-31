"""
Tests for Core Agent Tools (Assignment 1 & Assignment 2)
"""
import pytest

def test_tool_get_student_profile(a1_agent):
    ctx = {"student_id": "S1001", "question": "Who am I?"}
    profile = a1_agent.execute_tool("get_student_profile", {"student_id": "S1001"}, ctx)
    assert profile["student_id"] == "S1001"
    assert profile["name"] == "Aarav Shah"
    assert "programme" in profile
    assert "academic_year" in profile
    assert "email" in profile

def test_tool_get_fee_status(a1_agent):
    ctx = {"student_id": "S1001", "question": "Fee status?"}
    fee = a1_agent.execute_tool("get_fee_status", {"student_id": "S1001"}, ctx)
    assert fee["student_id"] == "S1001"
    assert fee["total_fee"] == 250000
    assert fee["outstanding"] == 45000
    assert fee["status"] == "Partially Paid"

def test_tool_get_scholarship_status(a1_agent):
    ctx = {"student_id": "S1001", "question": "Scholarship status?"}
    sch = a1_agent.execute_tool("get_scholarship_status", {"student_id": "S1001"}, ctx)
    assert sch["student_id"] == "S1001"
    assert sch["name"] == "Merit Scholarship"
    assert sch["status"] == "Approved"

def test_tool_search_policy(a1_agent):
    ctx = {"student_id": "S1001", "question": "Late fee rules?", "retrieved_chunks": []}
    res = a1_agent.execute_tool("search_policy", {"query": "late fee per day"}, ctx)
    assert "results" in res
    assert len(res["results"]) > 0
    # Must retrieve relevant chunk mentioning late fee
    texts = " ".join(r["text"] for r in res["results"])
    assert "500" in texts

def test_tool_search_student_policy_alias(a1_agent):
    ctx = {"student_id": "S1001", "question": "Admission documents?", "retrieved_chunks": []}
    res = a1_agent.execute_tool("search_student_policy", {"query": "admission documents required"}, ctx)
    assert "results" in res
    assert len(res["results"]) > 0
    texts = " ".join(r["text"] for r in res["results"]).lower()
    assert "admission" in texts or "documents" in texts or "marksheets" in texts

def test_tool_create_support_ticket(a1_agent):
    ctx = {"student_id": "S1001", "question": "Need ID card"}
    ticket = a1_agent.execute_tool("create_support_ticket", {
        "student_id": "S1001",
        "category": "id_card",
        "description": "Lost my student ID card on campus"
    }, ctx)
    assert "ticket_id" in ticket
    assert ticket["ticket_id"].startswith("TCK-")
    assert ticket["category"] == "id_card"
    assert ticket["status"] == "Open"

def test_tool_create_course_change_request(a2_agent):
    ctx = {"student_id": "S1001", "question": "Change elective"}
    req = a2_agent.execute_tool("create_course_change_request", {
        "student_id": "S1001",
        "change_type": "elective",
        "new_value": "Deep Learning & AI"
    }, ctx)
    assert req["request_id"].startswith("APR-")
    assert req["status"] == "pending"
    assert req["approval_required"] is True

def test_tool_invalid_arguments_handling(a1_agent):
    ctx = {"student_id": "S1001", "question": "invalid"}
    # Missing required argument
    res = a1_agent.execute_tool("get_fee_status", {}, ctx)
    assert "error" in res

def test_tool_unknown_student_handling(a1_agent):
    ctx = {"student_id": "S9999", "question": "Fee"}
    res = a1_agent.execute_tool("get_fee_status", {"student_id": "S9999"}, ctx)
    assert "error" in res
    assert "not found" in res["error"].lower()

