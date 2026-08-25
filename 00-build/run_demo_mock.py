"""Run a mock happy-path demo without requiring OpenAI credentials.
This injects a fake `openai` module before importing `agent` so the loop
runs with deterministic, minimal responses that exercise the tools flow.
"""
from __future__ import annotations
import sys
import types
import json
from types import SimpleNamespace

# Build a fake openai module with an OpenAI class that simulates chat calls
fake_mod = types.ModuleType("openai")

class FakeMessage:
    def __init__(self, content=None, tool_calls=None, id=None):
        self.content = content
        self.tool_calls = tool_calls or []
        self.id = id

class FakeChoice:
    def __init__(self, message):
        self.message = message

class FakeUsage:
    def __init__(self, prompt_tokens=10, completion_tokens=20):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens

class FakeResp:
    def __init__(self, message, prompt_tokens=10, completion_tokens=20):
        self.choices = [FakeChoice(message)]
        self.usage = FakeUsage(prompt_tokens, completion_tokens)

class FakeOpenAI:
    def __init__(self):
        self.chat = SimpleNamespace()
        # create a stateful counter for call sequencing
        self._seq = 0
        # attach the method
        self.chat.completions = SimpleNamespace()
        self.chat.completions.create = self._create

    def _create(self, *args, **kwargs):
        # Sequence:
        # 1) drafter asks -> return tool_calls to drive get_project/get_activity
        # 2) drafter next -> return a proposed draft (no tool_calls)
        # 3) critic -> return a JSON verdict (response_format present)
        self._seq += 1
        seq = self._seq
        if kwargs.get("response_format"):
            # critic call: return a pass verdict
            msg = FakeMessage(content=json.dumps({"verdict": "pass", "reasons": []}))
            return FakeResp(msg, prompt_tokens=5, completion_tokens=5)

        if seq == 1:
            # First drafter call: ask for project and activity
            tc1 = SimpleNamespace(function=SimpleNamespace(name="get_project", arguments=json.dumps({"project_id": "P-NORTH"})), id="call-1")
            tc2 = SimpleNamespace(function=SimpleNamespace(name="get_activity", arguments=json.dumps({"project_id": "P-NORTH"})), id="call-2")
            msg = FakeMessage(content=None, tool_calls=[tc1, tc2], id="m1")
            return FakeResp(msg, prompt_tokens=30, completion_tokens=0)

        # seq >=2: drafter produces a proposed output
        proposed = (
            "Weekly status update draft:\n\n- Project P-NORTH: core work on schedule.\n- No Sev-1s open.\n- Proposed stories queued for review.\n"
        )
        msg = FakeMessage(content=proposed)
        return FakeResp(msg, prompt_tokens=40, completion_tokens=120)

# Inject fake module before importing agent
sys.modules["openai"] = fake_mod
setattr(fake_mod, "OpenAI", FakeOpenAI)

# Now import and run the agent with the 'happy' fixture
import importlib
agent = importlib.import_module("agent")

if __name__ == "__main__":
    agent.run("happy")
