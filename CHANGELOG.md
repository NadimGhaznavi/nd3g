# Changelog

## [Unreleased]

## [0.2.1] - 2026-11-14 @ 12:03

## [0.2.0] - 2026-11-14 @ 11:45

### Summary

Prepared Nd3G's documentation site with the shared dark theme, a transparent
project logo, English metadata and GitHub Pages build workflow. The migrated
architecture proposal includes configurable epsilonNice exploration with source
evidence, run-local state and validation, distinct from a possible additional
generated-code slot.

### Added

- Install `bmforge-github-pages` specification 0.1.0 from BMForge revision
  `29a100c39997349ecfd40e190319aeb5018ffab8` and record it in the project skill
  selection and lock file.
- Add the BMForge-standard documentation homepage, Jekyll configuration and
  main-only GitHub Pages workflow for `nd3g.osoyalce.com`, with the shared
  Minimal Mistakes theme, Mermaid rendering, MyCount and English metadata.
- Add the owner-supplied `pages/images/nd3g.png` project logo, shared by the
  masthead and documentation homepage.
- Fixed sidebar.

### Changed

- Move the existing architecture proposal from `docs/architecture/` to
  `pages/architecture/`, preserving its content and diagrams while adding
  baseurl-aware navigation, stable page URLs and translation keys.
- Keep the repository README concise, exclude application and local tooling
  from site output, and ignore generated Jekyll files.
- Specify exploration-policy identity, settings, episode feedback, reset,
  reporting and candidate provenance alongside the retained baseline policy.
- Trace epsilonNice through analysis responsibilities, runtime skills, BMForge
  adoption and acceptance tests without implementing or enabling it.

### Fixed

- Replace the logo's baked-in checkerboard with transparency, including the
  handle opening and background gaps, while retaining its original dimensions
  and artwork.
- Resolve the changelog merge conflict while preserving the GitHub Pages and
  epsilonNice entries under one unreleased summary.

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
