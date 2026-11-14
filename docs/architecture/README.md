# Nd3G architecture proposal

**Status:** proposed analysis, not an implementation specification or permission to implement.  
**Date:** 2026-11-14, epsilonNice revision  
**Question:** Can an LLM tune the Snake AI to improve high scores?

Nd3G should retain Ax3l's outer experiment loop and integrated reporting pattern, and SnakeLab's simulation capabilities, while expanding the search space from parameter values to selected learning modules. The structure is one Nd3G application with long-running controller and web reporting services outside a fresh disposable simulation environment. Each simulation runs its server and a temporary MariaDB instance inside that environment, using the application’s normal simulation code and database contracts. The existing LlamaSrv deployment remains an external inference provider. The web server makes inspection available throughout development and troubleshooting; the TUI remains a useful real-time simulation client.

The central new boundary is an **immutable experiment candidate**: a complete parameter set, an explicit version of every selected module, and the evidence that this exact combination passed admission checks. Qwen proposes candidates through focused runtime skills and narrow tools. Deterministic application activities control validation, submission, scoring and champion selection. Generated code runs only in the disposable environment, including during import-time tests. The LLM can write only designated module slots. Static, non-LLM-writable simulation code publishes game state over ZMQ to external TUI/reporting consumers. After execution, host-owned activities inspect the captured artifacts and import accepted results into persistent storage before disposal.

## epsilonNice addition

Include epsilonNice as an explicit configurable exploration-policy component, grounded in AI Hydra’s documented behavior and implementation. The recommendation is a versioned optional epsilonNice layer and bounded configuration first, after the retained epsilon-greedy base policy. A new LLM-writable exploration-code slot is an alternative to review, not an assumption hidden in the word “configurable.” See [Exploration policy and epsilonNice](08-exploration-and-epsilon-nice.md) for the contract, source distinctions and tests.

## Disposable-simulation decisions

- A fresh execution environment contains the entire simulation server and temporary MariaDB for each run. This replaces the earlier proposal for a permanent simulation server outside a restricted learning worker.
- Reuse the same simulation persistence interfaces and versioned schema inside the environment; do not hand-build a second storage implementation. Temporary data is not automatically authoritative.
- Capture artifacts, inspect them, import accepted data into the persistent database, then dispose of the environment. Import and cleanup have explicit recovery semantics.
- Keep the TUI and web reporting outside the sandbox. Static simulation code publishes bounded ZMQ state; consumers treat it as provisional live evidence until result inspection.
- The sandbox technology and inspection mechanism remain design choices. Read-only source and passing tests do not alone establish containment or result integrity.

## Prior second-draft changes

- The user confirmed the first draft's working assumptions as sound. Architecture choices below still need design validation; this is not implementation authorization.
- Web reporting is now a requirement, not a later UI option. Inspectable state, decisions, test results and failures are essential; visualizations are optional additions.
- [Generated-code risk mitigation](07-generated-code-risk.md) now explains testing before activation, the limits of tests, practical containment options and separate score-integrity concerns.
- The rejected-candidate Mermaid sequence no longer contains the semicolon that was parsed as a statement separator.

## Read the proposal

1. [Requirements and source baseline](01-requirements-and-baseline.md): what is required, what exists, and what is assumed.
2. [Use cases and analysis model](02-analysis-model.md): boundary, control and entity responsibilities, Mermaid class diagrams and use-case realizations.
3. [Runtime skills and experiment contracts](03-skills-and-candidates.md): skill execution, tool authority, configurable modules and complete-candidate rules.
4. [Runtime boundaries and execution](04-runtime-and-integrity.md): disposable environments, temporary/persistent storage, inspected result import, communications and recovery.
5. [BMForge adoption and iteration plan](05-bmforge-and-delivery.md): component gaps, development sequence, acceptance criteria and open decisions.
6. [Source register](06-sources.md): pinned repository evidence and Unified Process references.
7. [Generated-code risk mitigation](07-generated-code-risk.md): a staged pre-execution test gate, containment choices, residual risks and admission evidence.
8. [Exploration policy and epsilonNice](08-exploration-and-epsilon-nice.md): AI Hydra behavior, configurable policy contract, runtime state and validation.

## Decisions recommended for review

- Adopt BMForge's Activity / Interface / Entity classification as the project convention, mapped explicitly to Unified Process control / boundary / entity analysis roles.
- Preserve the current high-score champion rule initially. Treat generated reward as a training signal, never as the authoritative score.
- Retain the four proposed writable learning slots: model, trainer, replay memory and reward function. Add configurable exploration, including epsilonNice, without implicitly extending source-write authority. Keep game mechanics, scoring, storage, tool handlers, service management and validation outside the model's edit authority.
- Use a small, explicit runtime skill host. Do not introduce an agent framework, generic workflow engine or new message broker.
- Include the integrated web reporting server in the first working slice, with read-only domain queries and clear live/persisted/stale state. Add charts only when they answer useful questions.
- Specify new reusable components in BMForge first. Adopt reviewed, pinned skills in Nd3G in separate implementation work. BMForge remains a development dependency in the ordinary sense of engineering guidance, never a runtime import.
- Make the execution boundary and trusted score path an elaboration gate. A Python subprocess, import allowlist or systemd service separation alone is not a sandbox.

All names, method sketches and process labels below are proposals. Mermaid source is embedded in Markdown for review and revision. No code, deployed configuration, skills, database or service is changed by this proposal.
