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

"""Human-in-the-loop approval tools."""

from datetime import datetime
from typing import Any


def format_approval_request(
    disaster_summary: dict[str, Any],
    agent_responses: dict[str, dict[str, Any]],
    recommended_actions: list[str],
    estimated_cost: int
) -> dict[str, Any]:
    """Format data for human approval request.
    
    Args:
        disaster_summary: Summary of the disaster
        agent_responses: Responses from all specialist agents
        recommended_actions: List of recommended actions
        estimated_cost: Total estimated cost in dollars
        
    Returns:
        Formatted approval request
    """
    approval_id = f"FIRE-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
    
    return {
        "approval_id": approval_id,
        "timestamp": datetime.now().isoformat(),
        "disaster_summary": disaster_summary,
        "agent_recommendations": agent_responses,
        "recommended_actions": recommended_actions,
        "estimated_total_cost": estimated_cost,
        "cost_breakdown": _calculate_cost_breakdown(agent_responses),
        "approval_options": [
            {
                "option": "APPROVE_FULL",
                "description": "Execute all recommended actions immediately",
                "action": "approve"
            },
            {
                "option": "APPROVE_PARTIAL",
                "description": "Select specific actions to approve",
                "action": "partial"
            },
            {
                "option": "DENY",
                "description": "Reject plan and request alternatives",
                "action": "deny"
            }
        ],
        "timeout_minutes": 15,
        "escalation_to": "Emergency Operations Center Director",
        "urgency": "HIGH" if disaster_summary.get("severity") == "EXTREME" else "MODERATE"
    }


def _calculate_cost_breakdown(agent_responses: dict[str, dict[str, Any]]) -> dict[str, int]:
    """Calculate cost breakdown from agent responses.
    
    Args:
        agent_responses: Agent responses containing cost information
        
    Returns:
        Cost breakdown by department
    """
    breakdown = {}
    
    # Extract costs from each agent's response
    if "police" in agent_responses:
        police_data = agent_responses["police"]
        if "mutual_aid" in police_data:
            breakdown["police_mutual_aid"] = police_data["mutual_aid"].get("estimated_cost", 0)
    
    if "fire" in agent_responses:
        fire_data = agent_responses["fire"]
        if "mutual_aid" in fire_data:
            breakdown["fire_mutual_aid"] = fire_data["mutual_aid"].get("estimated_cost", 0)
    
    if "hospital" in agent_responses:
        # Hospital costs typically covered by healthcare system
        breakdown["medical_coordination"] = 5000
    
    return breakdown


def request_human_approval(approval_data: dict[str, Any]) -> str:
    """Request human approval for the disaster response plan.
    
    This function formats the approval request for display to the human operator.
    In a real system, this would trigger a UI notification or webhook.
    
    Args:
        approval_data: Formatted approval request data
        
    Returns:
        String representation of the approval request
    """
    summary = approval_data["disaster_summary"]
    cost = approval_data["estimated_total_cost"]
    actions = approval_data["recommended_actions"]
    
    approval_text = f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                     🚨 HUMAN APPROVAL REQUIRED 🚨                            ║
╚══════════════════════════════════════════════════════════════════════════════╝

APPROVAL ID: {approval_data['approval_id']}
TIMESTAMP: {approval_data['timestamp']}
URGENCY: {approval_data['urgency']}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

DISASTER SUMMARY:
  • Type: {summary.get('type', 'UNKNOWN')}
  • Severity: {summary.get('severity', 'UNKNOWN')}
  • Location: {summary.get('location', 'UNKNOWN')}
  • Affected Population: {summary.get('affected_population', 'UNKNOWN'):,}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RECOMMENDED ACTIONS:
"""
    
    for i, action in enumerate(actions, 1):
        approval_text += f"  {i}. {action}\n"
    
    approval_text += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ESTIMATED TOTAL COST: ${cost:,}

COST BREAKDOWN:
"""
    
    for dept, cost_value in approval_data["cost_breakdown"].items():
        approval_text += f"  • {dept.replace('_', ' ').title()}: ${cost_value:,}\n"
    
    approval_text += f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

APPROVAL OPTIONS:
  [1] APPROVE FULL - Execute all actions immediately
  [2] APPROVE PARTIAL - Select specific actions
  [3] DENY - Request alternative plan

TIMEOUT: {approval_data['timeout_minutes']} minutes
ESCALATION: {approval_data['escalation_to']}

╚══════════════════════════════════════════════════════════════════════════════╝

⏳ Awaiting human decision...
"""
    
    return approval_text


def simulate_human_approval(approval_data: dict[str, Any], auto_approve: bool = True) -> dict[str, Any]:
    """Simulate human approval decision (for testing/demo purposes).
    
    Args:
        approval_data: The approval request data
        auto_approve: Whether to automatically approve (default: True)
        
    Returns:
        Approval decision
    """
    if auto_approve:
        decision = "APPROVED"
        rationale = "Auto-approved for demonstration purposes. All critical resource requirements justified by extreme fire conditions."
    else:
        decision = "PENDING"
        rationale = "Awaiting human operator input"
    
    return {
        "approval_id": approval_data["approval_id"],
        "decision": decision,
        "decision_timestamp": datetime.now().isoformat(),
        "approved_actions": approval_data["recommended_actions"] if decision == "APPROVED" else [],
        "rationale": rationale,
        "approved_by": "System Administrator (Demo Mode)" if auto_approve else "Pending",
        "notes": "This is a demonstration with mock data"
    }

