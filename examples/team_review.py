"""Approach 3 — Agent Teams (Conversational)

Demonstrates the Agent Teams pattern where agents are spawned
from natural language descriptions. No code definitions. No config
files. Just a prompt describing the team you need.

Usage
-----
    python examples/team_review.py
    python examples/team_review.py "Design a caching layer for our API"
"""

import sys


# ── Team Definitions (Natural Language) ───────────────────────────


TEAM_PROMPTS = {
    "api-review": {
        "description": "API design review team with diverse perspectives",
        "spawn_prompt": (
            "Create a team to review this API design.\n"
            "One teammate focused on security — they should challenge every "
            "authentication decision and flag data exposure risks.\n"
            "One focused on developer experience — they should evaluate the "
            "API from the perspective of a developer integrating it for the "
            "first time.\n"
            "One playing devil's advocate — they should question every design "
            "decision and propose alternatives."
        ),
        "roles": [
            {"name": "Security Specialist", "focus": "Auth, data exposure, injection vectors"},
            {"name": "DX Advocate", "focus": "Ergonomics, documentation, error messages"},
            {"name": "Devil's Advocate", "focus": "Challenge assumptions, propose alternatives"},
        ],
    },
    "architecture": {
        "description": "Architecture decision team for system design",
        "spawn_prompt": (
            "Create a team to evaluate this architecture decision.\n"
            "One teammate is a distributed systems expert — they care about "
            "consistency, partition tolerance, and failure modes.\n"
            "One is a performance engineer — they care about latency, "
            "throughput, and resource utilisation.\n"
            "One is a pragmatist — they care about team velocity, "
            "maintenance burden, and operational simplicity."
        ),
        "roles": [
            {"name": "Distributed Systems Expert", "focus": "CAP, failure modes, consistency"},
            {"name": "Performance Engineer", "focus": "Latency, throughput, resources"},
            {"name": "Pragmatist", "focus": "Velocity, maintenance, simplicity"},
        ],
    },
    "incident": {
        "description": "Incident response team for production issues",
        "spawn_prompt": (
            "Create a team to investigate this production incident.\n"
            "One teammate traces the request path through the system to "
            "identify where the failure originated.\n"
            "One analyses logs and metrics to establish a timeline.\n"
            "One drafts the customer communication and incident report."
        ),
        "roles": [
            {"name": "Request Tracer", "focus": "Trace path, identify failure origin"},
            {"name": "Log Analyst", "focus": "Timeline, metrics correlation"},
            {"name": "Communications Lead", "focus": "Customer updates, incident report"},
        ],
    },
}


# ── Team Execution ────────────────────────────────────────────────


def demonstrate_team(team_name: str, task: str):
    """Show how Agent Teams work — conversational, not programmatic.

    In Claude Code, you would simply type the spawn_prompt in conversation.
    Claude creates the team. Each agent gets its own context window.
    They communicate peer-to-peer. No DAG. No orchestration code.
    """
    team = TEAM_PROMPTS[team_name]

    print("=" * 60)
    print("APPROACH 3 — Agent Teams (Conversational)")
    print("=" * 60)

    print(f"\nTeam: {team['description']}")
    print(f"Task: {task}")

    print(f"\n{'─' * 60}")
    print("SPAWN PROMPT (what you type in Claude Code):")
    print(f"{'─' * 60}")
    print(f"\n{team['spawn_prompt']}")

    print(f"\n{'─' * 60}")
    print("TEAM COMPOSITION (what Claude creates):")
    print(f"{'─' * 60}")

    for i, role in enumerate(team["roles"], 1):
        print(f"\n  Agent {i}: {role['name']}")
        print(f"  Focus:   {role['focus']}")
        print(f"  Context: Own window (isolated)")
        print(f"  Comms:   Can message other teammates directly")

    print(f"\n{'─' * 60}")
    print("HOW IT WORKS:")
    print(f"{'─' * 60}")
    print("""
  1. You describe the team in natural language
  2. Claude spawns N agents, each with its own context window
  3. Each agent works on its focus area independently
  4. Agents can send messages to each other (peer-to-peer)
  5. They collaborate, disagree, converge
  6. Results flow back to you as a synthesised output

  No code. No config files. No orchestration DAG.
  The team self-organises around the problem.
    """)

    # Show the Claude Code interaction pattern
    print(f"{'─' * 60}")
    print("CLAUDE CODE INTERACTION:")
    print(f"{'─' * 60}")
    print(f"""
  You:     {team['spawn_prompt'][:60]}...

  Claude:  I've created a team with 3 members:
           - {team['roles'][0]['name']}
           - {team['roles'][1]['name']}
           - {team['roles'][2]['name']}

           Each is now analysing the {task.lower()[:40]}...

  [Agents work in parallel, message each other]

  Claude:  Here's the team's combined analysis:
           [Synthesised findings from all three perspectives]
    """)

    print(f"{'─' * 60}")
    print("KEY DIFFERENCES FROM SDK AND MARKDOWN APPROACHES:")
    print(f"{'─' * 60}")
    print("""
  - No Python code required
  - No configuration files
  - Agents defined by description, not specification
  - Peer-to-peer communication (not parent-child)
  - Emergent collaboration (not orchestrated)
  - Session-based (not persistent)
  - Low determinism, high flexibility
    """)


def show_all_teams():
    """Display all available team templates."""
    print("=" * 60)
    print("AVAILABLE TEAM TEMPLATES")
    print("=" * 60)

    for name, team in TEAM_PROMPTS.items():
        print(f"\n  {name}")
        print(f"  {team['description']}")
        print(f"  Roles: {', '.join(r['name'] for r in team['roles'])}")

    print(f"\n{'─' * 60}")
    print("Usage: python examples/team_review.py [team_name] [task]")
    print("Teams: api-review, architecture, incident")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in TEAM_PROMPTS:
        team_name = sys.argv[1]
        task = sys.argv[2] if len(sys.argv) > 2 else "Review the current system design"
        demonstrate_team(team_name, task)
    elif len(sys.argv) > 1:
        # Custom task with default team
        demonstrate_team("api-review", sys.argv[1])
    else:
        demonstrate_team("api-review", "Design a caching layer for our API")
        print("\n")
        show_all_teams()
