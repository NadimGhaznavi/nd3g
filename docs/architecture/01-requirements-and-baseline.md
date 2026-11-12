# Requirements and source baseline

[Overview](README.md) · [Analysis model](02-analysis-model.md)

## Explicit requirements

| ID | User requirement | Architectural response |
| --- | --- | --- |
| R1 | Preserve the experiment: can an LLM improve Snake AI high scores? | Separate candidate generation from authoritative run scoring and comparison. |
| R2 | Use the already-deployed Qwen 3.5 4B through LlamaSrv. | An inference boundary calls the existing llama.cpp endpoint; Nd3G does not own model deployment. |
| R3 | A systemd-managed Nd3G process coordinates LLM and simulations. | Experiment-controller service owns the outer loop and durable experiment history. |
| R4 | Integrate SnakeLab functionality into Nd3G, with its own simulation-server systemd process. | Same application/repository, separate process and responsibility boundary. No dependency on a running legacy SnakeLab service. |
| R5 | Reuse the real-time TUI, considering other interfaces. | Adapt the existing Textual client for live simulation observation alongside the required web reporting server. |
| R6 | Let the LLM configure current hyperparameters and potentially more. | A versioned parameter catalogue covers the current tuning surface; extensions require deliberate contract changes. |
| R7 | Let the LLM write selected simulation modules, such as RNNModel, Trainer, ReplayMemory and RewardFunction. | Named writable module slots with stable contracts, bounded artifacts and executable admission checks. |
| R8 | Submit only after all configurable elements have been set. | Freeze a complete candidate; reject missing, stale or invalid elements before submission. |
| R9 | Keep scoring and reporting largely unchanged. | Retain high scores, episode results, winning-game evidence and champion history; add provenance rather than replace existing measures. |
| R10 | Explore skills with supporting tools rather than simply reusing prompt architecture. | Focused runtime skills with bounded context, explicit outputs and host-enforced tools. |
| R11 | Build through BMForge, introducing new components there before deploying skills to Nd3G. | BMForge-first specification and acceptance-test work, followed by explicit pinning and consumer implementation. |
| R12 | Produce analysis, Mermaid analysis classes and documentation in an Nd3G PR targeting dev. | This documentation set; no executable implementation. |
| R13 | Include integrated web reporting like Ax3l, essential for inspecting the running system during development and troubleshooting; visualizations are nice to have. | A reporting service uses Nd3G's domain records and live service-query interfaces. State, decisions, errors and validation evidence come before optional charts. |
| R14 | Explore mitigation for AI-generated simulation code, including testing the module before deploying it. | A staged test/admission gate precedes candidate activation. Test execution itself is restricted, and testing, containment and score integrity are evaluated separately. |

## Observed baseline

Inspection is pinned to the revisions in the [source register](06-sources.md), not a claim about production state.

- **Nd3G:** an initial scaffold with metadata and four pinned baseline skills: project, constants, localization and installation. There is no implemented game or LLM runtime to extend yet. The inspected remote had only `main`; establishing `dev` is a repository setup decision, not an architectural dependency.
- **BMForge:** standalone specifications, templates, frozen references and project-local pinned skills. Its role convention is `activity/`, `interface/`, `entity/`; it does not provide a shared runtime framework. Current Nd3G pins originate from BMForge `29a100c39997349ecfd40e190319aeb5018ffab8`.
- **Ax3l:** the active loop selects one parameter or a prescribed pair, asks the model to propose a change, waits for a completed simulation and promotes only a strictly higher high score. It uses fresh conversations and numeric history. Its controller also contains seed rotation and restart reconciliation. Future Ax3l design notes must not be mistaken for this implemented behavior.
- **SnakeLab:** validates complete simulation configuration, queues runs serially, constructs fresh learning state, records episodes and terminal results, and exposes control plus separate best-effort telemetry/completion streams. Run-status lookup currently depends on process-local run objects; persisted winning snapshots are separate. Repeated submit requests create new run IDs, even if a correlation ID is reused.
- **Learning code:** `RNNModel` maps sequences to action values; `Trainer` implements recurrent Double DQN with a target model; `ReplayMemory` samples episode-aware windows. Reward shaping is currently intertwined with game transitions through `GameRules` and `RewardConfig`. A standalone writable `RewardFunction` is an extraction to design, not an existing drop-in module.
- **LlamaSrv:** manages llama.cpp inference separately from its browser control panel. Its documented application endpoint is `/v1/chat/completions`, with `/v1/models` for the actual model identifier. The repository defaults to Qwen3.5-4B; the user's statement establishes that it is deployed. This review did not probe the host, model quality, tool-calling reliability or effective context limits.

## Current tuning surface

Ax3l's own configuration schema, together with `SingleParameters` and `PairParameters`, is the authority for what it currently tunes. SnakeLab's broader schema is not identical: for example, Ax3l fixes `epochs` at 1500 while SnakeLab's schema defaults to 500.

| Group | Current LLM-controlled paths | Initial Nd3G treatment |
| --- | --- | --- |
| Model | `model.hidden_size` | Retain a typed value and validate against the selected model contract. |
| Training | `training.sequence_length`, `training.batch_size`, `training.learning_rate`, `training.gamma` | Retain all four; cross-validate model, replay and trainer together. |
| Exploration | `epsilon.initial`, `epsilon.decay` | Retain both; keep a host-owned schedule in the first module contract. |
| Reward shaping | `game.rewards.closer_to_food`, `game.rewards.further_from_food` | Retain both as inputs to the reward module. |

This is nine tunable values, with epsilon and reward values currently proposed as pairs. Nd3G need not inherit coordinate-only scheduling: the controller may request a complete coordinated proposal, with every field explicitly resolved. Copying an unchanged value from a named baseline counts as setting it; silence or an implicit default does not.

The current schema fixes other fields, including board dimensions, initial snake length, move-limit multiplier, several event rewards, model layers/dropout, replay capacity, target-update rate, gradient clipping and epsilon minimum. The seed is controller-managed. Keep those fixed in the first comparable baseline. Candidate extensions include layers, dropout, replay capacity, optimizer choice and target-update strategy; they require a reviewed search-space/contract revision and resource bounds, not an unrestricted configuration dictionary.

## Reviewed working assumptions

The user reviewed these assumptions on 2026-11-10 and said they look solid. Keep them as the working baseline; confirmation of these assumptions does not select an isolation technology, approve implementation or make untested capabilities real.

| ID | Working assumption | Consequence if changed |
| --- | --- | --- |
| A1 | One host and one active simulation initially. | Remote artifact transfer, authentication and competing resource allocation need additional design for multi-host or concurrent execution. |
| A2 | Preserve current board, observation/action meanings, episode budget and seed policy for the baseline. | A changed environment or budget produces a distinct comparison cohort, not a directly comparable record. |
| A3 | Retain MariaDB for durable experiment/run reporting, subject to component selection. | Another backend requires a separately approved BMForge component. No database is installed here. |
| A4 | Each candidate begins from fresh weights, replay, optimizer and exploration state. | Warm starts would be a different experiment with checkpoint provenance and fairness implications. |
| A5 | Generated Python may be defective or hostile even when produced locally. | Tests and production candidate execution both require the same reviewed restriction boundary. |
| A6 | Human review is required for new contracts, dependencies and skill releases, not for each ordinary candidate within an approved experiment policy. | Per-candidate approval can be selected later, but should not be silently inserted into the automated experiment. |

## Out of scope

No distributed training, generic agent marketplace, arbitrary shell tool, online dependency installation, new LLM deployment, automatic deployment of winning code into installed application services, automatic changes to BMForge pins, or compatibility layer preserving legacy application APIs. Candidate activation for a bounded simulation is distinct from an application release. Existing TUI behavior can be deliberately adapted to a clean Nd3G contract. Historical experiments remain historical; any import of old databases is separate work. The web reporting server is in scope; elaborate visualizations and browser-based experiment controls are not required for the first slice.
