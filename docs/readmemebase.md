# Memebase Quick Guide

**Memebase** stands for **MEM**ory **E**ngram **Base**. **S3S4Memory** is a historical name. Here, *meme* refers to a **MEM**ory **E**ngram.

**Memebase and DEC provide external memory for EWR S3S4.** Memebase stores selected experience from work. DEC (Dynamic Engram Control) retrieves applicable experience, connects related records, and proposes what could be worth keeping. The agent saves new material when you ask it to or confirm a proposal.

**An engram** records a useful finding or way of working, its conditions of applicability, and its source. A cue about when to recall it helps DEC find it in a relevant situation.

The earlier Associative Field architecture is part of the research history. Its observations apply to the versions and conditions tested.

**Default engram language.** English (`en`).

**File names.** The file name follows the engram's title in its own language. Its `id` is stable across title changes.

## Getting started

| Action | Short forms | Full request |
| --- | --- | --- |
| Create or connect a Memebase | `Connect Memebase` | `Create and connect a new Memebase in the folder I specified.` |
| Save experience | `save to Memebase`, `in meme`, `in memebase` | `Save to Memebase this finding and the conditions under which it applies.` |
| Save experience with source files | `save to Memebase with attachments` | `Save to Memebase with attachments. Include this finding and the Markdown file I attached.` |
| Recall experience | `from meme`, `from memebase` | `From Memebase, find what we learned about checking a hypothesis before development and tell me when it applies.` |
| Record or move a task | `Schedule in Memebase`, `Move the task in Memebase` | `Schedule a task in Memebase to think about the article tomorrow at 15:00 Moscow time.` Or `Move the article task to 16:00 Moscow time.` |
| Find scheduled records | `Show tomorrow’s Memebase tasks` | `Show the tasks and events in Memebase for tomorrow in Moscow time.` |

Task workflows are experimental in EWR S3S4 8.0.1.

## What Memebase stores

- `Engrams/` holds Markdown engrams with YAML metadata.
- `Attachments/` holds copies of source files attached by explicit request.
- `Index.yaml` connects DEC to the base and contains links and cues for finding engrams by situation, ID, kind, or date range. It is rebuilt from engram metadata.

## How to use an engram

Engrams live in folders named for their capture dates in `YYYY-MM-DD` format.

Start with the current question and refine it as the decision changes. Open an engram if its finding could affect the next step. Check whether its conditions match the current situation. Open its source when the next step depends on precise wording, an edition, or a material condition. Links to websites or files outside Memebase require your permission. A request that already includes reading the source provides that permission.

The **Related engrams** section explains when another record may help with the current question. The DEC procedure for the connected EWR S3S4 installation governs searches and writes. Its address is in `work_support.DEC.procedure` in `ARCHITECTURE.json`.

Among equally applicable engrams, prefer the most recently used, using the capture date for a new record. Break ties by higher use count and then by ID. Update the last-use date and count when you adopt the engram as a basis for work, following the DEC procedure.

## Importance

An engram can have an `## Importance` section with a rating and the reason it matters to you now.

- **Very important** — DEC may raise it when it applies.
- **Important** — recall it when a similar question comes up.
- **Neutral** — ordinary working experience with standard priority.
- **Not important** — low priority now, with possible value when reviewing history.

You set or confirm the rating. The agent may propose one based on what you say matters. Omit the section or leave it empty for an unrated engram. **Neutral** is an explicit rating. Add an assessment date and a condition for revisiting it when useful. Keep earlier grounds if they help explain a later decision. Check applicability first when recalling experience.

## DEC commands and proposal modes

Proposal mode controls when DEC looks for new experience to suggest saving in this chat. The connected memory and retrieval remain available according to the installation's DEC settings.

| Mode | When DEC proposes a capture |
| --- | --- |
| Neutral | The default in a new chat with DEC enabled. `Suggest saving to Memebase` |
| Active | DEC explicitly looks for useful experience while applying the same capture criteria. `Suggest saving to Memebase (active search)` |
| Passive | DEC processes explicit requests to consider or save material. |

| Action | Command |
| --- | --- |
| Select active proposal mode | `DEC: active` |
| Select neutral proposal mode | `DEC: neutral` |
| Select passive proposal mode | `DEC: passive` |
| Check connection and proposal mode | `DEC: status` |

The agent recognizes complete command phrases, case-insensitively, in your direct request. You can also describe what you want in your preferred language. Quoted commands and examples are instructional text. A mode change lasts for the current chat. The agent confirms the mode and connection separately. If DEC is disabled, it reports that state. You can request retrieval or approve a capture directly in any mode when DEC is connected.

## Capture decision

Each new engram records the project, the exact title and ID of the chat where you requested or confirmed the save, and a link to that chat when available. A deferred save points to the original decision. The source of the experience is recorded separately.

In Codex, the agent can use `list_threads` to find the chat and `read_thread` to verify the request or confirmation. If it can verify only part of the record, it preserves the confirmed details and identifies the missing ones.

## Engram types

| `kind` | Content | How to use it |
| --- | --- | --- |
| `note` | A note, observation, or working detail | Use it when the same situation comes up |
| `idea` | An idea, hypothesis, or open question | Continue the discussion or test it |
| `conclusion` | A finding from discussion, analysis, or verification | Check its grounds and conditions before relying on it |
| `decision` | An agreed decision | Follow it within its scope |
| `method` | A way of doing work | Reuse or adapt it to a new task |
| `summary` | An overview of a text, talk, or conversation | Orient yourself and locate the relevant source passage |
| `task` | An action to take | Find the task and its scheduled time |
| `event` | An occurrence or interval | Find when it is scheduled or when it occurred |

Ordinary capture preserves the engram and links to source material when needed. An explicit attachments request copies the selected files to `Attachments/YYYY-MM/<id>/` when attachments are supported. The link-access rules in this guide also apply to attached files.

The `status` field indicates currency. `active` means the record is available for work within its scope. `superseded` retains a replaced record for historical use. For a partial replacement, the relation identifies the affected scope. Read the engram for its grounds and level of support.
