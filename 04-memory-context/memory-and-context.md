# Context Engineering & Memory: Cortex PM Chief-of-Staff Agent

> Module 4 · Context Engineering & Memory
>
> ✅ **What this validates:** the agent reasons on the right, safe inputs — by the end you'll have proven a context budget, per-source retrieve-vs-long-context decisions, and a memory map with risk mitigations.
>
> 🗂️ **How the lab maps to this file:** In **Part A** (before the lecture) you don't edit this file — you rough-draft on scratch, focused on the per-source calls in **section 2** plus a quick remember/forget + "how it rots" sketch. In **Part B** (after the lecture) you complete **all five sections**; the Lab Guide's guided builder writes this file for you to copy in and commit.

## 1. Context budget

_What does each loop iteration actually receive, and why? (You can't fit everything, what's the priority order?)_

Priority (highest → lowest):
- 1) Task brief (`get_task`) — the immediate ask and any constraints (always in long-context for accuracy).
- 2) Recent engineering activity (`get_activity`) — retrieval slices for the last N items (high volatility; cite exact records).
- 3) Team norms / playbook (`get_norms`) — long-context policy that gates allowed actions and escalation rules.
- 4) Roadmap (`get_roadmap`) — long-context except when a targeted slice is required; pay attention to confidential flags.
- 5) Past updates (`search_past_updates`) — long-context summary history used for tone/precedent, not full history in every run.

Rationale: the task brief and recent activity are what the draft must ground its claims in; norms and roadmap are smaller policy documents that should be in long-context so Cortex can cite exact rules; past updates are useful for tone and precedent but kept as summarized long-context to limit context size.

## 2. Retrieve vs. long-context: per source

For each data source, decide: **retrieve** (narrow a large/changing corpus to the relevant slice) or **long-context** (just include a bounded set you can reason over).

| Source | Size / volatility | Decision | Deciding factor |
|---|---:|---|---|
| `get_task` (task brief) | bounded / static | Long-context | The brief is small and authoritative; include whole text so Cortex reasons from the exact ask.
| `get_activity` (engineering activity) | large / high volatility | Retrieve | High churn and size; retrieve a slice (most recent N entries) and require explicit key-path citation for metric/date claims.
| `search_past_updates` (past updates) | unbounded / archival | Long-context (summarized) | Use a bounded summary or most-recent weeks for tone/precedent; avoid pulling the entire history each run.
| `get_roadmap` | medium / slow | Long-context (guarded) | Roadmap items are policy-like; include full shareable roadmap but respect `confidential` flags and treat embargoed items as read-only.
| `get_norms` | small / policy | Long-context | Norms must be available verbatim so Cortex can cite rules (evidence for escalation and must-not-do checks).

Priority notes: if a retrieved slice is missing a cited fact required by the draft, the agent must escalate rather than invent; retrieval moves must include the source key paths used for each claim.

## 3. Retrieval quality plan

_Which of these apply, and how? (This is what separates modern agentic retrieval from naive "embed → top-k → stuff".)_

- **Routing**: _which source to query?_
- **Document grading**: _is what I retrieved actually relevant?_
- **Reranking**: _…_
- **Self-verification**: _did the update use the retrieved evidence?_
- **Caching**: _…_

Worked example (per source):

- `get_activity` (engineering activity):
	- Moves: **routing → document grading → reranking → self-verification → caching (short TTL)**.
	- Why: activity is high-volume and noisy. Route to the project slice, grade documents for signal (PRs, metrics), rerank by recency+relevance, require the agent to cite the exact key-path for any numeric/date/PR claim, and cache the retrieved slice for the run to avoid repeated calls.

- `search_past_updates` (past updates):
	- Moves: **routing → summarization → reranking**.
	- Why: past updates are unbounded. Route to recent weeks, summarize / extract precedent phrasing, and rerank to support tone and avoid pulling full history into context.

- `get_roadmap`:
	- Moves: **document grading → confidentiality guard → caching (longer TTL)**.
	- Why: roadmap entries are policy-like. Grade the retrieved section for shareability, apply a confidentiality guard (do not include embargoed items in external drafts), and cache for durability across runs.

- `get_norms`:
	- Moves: **long-context inclusion + citation checks**.
	- Why: norms are small policy documents that should be available verbatim; require the agent to cite the specific rule (key/line) it relied on when choosing to escalate or to omit a date.

- `get_task` (task brief):
	- Moves: **long-context inclusion + self-verification**.
	- Why: the brief is authoritative for intent; include in full and verify final draft aligns with the original ask before finishing.

Operational rules to enforce in the build:
- Every numeric or date claim must be accompanied by the source key-path used for verification (e.g., `activity[3].value`). If missing, the drafter must escalate.
- Caching TTLs: activity (short, e.g., 5–15 minutes), roadmap/norms (session/longer), past-updates summaries (session).
- All retrieval moves must produce a brief provenance object that the critic can consume to validate claims.

## 4. Memory map (your PM brain)

| Memory type | What Cortex stores | Scope / TTL |
|---|---|---|
| **Working** (in-loop) | _…_ | _this run_ |
| **Episodic** (past runs) | _past status updates, decisions_ | _…_ |
| **Semantic** (durable facts/prefs) | _team norms, roadmap facts_ | _…_ |
| **Shared** (across agents) | _…_ | _…_ |

## 5. Memory risks & mitigations

| Risk | Mitigation |
|---|---|
| _Drift_ | _…_ |
| _Poisoning_ | _…_ |
| _Staleness_ | _…_ |
| _Confidential / retention_ | _scoping + flags (Cortex touches embargoed roadmap)_ |
