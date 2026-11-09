# Runtime boundaries and execution

[Overview](README.md) · [BMForge adoption](05-bmforge-and-delivery.md)

## Process and component view

This is a deployment/design view, separate from the analysis classes. Unit names are proposed. There are two new long-running Nd3G services, not one service for each skill or class.

```mermaid
flowchart TB
    Researcher[Researcher] --> TUI[Nd3G TUI]
    subgraph External[Existing external deployment]
        LLM[LlamaSrv-managed llama.cpp and Qwen 3.5 4B]
    end
    subgraph ND[Nd3G application]
        C[nd3g.service: experiment controller]
        S[nd3g-simulation.service: simulation supervisor and trusted game]
        A[(Finalized candidate artifacts)]
        DB[(MariaDB: separately owned experiment and run records)]
        subgraph Restricted[Per-run restricted execution boundary]
            W[Learning worker: generated model, trainer, replay and reward]
        end
        C -->|Inference API| LLM
        C -->|Finalize and read| A
        C -->|Control and result queries| S
        C -->|Experiment records| DB
        S -->|Read verified artifacts| A
        S -->|Run evidence| DB
        S -->|Observations and permitted transition facts| W
        W -->|Actions and untrusted learning diagnostics| S
    end
    TUI -->|Snapshot and operator controls| S
    TUI -->|Experiment status| C
    S -.->|Best-effort live telemetry| TUI
```

The learning worker is a bounded child workload, not another permanent systemd daemon. The simulation supervisor remains responsive while learning code runs and owns cancellation/time limits. Execution may require an isolated launcher or systemd transient scope; the mechanism is an open, security-relevant design decision, not an already selected dependency.

The controller never imports candidate modules. It calls the existing inference endpoint, not the unauthenticated LlamaSrv control panel. It has no reason to restart or reconfigure the shared inference service. Starting Nd3G should check inference readiness and report a failure rather than take ownership of LlamaSrv.

For the application-owned services, future `scripts/services start` should start simulation then controller; `stop` should stop controller then simulation. Keep the sequential helper required by BMForge. Unit dependency/readiness semantics, least-privilege service accounts, directories, resource limits and shutdown deadlines belong to the approved installation specification, not this documentation change.

## Communication contract

Reuse ZeroMQ for short control/query requests, with handlers returning promptly after durable acceptance. Preserve separate control and observation concerns, not the old protocol byte for byte. Deliberately adapt the TUI and controller to one new contract rather than add legacy compatibility shims.

BMForge's inspected `bmforge.zmq-server` 0.4.0 is **REQ/REP only**, using a socket-owning thread. SnakeLab's asyncio control implementation and PUB/SUB channels are not compliant drop-ins. Adopt BMForge's control mechanics and domain handlers. Introduce the needed telemetry specification in BMForge first; do not claim its current skill already authorizes PUB/SUB or asyncio transport infrastructure.

Proposed envelope: BMForge's `protocol_version`, `sender`, `target`, `method`, object `payload`, plus an explicitly specified `request_id` correlation contract. A version is an integer, not a Boolean. Validate finite numeric payloads, Unicode, size, method and exact response correlation. Routing labels are not authentication. Use one configured local endpoint transport, with access controls and no automatic TCP/IPC fallback. Remote access needs a separate security review.

| Operation | Responsibility and result |
| --- | --- |
| `submit` | Candidate digest plus idempotency key; return run ID and accepted state only after reservation is durable. |
| `submission-status` | Resolve an idempotency key after a lost reply, including after restart. |
| `run-status`, `run-result` | Authoritative current/terminal state and persisted result, not only in-memory objects. |
| `active-run`, `snapshot` | Reconstruct live display and detect no active run without requiring event delivery. |
| `pause`, `resume`, `cancel` | Operator controls with explicit state/result semantics and bounded acknowledgement. |
| `high-score-snapshot`, `high-score-frames` | Preserve current winning-game inspection and animation inputs. |
| `health` | On-demand readiness of required application dependencies through existing interfaces. |

Transport requests have finite overall deadlines and explicit socket ownership. A timed-out mutation has an unknown outcome until reconciled. The domain layer, not a generic transport retry loop, owns any permitted retry.

### Submission and state ownership

- The controller durably writes submission intent before sending. The simulation service atomically reserves `(experiment_id, idempotency_key)` with the candidate digest and run ID. Same key/same digest returns the existing run; same key/different content is a conflict.
- A durable queued-run record is the source of truth. An in-memory queue is at most a scheduling aid. Begin with one executing run and a small, explicitly bounded admission capacity; no broker or distributed scheduler is needed.
- Persist terminal results before publishing notifications. Retain deduplication records at least as long as experiment records, and never permit an expired key silently to mean a new run.
- Idempotency prevents duplicate admission, not magical exactly-once execution. Record execution attempts. After supervisor failure, reconcile/terminate any surviving child before another attempt. Mark a lost running attempt `interrupted`; do not resume training weights implicitly. A fresh run requires an explicit experiment-policy decision and a new run identity.
- On controller restart, query the saved key/run, recover an already committed comparison and continue from durable progress. Commit comparison and champion choice atomically, using the expected champion revision so a stale result cannot overwrite a later choice.

Proposed run states: `queued`, `running`, `paused`, `cancelling`, and terminal `completed`, `failed`, `cancelled`, `interrupted`. Queued cancellations never execute. Cancellation acknowledgement is not terminal cancellation; the supervisor confirms the child stopped before finalization. A paused process after service restart is interrupted unless a separately designed checkpoint capability exists.

## Trusted scoring and generated code

Code generation expands the trust boundary. Read-only source files, Python AST filters, import allowlists, a subprocess, systemd restart policy and per-process service separation do **not** by themselves stop malicious Python, native extensions, resource exhaustion or score fabrication.

Recommended realization: the trusted game/evaluator remains outside the candidate's restricted process. It owns legal moves, food placement, collisions, termination, episode budgets and score. The learning worker receives bounded observations/transition facts and returns actions. The supervisor validates these inputs and derives metrics itself. Candidate-reported reward/loss is labeled learning telemetry, never authoritative score.

An alternative is isolated whole-simulation execution followed by trusted replay of the **full** action evidence for every scored episode, using fixed seeds and evaluator revision. It may reduce per-step boundary overhead, but validation cost and completeness are substantial. Verifying only the claimed winning frame or a candidate-supplied summary is insufficient. Benchmark the recommended per-step boundary before choosing the alternative.

Required restriction properties, to be specified and tested before generated code runs:

- no database credentials, LlamaSrv/service-control credentials, host secrets, writable application source, other runs or controller sockets;
- no network access and no inherited privileged handles;
- read-only approved runtime/artifacts and a bounded private scratch area;
- bounded CPU, memory, process count, file output, wall time and device allocation;
- no ability to write authoritative result records, validator results or game state;
- bounded shutdown that terminates descendants and records failure visibly.

Select a concrete OS containment mechanism and its approved modules in BMForge. GPU access is especially important: device exposure, drivers and native libraries can weaken isolation, and GPU-memory limits are not automatically enforced by ordinary systemd memory controls. Until the mechanism is demonstrated on the actual host, code-mutating experiments are blocked; parameter-only experiments using trusted fixed modules remain a separate eligible stage. This is a design gate, not a guarantee that finite tests prove total security.

## Scoring, reporting and reproducibility

The initial champion rule remains Ax3l's: two completed, comparable runs with recorded high scores; promote only if `candidate.high_score > champion.high_score`. Ties retain the champion. A failure, interruption or invalid run never counts as a zero-score completed run. Preserve episode counts, total steps, rewards, losses, high score, winning snapshot/frames and golden-history reporting where applicable, adding candidate/module/skill identities and failure categories.

Learning reward and food-count score are separate. A reward function cannot improve the experiment merely by returning larger numbers. Likewise, generated modules cannot increase the episode budget or change the board to manufacture higher records.

A single-run maximum is noisy and benefits from a larger search/episode budget. Keep it for continuity, but label it a best observed score rather than proof of general improvement. Supplement reports with seed, episode budget, parameter/code differences, compute cost and failure/repair counts. A later confirmation cohort with fixed seeds and repeated runs can assess robustness without silently replacing the existing champion rule. Recommended, pending confirmation against Ax3l's seed-rotation behavior: establish a fresh comparable baseline when rotating seeds. Do not compare across changed rules or budgets as if they were the same experiment.

Record software/dependency versions, hardware/device details, seed derivation, model/skill settings and exact artifacts. Reproduction means sufficient evidence to rerun under known conditions; bit-for-bit GPU determinism is not promised without testing the chosen stack.

## TUI first, browser later

Reuse the existing board, plots and run controls. Likely changes include endpoint/package names, the new envelope and result-query contract, candidate/module identities, validation status and reconnect/snapshot handling. The current client already speaks SnakeLab-specific contracts, so “minor tweaks” is a hypothesis to validate, not a guarantee.

Live messages are disposable: bounded queues, documented overflow policy, publisher-instance identity and sequence numbers aid diagnosis. A sequence cannot reveal drops occurring before numbering unless local drop counters are also exposed. Completion notifications prompt a durable query. A TUI disconnect or slow subscriber must not stall the experiment.

An optional browser UI could help compare source diffs and long experiment histories. It would require deliberate HTTP/visualization component selection and should consume the same domain queries, not reach directly into run tables or become another experiment controller. Do not build both interfaces in the first iteration.
