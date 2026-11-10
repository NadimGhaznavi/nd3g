# BMForge adoption and iteration plan

[Overview](README.md) · [Source register](06-sources.md)

## Specification first, application adoption second

This proposal belongs in Nd3G because it defines the application. It does not change BMForge specifications, install optional skills or imply that proposed technologies are approved. Subsequent work must preserve the repository boundary:

1. Agree on Nd3G use cases, responsibility boundaries and acceptance scenarios.
2. Introduce or amend each required component **in BMForge**, with a specification ID/version/status, approved runtime-module inventory, references/templates, skill packaging and acceptance checks. Record policy decisions in BMForge's decision record.
3. Review and merge that BMForge work. A draft specification label is not evidence of implementation readiness.
4. With explicit adoption approval, install/update the relevant pinned Nd3G skills and lock. Do not hand-edit their vendored instructions or import BMForge at runtime.
5. Implement application-owned activities, interfaces and entities in a separately authorized Nd3G task. Copy the canonical `DbMgr` unchanged if selected; put SQL in domain `*Db` interfaces.
6. Pass component acceptance checks in Nd3G, record the literal `BMFORGE_COMPONENT` marker in each owning module and update the changelog. The marker states provenance, not certified compliance.

```mermaid
flowchart LR
    R[Nd3G requirements and analysis] --> B[BMForge component specification]
    B --> T[Template, skill and acceptance checks]
    T --> V[Review and merge in BMForge]
    V --> P[Explicit pinned-skill adoption in Nd3G]
    P --> I[Nd3G-owned implementation]
    I --> A[Acceptance and architecture review]
    A --> D[Separately authorized deployment]
    A -->|Contract gap| B
```

## Component inventory and gaps

| Component/capability | Current evidence | Proposed next work |
| --- | --- | --- |
| Project, constants, localization, installation | Already pinned in Nd3G; installation stubs do not deploy the runtime. | Keep pins unchanged for this proposal. Complete the actual controller/simulation/reporting lifecycle before first release; source-language UI keys from the first feature. |
| Control/query transport | BMForge `bmforge.zmq-server` 0.4.0, draft, REQ/REP with thread-owned sockets. Not installed in Nd3G yet. | Explicitly select it; specify Nd3G envelope correlation and domain admission/query semantics without replacing its approved infrastructure. |
| Durable data access | BMForge `bmforge.db-server` 0.5.0, draft, MariaDB/PyMySQL. Not installed in Nd3G yet. | Select after architecture approval; unchanged manager, separate experiment/run interfaces and owned tables. Use required charset/collation and application-mediated health checks. |
| Required web reporting | Ax3l has an independent HTTP reporting process integrated with its state/events. BMForge HTTP 0.5.1 supplies app-owned HTTP/Jinja2 patterns; it is not installed in Nd3G yet. | Select the HTTP skill explicitly during implementation. Build read-only state, history, candidate and test-detail pages using the same application domain records and bounded live queries. Follow autoescaping, request limits, truthful health and local-time display requirements. |
| Optional reporting visuals | BMForge visualization 0.1.0 provides capability-selected approved browser libraries. | Add only useful charts/graphs to the existing reporting server. Text/tables/detail pages need no visualization library; do not add a visualization service. |
| Live telemetry | SnakeLab has PUB/SUB reference behavior; current BMForge REQ/REP skill does not cover it. | New telemetry component specification for framing, socket ownership, bounded queues, drops, restart identity and snapshot reconciliation. |
| Runtime task skills and inference client | No inspected BMForge component establishes this contract. | New component for task-package format, registry, narrow tool dispatch, bounded inference interaction, audit and model/skill evaluation. Do not assume the HTTP-server component supplies an inference client. |
| Candidate artifacts and restricted execution | Generated module admission and isolation are new requirements. | New component for immutable bundles, validation evidence, restricted execution, resource controls and trusted output boundary. Select containment technology and dependencies before implementation. |
| Configurable learning modules | Current SnakeLab code is a reference, not a modular code-generation contract. | Nd3G-driven BMForge component for model/replay/trainer/reward slots and fixtures. Inventory existing PyTorch/NumPy needs explicitly; no arbitrary packages in candidates. |
| TUI | Existing Textual client is useful source behavior, not a selected BMForge runtime inventory. | Specify the reused client boundary and approved dependencies before adaptation. Retain its real-time simulation role alongside required web inspection. |

Rows that call for a new component are **proposed capabilities**, not existing skill IDs or released components. Their final grouping/names should follow actual reuse and acceptance boundaries. Do not create a generic framework merely because multiple responsibilities are documented.

Keep Nd3G domain policies in Nd3G: what a high score means, the seed schedule, champion selection, candidate task ordering and report content. BMForge defines how component contracts are built and adopted. Its specification can include the required Nd3G module contracts without importing live application code or imposing Snake mechanics on unrelated applications.

## Unified Process-style iterations

Use-case-driven, architecture-centric and risk-first iterations avoid treating these documents as a waterfall contract. Each iteration yields reviewed evidence, not simply more class names.

| Stage | Narrow outcome | Exit evidence |
| --- | --- | --- |
| Inception | Agree on experiment scope, baseline, reporting requirement, success definition and writable slots. | R1–R14 traced; reviewed assumptions retained; open decisions assigned; baseline records identified. |
| Elaboration A | Prove the LlamaSrv skill interaction and complete-candidate contract. | Representative Qwen parameter and code tasks measured for valid outputs, repair cost and context limits; no claim based on model size alone. |
| Elaboration B | Evaluate the test/containment/score boundary on the intended host. | Pre-activation module tests and policy probes run in restricted workers; actual controls, timeout/child cleanup, GPU limits and residual risks are documented. Choose the integrity path after measuring feasibility. Code mutation stays disabled when required controls are absent. |
| Construction A | Establish controller, simulation and reporting with trusted fixed learning modules. | Serial parameter-only loop, persistent results, current scoring, basic web inspection, TUI observation and restart reconciliation pass end to end. Reports remain useful when an experiment service stops. |
| Construction B | Enable bounded module variation incrementally. | Reward slot first after extraction tests; then model/replay/trainer with combined contract tests. Each slot has independent versioned fixtures. |
| Construction C | Refine runtime skills using experiment evidence. | Compare parameter-only versus parameter-plus-code under declared budgets; inspect code and failed attempts, not only record wins. |
| Transition | Complete and validate installation, operations and reproducibility. | Install/upgrade/uninstall, service helper, health, ownership/version records and operator documentation verified before authorized deployment. |

These are future implementation increments. This PR supplies analysis only and does not execute them. No dates or performance guarantees are inferred.

## Architecture acceptance scenarios

| Scenario | Expected evidence | Requirements |
| --- | --- | --- |
| All current knobs represented | Nine current tunable values are explicitly resolved; fixed values and seed policy are separately identified. | R6, R8 |
| Missing or changed artifact | Missing slot, modified digest or stale validation prevents admission; previous champion stays intact. | R7, R8 |
| Cross-module mismatch | Model/replay/trainer dimension or parameter incompatibility fails before a scored run. | R7, R8 |
| Malformed/looping model response | Structured error and bounded repair/turn budget; no fabricated tool execution. | R2, R10 |
| Candidate tries to forge score | The selected trusted evaluation/replay path rejects fabricated metrics before champion comparison; test the implementation rather than assume process separation suffices. | R1, R7, R9, R14 |
| Candidate hangs or allocates excessively | Defined resource failure, descendants stopped, supervisor responsive, no credential/source access. | R3, R4, R7 |
| Lost submit response | Query by persistent idempotency key returns the original run; no duplicate admission. | R3, R8 |
| Restart at each state transition | Durable records reconcile queued/running/terminal states; interrupted work never silently resumes or becomes completed. | R3, R4, R9 |
| Telemetry lost or TUI detached | Simulation continues; snapshots/results recover the view; completion is not inferred from PUB delivery. | R5, R9 |
| Reward magnitude increases | Training reward may change while food-count score remains independently computed. | R1, R7, R9 |
| Run ties or fails | Tie retains champion; failed run is excluded, with clear cause and cost. | R1, R9 |
| Component adopted | Exact approved pin, module inventory, provenance marker and consumer acceptance evidence exist. | R11 |
| Module tested before activation | Import/contract/invariant and combined smoke tests run under selected restrictions; admission binds to the exact artifact and environment; a changed artifact is retested. | R7, R8, R14 |
| Report during service failure | Web pages distinguish live unavailable state from timestamped persisted evidence and link to the failed task/run. No empty-success or fabricated current state. | R3, R4, R13 |
| Untrusted text in a report | Candidate source, model output and logs display as escaped bounded text, never execute as HTML/script or Python objects. | R13, R14 |
| Reporting load and freshness | Paginated reads and bounded live queries do not block training; a page refresh cannot mark stale data fresh. Essential reports work without optional chart libraries. | R9, R13 |

## Open decisions for architecture review

1. **Execution boundary:** choose the least complex mechanism whose tested restrictions and residual risk are acceptable on the host. Compare restricted OS worker/container options before adding a stronger VM boundary; review GPU access separately. Test before activation, but do not equate passing tests with containment.
2. **Resource policy:** choose CPU/GPU placement, hard limits, repair/turn budgets, maximum source size and admission capacity. LlamaSrv and simulation may contend for the same GPU; do not assume concurrent operation is free.
3. **Experiment comparison:** confirm Ax3l's 1500-episode baseline and seed-rotation policy, and whether repeated confirmation runs should be a separate reporting cohort. Preserve the current high-score rule unless explicitly changed.
4. **Runtime skill protocol:** verify actual llama.cpp/Qwen native tool and structured-output support, then select one explicit supported contract and context budget.
5. **Expansion of the search space:** begin with the nine current values and four named module slots; decide which additional hyperparameters/algorithm variants warrant the next contract version.
6. **Reporting placement and integrity path:** web inspection is required. A separate reporting process is recommended for troubleshooting independence; confirm its deployment/exposure details. Separately validate protected game/learning exchange versus trusted replay of full run evidence, including throughput cost.
7. **Persistence organization:** recommend one application-owned database with explicit experiment/run table ownership and separate domain interfaces; decide final schema and artifact retention/backup policy during design. The controller accesses simulation results through its domain API, not ad hoc joins into simulation tables.

## Verification of this documentation change

- Inspected repository requirements, pinned baseline skills, BMForge component specifications and representative active Ax3l/SnakeLab/LlamaSrv code, including Ax3l's HTTP reporting, event detail, live queries and cached projections for this second draft.
- Materialized Nd3G's pinned files and verified their hashes with the offline BMForge `verify` operation. No skills were updated.
- Reproduced the rejected-candidate sequence failure on Mermaid 11.17.2 and 12.3.0, then verified the semicolon correction. All 10 second-draft Mermaid blocks pass both parsers. This verifies syntax, not visual layout; browser rendering was unavailable in the validation environment.
- Checked relative links and heading targets, balanced Markdown fences, changelog structure and preservation of repository instructions. A second architecture review found no material issues.
- The normal BMForge update check was unavailable in the connector-materialized workspace because it lacked the expected Git/cache checkout. The separately inspected upstream source revision matched Nd3G's lock; that observation is not a substitute for a successful local update check.
- This is not an application test result or evidence of runtime isolation. Proposed acceptance scenarios remain to be implemented and run in later work.
