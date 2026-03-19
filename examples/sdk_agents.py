"""Approach 1 — Agent SDK (Programmatic)

Defines three agents in Python using the Claude Code SDK.
A security auditor, a code quality reviewer, and an orchestrator
that delegates between them.

Usage
-----
    pip install claude-code-sdk
    python examples/sdk_agents.py
    python examples/sdk_agents.py --target ./src
"""

import asyncio
import sys
from dataclasses import dataclass


# ── Agent Definitions ─────────────────────────────────────────────


@dataclass
class AgentConfig:
    """Programmatic agent definition — full control over every parameter."""
    name: str
    system_prompt: str
    tools: list[str]
    model: str = "sonnet"
    max_turns: int = 10


SECURITY_AGENT = AgentConfig(
    name="security-auditor",
    system_prompt=(
        "You are a security auditor. Your job is to find vulnerabilities.\n\n"
        "Focus on:\n"
        "- Injection risks (SQL, command, XSS)\n"
        "- Hardcoded secrets or API keys\n"
        "- Insecure dependencies\n"
        "- Authentication and authorisation gaps\n"
        "- Path traversal and file access issues\n\n"
        "Report each finding with severity (CRITICAL, HIGH, MEDIUM, LOW), "
        "the file and line number, and a recommended fix.\n"
        "Be concise. No preamble."
    ),
    tools=["Read", "Grep", "Glob"],
    model="sonnet",
    max_turns=15,
)


QUALITY_AGENT = AgentConfig(
    name="quality-reviewer",
    system_prompt=(
        "You are a code quality reviewer. Your job is to improve code quality.\n\n"
        "Focus on:\n"
        "- Dead code and unused imports\n"
        "- Functions longer than 30 lines\n"
        "- Missing error handling at system boundaries\n"
        "- Naming clarity\n"
        "- Duplicated logic that should be extracted\n\n"
        "Rate each file: GOOD, NEEDS_WORK, or POOR.\n"
        "Be specific. Reference line numbers."
    ),
    tools=["Read", "Grep", "Glob"],
    model="sonnet",
    max_turns=10,
)


ORCHESTRATOR = AgentConfig(
    name="review-orchestrator",
    system_prompt=(
        "You are a review orchestrator. You coordinate security and quality reviews.\n\n"
        "1. First delegate to the security auditor\n"
        "2. Then delegate to the quality reviewer\n"
        "3. Combine their findings into a single report\n"
        "4. Prioritise by severity\n"
        "5. Add an overall risk assessment (LOW, MEDIUM, HIGH, CRITICAL)\n\n"
        "Output a structured markdown report."
    ),
    tools=["Read", "Grep", "Glob", "Bash"],
    model="sonnet",
    max_turns=20,
)


# ── SDK Integration ───────────────────────────────────────────────


async def run_agent(agent: AgentConfig, prompt: str) -> str:
    """Execute an agent using the Claude Code SDK.

    In production, this calls claude_code_sdk.query().
    This prototype shows the exact API shape.
    """
    # Production usage:
    #
    # from claude_code_sdk import query, ClaudeCodeOptions
    #
    # messages = []
    # async for event in query(
    #     prompt=prompt,
    #     options=ClaudeCodeOptions(
    #         system_prompt=agent.system_prompt,
    #         allowed_tools=agent.tools,
    #         model=agent.model,
    #         max_turns=agent.max_turns,
    #     )
    # ):
    #     if event.type == "text":
    #         messages.append(event.content)
    # return "".join(messages)

    print(f"\n{'─' * 60}")
    print(f"Agent: {agent.name}")
    print(f"Model: {agent.model}")
    print(f"Tools: {', '.join(agent.tools)}")
    print(f"Max turns: {agent.max_turns}")
    print(f"Prompt: {prompt[:80]}...")
    print(f"{'─' * 60}")
    print(f"\nSystem prompt:\n{agent.system_prompt}")
    print(f"\n[In production, claude_code_sdk.query() executes here]")

    return f"[{agent.name} findings would appear here]"


async def run_orchestrated_review(target_path: str):
    """Run the full orchestrated review pipeline.

    Demonstrates the SDK pattern:
    - Agents defined as Python dataclasses
    - Orchestrator delegates to specialised subagents
    - Full programmatic control over every parameter
    """
    print("=" * 60)
    print("APPROACH 1 — Agent SDK (Programmatic)")
    print("=" * 60)
    print(f"\nTarget: {target_path}")
    print(f"Pipeline: orchestrator → security-auditor + quality-reviewer")

    # Step 1: Security audit
    security_findings = await run_agent(
        SECURITY_AGENT,
        f"Audit all files in {target_path} for security vulnerabilities.",
    )

    # Step 2: Quality review
    quality_findings = await run_agent(
        QUALITY_AGENT,
        f"Review all files in {target_path} for code quality issues.",
    )

    # Step 3: Orchestrator combines findings
    combined = await run_agent(
        ORCHESTRATOR,
        f"Combine these review findings into a single prioritised report:\n\n"
        f"## Security Findings\n{security_findings}\n\n"
        f"## Quality Findings\n{quality_findings}",
    )

    print(f"\n{'=' * 60}")
    print("PIPELINE COMPLETE")
    print(f"{'=' * 60}")
    print(f"\nAgents executed: 3")
    print(f"  1. {SECURITY_AGENT.name} (tools: {', '.join(SECURITY_AGENT.tools)})")
    print(f"  2. {QUALITY_AGENT.name} (tools: {', '.join(QUALITY_AGENT.tools)})")
    print(f"  3. {ORCHESTRATOR.name} (tools: {', '.join(ORCHESTRATOR.tools)})")
    print(f"\nKey SDK features demonstrated:")
    print(f"  - Agents as Python dataclasses (version-controlled, testable)")
    print(f"  - Explicit tool allowlists per agent")
    print(f"  - Model selection per agent")
    print(f"  - Sequential orchestration with data flow between agents")


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    asyncio.run(run_orchestrated_review(target))
