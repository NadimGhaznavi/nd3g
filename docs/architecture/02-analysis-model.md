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

Primary actor: the **researcher**, who starts/stops an experiment, chooses its policy and inspects evidence. The existing **inference service** is a supporting actor. The simulation server and disposable execution environment are internal Nd3G subsystem boundaries, not independent product actors.

| Use case | Trigger and success condition | Important alternative |
| --- | --- | --- |
| UC1 Configure an experiment | Researcher selects a baseline and policy; a reproducible experiment record exists. | Missing model, module contract or execution capability prevents readiness. |
| UC2 Prepare a candidate | Controller requests parameter/module tasks; one complete, validated candidate is frozen. | Invalid output produces bounded repair feedback or a recorded rejection. |
| UC3 Execute a candidate | Frozen candidate is accepted once; a fresh simulation environment produces captured evidence, inspected and imported before successful completion. | Timeout, rejection, failed import or cleanup is recorded distinctly; a sandbox completion flag is not a successful score. |
| UC4 Assess a result | Completed result is compared under the experiment policy; champion decision is recorded. | Tie/lower score retains the champion; incomparable/failed runs are excluded. |
| UC5 Observe/control a run | TUI shows progress and accepts permitted pause/resume/cancel controls. | External consumers distinguish provisional telemetry from accepted results and reconnect to the next run’s endpoint. |
| UC6 Recover an experiment | A service restarts or a response is lost; external durable intent, capture/import receipts and environment identity resolve what happened. | Unresolvable outcome stops that experiment with actionable status. |
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
- **SimulationAccess** expresses submission/status/result operations in domain terms. It addresses the persistent lifecycle owner outside the sandbox and hides transport, not failure or uncertain outcomes.
- **AssessResult** applies the fixed comparison policy. It reads only accepted imported results, never a sandbox or LLM claim of success.
- **ExperimentJournal** abstracts durable progress and champion decisions. A later `ExperimentDb` interface owns SQL and composes with BMForge's unchanged `DbMgr`.
- **Candidate**, **RunResult**, **Experiment** and **Champion** carry values and identities. They do not save themselves, call LlamaSrv or own sockets. The diagram permits repeated evaluation of a candidate; a repetition is an explicit new run request, never a hidden retry.

## Simulation subsystem analysis classes

```mermaid
classDiagram
    class SimulationEndpoint {
        <<boundary>>
        acceptSubmission()
        answerDurableStatus()
    }
    class ManageRun {
        <<control>>
        reserveRun()
        advanceLifecycle()
        reconcileCleanup()
    }
    class RunEnvironmentAccess {
        <<boundary>>
        createFreshEnvironment()
        captureArtifacts()
        stopAndDispose()
    }
    class ExecuteSimulation {
        <<control>>
        runEpisodes()
        finalizeTemporaryEvidence()
    }
    class EvaluateGame {
        <<control>>
        applyGameRules()
        deriveProvisionalScore()
    }
    class SimulationEvidenceStore {
        <<boundary>>
        saveTemporaryRecords()
        exportRunData()
    }
    class LiveRunView {
        <<boundary>>
        publishGameState()
        answerSnapshot()
    }
    class InspectRunArtifacts {
        <<control>>
        checkBundle()
        acceptOrReject()
    }
    class ResultArchive {
        <<boundary>>
        recordLifecycle()
        importAcceptedResult()
        queryImportReceipt()
    }
    class Run {
        <<entity>>
        runId
        candidateDigest
        executionState
        resultDisposition
        cleanupState
    }
    class ArtifactBundle {
        <<entity>>
        runId
        capturedDigest
        evidenceManifest
    }
    class InspectionDecision {
        <<entity>>
        policyVersion
        bundleDigest
        outcome
        assuranceLevel
    }
    SimulationEndpoint --> ManageRun : invokes outside sandbox
    ManageRun --> Run : advances
    ManageRun --> RunEnvironmentAccess : controls lifetime
    RunEnvironmentAccess --> ExecuteSimulation : launches inside sandbox
    ExecuteSimulation --> EvaluateGame : runs static game
    ExecuteSimulation --> SimulationEvidenceStore : persists temporarily
    ExecuteSimulation --> LiveRunView : publishes provisionally
    RunEnvironmentAccess --> ArtifactBundle : captures externally
    ManageRun --> InspectRunArtifacts : requests inspection
    InspectRunArtifacts --> ArtifactBundle : checks immutable evidence
    InspectRunArtifacts --> InspectionDecision : records
    ManageRun --> ResultArchive : imports only accepted data
    ResultArchive --> InspectionDecision : verifies acceptance
    Run "1" --> "0..1" ArtifactBundle : finalized evidence
```

**ManageRun** owns the durable lifecycle outside the disposable environment. **RunEnvironmentAccess** hides the selected launcher/capture/disposal technology, not uncertain outcomes. **ExecuteSimulation**, **EvaluateGame**, **SimulationEvidenceStore** and **LiveRunView** are static simulation responsibilities inside the environment. They use temporary MariaDB and invoke only the allowed generated slots. Neither a MariaDB process nor a systemd unit is itself an analysis class.

**InspectRunArtifacts** applies the selected inspection policy to externally captured immutable data; **ResultArchive** owns the persistent import and deduplication contract. Domain interfaces own SQL. Inspection acceptance, successful import and cleanup are distinct decisions/facts. Temporary records and ZMQ observations do not bypass this boundary. **EvaluateGame** owns legal transitions and food-count scoring in the static code, but shared-process Python can still alter runtime state; [result integrity](04-runtime-and-integrity.md#trusted-scoring-and-generated-code) remains an explicit design concern rather than an assumed guarantee.

## UC2–UC4: normal experiment iteration

```mermaid
sequenceDiagram
    participant C as ConductExperiment
    participant P as PrepareCandidate
    participant S as SkillSession
    participant L as External LlamaSrv inference
    participant V as ValidateCandidate
    participant J as Persistent journal and result archive
    participant R as ManageRun outside sandbox
    participant X as Disposable simulation and temporary MariaDB
    participant I as InspectRunArtifacts outside sandbox
    participant A as AssessResult
    C->>P: Prepare from baseline and experiment policy
    loop Each required configuration task
        P->>S: Selected skill, bounded context, permitted tools
        S->>L: Request structured proposal
        L-->>S: Parameter or module proposal
        S-->>P: Proposed artifact and tool feedback
    end
    P->>V: Check complete revision in fresh restricted test environment
    V-->>P: Admit exact candidate with test evidence
    P->>J: Save immutable candidate and provenance
    P-->>C: Candidate identity
    C->>R: Submit candidate with idempotency key
    R->>J: Atomically reserve run before launch
    R-->>C: Accepted run ID, not completed
    R->>X: Create clean runtime and temporary DB, then execute
    Note over X: Static publisher sends provisional ZMQ state to external viewers
    X-->>R: Execution ends with provisional evidence
    R->>X: Stop writers and capture bounded consistent artifacts
    R->>J: Record immutable capture and external exit outcome
    R->>I: Inspect captured bundle under versioned policy
    I-->>R: Accepted bundle digest and inspection decision
    R->>J: Atomically import accepted data with receipt
    R->>X: Stop and dispose environment and temporary DB
    R->>J: Record confirmed cleanup
    C->>J: Read accepted imported result
    C->>A: Compare under experiment policy
    A->>J: Atomically record comparison and champion choice
```

The test environment is also disposable and uses the same approved runtime/policy; its state is not reused for the full simulation. Candidate admission and post-run result inspection are separate gates. The normal diagram assumes inspection accepts; the next alternative covers rejection and interrupted import.

```mermaid
sequenceDiagram
    participant M as ManageRun
    participant A as Captured artifact store
    participant I as InspectRunArtifacts
    participant D as Persistent result archive
    participant X as Disposable environment
    M->>A: Seal captured bundle for run R
    M->>I: Inspect exact captured digest
    alt Rejected or incomplete evidence
        I-->>M: Rejection and bounded reason
        M->>D: Record failure and retained evidence reference
        M->>X: Stop and dispose, then record cleanup
        Note over M,D: No successful result or champion promotion
    else Accepted but import reply is lost
        I-->>M: Accepted under recorded policy
        M->>D: Import run R and bundle digest atomically
        D--xM: Receipt reply is lost
        M->>D: Query import receipt for R and digest
        alt Receipt exists
            D-->>M: Original import outcome
        else Proven absent
            M->>D: Retry same accepted-data transaction
        end
        M->>X: Dispose only after durable outcome or verified capture
        M->>D: Record cleanup independently
    end
```

If the archive is unavailable, stop execution and retain verified captured evidence for later reconciliation. Do not treat an unavailable receipt query as proof that import did not commit. Disposal failure is visible and blocks another environment launch; it does not erase an already accepted result.


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
    participant S as External SimulationEndpoint
    participant D as Persistent run journal
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

The lost-reply reservation belongs to the external journal, never temporary MariaDB. No diagram implies that today's SnakeLab already provides durable idempotency, a restart-safe queue, inspected import or candidate isolation. Those are explicit Nd3G contract additions.

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
        readProvisionalSimulationState()
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

**ReportingPages** translates requests and presents results, including safely escaped code/log text. **InspectExperiment** assembles domain views without changing the experiment. **SystemStatusAccess** consumes bounded ZMQ state from the static in-sandbox publisher and queries external lifecycle status or a bounded snapshot. It records run/publisher identity, observation time, timeout and stale/provisional state, without reading temporary MariaDB. **ExperimentEvidenceAccess** uses the application's named read-only data operations for history, candidate provenance, test reports and failures. **ReportSnapshot** carries values and freshness metadata. These analysis roles do not mandate a new generic reporting framework or a separate class for every page.

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
    I->>S: Read controller lifecycle and latest provisional ZMQ state
    alt Current observations available
        S-->>I: Provisional observations with run identity and times
    else Environment gone or observation stale
        S-->>I: Explicit unavailable or stale state
    end
    I-->>P: Report with separate live and persisted sections
    P-->>R: Inspectable state and failure evidence
    Note over P,S: A report refresh does not mutate or delay the experiment
```
