# Mitigating risk from generated simulation code

[Overview](README.md) · [Candidate contracts](03-skills-and-candidates.md) · [Runtime boundaries](04-runtime-and-integrity.md)

## Start by testing the module before activating it

The proposed minimum workflow is: create a candidate in a staging area, run trusted module tests and a short combined simulation, inspect the evidence, then activate the **same tested artifacts** for a bounded full run. “Deployment” here means selecting a candidate for an experiment. It does not mean installing generated files over Nd3G's application code, changing systemd units or automatically releasing a champion.

This is useful even for a local, single-user system. Most failures will look mundane: a wrong tensor shape, a trainer that stops learning, replay memory that crosses episodes, NaN rewards, an infinite loop or excessive GPU allocation. Tests can catch these before a long experiment consumes time and resources.

However, a Python module can execute arbitrary work when imported. Running a test suite on the host first and isolating only the later simulation puts the risk in the wrong place. The test worker must receive the same restrictions as the full-run worker from its first import.

## Three different questions

| Question | Primary mitigation | What it does not establish |
| --- | --- | --- |
| Does the module behave correctly for this contract? | Syntax, interface, invariant, numerical and integration tests using trusted fixtures. | Finite tests cannot prove behavior for every input or detect every deliberately hidden action. |
| What damage can the code do if it misbehaves? | Restricted identity/environment, limited writable storage, no secrets/network, resource limits and supervisor termination. | A process boundary alone is not a security boundary; kernels, drivers and runtime configuration still matter. |
| Can the candidate falsify a high score? | Protected game rules/results and an independently trusted evaluation or replay path. | Containing filesystem/network access does not make a score computed in the candidate's own address space trustworthy. |

Treat generated code as untrusted executable content whether produced locally or downloaded. Prompt instructions such as “do not access files” are useful task guidance, not access control. AST/import checks reduce accidental surface area but cannot establish a Python sandbox. Restricting builtins or using a restricted-Python language subset is not a substitute for an OS-enforced boundary around arbitrary PyTorch/NumPy code.

## Practical pre-activation test plan

The host chooses and versions the tests. The LLM may propose extra tests, but cannot remove fixtures, replace the runner, relax timeouts or issue a passing verdict. Every executable stage runs with limits from the start.

| Stage | Concrete checks | Failure outcome |
| --- | --- | --- |
| 1. Artifact preflight, without import | Allowed slot/path, source-size limit, syntax parse, declared dependency/import inventory, complete parameter/schema resolution, exact artifact digest. | Reject before execution with a precise syntax/contract error. A clean scan is not a safety certificate. |
| 2. Import and interface tests | Import inside the restricted worker; verify required entry points, construction/reset behavior, signatures and permitted return structures. Enforce short import/startup deadlines. | Import error, missing interface or timeout is a rejected revision. |
| 3. Module behavior tests | Exercise the per-slot cases below, including edge cases and fixed-seed regressions. | Record the failed invariant and bounded diagnostic output; preserve the last good candidate. |
| 4. Combined smoke run | Wire the actual four modules and full parameter set into a small episode/step budget. Check observation/action compatibility, one or more training updates, finite outputs, cleanup and resource use. | Reject incompatible combinations even when each module passed individually. |
| 5. Admission and fresh execution | Bind results to candidate, fixtures, host/evaluator, runtime/dependency and restriction-policy digests. Verify those identities before launching a fresh full-run worker. | Changed bytes or incompatible environment require retesting. No live-service hot reload. |

Suggested per-module cases are behavioral contracts rather than a mandated testing framework:

- **RNNModel:** small and representative `[B,T,F]` inputs produce the required `[B,T,A]` and `[B,A]` outputs; check dtype/device, finite values, seeded initialization and parameter-count/resource bounds. Test expected state reset and serialization semantics within the worker.
- **ReplayMemory:** empty/insufficient history, terminal transition, short episode, capacity overflow and multiple episodes. Returned sequences must not cross episode boundaries; check batch shapes, reproducible sampling, buffer ownership and capacity accounting.
- **Trainer:** a controlled batch produces a bounded update with finite loss and parameters; warm-up is explicit; reset starts cleanly; target/gradient/update behavior meets the selected algorithm contract. A tiny learning fixture can detect obvious no-op trainers, but does not prove the algorithm will improve Snake scores.
- **RewardFunction:** deterministic fixtures for food, wall/self collision, ordinary movement and move-limit termination return finite scalars. Input transition facts remain unchanged. Tests check the declared reward contract without allowing the function to change authoritative score or termination.
- **Combined candidate:** baseline parity fixtures, observation/action range checks, repeated initialization, a bounded learning cycle, termination and cancellation. Test the actual parameter combination, not just default constructor values.

Add a small set of **execution-policy tests** to the harness: attempt to read a protected fixture, write outside scratch, open a network connection, spawn excess descendants, exhaust a defined resource budget and hang. Confirm the intended denial/termination and the recorded result on the actual host. These probe chosen controls; they are not proof that every escape is impossible. Do not run intentionally destructive probes against real user data.

## Admission evidence and repair

A trusted supervisor records exit status, timeout/OOM/policy failures, selected fixture results and bounded output with candidate/run IDs. Where test assertions execute alongside candidate code, recognize that malicious code may tamper with that test process. Keep the admission decision and record writer outside it, use supervisor-observed outcomes, and use out-of-process comparisons for critical invariants where feasible. Passing same-process unit tests remains useful correctness evidence, not a security attestation.

On failure, return only the relevant bounded diagnostics to the skill and allow a small explicit repair budget. Any edit creates a new candidate revision and invalidates affected checks; dependent modules are retested together. Record failed attempts as evidence, not as zero-score runs. Do not automatically install an undeclared package to make a candidate pass.

The web reporting server should show the source/diff, test stage, case outcome, duration, resource failure, diagnostics, skill version and repair lineage. “Passed admission” means the recorded suite passed under the recorded limits; it must not be displayed as “safe code.”

## Practical containment options

Select one mechanism appropriate to the machine and risk, rather than layering every available technology. All choices need an explicit approved BMForge component/inventory before application implementation.

| Option | Useful scope | Costs and residual risk |
| --- | --- | --- |
| Fresh worker under a dedicated restricted OS identity, with carefully configured systemd/OS controls | Smallest operational step for accidental failures; no secrets, minimal read-only runtime, bounded scratch, denied network and resource controls can reduce blast radius. | A subprocess or ordinary service unit does not provide these properties automatically. Same-kernel/native-code exposure remains. Verify real permissions, namespaces, capabilities, descendants and device access. |
| Unprivileged/rootless container with read-only base, narrow mounts, no network and explicit limits | Reproducible disposable runtime and a clearer filesystem/process view; often a practical first candidate to evaluate. | Shares the host kernel and is not a complete hostile-code boundary. No privileged mode, container-engine socket or broad host mount. Rootless resource enforcement depends on the actual cgroup configuration. GPU/device access complicates the boundary. |
| Disposable VM or other stronger isolated execution environment | Stronger separation when hostile-code risk or host sensitivity justifies it. | More provisioning and resource overhead; GPU support, data exchange and reproducibility need validation. It still requires patching, limits and protected result handling. |

An additional sandbox runtime is an option if the chosen platform supports the required workload, not a default new dependency. Compatibility with PyTorch, native extensions and GPU drivers must be established, not inferred from a product name.

**Recommended next step:** retain trusted parameter-only experiments while elaborating a disposable CPU test worker. Compare the smallest OS-restricted worker and an unprivileged container on the actual host against the same policy tests. Choose the least complex option whose measured restrictions and residual risk the owner accepts. Add GPU access only after a separate device/resource review, or use a dedicated disposable machine if adequate isolation is impractical. Do not label a lightly hardened process a secure sandbox to avoid that decision.

## Score integrity is a separate design choice

Read-only evaluator source is insufficient if imported generated Python shares the evaluator's process: it may alter objects, global state, functions or the reported result in memory. Likewise, a reward module can return large numbers without improving gameplay. The proposed design keeps **training reward** separate from the game's **food-count score**.

The preferred design to test is a protected game/evaluator exchanging bounded, data-only observations and actions with the learning worker. Check the effect on simulation throughput and reproducibility before committing to it. The alternative is isolated whole-simulation work followed by trusted replay of complete action evidence for every scored episode. That needs explicit seed/rule versions, evidence completeness and rejection of fabricated or missing traces. Neither option is implemented by this proposal.

The trusted service owns final result storage and champion comparison. Candidate-reported counters remain untrusted until derived or verified by that chosen path. Use a bounded data-only exchange format; do not unpickle candidate-produced objects in a trusted process. PyTorch checkpoint loading also needs deliberate restrictions: keep model-code loading inside the worker and use appropriate restricted state-dictionary handling when needed. A filename or a `weights_only` setting alone is not a general guarantee against resource exhaustion or unsafe surrounding code.

## Stop criteria and remaining risk

Do not activate a candidate after failed/absent checks, changed artifacts, unavailable required controls or an unresolved resource/score-integrity violation. Kill the bounded worker and descendants, record the cause and retain the previous champion. Operator review is for changing the accepted contracts or execution policy; routine passing candidates can still run automatically within an approved experiment policy.

Testing reduces the chance of bad behavior. Containment reduces the damage if it occurs. Trusted evaluation reduces the chance of a false scientific result. Residual kernel/driver/runtime vulnerabilities and untested behavior remain, so the proposal makes those limits visible instead of claiming that tests prove arbitrary code safe.
