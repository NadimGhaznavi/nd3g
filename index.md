---
title: "Nd3G"
layout: single
classes: wide
author_profile: true
lang: en
locale: en-US
language_name: English
translation_key: nd3g-home
permalink: /
---

![{{ site.title }} logo]({{ site.logo | relative_url }})

LLM configured Snake Game AI.

**Can an LLM tune the Snake AI to improve high scores?**

Nd3G explores an experiment loop with configurable learning modules,
epsilonNice exploration, disposable simulation environments, inspected result
import and integrated web reporting. The documentation describes the proposed
architecture; the application runtime remains to be implemented.

## Documentation

Start with the [architecture proposal]({{ site.baseurl }}{% link pages/architecture/index.md %})
for the overview, working assumptions and decisions recommended for review.

1. [Requirements and source baseline]({{ site.baseurl }}{% link pages/architecture/01-requirements-and-baseline.md %}): requirements, existing capabilities and assumptions.
2. [Use cases and analysis model]({{ site.baseurl }}{% link pages/architecture/02-analysis-model.md %}): responsibilities, class diagrams and use-case realizations.
3. [Runtime skills and experiment contracts]({{ site.baseurl }}{% link pages/architecture/03-skills-and-candidates.md %}): tool authority, configurable modules and complete candidates.
4. [Runtime boundaries and execution]({{ site.baseurl }}{% link pages/architecture/04-runtime-and-integrity.md %}): disposable environments, storage, communications and recovery.
5. [BMForge adoption and iteration plan]({{ site.baseurl }}{% link pages/architecture/05-bmforge-and-delivery.md %}): component gaps, development sequence and acceptance criteria.
6. [Source register]({{ site.baseurl }}{% link pages/architecture/06-sources.md %}): repository evidence and modeling references.
7. [Generated-code risk mitigation]({{ site.baseurl }}{% link pages/architecture/07-generated-code-risk.md %}): pre-activation tests, containment choices and admission evidence.
8. [Exploration policy and epsilonNice]({{ site.baseurl }}{% link pages/architecture/08-exploration-and-epsilon-nice.md %}): policy configuration, runtime state and validation.

## Project

- [Source repository](https://github.com/NadimGhaznavi/nd3g)
- [Changelog](https://github.com/NadimGhaznavi/nd3g/blob/main/CHANGELOG.md)
