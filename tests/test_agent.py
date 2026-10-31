"""
Tests for Agent Architecture, Context Selection & Tracing (Section 5.1, 5.5, 8)
"""
import json
from tests.conftest import MockToolCall

def test_agent_direct_answer(a1_agent, mock_llm):
    mock_llm.queue_response(content="Hello! I am your student support agent.", tool_calls=[])
    trace = a1_agent.run("S1001", "session_1", "Hello")
    assert trace["answer"] == "Hello! I am your student support agent."
    assert trace["finish_reason"] == "final_answer"
    assert trace["model_calls"] == 1
    assert "steps" in trace

def test_agent_tool_execution_loop(a1_agent, mock_llm):
    # Model first calls get_fee_status, then provides final answer based on result
    mock_llm.queue_response(content="", tool_calls=[
        MockToolCall("get_fee_status", json.dumps({"student_id": "S1001"}))
    ])
    mock_llm.queue_response(content="Your outstanding fee is INR 45,000.", tool_calls=[])

    trace = a1_agent.run("S1001", "session_1", "What is my fee status?")
    assert "45,000" in trace["answer"]
    assert trace["model_calls"] == 2
    assert len(trace["tool_calls"]) == 1
    assert trace["tool_calls"][0]["tool"] == "get_fee_status"
    assert trace["tool_calls"][0]["ok"] is True

def test_persistent_memory_across_sessions(a1_agent):
    # Session 1: Save preference
    ctx = {"student_id": "S1001", "question": "I prefer SMS notifications"}
    a1_agent.execute_tool("save_memory", {"key": "notification_channel", "value": "SMS"}, ctx)

    # Session 2: Recall preference
    relevant = a1_agent.memory.select_relevant("S1001", "What was my notification channel preference?")
    assert any(m["key"] == "notification_channel" and m["value"] == "SMS" for m in relevant)

    # Student deletes preference
    deleted = a1_agent.memory.delete("S1001", "notification_channel")
    assert deleted is True
    assert len(a1_agent.memory.all_items("S1001")) == 0

def test_trace_contains_full_evidence(a2_agent, mock_llm):
    mock_llm.queue_response(content="", tool_calls=[
        MockToolCall("get_scholarship_status", json.dumps({"student_id": "S1001"}))
    ])
    mock_llm.queue_response(content="Your scholarship is Approved.", tool_calls=[])

    trace = a2_agent.run("S1001", "session_trace_test", "Scholarship status?")
    assert "trace_id" in trace
    assert trace["student_id"] == "S1001"
    assert "latency_ms" in trace
    assert "input_tokens" in trace
    assert "output_tokens" in trace
    assert "tool_calls" in trace
    assert trace["tool_calls"][0]["permission"] == "allowed"

