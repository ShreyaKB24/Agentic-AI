"""
Tests for Evaluation & Benchmarking System (Section 9)
"""
from app import load_test_cases, check_case, summarise_runs

def test_load_test_cases():
    suite_a1 = load_test_cases("a1")
    assert "cases" in suite_a1
    assert len(suite_a1["cases"]) >= 8

    suite_a2 = load_test_cases("a2")
    assert "cases" in suite_a2
    assert len(suite_a2["cases"]) >= 6

def test_check_case_success():
    case = {
        "id": "T-1",
        "expect_tools": ["get_fee_status"],
        "answer_any": ["45,000", "45000"],
    }
    mock_trace = {
        "tool_calls": [{"tool": "get_fee_status"}],
        "answer": "Your outstanding balance is INR 45,000.",
        "error": None
    }
    tool_ok, success = check_case(case, mock_trace, "")
    assert tool_ok is True
    assert success is True

def test_check_case_tool_mismatch():
    case = {
        "id": "T-2",
        "expect_tools": ["search_policy"],
        "answer_any": ["policy"],
    }
    mock_trace = {
        "tool_calls": [{"tool": "get_fee_status"}],
        "answer": "Here is policy",
        "error": None
    }
    tool_ok, success = check_case(case, mock_trace, "")
    assert tool_ok is False
    assert success is False

def test_summarise_runs():
    rows = [
        {"success": True, "latency_ms": 500, "input_tokens": 100, "output_tokens": 50},
        {"success": False, "latency_ms": 700, "input_tokens": 120, "output_tokens": 60},
    ]
    summary = summarise_runs(rows)
    assert summary["runs"] == 2
    assert summary["accuracy"] == 0.5
    assert summary["avg_latency_ms"] == 600
    assert summary["avg_input_tokens"] == 110
    assert summary["avg_output_tokens"] == 55

