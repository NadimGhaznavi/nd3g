# Mitigating risk from generated simulation code

[Overview](README.md) · [Candidate contracts](03-skills-and-candidates.md) · [Runtime boundaries](04-runtime-and-integrity.md)

## Whole-simulation sandbox, with tests before activation

The selected placement is a fresh disposable environment containing the simulation server and temporary MariaDB. Only the named module slots are LLM-writable; game rules, ZMQ publishing, storage and export remain static application code. The external controller owns environment lifetime. TUI/reporting consumers stay outside, and persistent results are written only after captured artifacts pass external inspection. This replaces the earlier preferred topology of a permanent trusted game service outside a learning-only worker. The containment product and inspection mechanism remain open.

### Test before activation

The proposed minimum workflow is: create a candidate in a staging area, run trusted module tests and a short combined simulation, inspect the evidence, then activate the **same tested artifacts** for a bounded full run. “Deployment” here means selecting a candidate for an experiment. It does not mean installing generated files over Nd3G's application code, changing systemd units or automatically releasing a champion.

This is useful even for a local, single-user system. Most failures will look mundane: a wrong tensor shape, a trainer that stops learning, replay memory that crosses episodes, NaN rewards, an infinite loop or excessive GPU allocation. Tests can catch these before a long experiment consumes time and resources.

However, a Python module can execute arbitrary work when imported. Running a test suite on the host first and isolating only the later simulation puts the risk in the wrong place. The disposable test environment must receive the same reviewed restrictions as the full simulation from its first import. Use the same runtime, schema and static simulation code for combined tests, with a small budget; provision fresh state for the full run rather than reuse test weights or temporary DB contents.

## Three different questions

| Question | Primary mitigation | What it does not establish |
| --- | --- | --- |
| Does the module behave correctly for this contract? | Syntax, interface, invariant, numerical and integration tests using trusted fixtures. | Finite tests cannot prove behavior for every input or detect every deliberately hidden action. |
| What damage can the code do if it misbehaves? | Restricted identity/environment, limited writable storage, no host secrets or general network access, narrowly allowed temporary DB/ZMQ channels, resource limits and supervisor termination. | A process boundary alone is not a security boundary; kernels, drivers and runtime configuration still matter. |
| Can the candidate falsify a high score? | External artifact inspection with an explicitly chosen score-verification assurance level; stronger replay or protected evaluator options where needed. | Containing filesystem/network access does not make a score computed in the candidate's own address space trustworthy. |

Treat generated code as untrusted executable content whether produced locally or downloaded. Prompt instructions such as “do not access files” are useful task guidance, not access control. AST/import checks reduce accidental surface area but cannot establish a Python sandbox. Restricting builtins or using a restricted-Python language subset is not a substitute for an OS-enforced boundary around arbitrary PyTorch/NumPy code.

## Practical pre-activation test plan

The host chooses and versions the tests. The LLM may propose extra tests, but cannot remove fixtures, replace the runner, relax timeouts or issue a passing verdict. Every executable stage runs with limits from the start.

| Stage | Concrete checks | Failure outcome |
| --- | --- | --- |
| 1. Artifact preflight, without import | Allowed slot/path, source-size limit, syntax parse, declared dependency/import inventory, complete parameter/schema resolution, exact artifact digest. | Reject before execution with a precise syntax/contract error. A clean scan is not a safety certificate. |
| 2. Import and interface tests | Import inside the disposable test environment; verify required entry points, construction/reset behavior, signatures and permitted return structures. Enforce short import/startup deadlines. | Import error, missing interface or timeout is a rejected revision. |
| 3. Module behavior tests | Exercise the per-slot cases below, including edge cases and fixed-seed regressions. | Record the failed invariant and bounded diagnostic output; preserve the last good candidate. |
| 4. Combined smoke run | Wire the four generated-module slots, ordinary epsilon policy, configured epsilonNice component and full parameter set into a small episode/step budget. Check observation/action compatibility, one or more training updates, finite outputs, cleanup and resource use. | Reject incompatible combinations even when each module passed individually. |
| 5. Admission and fresh execution | Bind results to candidate, fixtures, host/evaluator, runtime/dependency and restriction-policy digests. Verify those identities before launching a fresh full simulation environment. | Changed bytes or incompatible environment require retesting. No live-service hot reload. |

Suggested per-module cases are behavioral contracts rather than a mandated testing framework:

- **RNNModel:** small and representative `[B,T,F]` inputs produce the required `[B,T,A]` and `[B,A]` outputs; check dtype/device, finite values, seeded initialization and parameter-count/resource bounds. Test expected state reset and serialization semantics inside the environment.
- **ReplayMemory:** empty/insufficient history, terminal transition, short episode, capacity overflow and multiple episodes. Returned sequences must not cross episode boundaries; check batch shapes, reproducible sampling, buffer ownership and capacity accounting.
- **Trainer:** a controlled batch produces a bounded update with finite loss and parameters; warm-up is explicit; reset starts cleanly; target/gradient/update behavior meets the selected algorithm contract. A tiny learning fixture can detect obvious no-op trainers, but does not prove the algorithm will improve Snake scores.
- **RewardFunction:** deterministic fixtures for food, wall/self collision, ordinary movement and move-limit termination return finite scalars. Input transition facts remain unchanged. Tests check the declared reward contract without allowing the function to change authoritative score or termination.
- **epsilonNice configuration:** use controlled RNG and score/gate fixtures for disabled passthrough, next-step arming, exact detour attempts, safe-alternative/fallback action selection, stagnation transitions and run/episode reset semantics. Validate replay uses the executed action. This tests a fixed configurable component, not an implicitly authorized new generated-code slot; see [the detailed contract](08-exploration-and-epsilon-nice.md#acceptance-fixtures).
- **Combined candidate:** baseline parity fixtures, observation/action range checks, repeated initialization, a bounded learning cycle, termination and cancellation. Test the actual parameter combination, not just default constructor values.

Add a small set of **execution-policy tests** to the harness: attempt to read a protected fixture, write outside scratch, open a disallowed network connection, connect to the persistent DB, spawn excess descendants, exhaust a defined resource budget and hang. Confirm the intended denial/termination and the recorded result on the actual host. These probe chosen controls; they are not proof that every escape is impossible. Do not run intentionally destructive probes against real user data.

## Admission evidence and repair

A trusted supervisor records exit status, timeout/OOM/policy failures, selected fixture results and bounded output with candidate/run IDs. Where test assertions execute alongside candidate code, recognize that malicious code may tamper with that test process. Keep the admission decision and record writer outside it, use supervisor-observed outcomes, and use out-of-process comparisons for critical invariants where feasible. Passing same-process unit tests remains useful correctness evidence, not a security attestation.

On failure, return only the relevant bounded diagnostics to the skill and allow a small explicit repair budget. Any edit creates a new candidate revision and invalidates affected checks; dependent modules are retested together. Record failed attempts as evidence, not as zero-score runs. Do not automatically install an undeclared package to make a candidate pass.

The external web reporting server should show the source/diff, test stage, case outcome, duration, resource failure, diagnostics, skill version and repair lineage, together with post-run capture, inspection, import and cleanup status. Live ZMQ state is provisional and never automatically upgrades a failed or uninspected run to success. “Passed admission” means the recorded suite passed under the recorded limits; it must not be displayed as “safe code.”

## Practical containment options

Select one mechanism appropriate to the machine and risk, rather than layering every available technology. All choices need an explicit approved BMForge component/inventory before application implementation.

| Option | Useful scope | Costs and residual risk |
| --- | --- | --- |
| Per-run OS-isolated environment with dedicated identities and carefully configured systemd/OS controls | May keep deployment small while enclosing simulation, temporary MariaDB, scratch and run-local channels. | A subprocess or ordinary unit is insufficient. Demonstrate enforced filesystem/process/network boundaries and whole-environment cleanup. If it cannot meet the selected sandbox policy, it is not an acceptable substitute. Same-kernel/native-code exposure remains. |
| Unprivileged/rootless container environment with read-only base, narrow mounts and explicit limits | Reproducible simulation plus temporary MariaDB, with only their private DB link and approved ZMQ/control routes. One or more containers may form a single per-run lifecycle. | Shares the host kernel and is not a complete hostile-code boundary. No privileged mode, container-engine socket or broad host mount. Rootless resource enforcement depends on the actual cgroup configuration. GPU/device access complicates the boundary. |
| Disposable VM or other stronger isolated execution environment | Stronger separation when hostile-code risk or host sensitivity justifies it. | More provisioning and resource overhead; GPU support, data exchange and reproducibility need validation. It still requires patching, limits and protected result handling. |

An additional sandbox runtime is an option if the chosen platform supports the required workload, not a default new dependency. Compatibility with PyTorch, native extensions and GPU drivers must be established, not inferred from a product name.

**Recommended next step:** elaborate one disposable environment with the baseline simulation and temporary MariaDB first. Prove clean creation, schema reuse, bounded ZMQ observation, artifact capture/import and complete disposal with trusted fixed modules. Evaluate the least complex OS/container mechanism that can enforce the chosen policy before enabling generated modules; use a VM when the accepted risk calls for it. Tests and full simulations use fresh instances of the same versioned environment. Add GPU access only after a device/resource review. This chooses an experiment sequence, not a sandbox product, and does not label a lightly hardened process secure.

## Score integrity is a separate design choice

Read-only evaluator source is insufficient if imported generated Python shares the evaluator's process: it may alter objects, global state, functions or the reported result in memory. Likewise, a reward module can return large numbers without improving gameplay. The proposed design keeps **training reward** separate from the game's **food-count score**.

The whole-simulation sandbox is now decided; the result inspection mechanism is not. Inspect captured manifests, table data, counts, numeric bounds and completeness before persistent import. Those checks detect malformed or inconsistent output, not every fabricated score. A stronger inspection can replay complete action evidence for every scored episode using fixed seeds/rules and derive scores independently. That validates legal trajectories, but does not alone establish that the declared model or training procedure generated the actions. Alternatively, isolate the static game/evaluator from the learning code inside the disposable environment and exchange bounded data-only observations/actions. Its enforcement and throughput still need validation. Keep the selected assurance level visible in result metadata, and do not turn either option into an unapproved mandatory redesign.

External application code owns persistent result import and champion comparison. Temporary MariaDB, static publisher output and exported counters remain provisional until inspected under the selected policy. Reusing the same schema does not make a raw SQL dump safe to restore. Import only allowlisted data with host-owned SQL, validating IDs, relationships, lengths and totals; reject executable objects, unexpected tables and arbitrary filesystem references. Keep persistent credentials outside the sandbox and make the import atomic/idempotent, as specified in the [lifecycle contract](04-runtime-and-integrity.md#disposable-run-lifecycle-and-data-ownership). Use a bounded data-only exchange format; do not unpickle candidate-produced objects in a trusted process. PyTorch checkpoint loading also needs deliberate restrictions: keep model-code loading inside the environment and use appropriate restricted state-dictionary handling when needed. A filename or a `weights_only` setting alone is not a general guarantee against resource exhaustion or unsafe surrounding code.

## Stop criteria and remaining risk

Do not activate a candidate after failed/absent checks, changed artifacts, unavailable required controls or an unresolved resource/score-integrity violation. Stop the entire environment and descendants, retain bounded diagnostic evidence, record the cause and dispose temporary state. Rejected or incomplete results never become completed scientific runs. Failed cleanup must be reconciled before the next launch; the previous champion remains intact. Operator review is for changing the accepted contracts or execution policy; routine passing candidates can still run automatically within an approved experiment policy.

Testing reduces the chance of bad behavior. Containment reduces the damage if it occurs. Trusted evaluation reduces the chance of a false scientific result. Residual kernel/driver/runtime vulnerabilities and untested behavior remain, so the proposal makes those limits visible instead of claiming that tests prove arbitrary code safe.
