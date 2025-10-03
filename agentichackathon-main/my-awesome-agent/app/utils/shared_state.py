# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Shared state management for inter-agent communication."""

from datetime import datetime
from typing import Any

# Shared message queue for agent-to-agent communication
agent_messages: dict[str, list[dict[str, Any]]] = {}

# Shared disaster context
disaster_context: dict[str, Any] = {}

# Agent response storage
agent_responses: dict[str, dict[str, Any]] = {}


def send_message_to_agent(target_agent: str, message: dict[str, Any]) -> None:
    """Send a message to another agent.
    
    Args:
        target_agent: Name of the target agent
        message: Message data to send
    """
    if target_agent not in agent_messages:
        agent_messages[target_agent] = []
    
    message["timestamp"] = datetime.now().isoformat()
    agent_messages[target_agent].append(message)


def get_agent_messages(agent_name: str) -> list[dict[str, Any]]:
    """Retrieve messages for an agent.
    
    Args:
        agent_name: Name of the agent
        
    Returns:
        List of messages for the agent
    """
    return agent_messages.get(agent_name, [])


def clear_agent_messages(agent_name: str) -> None:
    """Clear messages for an agent.
    
    Args:
        agent_name: Name of the agent
    """
    if agent_name in agent_messages:
        agent_messages[agent_name] = []


def set_disaster_context(context: dict[str, Any]) -> None:
    """Set the current disaster context.
    
    Args:
        context: Disaster context data
    """
    global disaster_context
    disaster_context = context


def get_disaster_context() -> dict[str, Any]:
    """Get the current disaster context.
    
    Returns:
        Current disaster context
    """
    return disaster_context


def store_agent_response(agent_name: str, response: dict[str, Any]) -> None:
    """Store an agent's response.
    
    Args:
        agent_name: Name of the agent
        response: Response data
    """
    response["timestamp"] = datetime.now().isoformat()
    agent_responses[agent_name] = response


def get_agent_response(agent_name: str) -> dict[str, Any] | None:
    """Get an agent's response.
    
    Args:
        agent_name: Name of the agent
        
    Returns:
        Agent's response or None if not found
    """
    return agent_responses.get(agent_name)


def get_all_agent_responses() -> dict[str, dict[str, Any]]:
    """Get all agent responses.
    
    Returns:
        Dictionary of all agent responses
    """
    return agent_responses


def reset_shared_state() -> None:
    """Reset all shared state (useful for testing)."""
    global agent_messages, disaster_context, agent_responses
    agent_messages = {}
    disaster_context = {}
    agent_responses = {}

