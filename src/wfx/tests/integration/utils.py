"""Shared utilities for wfx integration tests."""

import importlib.util
import json
import os
from pathlib import Path

import pytest


def has_integration_deps() -> bool:
    """Check if integration dependencies are installed."""
    required_modules = ["langchain_openai", "langchain_community", "bs4", "lxml"]
    return all(importlib.util.find_spec(module) is not None for module in required_modules)


def get_starter_projects_path() -> Path:
    """Get path to starter projects directory."""
    test_file_path = Path(__file__).resolve()
    current = test_file_path.parent
    while current != current.parent:
        starter_path = current / "src" / "backend" / "base" / "primeagent" / "initial_setup" / "starter_projects"
        if starter_path.exists():
            return starter_path
        current = current.parent
    return Path()


def get_simple_agent_flow_path() -> Path:
    """Get path to Simple Agent starter project."""
    return get_starter_projects_path() / "Simple Agent.json"


def has_openai_api_key() -> bool:
    """Check if OPENAI_API_KEY is set."""
    key = os.getenv("OPENAI_API_KEY", "")
    return bool(key) and key != "dummy" and len(key) > 10


def parse_json_from_output(output: str, context: str = "output") -> dict:
    """Parse JSON from command output, searching in reverse if direct parsing fails."""
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        lines = output.split("\n")
        for line in reversed(lines):
            try:
                return json.loads(line)
            except json.JSONDecodeError:
                continue
        pytest.fail(f"No valid JSON in {context}: {output}")
