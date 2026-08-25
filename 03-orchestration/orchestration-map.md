# Orchestration Map — Module 3

## 1. Why split / why not
Decision: Split into a single drafter (`Cortex`) + one independent validator (`Critic`).
Reason (learner words): The independent validator is required so the drafter cannot grade its
own work — we need a second check that enforces traceability and bounds before human review.

## 2. Topology (text diagram)
```
[Inbound PM task] → [Cortex: pull data, draft update + propose stories]
                      → [Validator / Critic]
                         — fail -> back to Cortex (max 2 revisions) -> escalate
                         — pass -> [PM review checkpoint] (no auto-send)
```

## 3. Roster
- Cortex: drafts status updates and proposes story batches. Runs the Loop Spec from `02-loop-design/loop-spec.md`.
- Validator (Critic): independent model that checks traceability, numeric claims, unconfirmed dates, and story-batch caps.

## 4. Hand-offs
- Cortex → Validator: proposed draft (text) + source log (list of pulled results and tool call outputs).
- Validator → Cortex: verdict (pass|fail) and reasons; on fail includes the failing checks to guide revision.
- PM review gets the final draft and the source log; nothing is posted or committed automatically.

## 5. The validator (checks, fail-action, revision cap)
- Checks (concrete):
  1. Project identity and referenced PR/issue IDs exist in pulled `get_project`/`get_activity` data.
  2. Every numerical claim or metric (e.g., activation rates, percentages) is traceable to pulled data.
  3. No unconfirmed date is presented as a committed launch date.
  4. Proposed story batch count does not exceed the `CORTEX_MAX_QUEUE_ITEMS` cap; if it does, the tool will have rejected it and the draft must escalate.
  5. No confidential roadmap items are exposed.
- Fail-action: `revise` — return to Cortex with explicit reasons; allow up to `MAX_REVISIONS=2` then `escalate`.

## 6. Shared vs isolated state
- Shared: the pulled source data (read-only) and the task brief.
- Isolated: the validator's internal reasoning and critique notes (must not be fed back into Cortex as model context to avoid contamination).

## 7. Cost & latency budget
- The validator adds one extra model call per draft cycle; worst-case (2 revisions) means up to 3 drafter calls + 2 validator calls per run. Expect small latency increase (seconds) and modest extra cost; enforce revision cap to bound costs.

---
Saved-by: coding-agent (draft). Next step: implement the validator checks in the build and force a failing draft to capture evidence.
# Orchestration Map: Cortex PM Chief-of-Staff Agent

> Module 3 · Orchestration & Subagents, ★ Deliverable 3
>
> ✅ **What this validates:** nothing advances unchecked — by the end you'll have proven a justified topology, a roster, and a validator with a defined fail action.
>
> Builds on your M2 Loop Spec. Only split one agent into a team when there's a real reason, coordination has a cost.

## 1. Why split? (or why not)

_Run the default-to-simple check. Do you actually need subagents/a fleet? What's the real reason (separation of concerns · parallelism · independent validation · context-window pressure)? If not, say so and stop here._

## 2. Topology

**Pattern:** _single+subagents · sequential · parallel+aggregate · hierarchical_

```
[ simple text diagram of the flow ]
e.g.  task → [Research] + [GitHub/Jira reader] → [Writer] → [Critic ✓] → human checkpoint → queued
```

## 3. Roster

| Agent / subagent | Responsibility | Runs which Loop Spec |
|---|---|---|
| _Chief-of-staff (Cortex)_ | _orchestrates + assembles the update_ | _M2 loop_ |
| _Research subagent_ | _pulls competitive / market context_ | _research loop_ |
| _GitHub/Jira reader_ | _summarizes recent activity_ | _read loop_ |
| _Critic / Validator_ | _checks the draft before it advances_ | _validation loop_ |
| _…_ | | |

## 4. Communication & hand-offs

_What passes between the parts? Any protocol (MCP / A2A, optional, note if used)._

## 5. The validator

- **What the critic checks:** _grounded claims · norms compliance · no confidential leak · nothing posted/committed_
- **Fail action:** _what happens when it fails (retry · revise · escalate to human)_

## 6. State: shared vs isolated

_What's shared across the fleet vs kept isolated per subagent (carry from M2)._

## 7. Cost & latency budget

_Coordination has a price. Rough token/latency cost of the fleet vs a single agent. (Forward-link to M5 bounds.)_
