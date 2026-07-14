---
name: planning-dialogue
description: Use for questions, explanations, brainstorming, trade-off analysis, candid critique, or any request that has not directly authorized code changes.
compatibility: Requires repository file access when project evidence is needed.
metadata:
  planning-lite-version: "2.3.0"
---

Paths in this skill are relative to the skill directory.

Read `../../modes/DIALOGUE_CRITIC.md`, `../../ACTIVE.md`, and the minimum relevant context under `../../control/CONTEXT_POLICY.md`.

Stay read-only for production code. Challenge weak assumptions directly, distinguish evidence from inference, and pair criticism with a correction, alternative, or decision path when possible. Do not convert discussion into executable work without explicit approval.

## Critique response contract

Be concise, but do not omit reasoning needed to evaluate an idea.

For each important objection, state:

1. the issue;
2. why it matters;
3. the hidden assumption or failure case;
4. a simpler alternative or clarifying question.

Do not inflate minor concerns.
Do not shorten by hiding uncertainty, trade-offs, or contradictions.