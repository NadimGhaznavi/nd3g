# Exploration policy and epsilonNice

[Overview](README.md) · [Candidate contracts](03-skills-and-candidates.md) · [Source register](06-sources.md#ai-hydra-epsilonnice)

## Requirement and recommended scope

The user requested epsilonNice as a configurable component and identified AI Hydra as the reference. Include it as a named **exploration component layered after ordinary epsilon-greedy action selection**, not as another epsilon-decay formula. It changes which actions the agent takes, so its configuration and intervention history belong in the experiment evidence.

Recommend configuration first: the LLM selects disabled or epsilonNice and supplies bounded settings for a fixed, versioned application-owned implementation. Preserve the four existing proposed generated-code slots. A fifth slot, such as an editable exploration-policy module, is a reasonable alternative if algorithm generation is desired, but the latest request does not distinguish it from parameter configuration. Record that as an open decision rather than silently granting new source-write authority. No implementation or component installation is authorized by this analysis.

## What AI Hydra actually does

Inspection is pinned to AI Hydra `b348e6be6d0f2458bc9401ed01035e85fa09527f`. The repository requested as `ai-hydra` now resolves to `ai_hydra`. Its [epsilonNice guide](https://github.com/NadimGhaznavi/ai_hydra/blob/b348e6be6d0f2458bc9401ed01035e85fa09527f/pages/epsilon-nice.md) describes a conditionally enabled, bounded safe-detour wrapper. The implementation divides responsibilities across several files; copying `EpsilonNiceAlgo.py` alone would omit activation and detour state.

- **Composition:** `HydraMgr` builds the neural policy, wraps it in `EpsilonPolicy`, then `BehaviourPolicy`. The latter owns enabled state, probabilistic arming and remaining detour steps. `EpsilonNiceAlgo` selects an alternative action and collects statistics.
- **Post-epsilon gate:** `BehaviourPolicy` calls the base policy first. When current epsilon is greater than `0.0001`, it clears pending Nice steps and returns the base action. AI Hydra's separate `EpsilonAlgo` decays at episode end and snaps values below `0.001` to zero. These are two distinct source behaviors, not interchangeable thresholds or instructions to change Nd3G's baseline schedule.
- **External enable/disable:** `TrainMgr.handle_stagnation(final_score)` runs at episode end. No-new-high-score stagnation enables Nice; a new high score clears the alert and disables it. Its critical-stagnation path also enables Nice while performing ATH-memory recovery. Neither reward magnitude nor loss is the high-score signal here.
- **Arming:** when enabled, post-epsilon and not in an MCTS burst, the wrapper counts an eligible call. If no detour is pending, a draw below `nice_p_value` sets `nice_steps_remaining`. The arming step still returns the base action. Interventions begin on the **next eligible step**, not immediately.
- **Detour:** each pending step decrements the counter and asks `EpsilonNiceAlgo` for an override. It samples from the other actions that `GameLogic.would_collide` considers non-colliding. It excludes the suggested action even if that action is safe. If no alternative exists, it preserves the suggestion, which can still be fatal. “Safe” means immediate collision avoidance under that predicate, not guaranteed survival, improved score or software security.
- **Lifetime:** enabled is initially false and remaining steps zero. Disabling or the epsilon gate clears pending steps. The inspected `played_game()` advances epsilon/statistics but does not itself clear a Nice detour; the inherited episode-reset hook is a no-op for this wrapper. A pending detour can therefore span episode boundaries unless another gate clears it. Fresh simulations must start with new policy state.
- **Randomness:** a dedicated Nice RNG is derived from the master seed, separate from epsilon/replay/game streams. Arming and alternative selection share that Nice stream. Reproducible seed derivation and draw ordering matter; splitting the two Nice operations into unrelated RNGs changes behavior.
- **Native settings:** the Linear/RNN/GRU constants specify `nice_p_value = 0.005` and `nice_steps = 20`. The usual stagnation threshold is 300 episodes, with a separate critical threshold initially 500. These are inspected reference defaults, not measured optimal values or approved Nd3G tuning limits.

AI Hydra also coordinates MCTS and ATH memory. Those systems are not prerequisites for adding epsilonNice to Nd3G. Keep MCTS and ATH-specific recovery out of this proposal. Reuse the behavior and responsibility separation, not Hydra's entire training manager or event infrastructure.

## Nd3G configuration and state contract

The following is a proposed contract, not a claim that these paths already exist:

| Item | Proposed treatment |
| --- | --- |
| Component selection | Explicit disabled or epsilonNice reference. Disabled retains the existing epsilon-greedy baseline and must not consume Nice RNG draws. |
| `nice_p_value` | LLM-configurable, finite numeric probability in `[0,1]`, excluding Boolean values; experiment policy may impose a narrower search range. Zero disables arming. |
| `nice_steps` | LLM-configurable positive integer with a host-owned maximum; reject Boolean, fractional, negative and unbounded values. It counts override attempts, including attempts with no alternative. |
| Activation policy | Versioned, static simulation responsibility driven by actual episode food-count scores and no-new-high-score history. Begin with the reference stagnation behavior, fixing the chosen threshold in the experiment contract rather than implicitly adding another tunable. No ATH hard-reset side effect. |
| Epsilon gate and episode semantics | Record the cutoff, update ordering and pending-detour carry/reset rule. A reference-behavior profile preserves next-step arming and carry across episodes. Resetting at each episode is a distinct deliberate variant, not an unnoticed refactor. |
| Implementation identity | Record component ID/version/digest even when its source is not LLM-writable. Epsilon algorithm identity is recorded separately. |
| Mutable state | Run-local enabled flag, remaining steps, stagnation counter/high score and RNG state. This state evolves during simulation, never through live LLM tool calls. It is not part of an editable candidate manifest. |

Keep the existing `epsilon.initial`, `epsilon.minimum` and `epsilon.decay` meanings. The inspected Ax3l/SnakeLab schemas fix minimum at zero, but settings and episode budget can still keep epsilon above the Nice cutoff throughout a run. Admission should expose that reachability issue explicitly, and reports must distinguish “configured but never eligible” from “eligible but no arm/override occurred.” A smoke fixture must exercise the gate by controlled state; it cannot depend on a short random training run happening to stagnate and arm a detour. Do not silently shorten decay or move the threshold to force activity.

## Simulation integration

Static simulation orchestration owns the sequence: obtain the ordinary epsilon-greedy suggestion, apply epsilonNice when eligible, validate the selected action, apply the unchanged game transition, and pass the **executed action** into replay/training. Storing the pre-override suggestion as if it was executed would corrupt the learning evidence. At episode completion, update the chosen epsilon schedule and score-based activation state in the documented order.

Collision facts come from the static game-rules implementation, using the same action vocabulary and collision semantics as execution. A read-only board value or derived collision mask is sufficient; epsilonNice does not need authority to modify the game, rewards, score, episode budget, storage or telemetry publisher. State and code live inside the disposable simulation environment. No new service, database or messaging channel is needed.

Before admitting a candidate, bind the full exploration selection/settings, epsilon schedule, module contracts and budgets to its digest. Every run receives fresh exploration state, its own seed-derived Nice stream and an immutable configuration. An explicit disabled setting counts as resolved configuration. If an editable exploration-code slot is later selected, it must receive the same candidate versioning, restricted tests and inspected-output treatment as other generated modules; validators and collision rules remain static.

## Evidence and comparison

Report configured selection/settings, current epsilon, eligible/enabled state, remaining detour steps, activation/deactivation reason and counts of eligible calls, armed detours, attempted overrides, actual overrides and no-alternative outcomes. Preserve cumulative run totals as well as any live windows, with a final partial window at capture. Treat ZMQ observations as provisional; accepted records follow the existing inspection/import path.

AI Hydra's telemetry needs careful mapping: `triggered` counts calls to `override_action`, not newly armed detours; `calls` counts eligible Nice consultations. `fatal_suggested` increments only after at least one safe alternative is found. Its rates divide by eligible calls, and the algorithm publishes/reset counters every 100 episodes. Do not relabel those legacy counters as different metrics. Separate names and counter definitions in Nd3G avoid implying that a detour's 20 attempts were 20 independently armed detours.

Preserve the strict high-score champion rule within a declared comparable experiment. Show whether epsilonNice was allowed and used, the selected policy configuration and equal episode/compute budgets. A score from a model-plus-epsilonNice controller is not automatically evidence of the neural policy's unaided performance. A matched baseline comparison can measure the component's contribution without changing scoring or requiring a new experiment framework.

## Acceptance fixtures

- Disabled and `p=0` return base actions and do not arm; active ordinary epsilon clears pending detours. Test both sides and equality at the exact cutoff.
- With controlled RNG and `p=1`, the arming step returns the base action; the following configured number of eligible steps attempt overrides. Test one step, multiple steps, exhaustion and rearming.
- Sample only non-colliding alternatives excluding the suggestion, including when the suggestion is safe. With no alternative, return the original action and record the outcome without claiming a safe move.
- Verify stagnation enable, new-high-score disable, tied/lower-score behavior, and chosen episode-boundary carry/reset semantics. Confirm training reward cannot substitute for food-count score.
- Verify the replay transition records the final executed action; collision classification agrees with actual game transition fixtures, including boundary/tail cases.
- Identical policy inputs and Nice RNG state produce identical choices in fixtures. A fresh run resets state; a viewer attaching/detaching cannot consume policy randomness.
- Validate parameter types/bounds, gate reachability diagnostics, manifest digests, counter meanings and the final partial telemetry window. Combined tests cover model, epsilon, epsilonNice, replay, trainer and reward together.

These tests are proposed, not executed application tests. The inspected AI Hydra test file does not establish focused epsilonNice coverage. Passing future fixtures would establish the specified behavior, not guarantee better learning or containment of generated Python.
