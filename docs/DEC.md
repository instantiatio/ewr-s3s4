# DEC — Dynamic Engram Control

> What from our experience can help us now and in the future?

DEC helps EWR S3S4 reuse joint experience and propose what to remember. The working agent performs DEC using Markdown and available file operations. [ARCHITECTURE.json](../ARCHITECTURE.json) holds the connection settings in `work_support.DEC`. If DEC is disabled, memory is unavailable, or no entry fits, CF and DMG continue from their other grounds. For an explicit memory request, report the relevant limitation.

Memebase is the working engram store. Memebase and DEC form the current EWR S3S4 memory architecture.

The earlier Associative Field architecture and its associated mechanisms are historical research. Its trial results apply to the versions and conditions tested.

## Capabilities and boundaries

| Capability | Contribution to joint work | Operational rule |
| --- | --- | --- |
| Initiated recall | Recognize a material work cue and bring applicable experience into the current decision without a special recall command. | [Find experience](#find-experience) |
| Shared tasks and events | Record and reschedule commitments in Memebase and find dated records across connected installations. | [Tasks, events, and the structured index](#tasks-events-and-the-structured-index) |
| Connected understanding | Recover a bounded synthesis, distinction, or open question from relevant engrams and state its effect on the next action. | [Find experience](#find-experience) |
| Experience acquisition | Notice a reusable acquisition and relate it to existing experience, within the current proposal mode; new memory content is saved only when authorized. | [Propose what to remember](#propose-what-to-remember) |
| Consultation journal | Preserve the question, examined/adopted experience, selection outcome and known effect in `project/artifacts/DEC_MEMORY_LOG.md`, including empty or rejected consultations. | [Project memory-access journal](#project-memory-access-journal) |
| Usage and continuation | Count adoption once per working event, distinguish it from benefit, and reconcile journal/counter state after interruption. | [Count actual use](#count-actual-use) |
| Conditional revision | Retain sources, applicability, exceptions and replacement scope when confirmed memory content changes. | [Record a confirmed change](#record-a-confirmed-change) |

The working agent enacts these rules through the available ADE. They introduce no background memory service, whole-memory search before every operation, or automatic permission to change engram content. Proposal modes control capture initiative, not retrieval. Routine authorized journal/usage maintenance and confirmation of new memory content remain separate. [ConOps](EWR_CONOPS.md#memebase-and-dec) explains the functional relationships; [STATUS](../STATUS.md) states the checked scope and remaining limits.

## Connect Memebase

A clean installation has `work_support.DEC.enabled` set to `false` and `field_index` set to `null`. To connect or replace Memebase, give the agent the directory path and ask it to connect that memory. The agent performs these steps in the chosen installation.

1. Read the current `work_support.DEC` settings in [ARCHITECTURE.json](../ARCHITECTURE.json). Keep the current `enabled` and `field_index` values recoverable until the change is verified.
2. Before changing the settings, confirm that `Index.yaml` and `Engrams/` resolve inside the selected memory directory and are readable in the current agent execution environment. Read the schema version and entries. For a nonempty index, resolve a candidate `path` relative to the index, including any symbolic links, before opening its target. Skip targets outside the resolved `Engrams/` directory. The access check passes for a nonempty index when one eligible engram opens. For an empty index, confirm it is readable and `Engrams/` has no engrams. If a legacy Markdown catalogue still holds navigation cues, use the [migration procedure](#migrate-an-existing-memebase) before activating the replacement.
3. If the access check fails, leave both settings as found and report what could not be opened or which eligible sample is missing. On success, prepare the new settings. Set `field_index` to the path from the installation root to `Index.yaml` and `enabled` to `true`. For a memory directory next to the installation, use `../Memebase/Index.yaml`. Keep this intended pair recoverable alongside the prior pair before writing both settings together in `ARCHITECTURE.json`.
4. Reopen the configuration and confirm both values. Check retrieval using a question covered by the new index, equivalent to `из меме <вопрос>` or `from meme <question>`. For an empty index, confirm that it still opens. Both the initial access check and this retrieval check are connection checks. They leave the usage fields described in [Count actual use](#count-actual-use) untouched.
5. If the update or retrieval check fails after the write was attempted, reopen `ARCHITECTURE.json`. Compare its current `enabled` and `field_index` together with the prior pair from step 1 and the intended pair from step 3.
   - If the pair cannot be read, either setting is known to have been changed by another writer since the attempt, or the pair matches neither saved pair, leave the configuration as found. Report why recovery stopped and what connection state you could verify.
   - If the pair matches the prior pair, keep it. If it matches only the intended pair, restore the prior pair and reopen the file to verify it.

   Once the prior pair is confirmed, repeat the access check if that connection was enabled. During migration, check a restored legacy connection under its saved prior procedure and index format. If the prior memory is also unavailable, retain its `field_index`, set `enabled` to `false` and verify the result. Report the failure and the connection state you could verify.

   For each recovery write, compare against the expected pair at the write using a conditional update or one writer for the comparison and write. Expect the intended pair when restoring the prior pair, and the prior pair when disabling an unavailable prior connection. Preserve all other current settings. If you cannot make the write under those conditions, leave the configuration as found and report why recovery stopped.

The memory stays in the selected directory. Saving or updating entries requires write access granted by the agent execution environment and authorization under the procedure below. To disconnect the memory, set `work_support.DEC.enabled` to `false`.

### Create and connect a new Memebase

When Human asks to create and connect a new memory, use the requested directory or the location clear from the current project. Clarify the destination if the remaining options differ materially. Check write access and choose a new directory or an empty one for initialization. If the destination already contains memory files, preserve them and resolve whether Human intended to connect that memory or create a separate one.

Create `Engrams/` and `Attachments/`. Copy [readmemebase.md](readmemebase.md) into the memory root as its handbook. Use its default engram language unless Human chooses another, and record the effective language in the handbook. Initialize `Index.yaml` with `schema_version: 2` and an empty `entries` list. Apply the [connection procedure](#connect-memebase) to the new directory, then verify the handbook and empty index. In the confirmation, give the memory location and the handbook link. Keep an existing handbook when connecting an already initialized memory.

### Migrate an existing Memebase

Preserve the previous indexes, connection settings, and before-state of files that will change. On a copy, resolve each legacy `Index.md` navigation link to an engram and transfer its situation and useful result to that engram's `navigation` list. Preserve multiple situations for one ID and keep an alternate link title when it supplies a distinct label. Retain the engram's ID, status, usage history, paths, body and links. Carry the base's language and other guidance into `readmemebase.md` when needed. Resolve missing, ambiguous or out-of-scope targets before replacing the previous catalogue.

Rebuild `Index.yaml` from the engrams and compare all IDs and migrated navigation cues. Check a semantic lookup, a dated lookup, and recovery after rebuilding. Apply the checked mapping under the confirmed-change writer rules. Switch the authorized installation through [Connect Memebase](#connect-memebase), verify retrieval, then archive the legacy catalogue outside the active memory root. If a write is interrupted, reconcile the source records and index against the preserved before-state and the planned changes before continuing the switch.

## External links from engrams

Follow a link from an engram to a web page or to a local target that resolves outside the connected memory directory only with Human's permission. The current instruction is sufficient when it already authorizes reading that source.

Apply this rule during retrieval and review. If an external source is needed and permission is missing, ask Human, naming the source and what needs checking. Continue with the available grounds and state what remains unchecked.

## Find experience

1. Start from the current working question and the decision the result could change. When work starts, resumes, changes direction materially, or reaches a consequential choice, CF considers whether joint experience could change the understanding, constraint, or next action. DMG does so when choosing or adapting a method. When there is a relevant cue, consult DEC without waiting for a Human recall command; reuse already sufficient experience instead of repeating a search. A routine tool call or file edit alone is not a reason to search. Human may ask directly with `из меме <вопрос>`, `из мемебазы <вопрос>`, `from meme <question>`, or `from memebase <question>`.
2. Read the configured `Index.yaml` using the [index rules](#index-schema-and-rebuild). Use an entry's title and `navigation` cues and results to choose candidates for the working question. Before opening a candidate, resolve its `path` relative to the index, including any symbolic links. Open the target only if it resolves inside the connected memory's `Engrams/` directory and that directory itself resolves inside the connected memory. Skip candidates that do not meet this check and continue with eligible entries. Check the note's conditions against the current question. Follow links to related engrams only when the stated relation helps, using the same path check relative to the linking engram. Check the source when the next action depends on an exact condition, decision, or edition, subject to the [external link rule](#external-links-from-engrams). Method lookup follows the [existing source policy](../AGENTS.md#method-source-priority).
3. Use active notes in their applicable scope. Historical queries may use superseded notes. Among equally applicable notes, prefer the later `last_used`, using `date` for a new note. Break ties by higher `use_count` and then by `id`. Return the relevant content, note link, degree of support for the claim being reused, and any condition material to its use. CF or DMG decides what to adopt and carries that support and its limits into the working context.

When one engram is insufficient for the working question, open only related notes whose relation can change the answer. Recover what they jointly support, qualify, contradict, or leave open, with the source conditions and claim status. Return a bounded synthesis, contrast, useful new question, or method alternative to CF/DMG and state what it changes in the current work. Keep an agent interpretation distinct from a Human decision; a coherent account or silence does not establish shared understanding. Ask Human when a material interpretation, preference, or authority is unresolved, using the existing interaction rather than a separate approval for every link. Stop when the receiving question has sufficient grounds. New material may also reopen an already-known, still-relevant open question; it does not authorize a sweep of all past work or a new action on a completed assignment.

Use applicable experience independently within the mandate. Surface a material limitation before the Human decision it can change; take a nonurgent idea to a natural pause and recheck its relevance then. This does not introduce a background watcher or an automatic interruption schedule.

For a straightforward recall question, reuse sufficient connection and procedure grounds already recovered in this chat; recheck a material change or uncertainty. Once the note, its status, and the relevant conditions support an answer, give a brief finding update with the useful fact and note link if further bookkeeping calls would delay the reply. Complete the necessary bookkeeping in the same turn before the final reply, or report the exact pending update if it is blocked. Do not present an unchecked interpretation as a settled finding.

Use an untested idea as a hypothesis to check. For ambiguous experience, distinguish what was observed from the possible interpretations. Use a refuted claim as a counterexample and carry the correction and its scope. When support is unclear and the next action depends on it, check the cited source and retain any remaining uncertainty.

## Tasks, events, and the structured index

### Record and reschedule

- A direct request to record a task or event in Memebase authorizes the corresponding note write. In a conversation already using Memebase for scheduling, that includes a clear request such as `поставь задачу на сегодня в 15:00`. Use `kind: task` for an action to perform and `kind: event` for an occurrence. Keep ordinary task instructions in their working context unless the user requests a memory record or the active conversation establishes that destination.
- Preserve `date` as the capture date. Store optional `starts_at` and `ends_at` as top-level YAML scalars. Use `YYYY-MM-DD` for dates without a time and an ISO 8601 timestamp with its UTC offset for a specified time. Resolve relative dates in the user's working time zone. If a time zone or a necessary date is materially ambiguous, ask for that detail. Leave an unknown end absent. When supplied, it must use the same precision as the start and be equal to or later than it. Equal endpoints denote an instant. Calculate duration from both boundaries when requested. Retain a stated task deadline as a deadline in the body when it is distinct from its planned work time. Use [review time-sensitive claims](#review-time-sensitive-claims) for applicability or review dates.
- For rescheduling, recover the existing record by ID or unambiguous context. Keep its ID, capture date, path, and related links. Update the intended start and end. If only a new start is given, carry forward a known elapsed duration or all-day span unless the user changes it. An absent end stays absent. Edit affected time references in the body and navigation cues. Existing records can receive structured dates when Human authorizes that edit and their timing is known.
- Use [the confirmed-change procedure](#record-a-confirmed-change) for the note and the derived `Index.yaml`. If refreshing fails, report the source result and the index state separately. Confirm a time in the user's working zone and link the resulting record.

### Find dated records

For requests such as `что запланировано на сегодня?`, `покажи события за неделю` or `найди задачу по ID`, use the connected Memebase. By default, list active records. An explicit ID or historical request may find inactive records. Resolve date words using the user's working date and zone. A period includes its start and excludes its end. Include intervals that overlap the period. With only a start, or equal endpoints, include the record when the start falls inside the period. Date-only records use the corresponding local dates. When the question distinguishes a plan from what took place, check the selected records' descriptions for that distinction. Undated records remain searchable by ID, kind and ordinary semantic retrieval through `Index.yaml`.

### Index schema and rebuild

`Index.yaml` is the sole Memebase index and is derived from engram files. Its schema version is `2`. Each item in `entries` carries `id`, `title`, Memebase-relative `path`, `kind`, `status`, a `navigation` list and available `date`, `starts_at` and `ends_at`. The default title is the file stem. An engram may store `title` when the intended title differs. Each navigation item contains a `cue` and may carry a `result` and an alternate `label`. Add the intended cues in the engram's front matter and rebuild the index from the sources.

The expanded projection also carries the available `last_used` date and nonnegative integer `use_count`, `importance` and `links`. Read the usage values from the front matter. Prefer the canonical rating in the [engram front matter](#record-personal-importance). The helper can also recover English, Russian and French legacy ratings from the Importance section. Other historical ratings need a confirmed canonical value for automatic projection. The index uses `unrated` when no rating is available to the helper.

For `links`, map local Markdown destinations to IDs of indexed engrams within the memory, ignore page fragments and retain each target once, in first-appearance order. The helper recognizes single-line inline links with optional titles and balanced label brackets, and reference links with single-line definitions. An unquoted destination may contain balanced parentheses or backslash-escaped punctuation. A reference definition can begin a paragraph or follow another definition at its start. A definition-shaped line continuing ordinary paragraph text is read as text. It skips images, inline code, indented code blocks and fences, including fences started in a list item. Within a paragraph, matching backtick runs delimit inline code and can enclose a line break. A backslash can escape an opening backtick in ordinary text. Inline code also excludes example rating lines and reference definitions from the projection. Use those supported forms when a link needs to appear in the index. The engram remains the source for the meaning and scope of a link and the reason for a rating. A consumer can derive backlinks from the outgoing IDs. Rebuild earlier schema 2 indexes to obtain the expanded projection.

Use a current, verified index when available. Before opening a result, verify its path under `Engrams/` using the ordinary link check and confirm the needed fields in the note. File signatures can detect changed sources; they do not establish that index values match those sources. For a complete answer when the index has not been verified, use the source records to select entries as well as to confirm returned fields. If incomplete access or invalid metadata prevents a complete result, report the affected scope. An explicit rebuild derives entries anew and must reject duplicate IDs and conflicting or invalid dates. Publish the complete new index in one replacement under the confirmed-change writer rules.

The [optional helper](../tools/memebase_index.py) uses Python 3.11 or newer and its standard library. Source fields use plain or quoted single-line scalars, with `navigation` as a single-line JSON-compatible YAML list. Its output is JSON-form YAML with observed file signatures in `source`. `query` selects and returns fields from current engram metadata. `check` compares the whole index with the source projection, and `build` publishes that projection. With ADE file operations, read and verify the same fields and build or search the index directly. An index without helper file signatures can be checked by comparing its projected fields with the source records. Read-only queries leave the index file as found.

The local dashboard caches a source-verified projection for the current file signatures. It can reuse the verified index on later requests and reads the selected engram body when the reader opens it. If the index is absent or differs from the source projection, the dashboard uses the source projection in memory. A change to the source files triggers a fresh verification.

```yaml
navigation: [{"cue": "Preparing a pilot review", "result": "Identify the decisions that depend on the review."}]
```

```sh
python3 -B tools/memebase_index.py "/path/to/Memebase" build
python3 -B tools/memebase_index.py "/path/to/Memebase" check
python3 -B tools/memebase_index.py "/path/to/Memebase" query --text "pilot review"
python3 -B tools/memebase_index.py "/path/to/Memebase" query --kind task --on 2026-11-23 --timezone Europe/Moscow
```

## Review time-sensitive claims

At capture, label a claim whose applicability may change with time. Store an optional `time_sensitive` list in the Markdown note's YAML front matter. Use one item per affected statement, identified by `claim`. Record the last actual verification in `checked_on` (or `null` if unknown) and add `valid_until` or `review_after` where known. Use ISO dates (`YYYY-MM-DD`). For example:

```yaml
time_sensitive: [{"claim": "Recommended models for our tasks", "checked_on": "2026-11-18", "review_after": "2026-12-18"}]
```

When Human asks to refresh the memory, the agent searches for the `time_sensitive:` key in the Markdown files under `Engrams/` next to the memory index. Open the matches, confirm the key is in the front matter and the note is active, then compare each marked claim's dates with the date in Human's working context. Apply the first matching rule:

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
| `DEC: active` or `DEC: режим предложений — активный` | Select active mode for this chat. |
| `DEC: neutral` or `DEC: режим предложений — нейтральный` | Select neutral mode for this chat. |
| `DEC: passive` or `DEC: режим предложений — пассивный` | Select passive mode for this chat. |
| `DEC: status` or `DEC: статус` | Report the current connection state and proposal mode separately. |

HI confirms a switch in the reply language, naming both states. For example: `Режим предложений: пассивный. DEC включён.` Report actual access limitations separately; do not turn an enabled setting into a claim that the memory is readable or writable. When DEC is disabled, report proposal initiative as inactive. If a request is ambiguous between changing proposal initiative and disconnecting DEC, clarify that choice instead of inferring a connection change.

Active searching does not require a proposal in every answer or lower the capture threshold. Distinguish seeking a candidate from interrupting Human: place a useful proposal at a natural pause. In every mode, proposing a capture and obtaining authority to write are separate actions; a mode switch never authorizes an automatic save.

## Propose what to remember

Apply the current [proposal initiative mode](#proposal-initiative-modes). In neutral or active mode, when joint work settles a decision, yields a finding, or surfaces an idea, consider whether it would help in a specific recurring situation that matters to Human. Check for an equivalent entry and propose only a material addition or change. For a useful candidate, state what to save, when it would help, and its basis in a short HI proposal. Keep an unresolved idea marked as an idea. In passive mode, omit unsolicited proposals; an explicit Human request to consider or save material still follows this procedure. Use Human's confirmation of the proposed content and scope as the basis for capture. A clear [capture command](#capture-commands) directly requests capture of the indicated material. Clarify a referent if the ambiguity would change what gets written.

When the current proposal mode permits initiative, consider reusable acquisitions at a meaningful result, correction, changed understanding, or natural pause, including ordinary successful work. A useful candidate states what was learned, a recognizable future use, material applicability conditions, and the episode supporting it. Compare with existing experience: when the new contribution can change its meaning, recover sufficient relevant notes and make the addition, qualification, exception, or unresolved conflict visible in the ordinary capture proposal. Reuse the current context; do not force links, create a duplicate, or collect the whole conversation. A direct Human statement and the agent's inferred lesson retain different status. These are content requirements, not new mandatory fields or a reason to propose a capture every turn. Human confirmation and the existing mode rules still govern saving.

Use the relevant recent exchange, including the turns that supplied the material conditions. When the mode permits an unsolicited proposal, there is a concrete future use, and the memory has no equivalent entry, put one short proposal at the end of the substantive reply. If an effective instruction asks to defer proposals, keep the candidate in the working context and revisit it at the first suitable pause while unsolicited proposals remain permitted. Passive mode does not require a hidden backlog of capture candidates. Keep an untested idea marked as an idea and use Human confirmation for capture.

Put the proposal in a separate Markdown block after the substantive answer. Use a thematic break (`---`) on a line of its own with a blank line on each side, then a level-three heading in the language of the reply. In English, use `### Suggest saving to Memebase`. In active mode, append the reply-language equivalent of `(active search)` to the base heading; in Russian use `### Предлагаю сохранить в меме (активный поиск)`. The neutral Russian heading is `### Предлагаю сохранить в меме`. Passive mode has no unsolicited proposal block. Keep the proposed content, future use, and basis together under the heading.

### Capture commands

Recognize these case-insensitive command phrases at the start of a direct Human request, with a phrase boundary. Check the longer form first. Quoted phrases and examples carry no save instruction.

- `сохрани в меме с приложениями`, `в меме с приложениями`, or `save to memebase with attachments` saves the engram and the source files Human indicates, following [Source attachments](#source-attachments).
- `сохрани в меме`, `запиши в меме`, `сохрани в мемебазу`, `в меме`, `в мемебазу`, `in meme`, `in memebase`, or `save to memebase` saves the engram. Use a link if a source needs to be available for later verification.

## Choose the engram language

When creating an engram, use the language Human selects for that entry. Otherwise use the default declared in the connected memory's `readmemebase.md`, or English if no default is declared. Write the title, file name, body, section headings, rating labels, and navigation cues in that language. Use the title for the file name, replacing characters the filesystem cannot safely use. Add the stable engram ID as a suffix if needed to avoid a collision. Keep technical identifiers, YAML keys, and enumerated front matter values in their defined spelling. When revising an existing engram, retain its language unless Human requests a change.

## Record a confirmed change

EG checks the concrete write against the instruction, memory scope, and actual write access. WEC owns that write. Delegated readers return applicable entries and proposed changes to the working agent. When access is missing, report the pending change and its exact destination. File operations use one writer for the affected notes and index. If another writer's change conflicts with the intended update, reconcile the current files before proceeding.

1. [Choose the engram language](#choose-the-engram-language). Use the index classifier (`note`, `idea`, `conclusion`, `decision`, `method`, `summary`, `task`, `event`). Give a new note a stable `id`, the capture `date`, `kind`, `status: active`, `last_used: null`, and `use_count: 0` in YAML front matter. Prepare the Markdown content and choose its destination under `Engrams/YYYY-MM-DD/` with its title as the file name and the `.md` extension. Include the reusable content, when it helps, material conditions, and the direct source or decision. [Record the capture decision](#capture-decision). For time-sensitive claims, include the applicable dates under `time_sensitive`. Store a recognizable situation or question and the first useful result in the note's [`navigation` list](#index-schema-and-rebuild). Include links to existing notes where a stated relation helps a future working question. For tasks and events, also use the [structured time fields](#tasks-events-and-the-structured-index).
2. If a decision or its material conditions change, prepare a new engram and plan links between the old and new notes that state the scope of replacement. For a complete replacement, plan to mark the old note `superseded`. For a partial replacement, keep both active and show where each applies. If the change is only an editorial correction to the same content, preserve the existing ID and use history. If the file name will change, include the index entry and affected links in the planned edits.
3. Before writing the first engram or editing any other affected memory file, save the engram IDs, affected file paths, and expected edits in a work record that can be reopened after an interruption. Include the intended index entry or link change and any derived index refresh required by the change. Then apply the recorded edits.
4. If interrupted, reopen the work record and compare the files at the recorded paths with the expected edits. Reconcile conflicts before writing, then complete only the missing edits using the recorded IDs and paths. If the saved engram already matches the record and its index entry is missing, rebuild the index from the current source records.
5. Reopen the changed files and verify the body and any affected status or replacement link. After a change to projected fields or the file set, rebuild `Index.yaml` and verify that its entries point to the resulting records. Report what was saved and its address only after checking the source changes. Report an outstanding index refresh separately.

### Capture decision

For every new engram, add a **Capture decision** entry in the engram's language. Record the project and the exact title and ID of the chat in which Human gave the save instruction or confirmed the proposal. Include a link to that chat when available. For a deferred write, use the project and chat of the original decision. Cite the source of the material separately.

If the exact title or ID has not been verified, use available and authorized chat tools before marking either unavailable. In Codex, use `list_threads` when needed to find candidates in the relevant project, then use `read_thread` to confirm the save instruction or approval. If the tools are unavailable or some details remain uncertain after checking, record the verified details and mark the gaps explicitly.

### Notes, summaries, and source material

Use `note` for a standalone note, observation, or working detail whose content can be used directly. Use `summary` for an account of the main points of a text, talk, or conversation.

For ordinary capture, keep full texts and illustrated originals outside Memebase. Record a useful note or summary in the engram, tell the reader when to retrieve the original, and link to it. Follow the [external link rule](#external-links-from-engrams) when opening the source.

### Source attachments

With the [explicit attachments command](#capture-commands), copy the accessible original bytes of the files Human indicates. If it is unclear which files are meant, clarify that before copying. The source must be readable and the destination writable within the authorized scope.

1. Use `Attachments/YYYY-MM/<engram-id>/` inside the connected memory, next to `Engrams/`. Use the month of addition. Check that the destination and its existing parent directories stay inside the connected memory after resolving symbolic links. Use each supplied file name as a name only. If it is occupied, choose an unused name and preserve the existing file.
2. Include the source and destination paths, byte-verification basis and intended relative links in the [work record for the change](#record-a-confirmed-change) before writing. Create the folders as needed and copy without overwriting. Verify each copy against its original by bytes or digest before adding its link. On retry, reuse a recorded copy after verifying it. If a requested original is unavailable or its copy cannot be verified, report the item and keep the capture pending.
3. Save the short engram with the verified relative links and a note on when to open the material. Check that the engram and its index link work and its attachment links open the expected copies. Report the saved engram and attachment paths. Keep the paths stable so other engrams can link to the same copies.

## Record personal importance

An engram can include an **Importance** section in its Markdown body. Use the engram's language for the heading, rating label, and reason. Record the rating and why the experience matters to Human now. Use one of the following levels.

- **Very important** — Human wants DEC to bring up this experience when it applies.
- **Important** — bring it up when working on a similar question.
- **Neutral** — ordinary working experience with standard priority.
- **Not important** — low priority now, with possible value when reviewing history.

Human sets or confirms the rating. The agent may propose one based on what Human says matters. Leave the section empty or omit it for an unrated engram. **Neutral** is an explicit rating.

When recording or revising a confirmed rating, write the matching canonical `importance` value in the engram's YAML front matter. Use `very-important`, `important`, `neutral`, or `not-important`. Keep the human-readable rating and reason in the engram's language. When clearing the rating, remove the front matter field and clear the rating line in the body.

Record the date of the assessment and a condition for revisiting it when useful. When Human revises a rating, update the same section with the current rating and reason. Preserve earlier grounds when they help explain a later decision.

Apply the search conditions in [Find experience](#find-experience) first. An applicable engram rated **Very important** may be surfaced on the agent's initiative.

## Project memory-access journal

Keep `project/artifacts/DEC_MEMORY_LOG.md` in the active project, creating it on the first actual memory consultation. Use one brief entry for a working event: a stable event ID unique across consulting projects/chats and the actual use date, the working question or cue, examined and adopted engrams (IDs or links), the disposition, and the changed action or unresolved result. A related-note traversal belongs to the same event; a materially different question can start another. Reuse the same event ID for use counts and retries. Record consultations that find nothing or reject all candidates as well as adoption; candidate inspection in the journal does not itself increment an engram's use count. Do not log every file/tool operation, repeat a journal entry for a retry, or copy full memory contents into the journal. Metadata maintenance and a repeated use of already sufficient working context do not create another consultation entry.

Distinguish no result, not applicable, applicability unresolved, examined but not adopted, and adopted experience; an event can contain different dispositions for different notes. Add a known effect or a useful later correction to the same entry. “Found”, “adopted”, and “helped” remain different claims: leave benefit unknown when not established, and do not change rankings or memory content merely because an entry exists. The journal is an observation aid, not a new permission or a mandatory report to Human after each search.

WEC keeps the event, affected note references, and pending effects recoverable in this journal or a sufficient existing work record before a multi-file update. Group the short journal and usage updates where the ADE and write authority allow; verify actual files without separate per-access report files. After interruption or an uncertain write, inspect the existing journal entry and each note's `use_events` before completing the same event. A journal entry does not prove that all counters were written, and a counter does not prove that the journal is complete. Reconcile the missing part only; preserve conflicting edits and report a blocked write without claiming completion. Keep the useful finding available while this bookkeeping finishes.

## Count actual use

When a note enters the working context as a basis for the task, WEC records one use of that note for the working event, independently of whether the outcome later proves useful. For new events, use an ID unique across projects and chats consulting the memory (for example, a UUID or a project/chat identifier plus a local event ID), and carry that same ID through delegation and retries. With the same write conditions as above, update `last_used` to the latest date of use, increment `use_count` once, and retain that event ID in the same front matter as `use_events` (a sequence of strings). A missing `use_events` starts as an empty sequence and preserves the existing count. If the ID already appears, the event has been counted. An index read, candidate inspection, or memory maintenance alone leaves usage unchanged. If a use cannot be recorded, keep the note and event ID in the work record when a retry is needed.

Within assigned work using connected DEC, maintaining the project journal and the usage fields is routine bookkeeping; it does not require confirmation of new engram content. Actual project/memory write access and EG checks remain required. This authority covers only the journal and `last_used`, `use_count`, and `use_events`; it does not authorize changes to engram bodies, status, ratings, or the memory index. If task scope or access does not permit a write, retain the pending event in the project record and report the limitation.

After a usage update, use the source fields for ranking if index freshness has not been established. Refresh the index when the task authorizes that write.

For routine usage-metadata updates, group reading the current fields, checking the event ID, making the authorized change, and reopening the result in one tool call when the ADE permits. Separate staging, backup, and use-report files are not required for each such update. Reuse sufficient recoverable working context or an existing task record; retain a separate recovery record when interruption, conflicting changes, uncertain effects, or another dependent use requires it. This changes neither what counts as use nor write authority; preserve the note body and count the same event only once.
