# Changelog

## [Unreleased]

### Summary

Established Nd3G's initial engineering setup with pinned BMForge baseline
skills, project context and application metadata. Added an architecture
proposal for skill-guided parameter and learning-module experiments,
with explicit execution, scoring and BMForge adoption boundaries.

### Analysis

- Performed analysis on the structure and components of Ax3l and SnakeLab
  to identify core components required for Nd3g.
  - Report is a PR

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
