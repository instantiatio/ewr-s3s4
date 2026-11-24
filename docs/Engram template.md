---
# Index.yaml copies all YAML values, including nested values.
# The index builder adds path from this file's location.
id: "<stable engram ID>"
title: "<engram title>" # When omitted, use the file name.
date: "<YYYY-MM-DD>" # Capture date.
kind: note # note | idea | conclusion | decision | method | summary | task | event
status: active # active | superseded

# Add a list item for each recall situation. result and label are optional.
navigation: [{"cue":"<when to recall the engram>","result":"<what the engram offers in that situation>"}]
applies_when: null # Conditions for using the engram.
basis: null # Grounds, level of support, and limits of the claim.

last_used: null
use_count: 0
use_events: []

# null means unrated. neutral is an explicit personal rating.
importance: null # very-important | important | neutral | not-important
importance_assessed_on: null # Assessment date in YYYY-MM-DD.

# Details of the capture decision. Record known values.
capture:
  project: "<project in which the capture was approved>"
  chat_title: "<exact chat title>"
  chat_id: "<chat ID>"
  message_id: null # ID of the message that requested or confirmed the capture.
  host: null # Chat host, when known and useful.

# For tasks and events, use a date or a timestamp with offset.
starts_at: null
ends_at: null

# One item per claim. Set review_after and/or valid_until when known.
time_sensitive: []
# Example item: {"claim":"<claim>","checked_on":null,"review_after":"2026-12-24","valid_until":"2027-01-24"}

save_fingerprint: null # Preserve the original value when migrating an older engram.
---

<Engram body. State the finding, idea, decision, or method. Include explanations, examples, and the reason for the personal rating when useful.>

## Links

### Sources

- [Source title](<source URL or path>) — what it supports or provides.

### Attachments

- [File name](<relative path to the copy under Attachments>) — when to open it.

### Related engrams

- [Engram title](<relative path to the engram>) — what it adds, clarifies, or replaces.

### Capture chat

- [Chat where the capture was approved](<chat or message URL>).
