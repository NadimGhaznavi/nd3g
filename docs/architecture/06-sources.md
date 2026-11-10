# Source register

[Overview](README.md)

Initial inspection on 2026-11-09; second-draft reporting and risk review on 2026-11-10. Repository links below are pinned to exact revisions so the proposal does not silently change with upstream code. Source code establishes the observed baseline; recommendations in this proposal are not claims that those capabilities already exist.

## Nd3G and BMForge

- Publication base: Nd3G `dbf5e181b52a493110c919dd5033318ab4d969fa`, rechecked before creating the approved `dev` branch. Its added [design ideas](https://github.com/NadimGhaznavi/nd3g/blob/dbf5e181b52a493110c919dd5033318ab4d969fa/notes/design-ideas.md) support focused context, explicit signatures/examples and bounded validation/repair. Sampling settings and model-capability claims in those notes are hypotheses to measure on the actual deployment, not adopted defaults or guarantees. Its existing changelog entry and notes are preserved.
- Nd3G `1d7e07fff91f39791cff8e45a8b975d0c1e69f54`: [project instructions](https://github.com/NadimGhaznavi/nd3g/blob/1d7e07fff91f39791cff8e45a8b975d0c1e69f54/AGENTS.md), [BMForge lock](https://github.com/NadimGhaznavi/nd3g/blob/1d7e07fff91f39791cff8e45a8b975d0c1e69f54/.agents/bmforge/lock.json), [project skill](https://github.com/NadimGhaznavi/nd3g/blob/1d7e07fff91f39791cff8e45a8b975d0c1e69f54/.agents/skills/bmforge-project/SKILL.md). Basis for existing scaffold, selected skills, authorization boundary and changelog discipline.
- BMForge `29a100c39997349ecfd40e190319aeb5018ffab8`: [engineering contract](https://github.com/NadimGhaznavi/bmforge/blob/29a100c39997349ecfd40e190319aeb5018ffab8/pages/engineering-contract.md), [Activity / Interface / Entity classification](https://github.com/NadimGhaznavi/bmforge/blob/29a100c39997349ecfd40e190319aeb5018ffab8/pages/classification.md), [component blueprints](https://github.com/NadimGhaznavi/bmforge/blob/29a100c39997349ecfd40e190319aeb5018ffab8/pages/component-blueprints.md). Basis for responsibility placement, composition, owned implementations and mandatory module inventories.
- Same BMForge revision: [specification lifecycle](https://github.com/NadimGhaznavi/bmforge/blob/29a100c39997349ecfd40e190319aeb5018ffab8/pages/specification-lifecycle.md), [skill adoption](https://github.com/NadimGhaznavi/bmforge/blob/29a100c39997349ecfd40e190319aeb5018ffab8/pages/codex-skills.md), [repository boundary](https://github.com/NadimGhaznavi/bmforge/blob/29a100c39997349ecfd40e190319aeb5018ffab8/AGENTS.md). Basis for BMForge-first development, explicit pin upgrades and provenance limitations.
- Same BMForge revision: [REQ/REP 0.4.0](https://github.com/NadimGhaznavi/bmforge/blob/29a100c39997349ecfd40e190319aeb5018ffab8/pages/component-zmq.md), [DB Server 0.5.0](https://github.com/NadimGhaznavi/bmforge/blob/29a100c39997349ecfd40e190319aeb5018ffab8/pages/component-db-server.md). Both are labeled draft in the source. Basis for transport scope, the telemetry gap, unchanged DbMgr and MariaDB boundaries.
- Same BMForge revision: [HTTP 0.5.1](https://github.com/NadimGhaznavi/bmforge/blob/29a100c39997349ecfd40e190319aeb5018ffab8/pages/component-http.md) and [visualization 0.1.0](https://github.com/NadimGhaznavi/bmforge/blob/29a100c39997349ecfd40e190319aeb5018ffab8/pages/component-visualization.md): application-owned HTTP/Jinja2 server, safe rendering, meaningful health and capability-selected optional visualizations. No optional skill is installed by this proposal.

## Ax3l

Revision `6f4d778ae394bc60082a2d58c467f9358c5e20fe`:

- [SnakeLabLoop](https://github.com/NadimGhaznavi/ax3l/blob/6f4d778ae394bc60082a2d58c467f9358c5e20fe/ax3l/app/snakelab/SnakeLabLoop.py): active outer-loop control, fresh conversations, strict high-score comparison and restart handling.
- [Configuration schema](https://github.com/NadimGhaznavi/ax3l/blob/6f4d778ae394bc60082a2d58c467f9358c5e20fe/ax3l/app/snakelab/simulation-config-v2.schema.json), [single parameters](https://github.com/NadimGhaznavi/ax3l/blob/6f4d778ae394bc60082a2d58c467f9358c5e20fe/ax3l/app/snakelab/SingleParameters.py), [paired parameters](https://github.com/NadimGhaznavi/ax3l/blob/6f4d778ae394bc60082a2d58c467f9358c5e20fe/ax3l/app/snakelab/PairParameters.py): nine LLM-tuned values, fixed 1500-episode policy and pair semantics.

### Ax3l reporting evidence for the second draft

Same revision, rechecked 2026-11-10:

- [ReportingServer](https://github.com/NadimGhaznavi/ax3l/blob/6f4d778ae394bc60082a2d58c467f9358c5e20fe/ax3l/server/ReportingServer.py) and [reporting service unit](https://github.com/NadimGhaznavi/ax3l/blob/6f4d778ae394bc60082a2d58c467f9358c5e20fe/systemd/reporting-server.service): separate HTTP process, application handlers/templates and independently owned lifecycle.
- [Events page](https://github.com/NadimGhaznavi/ax3l/blob/6f4d778ae394bc60082a2d58c467f9358c5e20fe/ax3l/server/templates/events.html) and [EventLogDb](https://github.com/NadimGhaznavi/ax3l/blob/6f4d778ae394bc60082a2d58c467f9358c5e20fe/ax3l/app/EventLogDb.py): state/history inspection, filtered events and drill-down into exact records.
- [SnakeLab interface](https://github.com/NadimGhaznavi/ax3l/blob/6f4d778ae394bc60082a2d58c467f9358c5e20fe/ax3l/interface/SnakeLab.py) and [ReportBackground](https://github.com/NadimGhaznavi/ax3l/blob/6f4d778ae394bc60082a2d58c467f9358c5e20fe/ax3l/app/ReportBackground.py): live control-query versus persisted/cached-report distinction and 60-second stale-refresh behavior.
- [ReportingDb](https://github.com/NadimGhaznavi/ax3l/blob/6f4d778ae394bc60082a2d58c467f9358c5e20fe/ax3l/app/ReportingDb.py) and [ReportingRefresh](https://github.com/NadimGhaznavi/ax3l/blob/6f4d778ae394bc60082a2d58c467f9358c5e20fe/ax3l/app/ReportingRefresh.py): owned derived projections and transactional refresh. These justify explicit ownership if future Nd3G aggregates need caching; they do not require copying projection machinery into its first slice.

## SnakeLab

Revision `2bd021400d11017975a984ca9ac042b958349097`:

- [SimulationServer](https://github.com/NadimGhaznavi/snake-lab/blob/2bd021400d11017975a984ca9ac042b958349097/snakelab/server/SimulationServer.py): serial queue, new run on every submission, in-memory status map, controls, persisted result before notification and separate observation channels.
- [Configuration](https://github.com/NadimGhaznavi/snake-lab/blob/2bd021400d11017975a984ca9ac042b958349097/snakelab/server/Configuration.py) and [schema](https://github.com/NadimGhaznavi/snake-lab/blob/2bd021400d11017975a984ca9ac042b958349097/snakelab/schemas/simulation-config-v2.schema.json): server validation, cross-field rules and difference from Ax3l's narrowed schema.
- [RNNModel](https://github.com/NadimGhaznavi/snake-lab/blob/2bd021400d11017975a984ca9ac042b958349097/snakelab/nn/RNNModel.py), [Trainer](https://github.com/NadimGhaznavi/snake-lab/blob/2bd021400d11017975a984ca9ac042b958349097/snakelab/nn/Trainer.py), [ReplayMemory](https://github.com/NadimGhaznavi/snake-lab/blob/2bd021400d11017975a984ca9ac042b958349097/snakelab/nn/ReplayMemory.py): current sequence/action shapes, Double DQN implementation, episode-aware batches and buffer lifetime.
- [GameRules](https://github.com/NadimGhaznavi/snake-lab/blob/2bd021400d11017975a984ca9ac042b958349097/snakelab/game/GameRules.py), [RewardConfig](https://github.com/NadimGhaznavi/snake-lab/blob/2bd021400d11017975a984ca9ac042b958349097/snakelab/game/RewardConfig.py): score increments for food separately from reward values; reward extraction seam.
- [Client](https://github.com/NadimGhaznavi/snake-lab/tree/2bd021400d11017975a984ca9ac042b958349097/snakelab/client) and [protocol](https://github.com/NadimGhaznavi/snake-lab/blob/2bd021400d11017975a984ca9ac042b958349097/snakelab/zmq/Protocol.py): reuse starting point and protocol-specific coupling, not a commitment to preserve legacy wire compatibility.

## LlamaSrv

Revision `3a7405d346c52edd07934efdc95aec0604b3e043`:

- [README](https://github.com/NadimGhaznavi/llamasrv/blob/3a7405d346c52edd07934efdc95aec0604b3e043/README.md), [usage](https://github.com/NadimGhaznavi/llamasrv/blob/3a7405d346c52edd07934efdc95aec0604b3e043/pages/usage.md), [Qwen defaults](https://github.com/NadimGhaznavi/llamasrv/blob/3a7405d346c52edd07934efdc95aec0604b3e043/llamasrv/constants/DQwen.py): separation of service control/inference, documented application API and Qwen3.5-4B defaults. Repository defaults are not a measurement of the deployed host.

## Unified Process modeling references

- [IBM: Analysis model](https://www.ibm.com/docs/en/dma?topic=approaches-analysis-model): logical structure and responsibility-focused analysis rather than implementation detail.
- [Rational Unified Process: Analysis class guideline](https://home.iscte-iul.pt/~hro/RUPSmallProjects/core.base_rup/guidances/guidelines/analysis_class_7E97273E.html): boundary, control and entity analysis classes and use-case realization context. This is a published RUP guideline mirror, not a claim of conformance to a particular edition of a normative standard.

The user requested a Unified Software Development Process style, not formal certification. BMForge's own classification is the governing project convention. No unrelated metamodel, such as CWM, is imposed on this application.

## Generated-code risk references

These primary documentation references explain limitations and options, not approval to add dependencies or a claim that a particular deployment is secure:

- [Python `exec`](https://docs.python.org/3/library/functions.html#exec): arbitrary-code execution and the warning that overriding builtins is not a security mechanism.
- [Python pickle security warning](https://docs.python.org/3/library/pickle.html): never treat untrusted serialized Python objects as a safe data exchange format.
- [Docker security](https://docs.docker.com/engine/security/) and [rootless resource-limit prerequisites](https://docs.docker.com/engine/security/rootless/tips/#limiting-resources): namespaces/capabilities and configuration-dependent resource enforcement, not a complete hostile-code guarantee.
- [gVisor security architecture](https://gvisor.dev/docs/architecture_guide/security/): stronger isolation as a possible separately evaluated runtime, with its own trust assumptions and compatibility considerations.
- [PyTorch serialization](https://docs.pytorch.org/docs/stable/notes/serialization): checkpoint/loading restrictions and the limits of `weights_only`; restricting a load does not make surrounding generated Python safe.
