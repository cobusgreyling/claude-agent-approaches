"""Side-by-side comparison of all three agent approaches.

Shows how the same task (code review) is expressed differently
across the SDK, Markdown, and Teams paradigms.

Usage
-----
    python examples/compare_approaches.py
"""


def main():
    print("=" * 70)
    print("THREE APPROACHES TO THE SAME TASK: Code Review")
    print("=" * 70)

    # ── Approach 1: SDK ───────────────────────────────────────────

    print(f"\n{'━' * 70}")
    print("APPROACH 1 — Agent SDK (Programmatic)")
    print(f"{'━' * 70}")
    print("""
    HOW YOU DEFINE IT:

    agent = AgentConfig(
        name="code-reviewer",
        system_prompt="You are a code reviewer...",
        tools=["Read", "Grep", "Glob"],
        model="sonnet",
        max_turns=10,
    )

    async for event in query(
        prompt="Review ./src for quality issues",
        options=ClaudeCodeOptions(
            system_prompt=agent.system_prompt,
            allowed_tools=agent.tools,
        )
    ):
        process(event)

    CHARACTERISTICS:
    ┌────────────────────┬──────────────────────────┐
    │ Definition format  │ Python code              │
    │ Where it lives     │ Your application codebase│
    │ Control level      │ Full programmatic        │
    │ Determinism        │ High                     │
    │ Reusability        │ Import and call          │
    │ Testing            │ Unit testable            │
    │ Best for           │ Production applications  │
    └────────────────────┴──────────────────────────┘
    """)

    # ── Approach 2: Markdown ──────────────────────────────────────

    print(f"{'━' * 70}")
    print("APPROACH 2 — Markdown Agents (Declarative)")
    print(f"{'━' * 70}")
    print("""
    HOW YOU DEFINE IT:

    File: .claude/agents/code-reviewer.md

    ---
    name: code-reviewer
    description: Expert code reviewer. Use after code changes.
    tools: Read, Grep, Glob
    model: sonnet
    maxTurns: 10
    ---

    You are a code reviewer. When invoked:
    1. Run git diff to see changes
    2. Review modified files
    3. Report findings with line numbers

    CHARACTERISTICS:
    ┌────────────────────┬──────────────────────────┐
    │ Definition format  │ Markdown + YAML          │
    │ Where it lives     │ .claude/agents/ in repo  │
    │ Control level      │ Declarative frontmatter  │
    │ Determinism        │ Medium                   │
    │ Reusability        │ Copy the .md file        │
    │ Testing            │ Manual invocation        │
    │ Best for           │ Project tooling          │
    └────────────────────┴──────────────────────────┘
    """)

    # ── Approach 3: Teams ─────────────────────────────────────────

    print(f"{'━' * 70}")
    print("APPROACH 3 — Agent Teams (Conversational)")
    print(f"{'━' * 70}")
    print("""
    HOW YOU DEFINE IT:

    "Create a review team for this codebase.
     One agent focused on security.
     One on code quality.
     One on test coverage."

    That's it. No code. No files. Just a prompt.

    CHARACTERISTICS:
    ┌────────────────────┬──────────────────────────┐
    │ Definition format  │ Natural language          │
    │ Where it lives     │ Conversation (ephemeral) │
    │ Control level      │ Descriptive              │
    │ Determinism        │ Low                      │
    │ Reusability        │ Re-prompt each time      │
    │ Testing            │ Not applicable           │
    │ Best for           │ Exploration              │
    └────────────────────┴──────────────────────────┘
    """)

    # ── The Spectrum ──────────────────────────────────────────────

    print(f"{'━' * 70}")
    print("THE SPECTRUM")
    print(f"{'━' * 70}")
    print("""
    Imperative ◄──────────────────────────────────────► Conversational

    SDK               Markdown              Teams
    ├─────────────────┼─────────────────────┤
    Code              Config                Language
    Explicit          Declarative           Emergent
    Products          Tooling               Exploration
    High control      Medium control        Low control
    High determinism  Medium determinism    Low determinism

    Same task. Three paradigms. Choose based on your use case.
    """)


if __name__ == "__main__":
    main()
