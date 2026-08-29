# Production & Autonomy — Autonomy Dial (Step 1)

This file captures the Autonomy Dial by user segment (Module 6, Step 1). It records the chosen Trust Ladder rung for each segment and a one-line rationale.

## Autonomy Dial by segment

| Segment | Trust Ladder rung | One-line rationale |
|---|---|---|
| Seasoned ops user | bounded-autonomous | Runs trusted templates daily and can approve writes with audit logs; low-risk for scoped automated updates. |
| New eng lead | supervised | Needs human approval for external writes; uses automation for drafts and recommendations under oversight. |
| Exec stakeholder | assisted | Receives summaries and recommendations only; no automated external actions permitted. |

---

Checkpoint: Step 1 completed — Autonomy Dial table written. I will wait for your explicit "go" before proceeding to Step 2 (Trust Ladder placement + eval gate). 

## Step 2 — Trust Ladder placement & eval gate

**Current rung:** bounded-autonomous

**One-line justification:** bounded-autonomous — allows scoped automated updates under audit and single-use JIT permissions while keeping high-risk actions gated by HITL.

**Eval gate (Gate C):**
- Metric: ≥85% aggregate pass across EV-1..EV-4 (tool-call accuracy, path quality, recovery, cost-bound behavior).
- Window: measured over a 2-week rolling window of supervised runs.
- Cost stability: ≥95% of runs remain under configured budget limits during the window.

**Incident record (Point 2):**
- Definition: any safety/jailbreak acceptance or credential escalation attempt (i.e., any run that accepted an injected instruction to bypass policy or requested standing credentials) counts as an incident.

**Notes / sourcing:** The eval gate pulls concrete evals from `05-bounds-evals/bounds-and-evals.md` §3 (EV-1..EV-4) and the cost-bound behavior in EV-4.

Checkpoint: Step 2 drafted. I'll wait for your confirmation to proceed to Step 3 (deployment plan, ROI, widen rule). Say "go" to continue.

## Step 3 — Deployment plan, ROI, widen-autonomy rule, governance

### 1) Deployment plan
- Runtime: managed platform (Kubernetes/managed container) with autoscaling and an agent-runner service that enforces external bounds (iteration counter, timeout, budget guard).
- Operator / on-call: `Platform Ops (owner: ops-oncall@example.com)` — responsible for emergency pause endpoint and approving HITL checkpoints when escalation occurs.
- Rollback strategy: automated rollback script that (a) disables outgoing write tools, (b) reverts any pushed drafts via stored audit entries and one-use credential revocations, and (c) toggles the autonomy dial to `assisted` for affected segments.
- Monitoring signals: eval pass % (EV-1..EV-4), escalation rate, budget utilization, model latency, and failed-tool retry counts.

### 2) ROI metrics
- Outcome metric: Time-to-decision reduction — measure average time from request → parked draft; target: 30% reduction vs manual baseline, tracked via run timestamps.
- Cost-to-serve: $/delivered-draft (tokens + infra) — target: <$0.75 per parked draft; measured via billing exports and per-run cost logging.
- Trust incidents: number of incidents per 1,000 runs (incidents defined in Step 2) — target: <2 incidents per 1,000 runs.

### 3) Widen-autonomy decision rule
- Rule (one sentence): "If over a 4-week window the eval gate reaches ≥90% aggregate pass across EV-1..EV-4 and incidents remain <1 per 1,000 runs, raise the segment one rung and issue a controlled canary enabling bounded write templates for that segment." This rule is executed only after a manual review of the replay set results.

### 4) Governance & forward strategy
- Compliance: Define a data exclusion list (PII, CONFIDENTIAL roadmap items) that the runner strips from prompts; credential broker enforces separation and logs any attempted access.
- Safety: All external posts/DB writes remain HITL for `Exec stakeholder` and require single-use JIT tokens for `Seasoned ops user` bounded-autonomous actions; kill switch halts all writes.
- Reliability: Enforce `Max iterations=4`, `Timeout=90s`, `Cost cap $1/day` (M5 bounds); automatic degrade path to a read-only summary mode when model calls fail repeatedly.
- Next segment to widen into: `New eng lead` → after meeting the widen rule, pilot bounded-autonomous template writes for a subset of non-production update types.

Checkpoint: Step 3 written. I will wait for your "go" to proceed to Step 4 (write the two capstone prose deliverables and capture the end-to-end screenshot if needed).
# Production & Autonomy: Cortex PM Chief-of-Staff Agent

> Module 6 · ★ Deliverable 5, how you'd ship it, govern it, and widen trust over time
>
> ✅ **What this validates:** you can ship it, govern it, and widen trust deliberately — by the end you'll have proven an autonomy dial, a Trust Ladder rung with its eval gate, and a governance plan.

## Autonomy Dial by segment

_Autonomy is a product decision per user, not one global setting._

| Segment | Desired autonomy | Why |
|---|---|---|
| _Cautious PM ("Tesla driver")_ | _supervised_ | _wants to review every update before it goes out_ |
| _High-trust team lead ("Waymo passenger")_ | _bounded-autonomous_ | _happy to let the weekly update assemble itself_ |

## Trust Ladder

- **Current rung:** _shadow · assisted · supervised · bounded-autonomous · autonomous_
- **Eval gate to reach the next rung:** _which M5 evals must pass, at what threshold_
- **Incident record so far:** _…_

## Deployment plan

- **Runtime:** _managed agent platform · serverless · self-hosted, and why_
- **Operator / on-call owner:** _who owns it in production_
- **Rollback:** _how you turn it off / revert_
- **Monitoring:** _the dashboard + the signals you watch_

## ROI metrics (beyond adoption & tokens)

| Metric | Target |
|---|---|
| _Task completion rate_ | _…_ |
| _Time saved / cost-to-serve_ | _…_ |
| _Trust incidents_ | _…_ |

## Widen-autonomy decision rule

_What evidence lets you turn the dial up one notch, stated in advance._

## Governance & forward strategy

- **Compliance:** _what data must never enter a prompt; how PII is handled_
- **Safety:** _which actions stay above the agent line for everyone; kill switch_
- **Reliability:** _cost/iteration caps; escalate-on-stuck; fallback if the model is down_
- **Strategy:** _the next segment or capability you'd widen into, and the eval that gates it_
