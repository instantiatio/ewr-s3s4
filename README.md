# EWR S3S4 8.0.1 Eternal Alpha

**EWR S3S4 is an engineering environment for people and AI working together.**

EWR S3S4 continues the development of iEWR under a new name, retaining its functionality. All further development takes place within this single project. External memory through Memebase and DEC can be connected as needed.

In **S3**, the person and AI think together; in **S4**, AI carries out delegated work within agreed bounds. DEC and the external memory help preserve useful experience and apply it to later tasks.

You specify the result you need, why it matters, and the bounds within which the agent acts independently. The agent helps shape the work, select methods, carry out the assignment, and check the result. You can assign it, for example:

- developing an application or changing an existing software product;
- preparing an engineering concept for a system or workflow;
- investigating a question, comparing options, and preparing a reasoned decision.

**Eternal Alpha** indicates the environment's research character: its design and methods evolve through use. Each result is checked for its intended use.

## External memory: Memebase and DEC

**Memebase** is a separate Markdown directory containing engrams: decisions, findings, ideas and ways of working, with their sources and applicability conditions. It preserves selected experience across conversations.

**DEC (Dynamic Engram Control)** helps the agent bring relevant experience into current work and recover what related entries support together. When the current proposal mode permits, it proposes useful new experience for future tasks. The agent checks applicability and keeps a concise project journal of consultations. New memory content is saved following your confirmation or direct request.

A **clean installation starts with memory disconnected**. To connect an existing Memebase, give the agent its directory path and ask, for example:

> Connect Memebase from `/path/to/Memebase`.

The agent checks the index and available entries, configures DEC and verifies access. The memory stays in its own directory; actual reading and writing depend on the access granted by your agent environment. See [Connect Memebase](docs/DEC.md#connect-memebase) for the procedure and checks. An existing project's connection is retained when its environment is renamed.

## Getting started

1. Extract the archive and open the `EWR-S3S4-8.0.1-Eternal-Alpha` directory in an agent environment that can read and modify files and perform the actions your task requires.
2. Have the agent read [AGENTS.md](AGENTS.md) if the environment does not load it automatically.
3. Describe the task, required result, and material constraints. Put materials in `project/source/` or point to an existing working context.
4. Results are saved in `project/artifacts/`; materials for handoff and continuation between people and agents are saved in `project/handoff/`.

English is the primary language of the environment's own active internal materials. Communicate with the agent in your preferred language; project outputs follow the task and recipient's requirements.

For example: “Study the materials in project/source/, propose a solution, and discuss the material options with me.” Or: “Prepare and check a solution independently within these bounds.”

## Ask the environment itself

Ask an agent working in EWR S3S4 about its capabilities and design. For example:

- “List the methods in the MethodPack and briefly explain what each is for.”
- “How can I transfer an old project here while preserving its materials and unfinished work?”
- “How is EWR S3S4 organized, and how are its seven functions connected?”
- “How do I connect external memory and use experience from previous work?”
- “Which actions can you perform here, and which require additional tools or access?”

## Methodological basis

The working combination is **Instructions + FPF + MethodPack**. FPF (First Principles Framework), by Anatoly Levenchuk, provides general methodology; the exact original is included. MethodPack is the applied repertoire: one thematic book and a YAML index with 37 method descriptions. For a new choice, the agent first checks for a sufficient FPF contribution, then the necessary MethodPack detail, and develops what is missing for the task.

This mechanism is called **Dynamic Method Generation (DMG)**. It covers finding, reusing, adapting, and creating ways of doing work. Methods useful again accumulate with their grounds, relations, checks, and preserved editions. Neither a full FPF traversal nor use of the entire repertoire is required.

You can request methods directly: “Apply TEXT-EDIT from the MethodPack to this text.”

- [File map](docs/FILES.md): purposes and locations of distribution files.
- [Method catalog](docs/METHOD_CATALOG.md): available methods and links to their descriptions.
- [Architecture overview and mini ConOps](docs/MINI_CONOPS.md): how the environment works, with an example.
- [Full ConOps](docs/EWR_CONOPS.md): concept of operations, participants, functions, and working conditions.

## Project transfer into the environment

Choose a way to provide an existing project's materials to the agent:

1. **Specify the project directory path.** This is a convenient first step: the agent can study the project before transferring materials.
2. **Copy the whole project directory into `project/source/`.** This suits small projects.
3. **Put a ZIP of the project directory into `project/source/`.** This is the preferred way to transfer an entire project.

State what the agent is assigned to do with the project: study materials, propose a solution, or prepare a change. Preserve sources, data, methods, accepted decisions, and unfinished work. For changes, the agent prepares a working copy in an agreed location; original materials are preserved. Do not blindly extract a project archive over the environment files or working directory.

## Developing the environment

When instructed, the agent can [develop the environment itself](docs/SELF_DEVELOPMENT.md) and [create coherent domain methodologies (DPFs)](docs/DPF_CREATION.md) using the canonical FPF method.

## Project and lineage

[EWR S3S4 repository](https://github.com/instantiatio/ewr-s3s4). [Release changes](RELEASE_NOTES.md) describes this local edition; [STATUS](STATUS.md) states what has been checked.

EWR S3S4 develops [iEWR](https://github.com/instantiatio/iEWR). The [iEWR 7.0.9 release](https://github.com/instantiatio/iEWR/releases/tag/7.0.9) belongs to its development lineage. Exact predecessor and source editions are recorded in [PACKAGE.json](PACKAGE.json) and [ORIGINS.json](ORIGINS.json). Historical records retain their original names and conditions.

## Authorship and terms

Copyright (c) 2026 Instantiatio EWR contributors

The environment's own parts are distributed under the [MIT License](LICENSE). Independent sources retain their own terms: [applied-method authorship](docs/METHOD_SOURCE_NOTICES.md), [exact sources and editions](ORIGINS.json).

FPF — [Anatoly Levenchuk](https://ailev.ru/). [Author's FPF repository](https://github.com/ailev/FPF). The [exact edition and provenance](external-sources/fpf/SOURCE.json), [CC BY 4.0](external-sources/fpf/LICENSE), and [third-party material terms](external-sources/fpf/LICENSING.md) are preserved. Distribution does not imply endorsement of EWR S3S4 by FPF's author.
