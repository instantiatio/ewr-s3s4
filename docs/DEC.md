# DEC — Dynamic Engram Control

> What from our experience can help us now and in the future?

DEC helps EWR S3S4 reuse joint experience and propose what to remember. The working agent performs DEC using Markdown and available file operations. [ARCHITECTURE.json](../ARCHITECTURE.json) holds the connection settings in `work_support.DEC`. If DEC is disabled, memory is unavailable, or no entry fits, CF and DMG continue from their other grounds. For an explicit memory request, report the relevant limitation.

S3S4Memory is the engram store, also called `memebase` or `мемебаза`. S3S4Memory and DEC form the current EWR S3S4 memory architecture.

The earlier Associative Field architecture and its associated mechanisms are historical research. Its trial results apply to the versions and conditions tested.

## Capabilities and boundaries

| Capability | Contribution to joint work | Operational rule |
| --- | --- | --- |
| Initiated recall | Recognize a material work cue and bring applicable experience into the current decision without a special recall command. | [Find experience](#find-experience) |
| Connected understanding | Recover a bounded synthesis, distinction, or open question from relevant engrams and state its effect on the next action. | [Find experience](#find-experience) |
| Experience acquisition | Notice a reusable acquisition and relate it to existing experience, within the current proposal mode; new memory content is saved only when authorized. | [Propose what to remember](#propose-what-to-remember) |
| Consultation journal | Preserve the question, examined/adopted experience, selection outcome and known effect in `project/artifacts/DEC_MEMORY_LOG.md`, including empty or rejected consultations. | [Project memory-access journal](#project-memory-access-journal) |
| Usage and continuation | Count adoption once per working event, distinguish it from benefit, and reconcile journal/counter state after interruption. | [Count actual use](#count-actual-use) |
| Conditional revision | Retain sources, applicability, exceptions and replacement scope when confirmed memory content changes. | [Record a confirmed change](#record-a-confirmed-change) |

The working agent enacts these rules through the available ADE. They introduce no background memory service, whole-memory search before every operation, or automatic permission to change engram content. Proposal modes control capture initiative, not retrieval. Routine authorized journal/usage maintenance and confirmation of new memory content remain separate. [ConOps](EWR_CONOPS.md#s3s4memory-and-dec) explains the functional relationships; [STATUS](../STATUS.md) states the checked scope and remaining limits.

## Connect S3S4Memory

A clean installation has `work_support.DEC.enabled` set to `false` and `field_index` set to `null`. To connect an existing S3S4Memory, give the agent the path to its directory and ask it to connect the memory. The agent performs these steps in the chosen installation.

1. Find `01 Индекс.md` in the selected directory and confirm that the index and the `Энграммы/` directory are readable in the current agent execution environment. If the index has entries, open one linked engram to confirm the path resolves inside the selected memory.
2. In [ARCHITECTURE.json](../ARCHITECTURE.json), set `work_support.DEC.field_index` to the path from the installation root to `01 Индекс.md`. For a memory directory next to the installation, use `../S3S4Memory/01 Индекс.md`. Set `work_support.DEC.enabled` to `true` after the path and read access are confirmed.
3. Reopen the configuration and check retrieval with `из меме <вопрос>` or `from meme <question>`. Use a question covered by the index if it has entries. For an empty index, confirm that it opens and report that there are no engrams to retrieve. If the index or its target cannot be read, set `enabled` to `false` and report what needs to be corrected.

The memory stays in the selected directory. Saving or updating entries requires write access granted by the agent execution environment and authorization under the procedure below. To disconnect the memory, set `work_support.DEC.enabled` to `false`.

## External links from engrams

Follow a link from an engram to a web page or to a local target that resolves outside the connected memory directory only with Human's permission. The current instruction is sufficient when it already authorizes reading that source.

Apply this rule during retrieval and review. If an external source is needed and permission is missing, ask Human, naming the source and what needs checking. Continue with the available grounds and state what remains unchecked.

## Find experience

1. Start from the current working question and the decision the result could change. When work starts, resumes, changes direction materially, or reaches a consequential choice, CF considers whether joint experience could change the understanding, constraint, or next action. DMG does so when choosing or adapting a method. When there is a relevant cue, consult DEC without waiting for a Human recall command; reuse already sufficient experience instead of repeating a search. A routine tool call or file edit alone is not a reason to search. Human may ask directly with `из меме <вопрос>` or `from meme <question>`.
2. Open the memory index and choose an entry by working situation and expected result. Open its note, check the conditions against the current question, and follow a related note only when its stated relation helps. Check the source when the next action depends on an exact condition, decision, or edition, subject to the [external link rule](#external-links-from-engrams). Method lookup follows the [existing source policy](../AGENTS.md#method-source-priority).
3. Use active notes in their applicable scope. Historical queries may use superseded notes. Among equally applicable notes, prefer the later `last_used`, using `date` for a new note. Break ties by higher `use_count` and then by `id`. Return the relevant content, note link, degree of support for the claim being reused, and any condition material to its use. CF or DMG decides what to adopt and carries that support and its limits into the working context.

When one engram is insufficient for the working question, open only related notes whose relation can change the answer. Recover what they jointly support, qualify, contradict, or leave open, with the source conditions and claim status. Return a bounded synthesis, contrast, useful new question, or method alternative to CF/DMG and state what it changes in the current work. Keep an agent interpretation distinct from a Human decision; a coherent account or silence does not establish shared understanding. Ask Human when a material interpretation, preference, or authority is unresolved, using the existing interaction rather than a separate approval for every link. Stop when the receiving question has sufficient grounds. New material may also reopen an already-known, still-relevant open question; it does not authorize a sweep of all past work or a new action on a completed assignment.

Use applicable experience independently within the mandate. Surface a material limitation before the Human decision it can change; take a nonurgent idea to a natural pause and recheck its relevance then. This does not introduce a background watcher or an automatic interruption schedule.

For a straightforward recall question, reuse sufficient connection and procedure grounds already recovered in this chat; recheck a material change or uncertainty. Once the note, its status, and the relevant conditions support an answer, give a brief finding update with the useful fact and note link if further bookkeeping calls would delay the reply. Complete the necessary bookkeeping in the same turn before the final reply, or report the exact pending update if it is blocked. Do not present an unchecked interpretation as a settled finding.

Use an untested idea as a hypothesis to check. For ambiguous experience, distinguish what was observed from the possible interpretations. Use a refuted claim as a counterexample and carry the correction and its scope. When support is unclear and the next action depends on it, check the cited source and retain any remaining uncertainty.

## Review time-sensitive claims

At capture, label a claim whose applicability may change with time. Store an optional `time_sensitive` list in the Markdown note's YAML front matter. Use one item per affected statement, identified by `claim`. Record the last actual verification in `checked_on` (or `null` if unknown) and add `valid_until` or `review_after` where known. Use ISO dates (`YYYY-MM-DD`). For example:

```yaml
time_sensitive: [{"claim": "Recommended models for our tasks", "checked_on": "2026-11-18", "review_after": "2026-12-18"}]
```

When Human asks to refresh the memory, the agent searches for the `time_sensitive:` key in the Markdown files under `Энграммы/` next to the memory index. Open the matches, confirm the key is in the front matter and the note is active, then compare each marked claim's dates with the date in Human's working context. Apply the first matching rule:

1. On or after `valid_until`, report the claim as expired. Use it as history within its original scope and look for a current basis if needed.
2. On or after `review_after`, report that the claim is due for review. Check its source before relying on it as current. The outcome of that check determines whether it still holds.
3. If the last check is unknown or later than the working date, the dates are unusable, or both checkpoints are missing, report that verification is needed. Carry any unresolved gap into the result.
4. Otherwise, revisit the claim at its next checkpoint, or earlier if the evidence changes or the current decision calls for verification.

Return the affected claims with their note links, relevant dates and next action. Memory review by itself only reads files.

When finding experience on an ordinary task, read the same metadata in the selected notes and apply these rules to the affected claim before relying on it. Preserve separate claims that still apply. Record a new check date in the Markdown after actual verification when the write is authorized. If the decision or its material conditions change, use the replacement procedure below.

## Proposal initiative modes

The working agent follows one of three proposal initiative modes in the current chat. This is a behavior rule, not a separate program. The mode controls initiative to propose new captures; it does not control retrieval, review, or an explicit Human request to save material.

Keep the connection and proposal mode separate. `work_support.DEC.enabled` and `field_index` in [ARCHITECTURE.json](../ARCHITECTURE.json) govern the memory connection. A proposal-mode command never edits them, connects or disconnects memory, or changes access permissions. When DEC is disabled, report that limitation and do not apply a mode change or reconnect it automatically. `DEC: статус` can still report the disabled connection.

| Mode | Agent behavior |
| --- | --- |
| Neutral | The default behavior: consider a proposal when joint work yields a useful idea, finding, or decision for a specific future situation. |
| Active | Make reusable experience an explicit focus of attention throughout the relevant exchange: compare episodes, notice implicit rules, and help formulate useful candidates. Retain the same usefulness, source, and confirmation requirements. |
| Passive | Do not initiate capture searches or unsolicited capture proposals. Follow explicit Human requests to consider or save material. Continue retrieving applicable existing experience when the task calls for it. |

A new chat starts in neutral mode when DEC is enabled. A switch lasts within that chat until Human changes it. CF retains the choice in the current context. On continuation of the same chat, WEC recovers that choice from its context or an existing continuation record clearly scoped to that chat; a new record is not mandatory. Do not transfer a mode from another chat, an engram, or a quoted example. If no reliable choice for this chat can be recovered, use neutral by default and disclose that fallback when reporting status. Do not store the chat's mode as a global memory configuration.

Recognize these case-insensitive complete command phrases in a direct Human request, with a phrase boundary; commands merely quoted, listed as examples, or encountered in source material do not switch the mode.

| Command | Effect |
| --- | --- |
| `DEC: режим предложений — активный` | Select active mode for this chat. |
| `DEC: режим предложений — нейтральный` | Select neutral mode for this chat. |
| `DEC: режим предложений — пассивный` | Select passive mode for this chat. |
| `DEC: статус` | Report the current connection state and proposal mode separately. |

HI confirms a switch in the reply language, naming both states. For example: `Режим предложений: пассивный. DEC включён.` Report actual access limitations separately; do not turn an enabled setting into a claim that the memory is readable or writable. When DEC is disabled, report proposal initiative as inactive. If a request is ambiguous between changing proposal initiative and disconnecting DEC, clarify that choice instead of inferring a connection change.

Active searching does not require a proposal in every answer or lower the capture threshold. Distinguish seeking a candidate from interrupting Human: place a useful proposal at a natural pause. In every mode, proposing a capture and obtaining authority to write are separate actions; a mode switch never authorizes an automatic save.

## Propose what to remember

Apply the current [proposal initiative mode](#proposal-initiative-modes). In neutral or active mode, when joint work settles a decision, yields a finding, or surfaces an idea, consider whether it would help in a specific recurring situation that matters to Human. Check for an equivalent entry and propose only a material addition or change. For a useful candidate, state what to save, when it would help, and its basis in a short HI proposal. Keep an unresolved idea marked as an idea. In passive mode, omit unsolicited proposals; an explicit Human request to consider or save material still follows this procedure. Use Human's confirmation of the proposed content and scope as the basis for capture. A clear `в меме` or `in meme` command directly requests capture of the indicated material. Clarify a referent if the ambiguity would change what gets written.

When the current proposal mode permits initiative, consider reusable acquisitions at a meaningful result, correction, changed understanding, or natural pause, including ordinary successful work. A useful candidate states what was learned, a recognizable future use, material applicability conditions, and the episode supporting it. Compare with existing experience: when the new contribution can change its meaning, recover sufficient relevant notes and make the addition, qualification, exception, or unresolved conflict visible in the ordinary capture proposal. Reuse the current context; do not force links, create a duplicate, or collect the whole conversation. A direct Human statement and the agent's inferred lesson retain different status. These are content requirements, not new mandatory fields or a reason to propose a capture every turn. Human confirmation and the existing mode rules still govern saving.

Use the relevant recent exchange, including the turns that supplied the material conditions. When the mode permits an unsolicited proposal, there is a concrete future use, and the memory has no equivalent entry, put one short proposal at the end of the substantive reply. If an effective instruction asks to defer proposals, keep the candidate in the working context and revisit it at the first suitable pause while unsolicited proposals remain permitted. Passive mode does not require a hidden backlog of capture candidates. Keep an untested idea marked as an idea and use Human confirmation for capture.

Put the proposal in a separate Markdown block after the substantive answer. Use a thematic break (`---`) on a line of its own with a blank line on each side, then a level-three heading in the language of the reply. Use the heading listed for that language in the connected memory's index when available. In English, use `### Suggest saving to S3S4Memory`. In active mode, append the reply-language equivalent of `(active search)` to the base heading; in Russian use `### Предлагаю сохранить в меме (активный поиск)`. The neutral Russian heading is `### Предлагаю сохранить в меме`. Passive mode has no unsolicited proposal block. Keep the proposed content, future use, and basis together under the heading.

Recognize `в меме` and `in meme` case-insensitively as complete phrases at the start of a Human request, with a phrase boundary.

## Choose the engram language

When creating an engram, use the language Human selects for that entry. Otherwise use the default language declared in the connected memory's index. Write the title, file name, body, section headings, rating labels, and corresponding index entry in that language. Use the title for the file name, replacing characters the filesystem cannot safely use. Add the stable engram ID as a suffix if needed to avoid a collision. Keep technical identifiers, YAML keys, and enumerated front matter values in their defined spelling. When revising an existing engram, retain its language unless Human requests a change.

## Record a confirmed change

EG checks the concrete write against the instruction, memory scope, and actual write access. WEC owns that write. Delegated readers return applicable entries and proposed changes to the working agent. When access is missing, report the pending change and its exact destination. File operations use one writer for the affected notes and index. If another writer's change conflicts with the intended update, reconcile the current files before proceeding.

1. [Choose the engram language](#choose-the-engram-language). Use the index classifier (`note`, `idea`, `conclusion`, `decision`, `method`, `summary`). Give a new note a stable `id`, the capture `date`, `kind`, `status: active`, `last_used: null`, and `use_count: 0` in YAML front matter. Save the Markdown file under `Энграммы/YYYY-MM-DD/` with its title as the file name and the `.md` extension. Record the reusable content, when it helps, material conditions, and the direct source or decision. [Record the capture decision](#capture-decision). For time-sensitive claims, include the applicable dates under `time_sensitive`. Give it an index entry with a recognizable situation or question, the first useful result, and the relative note link. Add links to existing notes where a stated relation helps a future working question.
2. If a decision or its material conditions change, create a new engram and link the old and new notes with the scope of replacement. For a complete replacement mark the old note `superseded`. For a partial replacement keep both active and show where each applies. If the change is only an editorial correction to the same content, preserve the existing ID and use history. When changing a file name, update and check its index entry and affected links.
3. Before an update spanning several files, preserve the intended note IDs, affected paths, and expected edits in the working record. On interruption, inspect those exact files, complete missing edits for the same change, and reconcile conflicts before repeating a write. After writing, reopen the changed files and verify the body, index link, and any affected status or replacement link. Report what was saved and its address only after that check.

### Capture decision

For every new engram, add a **Capture decision** entry in the engram's language. Record the project and the exact title and ID of the chat in which Human gave the save instruction or confirmed the proposal. Include a link to that chat when available. For a deferred write, use the project and chat of the original decision. Cite the source of the material separately.

If the exact title or ID has not been verified, use available and authorized chat tools before marking either unavailable. In Codex, use `list_threads` when needed to find candidates in the relevant project, then use `read_thread` to confirm the save instruction or approval. If the tools are unavailable or some details remain uncertain after checking, record the verified details and mark the gaps explicitly.

### Notes, summaries, and source material

Use `note` for a standalone note, observation, or working detail whose content can be used directly. Use `summary` for an account of the main points of a text, talk, or conversation.

When the full text of a long-form work or material with illustrations needs to be kept, store the original outside S3S4Memory. Record a useful note or summary in the engram, state when to retrieve it, and link to the original. Follow the [external link rule](#external-links-from-engrams) when opening the source.

## Record personal importance

An engram can include an **Importance** section in its Markdown body. Use the engram's language for the heading, rating label, and reason. Record the rating and why the experience matters to Human now. Use one of the following levels.

- **Very important** — Human wants DEC to bring up this experience when it applies.
- **Important** — bring it up when working on a similar question.
- **Neutral** — ordinary working experience with standard priority.
- **Not important** — low priority now, with possible value when reviewing history.

Human sets or confirms the rating. The agent may propose one based on what Human says matters. Leave the section empty or omit it for an unrated engram. **Neutral** is an explicit rating.

Record the date of the assessment and a condition for revisiting it when useful. When Human revises a rating, update the same section with the current rating and reason. Preserve earlier grounds when they help explain a later decision.

Apply the search conditions in [Find experience](#find-experience) first. An applicable engram rated **Very important** may be surfaced on the agent's initiative.

## Project memory-access journal

Keep `project/artifacts/DEC_MEMORY_LOG.md` in the active project, creating it on the first actual memory consultation. Use one brief entry for a working event: a stable event ID unique across consulting projects/chats and the actual use date, the working question or cue, examined and adopted engrams (IDs or links), the disposition, and the changed action or unresolved result. A related-note traversal belongs to the same event; a materially different question can start another. Reuse the same event ID for use counts and retries. Record consultations that find nothing or reject all candidates as well as adoption; candidate inspection in the journal does not itself increment an engram's use count. Do not log every file/tool operation, repeat a journal entry for a retry, or copy full memory contents into the journal. Metadata maintenance and a repeated use of already sufficient working context do not create another consultation entry.

Distinguish no result, not applicable, applicability unresolved, examined but not adopted, and adopted experience; an event can contain different dispositions for different notes. Add a known effect or a useful later correction to the same entry. “Found”, “adopted”, and “helped” remain different claims: leave benefit unknown when not established, and do not change rankings or memory content merely because an entry exists. The journal is an observation aid, not a new permission or a mandatory report to Human after each search.

WEC keeps the event, affected note references, and pending effects recoverable in this journal or a sufficient existing work record before a multi-file update. Group the short journal and usage updates where the ADE and write authority allow; verify actual files without separate per-access report files. After interruption or an uncertain write, inspect the existing journal entry and each note's `use_events` before completing the same event. A journal entry does not prove that all counters were written, and a counter does not prove that the journal is complete. Reconcile the missing part only; preserve conflicting edits and report a blocked write without claiming completion. Keep the useful finding available while this bookkeeping finishes.

## Count actual use

When a note enters the working context as a basis for the task, WEC records one use of that note for the working event, independently of whether the outcome later proves useful. For new events, use an ID unique across projects and chats consulting the memory (for example, a UUID or a project/chat identifier plus a local event ID), and carry that same ID through delegation and retries. With the same write conditions as above, update `last_used` to the latest date of use, increment `use_count` once, and retain that event ID in the same front matter as `use_events` (a sequence of strings). A missing `use_events` starts as an empty sequence and preserves the existing count. If the ID already appears, the event has been counted. An index read, candidate inspection, or memory maintenance alone leaves usage unchanged. If a use cannot be recorded, keep the note and event ID in the work record when a retry is needed.

Within assigned work using connected DEC, maintaining the project journal and the usage fields is routine bookkeeping; it does not require confirmation of new engram content. Actual project/memory write access and EG checks remain required. This authority covers only the journal and `last_used`, `use_count`, and `use_events`; it does not authorize changes to engram bodies, status, ratings, or the memory index. If task scope or access does not permit a write, retain the pending event in the project record and report the limitation.

For routine usage-metadata updates, group reading the current fields, checking the event ID, making the authorized change, and reopening the result in one tool call when the ADE permits. Separate staging, backup, and use-report files are not required for each such update. Reuse sufficient recoverable working context or an existing task record; retain a separate recovery record when interruption, conflicting changes, uncertain effects, or another dependent use requires it. This changes neither what counts as use nor write authority; preserve the note body and count the same event only once.
