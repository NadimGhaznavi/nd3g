# Use cases and analysis model

[Overview](README.md) · [Skills and candidates](03-skills-and-candidates.md)

## Modeling convention

The Unified Process analysis model describes logical responsibilities needed to realize use cases. It is not a list of Python files, database tables or daemons. The analysis stereotypes below map to BMForge as follows:

| Analysis stereotype | BMForge classification | Meaning here |
| --- | --- | --- |
| `control` | Activity | Coordinates a use case or owns an application decision. |
| `boundary` | Interface | Mediates interaction with an actor, external technology or another responsibility boundary. |
| `entity` | Entity | Holds experiment data and results independently of transport or persistence. |

This is a project mapping, not a claim that every implementation adapter must be a Unified Process analysis class. Later design may split or combine responsibilities. `RNNModel.py` and its fellow writable slots are design-level extension contracts, not automatically entity classes because they contain model data. Systemd and socket topology appear in the separate [runtime view](04-runtime-and-integrity.md).

## Actors and use cases

Primary actor: the **researcher**, who starts/stops an experiment, chooses its policy and inspects evidence. The existing **inference service** is a supporting actor. The simulation server and restricted candidate executor are internal Nd3G subsystem boundaries, not independent product actors.

| Use case | Trigger and success condition | Important alternative |
| --- | --- | --- |
| UC1 Configure an experiment | Researcher selects a baseline and policy; a reproducible experiment record exists. | Missing model, module contract or execution capability prevents readiness. |
| UC2 Prepare a candidate | Controller requests parameter/module tasks; one complete, validated candidate is frozen. | Invalid output produces bounded repair feedback or a recorded rejection. |
| UC3 Execute a candidate | Frozen candidate is accepted once; a terminal run result is durably recorded. | Timeout, cancellation, process failure or resource violation cannot become a successful score. |
| UC4 Assess a result | Completed result is compared under the experiment policy; champion decision is recorded. | Tie/lower score retains the champion; incomparable/failed runs are excluded. |
| UC5 Observe/control a run | TUI shows progress and accepts permitted pause/resume/cancel controls. | Missed telemetry triggers snapshot refresh, not invented completion. |
| UC6 Recover an experiment | A service restarts or a response is lost; durable state resolves what happened. | Unresolvable outcome stops that experiment with actionable status. |
| UC7 Inspect and diagnose the system | Researcher opens the web report; current activity, persisted history, candidate/test evidence and failures are inspectable. | A stopped service or stale observation is labeled explicitly while available historical evidence remains readable. |

## Outer-loop analysis classes

```mermaid
classDiagram
    class ResearchConsole {
        <<boundary>>
        selectExperiment()
        showEvidence()
    }
    class ConductExperiment {
        <<control>>
        chooseNextTask()
        advanceExperiment()
    }
    class PrepareCandidate {
        <<control>>
        resolveParametersAndModules()
        freezeCandidate()
    }
    class SkillSession {
        <<boundary>>
        requestProposal()
        returnToolFeedback()
    }
    class ValidateCandidate {
        <<control>>
        checkCompleteCombination()
        admitOrReject()
    }
    class SimulationAccess {
        <<boundary>>
        submitCandidate()
        queryRun()
    }
    class AssessResult {
        <<control>>
        checkComparability()
        selectChampion()
    }
    class ExperimentJournal {
        <<boundary>>
        recordProgress()
        recordDecision()
    }
    class Experiment {
        <<entity>>
        experimentId
        policyVersion
        baselineId
    }
    class Candidate {
        <<entity>>
        candidateId
        contentDigest
        parentCandidateId
    }
    class RunResult {
        <<entity>>
        runId
        terminalState
        highScore
    }
    class Champion {
        <<entity>>
        runId
        decisionId
    }
    ResearchConsole --> ConductExperiment : requests
    ConductExperiment --> PrepareCandidate : directs
    PrepareCandidate --> SkillSession : obtains proposals
    PrepareCandidate --> ValidateCandidate : checks
    PrepareCandidate --> Candidate : creates
    ConductExperiment --> SimulationAccess : submits and queries
    ConductExperiment --> AssessResult : requests comparison
    ConductExperiment --> ExperimentJournal : persists progress
    ConductExperiment --> Experiment : advances
    AssessResult --> RunResult : compares
    AssessResult --> Champion : selects
    AssessResult --> ExperimentJournal : records decision
    Experiment "1" --> "0..*" Candidate : contains
    Candidate "1" --> "0..*" RunResult : evaluated by
    Champion --> RunResult : identifies
```

### Responsibility boundaries

- **ConductExperiment** owns experiment progression, the task order, budgets, stop policy and restart position. It does not interpret Python source or issue SQL.
- **PrepareCandidate** assembles all required choices. **SkillSession** presents one skill's instructions, inputs and permitted tools to the LLM. Neither the model nor the skill decides whether a candidate passes admission.
- **ValidateCandidate** owns the admission decision based on complete-candidate checks and trusted validator results. It invokes execution through a restricted boundary; importing candidate modules in the controller is prohibited.
- **SimulationAccess** expresses submission/status/result operations in domain terms. It hides transport, not failure or uncertain outcomes.
- **AssessResult** applies the fixed comparison policy. It cannot accept an LLM claim of success as run evidence.
- **ExperimentJournal** abstracts durable progress and champion decisions. A later `ExperimentDb` interface owns SQL and composes with BMForge's unchanged `DbMgr`.
- **Candidate**, **RunResult**, **Experiment** and **Champion** carry values and identities. They do not save themselves, call LlamaSrv or own sockets. The diagram permits repeated evaluation of a candidate; a repetition is an explicit new run request, never a hidden retry.

## Simulation subsystem analysis classes

```mermaid
classDiagram
    class SimulationEndpoint {
        <<boundary>>
        acceptSubmission()
        answerStatus()
    }
    class ExecuteRun {
        <<control>>
        reserveRun()
        superviseExecution()
        finalizeResult()
    }
    class CandidateExecution {
        <<boundary>>
        launchRestrictedWork()
        exchangeActions()
        terminateWork()
    }
    class EvaluateGame {
        <<control>>
        applyGameRules()
        deriveScore()
    }
    class RunEvidenceStore {
        <<boundary>>
        saveEpisodeEvidence()
        commitTerminalResult()
    }
    class LiveRunView {
        <<boundary>>
        publishProgress()
        refreshSnapshot()
    }
    class Run {
        <<entity>>
        runId
        candidateDigest
        state
    }
    class EpisodeEvidence {
        <<entity>>
        episodeId
        actionTrace
        score
    }
    SimulationEndpoint --> ExecuteRun : invokes
    ExecuteRun --> Run : advances
    ExecuteRun --> CandidateExecution : controls
    ExecuteRun --> EvaluateGame : requests trusted evaluation
    ExecuteRun --> RunEvidenceStore : persists
    ExecuteRun --> LiveRunView : reports
    EvaluateGame --> EpisodeEvidence : produces
    Run "1" --> "0..*" EpisodeEvidence : contains
    RunEvidenceStore --> EpisodeEvidence : stores
```

**EvaluateGame** owns legal transitions, termination and food-count score. Candidate code may propose actions and compute training rewards, but cannot mutate this state. The separation is logical here; the [execution design](04-runtime-and-integrity.md#trusted-scoring-and-generated-code) must realize it across a real privilege boundary or independently verify every scored action trace.

## UC2–UC4: normal experiment iteration

```mermaid
sequenceDiagram
    participant C as ConductExperiment
    participant P as PrepareCandidate
    participant S as SkillSession
    participant L as External LlamaSrv inference
    participant V as ValidateCandidate
    participant X as Restricted execution boundary
    participant J as ExperimentJournal
    participant R as SimulationAccess
    participant E as ExecuteRun
    participant A as AssessResult
    C->>P: Prepare from baseline and experiment policy
    loop Each required configuration task
        P->>S: Selected skill, bounded context, permitted tools
        S->>L: Request a structured proposal
        L-->>S: Parameter or module proposal
        S-->>P: Validated tool result and proposed artifact
    end
    P->>V: Validate complete candidate revision
    V->>X: Contract and smoke checks for exact content
    X-->>V: Trusted validation evidence
    V-->>P: Admit with bound content digest
    P->>J: Save immutable candidate and provenance
    P-->>C: Candidate identity
    C->>J: Save submission intent and idempotency key
    C->>R: Submit candidate with key
    R->>E: Admit and reserve run atomically
    E-->>R: Accepted with run ID
    R-->>C: Accepted, not completed
    E->>X: Execute admitted content
    Note over E,X: Trusted game scoring stays outside candidate authority
    E->>E: Persist terminal result before notification
    C->>R: Query authoritative result
    R-->>C: Completed result and evidence references
    C->>A: Compare against current champion
    A->>J: Atomically record comparison and champion choice
    A-->>C: Next champion and iteration evidence
```

## UC2 alternative: a candidate is rejected

```mermaid
sequenceDiagram
    participant P as PrepareCandidate
    participant S as SkillSession
    participant V as ValidateCandidate
    participant J as ExperimentJournal
    P->>V: Validate revision N
    V-->>P: Reject with stage, contract and bounded diagnostics
    P->>J: Record rejection and attempt cost
    alt Repair budget remains
        P->>S: Request repair of named slot
        S-->>P: New revision N+1
        P->>V: Revalidate changed content and all dependent contracts
    else Budget exhausted
        P->>J: Record rejected candidate and retain champion
    end
    Note over P,J: No simulation submission and no fabricated score
```

## UC6 alternative: the submit reply is lost

```mermaid
sequenceDiagram
    participant C as ConductExperiment
    participant J as ExperimentJournal
    participant S as SimulationEndpoint
    participant D as RunEvidenceStore
    C->>J: Record intent with key K and candidate digest
    C->>S: Submit with K
    S->>D: Atomically create K-to-run reservation
    S--xC: Accepted reply is lost
    C->>J: Record uncertain submission
    C->>S: Query submission K
    S->>D: Look up durable reservation
    D-->>S: Existing run and current state
    S-->>C: Original run ID and state
    C->>J: Reconcile, then track that run
    Note over C,S: Only a proven absent key permits bounded resubmission with the same K
```

No diagram implies that today's SnakeLab already provides durable idempotency, a restart-safe queue or candidate isolation. Those are explicit Nd3G contract additions.

## UC7: integrated reporting responsibilities

```mermaid
classDiagram
    class ReportingPages {
        <<boundary>>
        requestReport()
        displayEvidence()
    }
    class InspectExperiment {
        <<control>>
        assembleReport()
        distinguishFreshness()
    }
    class SystemStatusAccess {
        <<boundary>>
        queryController()
        querySimulation()
    }
    class ExperimentEvidenceAccess {
        <<boundary>>
        readHistory()
        readValidationEvidence()
    }
    class ReportSnapshot {
        <<entity>>
        observedAt
        sourceStatus
        experimentId
        runId
    }
    ReportingPages --> InspectExperiment : requests
    InspectExperiment --> SystemStatusAccess : obtains bounded live observations
    InspectExperiment --> ExperimentEvidenceAccess : reads persisted evidence
    InspectExperiment --> ReportSnapshot : assembles
    ReportingPages --> ReportSnapshot : presents
```

**ReportingPages** translates requests and presents results, including safely escaped code/log text. **InspectExperiment** assembles domain views without changing the experiment. **SystemStatusAccess** reports the outcome and observation time of each live query, including timeout. **ExperimentEvidenceAccess** uses the application's named read-only data operations for history, candidate provenance, test reports and failures. **ReportSnapshot** carries values and freshness metadata. These analysis roles do not mandate a new generic reporting framework or a separate class for every page.

```mermaid
sequenceDiagram
    actor R as Researcher
    participant P as ReportingPages
    participant I as InspectExperiment
    participant H as ExperimentEvidenceAccess
    participant S as SystemStatusAccess
    R->>P: Inspect experiment or failed candidate
    P->>I: Request bounded report
    I->>H: Read persisted progress and test evidence
    H-->>I: Records with timestamps and identities
    I->>S: Query controller and simulation status
    alt Services respond
        S-->>I: Live observations with observed times
    else Service unavailable or query timed out
        S-->>I: Explicit unavailable status for that service
    end
    I-->>P: Report with separate live and persisted sections
    P-->>R: Inspectable state and failure evidence
    Note over P,S: A report refresh does not mutate or delay the experiment
```
