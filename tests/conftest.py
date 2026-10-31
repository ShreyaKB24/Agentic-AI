import os
import shutil
import tempfile
import pytest

from app import (
    app,
    PolicyRetriever,
    POLICY_FILE,
    StudentSupportAgentA1,
    SafeStudentSupportAgentA2,
    StaffAssistantA2,
)

class MockLLMResponse:
    def __init__(self, content="", tool_calls=None):
        self.content = content
        self.tool_calls = tool_calls or []

class MockToolCall:
    def __init__(self, name, arguments, call_id="call_mock_1"):
        self.id = call_id
        class Func:
            def __init__(self, n, a):
                self.name = n
                self.arguments = a
        self.function = Func(name, arguments)

class MockLLM:
    def __init__(self, model="mock-model"):
        self.model = model
        self.responses = []

    def queue_response(self, content="", tool_calls=None):
        self.responses.append((MockLLMResponse(content, tool_calls), {"input_tokens": 50, "output_tokens": 25}))

    def chat(self, messages, tools):
        if self.responses:
            return self.responses.pop(0)
        return MockLLMResponse(content="Mock response from assistant.", tool_calls=[]), {"input_tokens": 40, "output_tokens": 20}

@pytest.fixture
def mock_llm():
    return MockLLM()

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret-key-12345"
    with app.test_client() as client:
        yield client

@pytest.fixture
def temp_runtime():
    temp_dir = tempfile.mkdtemp(prefix="agent_test_runtime_")
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)

@pytest.fixture
def retriever():
    return PolicyRetriever(POLICY_FILE)

@pytest.fixture
def a1_agent(mock_llm, retriever, temp_runtime):
    return StudentSupportAgentA1(mock_llm, retriever, os.path.join(temp_runtime, "a1"))

@pytest.fixture
def a2_agent(mock_llm, retriever, temp_runtime):
    return SafeStudentSupportAgentA2(mock_llm, retriever, os.path.join(temp_runtime, "a2"))

@pytest.fixture
def staff_agent(mock_llm, retriever, a2_agent):
    return StaffAssistantA2(mock_llm, retriever, a2_agent)

