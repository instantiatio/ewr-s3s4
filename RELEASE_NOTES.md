# EWR S3S4 8.0.2 Eternal Alpha

See [README](README.md) for the purpose of EWR S3S4, S3/S4 participation and optional external memory.

## 8.0.2 — one Memebase index

- DEC connects through `Index.yaml`. Schema 2 includes navigation cues and structured search fields for the same engram. The index can be rebuilt from engram files using ADE file operations or the optional helper.
- The helper's `query` reads current engram metadata before filtering and returning results. An edit to the generated index alone leaves query results tied to the source records.
- A new Memebase starts with an empty YAML index and the English [quick guide](docs/readmemebase.md). The [transition procedure](docs/DEC.md#migrate-an-existing-memebase) retains engram IDs and navigation cues when moving from the older catalogue.
- This is a local release candidate. The [status](STATUS.md) gives the verified scope.

## 8.0.1 — shared Memebase tasks and events

Task workflows are experimental and are being evaluated in everyday use.

- DEC supports recording tasks and events, rescheduling them by stable ID, and looking them up across EWR installations connected to the same Memebase.
- Optional `starts_at` and `ends_at` fields describe scheduled time. Existing undated engrams remain eligible for ID, kind and semantic search.
- A generated `Index.yaml` supports structured lookup. The optional helper builds, checks and queries the index, with source lookup when the index is missing or stale. Python is optional for DEC file operations. See the [DEC procedure](docs/DEC.md#tasks-events-and-the-structured-index) and [verification scope](STATUS.md).

## Refreshed 8.0.0 distribution — 22 November 2026

- Uses Memebase as the working name for the optional external engram store. The clean installation starts with DEC disconnected.
- Adds explicit capture with source attachments. The extended command copies the selected originals, verifies the copies, and links them from the engram. Ordinary capture saves the engram and can retain links to sources.
- Clarifies path checks during retrieval, preservation of another writer's changes during connection rollback, and recovery when the engram was written before its index entry.
- Separates project history and original inputs from the clean ZIP. The earlier 8.0.0 archive is preserved separately. See [STATUS](STATUS.md) for the verification scope.

## Corrections to the local 8.0.0 build

- Aligned the active architecture and maintenance instructions with version 8.0.0 and the [current-pair profile](docs/METHODPACK_CHECK.md#current-pair-profile).
- Updated the Mini ConOps reached from README to point to the current-pair update and recovery procedure.
- The checker verifies the method name in the body heading and requires the exact current-pair document and anchor. The [verification scope](STATUS.md) distinguishes pair consistency, guarded transition and the earlier FPF basis. The exact base-v3.17 book and all 37 method bodies are preserved.

## Baseline MP and current-only installation

- Restored the exact MP book from Human's `iEWR-7.0.9-Eternal-Alpha.zip`, base-v3.17. Its 37 method bodies and individual editions already matched the working descriptions; baseline identity is now explicit.
- Removed historical snapshots, activation records and the old FPF copy from the clean/runtime tree. Exact previous sources and control history remain in the development archive.
- Adapted only installation metadata and the checker for one current book/index pair, using exact book/body hashes, live dependency checks and the authorized ADE/archive update procedure. The baseline descriptions' snapshot-folder recipe is superseded by this profile; their bodies are unchanged.
- Historical FPF grounds retain their original editions as provenance. Current source routes are lookup candidates requiring task-specific reading, not blanket requalification. [Profile](docs/METHODPACK_CHECK.md#current-pair-profile) · [Scope](STATUS.md).

## 8.0.0 — architectural milestone

- Human designated 8.0.0 for the established EWR S3S4 architecture and defined the first version component as an architectural change. The environment continues iEWR in a single project, with S3/S4 participation, the common FPF/MethodPack basis and optional external memory through the engram store and DEC.
- This release designation updates version metadata, current titles and package names. It preserves the already assembled functional rules, 37 method bodies and source editions; no additional functional redesign is claimed by the versioning step.
- Includes the latest approved README statement: further development takes place within this single project and external memory can be connected as needed.
- The clean ZIP is reopened/extracted and its inventory, hashes, source/index and MethodPack consistency checked. Existing observations retain their original editions and conditions. The archive starts with memory disconnected and empty project directories. See [STATUS](STATUS.md).

## Preparation under the EWR S3S4 name — 7.0.9

### Rename on 21 November 2026

- Renamed the active product descriptions, instructions, metadata and distribution to EWR S3S4; selected `https://github.com/instantiatio/ewr-s3s4` as its repository address. This task performs local preparation and does not publish to the repository.
- Updated README with the agreed lineage and collaboration description, the functions of external memory and its explicit connection procedure. A clean installation remains disconnected; the working project keeps its existing connection.
- Renamed the maintained ConOps to `docs/EWR_CONOPS.md`. The old address remains an explicit compatibility redirect for saved project and memory links.
- Pack base-v3.19 changes its title and work-support metadata. All 37 applied method bodies, individual editions, source originals and historical snapshots are preserved. The FPF original and structural addresses retain the same edition; only the provenance owner label and its index hash binding change.
- Checked active naming, local paths/anchors, README claims against the DEC procedure, source preservation, MethodPack and the extracted clean package. [Verification scope](STATUS.md).

## Predecessor history

The following records describe iEWR builds and their actual checks. Their names, archive identities and observation conditions remain historical.

### iEWR 7.0.9 S3S4 Edition Eternal Alpha

This local S3S4 release is based on the iEWR 7.0.9 development instance identified in [PACKAGE.json](PACKAGE.json). See [README.md](README.md) for an overview and getting started.

- Includes the Markdown procedure for DEC and describes the role of the engram store in [ConOps](docs/IEWR_CONOPS.md#memebase-and-dec).
- DEC starts disabled. [Connect Memebase](docs/DEC.md#connect-memebase) explains how to link an existing external memory. The four project directories start empty.
- [Self-development](docs/SELF_DEVELOPMENT.md#technology-stack-and-approval) records the working stack and requires developer approval for stack changes.
- The supplied FPF pair and MethodPack base-v3.17 are carried forward byte for byte.

See [STATUS.md](STATUS.md) for this local archive's verification scope.

#### Working-source changes on 21 November 2026

- Connected the DEC core: material-work cues for initiated recall, bounded interpretation of related experience, and acquisition proposals that expose the new contribution and its conditions. Existing proposal modes and Human confirmation of new content are preserved. See the [functional account](docs/IEWR_CONOPS.md#memebase-and-dec) and [operational procedure](docs/DEC.md#capabilities-and-boundaries).
- Added the project consultation journal, once-per-event adoption accounting and reconciliation after interruption. Routine maintenance is grouped where possible; separate per-access report files are not required.
- Checked the instructions with an independent cold reading, repaired three ambiguities, and exercised recovery from a constructed partial update. A subsequent fresh agent in a separate installation/memory copy completed an ordinary editing case without a recall instruction, recorded two adopted notes and proposed a new acquisition after feedback without saving it. This is bounded evidence, not proof of general autonomous-recall efficacy, causal benefit or time savings. [Verification scope](STATUS.md).

These changes describe the active working source tree. The previously built clean ZIP and its `INSTALLATION.json` inventory have not been regenerated; their configuration, hashes and checks remain those of that recorded archive. The working installation may have memory connected while the clean package starts disconnected. Project journals and detailed trial records are working materials under `project/`, not required initial contents of a clean installation. README remains the overview and entry point.


#### FPF source update on 21 November 2026

- Updated the general FPF basis from `c3b34de07a6bd2df85c7081a4c367fd09978079c` to `25335ed69b71702b18d801f38f211e380a68fd45`, preserving the author's original text and terms. Added the exact local USING-FPF entry guide and regenerated the structural index from the new bytes.
- Repaired 71 exact architectural/task source addresses. Preserved the previous coherent FPF root and 228 historical MethodPack source references. Reference-only pack base-v3.18 retains all 37 bodies and individual editions.
- Checked the paired sources/indexes, reference resolution, MethodPack consistency, selected operating-rule compatibility and clean package extraction. The earlier DEC work trials remain observations of their original edition. See [compatibility scope](docs/FPF_COMPATIBILITY.md) and [status](STATUS.md).
- Prepared a refreshed local clean ZIP and inventory from the current environment sources. It starts with DEC disabled and empty project directories; the active project retains its connected memory and accumulated work. This new archive is separate from the earlier preserved build. The product version and README description are unchanged; no publication is performed.
