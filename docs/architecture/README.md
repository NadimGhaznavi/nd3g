# Nd3G architecture proposal

**Status:** proposed analysis, not an implementation specification or permission to implement.  
**Date:** 2026-11-09  
**Question:** Can an LLM tune the Snake AI to improve high scores?

Nd3G should retain Ax3l's outer experiment loop and SnakeLab's simulation and reporting capabilities, while expanding the search space from parameter values to selected learning modules. The recommended structure is one Nd3G application with two long-running systemd services: an experiment controller and a simulation server. The existing LlamaSrv deployment remains an external inference provider. The TUI remains the first observation client.

The central new boundary is an **immutable experiment candidate**: a complete parameter set, an explicit version of every selected module, and the evidence that this exact combination passed admission checks. Qwen proposes candidates through focused runtime skills and narrow tools. Deterministic application activities control validation, submission, scoring and champion selection. Generated code must never be imported into either long-running service.

## Read the proposal

1. [Requirements and source baseline](01-requirements-and-baseline.md): what is required, what exists, and what is assumed.
2. [Use cases and analysis model](02-analysis-model.md): boundary, control and entity responsibilities, Mermaid class diagrams and use-case realizations.
3. [Runtime skills and experiment contracts](03-skills-and-candidates.md): skill execution, tool authority, configurable modules and complete-candidate rules.
4. [Runtime boundaries and execution](04-runtime-and-integrity.md): services, communications, scoring integrity, recovery and TUI reuse.
5. [BMForge adoption and iteration plan](05-bmforge-and-delivery.md): component gaps, development sequence, acceptance criteria and open decisions.
6. [Source register](06-sources.md): pinned repository evidence and Unified Process references.

## Decisions recommended for review

- Adopt BMForge's Activity / Interface / Entity classification as the project convention, mapped explicitly to Unified Process control / boundary / entity analysis roles.
- Preserve the current high-score champion rule initially. Treat generated reward as a training signal, never as the authoritative score.
- Start with four writable learning slots: model, trainer, replay memory and reward function. Keep game mechanics, scoring, storage, tool handlers, service management and validation outside the model's edit authority.
- Use a small, explicit runtime skill host. Do not introduce an agent framework, generic workflow engine or new message broker.
- Specify new reusable components in BMForge first. Adopt reviewed, pinned skills in Nd3G in separate implementation work. BMForge remains a development dependency in the ordinary sense of engineering guidance, never a runtime import.
- Make the execution boundary and trusted score path an elaboration gate. A Python subprocess, import allowlist or systemd service separation alone is not a sandbox.

All names, method sketches and process labels below are proposals. Mermaid source is embedded in Markdown for review and revision. No code, deployed configuration, skills, database or service is changed by this proposal.
