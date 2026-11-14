# Source register

[Overview](README.md)

Initial inspection on 2026-11-09; second-draft reporting and risk review on 2026-11-10; disposable-simulation and epsilonNice revisions on 2026-11-14. Repository links below are pinned to exact revisions so the proposal does not silently change with upstream code. Source code establishes the observed baseline; recommendations in this proposal are not claims that those capabilities already exist.

## Latest user decisions

The 2026-11-14 discussion specifies a disposable simulation execution environment containing the simulation server and temporary MariaDB, artifacts inspected before import into the persistent database, and ZMQ publication from static non-LLM-writable simulation code to consumers in separate external processes. These are user requirements, not claims inferred from legacy code. No sandbox technology or particular inspection mechanism was selected.

The later 2026-11-14 request adds epsilonNice as a configurable component and explicitly requests a PR. It does not specify whether exploration source becomes an additional LLM-writable slot; this proposal identifies that choice instead of assuming it.

## Nd3G and BMForge

- EpsilonNice revision base: Nd3G release 0.1.1, [`80e64739574e23c4daa845f821769819d2de9aa8`](https://github.com/NadimGhaznavi/nd3g/commit/80e64739574e23c4daa845f821769819d2de9aa8), current `dev` when inspected. [PR #2](https://github.com/NadimGhaznavi/nd3g/pull/2) is merged. The prior release sections and all existing non-documentation content are preserved.

- Current revision base: Nd3G release 0.1.0, [`05bf7d7d34d5a34404927964aac0a5ced0b9191c`](https://github.com/NadimGhaznavi/nd3g/commit/05bf7d7d34d5a34404927964aac0a5ced0b9191c), shared by `dev` and `main` when inspected on 2026-11-14. [PR #1](https://github.com/NadimGhaznavi/nd3g/pull/1) is merged. Current architecture files, project instructions, BMForge lock and released changelog were reread; release history and pinned skills remain unchanged. Earlier repository observations below retain their original revision scope.

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

## AI Hydra epsilonNice

The requested `ai-hydra` repository redirects to `NadimGhaznavi/ai_hydra`. Inspected main at `b348e6be6d0f2458bc9401ed01035e85fa09527f` on 2026-11-14:

- [epsilonNice guide](https://github.com/NadimGhaznavi/ai_hydra/blob/b348e6be6d0f2458bc9401ed01035e85fa09527f/pages/epsilon-nice.md) and [policy settings](https://github.com/NadimGhaznavi/ai_hydra/blob/b348e6be6d0f2458bc9401ed01035e85fa09527f/pages/settings.md): conditional safe detours, probability/length settings and MCTS context.
- [BehaviourPolicy](https://github.com/NadimGhaznavi/ai_hydra/blob/b348e6be6d0f2458bc9401ed01035e85fa09527f/ai_hydra/nnet/Policy/BehaviourPolicy.py) and [EpsilonNiceAlgo](https://github.com/NadimGhaznavi/ai_hydra/blob/b348e6be6d0f2458bc9401ed01035e85fa09527f/ai_hydra/nnet/EpsilonNiceAlgo.py): enable/gate/next-step arming, remaining steps, safe-alternative selection and precise counter semantics.
- [TrainMgr](https://github.com/NadimGhaznavi/ai_hydra/blob/b348e6be6d0f2458bc9401ed01035e85fa09527f/ai_hydra/nnet/TrainMgr.py), [HydraMgr](https://github.com/NadimGhaznavi/ai_hydra/blob/b348e6be6d0f2458bc9401ed01035e85fa09527f/ai_hydra/server/HydraMgr.py), [EpsilonAlgo](https://github.com/NadimGhaznavi/ai_hydra/blob/b348e6be6d0f2458bc9401ed01035e85fa09527f/ai_hydra/nnet/EpsilonAlgo.py) and [HydraPolicy](https://github.com/NadimGhaznavi/ai_hydra/blob/b348e6be6d0f2458bc9401ed01035e85fa09527f/ai_hydra/nnet/Policy/HydraPolicy.py): score-based stagnation, composition, episode update order, epsilon snap-to-zero and reset-hook limits.
- [DNNet](https://github.com/NadimGhaznavi/ai_hydra/blob/b348e6be6d0f2458bc9401ed01035e85fa09527f/ai_hydra/constants/DNNet.py), [SimCfg](https://github.com/NadimGhaznavi/ai_hydra/blob/b348e6be6d0f2458bc9401ed01035e85fa09527f/ai_hydra/utils/SimCfg.py) and [HydraRng](https://github.com/NadimGhaznavi/ai_hydra/blob/b348e6be6d0f2458bc9401ed01035e85fa09527f/ai_hydra/nnet/HydraRng.py): settings/defaults and deterministic stream derivation. Coercion does not itself establish Nd3G admission bounds.
- [GameLogic](https://github.com/NadimGhaznavi/ai_hydra/blob/b348e6be6d0f2458bc9401ed01035e85fa09527f/ai_hydra/game/GameLogic.py), [HydraSnapshot](https://github.com/NadimGhaznavi/ai_hydra/blob/b348e6be6d0f2458bc9401ed01035e85fa09527f/ai_hydra/utils/HydraSnapshot.py), [HydraClient](https://github.com/NadimGhaznavi/ai_hydra/blob/b348e6be6d0f2458bc9401ed01035e85fa09527f/ai_hydra/client/HydraClient.py): immediate-collision predicate and reporting/TUI consumption.
- [Inspected regression tests](https://github.com/NadimGhaznavi/ai_hydra/blob/b348e6be6d0f2458bc9401ed01035e85fa09527f/tests/test_rnn_regression.py): no focused epsilonNice coverage was found. Source inspection is not proof of tested runtime behavior.

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
