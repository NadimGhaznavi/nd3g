# Changelog

## [Unreleased]

### Summary

Added pinned BMForge GitHub Pages guidance and templates for future
documentation-site work.

### Added

- Install `bmforge-github-pages` specification 0.1.0 from BMForge revision
  `29a100c39997349ecfd40e190319aeb5018ffab8` and record it in the project skill
  selection and lock file. Site setup and publication remain separate work.

## [0.1.1] - 2026-11-14 @ 10:41

### Summary

Refined the architecture around disposable per-simulation environments with
temporary MariaDB, external live observation and inspected result import.
The proposal separates execution completion, accepted evidence and cleanup
while preserving the existing experiment and BMForge-first approach.

### Changed

- Place the simulation server and temporary database inside a fresh environment
  for every run, with controller, persistent database and reporting outside.
- Specify artifact capture, inspection, idempotent accepted-data import and
  disposal/recovery responsibilities without selecting a sandbox technology.
- Keep game-state ZMQ publication in static non-LLM-writable simulation code,
  with external TUI/report consumers and clearly labeled provisional data.
- Update analysis classes, use-case diagrams, risk controls and acceptance
  scenarios. This remains documentation only, not runtime implementation.

## [0.1.0] - 2026-11-12 @ 05:35

### Summary

Established Nd3G's initial engineering setup with pinned BMForge baseline
skills, project context and application metadata. Added an architecture
proposal for skill-guided parameter and learning-module experiments,
with explicit execution, scoring and BMForge adoption boundaries.
The second draft makes web inspection essential, expands generated-code
risk mitigation and corrects the rejected-candidate Mermaid sequence.

### Analysis

- Performed analysis on the structure and components of Ax3l and SnakeLab
  to identify core components required for Nd3g.
- Reviewed analysis. Requested additonal refinements:
  - Reporting is a first class citizen
  - Sandboxing is a key subsystem
    - How to ensure generated code is safe before integrating it into a simulation run?


### Added

- Propose the Nd3G architecture in Markdown and Mermaid, including
  use cases and analysis classes, complete-candidate contracts,
  runtime skills, simulation integrity, recovery and a BMForge-first
  iteration plan. This is analysis only; no runtime is implemented.

- Install the four baseline BMForge skills with their local manager and lock
  file, pinned to revision `29a100c39997349ecfd40e190319aeb5018ffab8`.
- Document Nd3G's purpose, package, domain and selected skills in `AGENTS.md`.
- Add initial application metadata with the `Application` CMDB subtype and
  release, metadata-checking and deployment-disabled lifecycle scaffolding.

### Changed

- Revise the architecture proposal with required integrated web reporting,
  reviewed working assumptions, a practical test-before-activation gate,
  containment options and separate score-integrity considerations.

### Fixed

- Replace the Mermaid sequence-message semicolon that was parsed as a
  statement separator, preventing the rejected-candidate diagram from rendering.
