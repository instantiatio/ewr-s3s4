# Checking and maintaining MethodPack

<a id="current-pair-profile"></a>
## Current-pair profile

Human selected the baseline MP from `iEWR-7.0.9-Eternal-Alpha.zip` and requested removal of `methods/snapshots`. This installation therefore keeps exactly one active pair: `methods/METHOD_PACK.md` and `methods/index.yaml`. The book is byte-for-byte the selected **base-v3.17** original, including its historical iEWR title; all 37 method bodies and individual editions are unchanged. The index identifies this installation adapter as `pack.storage_profile: current-pair`.

The baseline IE-M003/IE-M004 descriptions retain their original snapshot-folder recipe. **For this installation, the current-pair procedure below replaces that recipe's storage paths and publication means.** It preserves the required properties: exact edition identity, coherent book/index, a single writer, checked transition, recoverable before state, pending reconciliation and honest checking scope. Do not recreate snapshot folders to satisfy a check for this profile. The author descriptions remain unchanged as Human requested.

The index binds the current book with `pack.book_sha256`. Each method has `body_sha256` over the UTF-8 heading-through-end body joined with LF, without a final LF. The checker also verifies actual IDs, editions, anchors, full method ranges, relations and declared live file grounds. Current FPF candidate routes require exact source digest, provenance edition, unique pattern ID and full structural range; the checker reuses the supplied structural reader. Hashes establish consistency of the given inputs, not authority or method quality.

Historical FPF grounds are recorded under `historical_FPF_basis`, retaining their original editions, claims and source citations. They are provenance, not required current local files. `locates_current_FPF_candidate` relations locate the corresponding pattern in the single installed current FPF; read its conditions before adoption. A route is not a claim that the unchanged baseline method has been rederived or qualified under the newer source.

## Read-only check

```sh
python3 -B tools/methodpack.py check --json
```

Use `--root /absolute/candidate-root` to check a separate complete candidate with its required local dependencies. The checker writes nothing. It checks safe parsing, unique IDs, the book/body digests, actual headings and full ranges, active relations, live source digests/anchors and changed checked inputs. In the current-pair profile it also matches indexed names against the method headings and requires `pack.installation_adapter` to identify [the installed current-pair procedure](#current-pair-profile) at `docs/METHODPACK_CHECK.md#current-pair-profile`. It checks that this file has exactly one explicit `current-pair-profile` anchor. It holds when either legacy pending or `project/artifacts/methodpack-maintenance/pending.json` exists. It returns the actual current token even on a failed check where the pair is readable.

Source citations in historical metadata are not fetched or represented as locally checked originals. A source needed by a later material decision must be obtained under the ordinary source policy. Missing historical evidence limits that historical claim; it does not justify a new source claim.

## Guarded update with ADE file operations

Use IE-M003's required properties through this approved local adapter. Python is optional for ordinary work; the supplied checker can be reused when available. Work needs one agreed writer and paused dependent readers, exact complete byte operations, SHA-256, safe parsing, sufficient candidate/history checks and a recoverable before state. If these conditions are unavailable, retain the candidate separately and hold activation.

1. Recover the assigned change, actual current pair, required live dependencies and pending state. Capture the exact current token and hashes of changed dependencies. A pending attempt must be reconciled before another update.
2. Prepare the new book/index pair in a task directory outside `methods/`. Preserve the exact old pair and necessary old dependencies in a verified development archive or a recoverable immutable repository edition. Keep this history outside the clean installation. Verify the archive members and hashes before relying on it.
3. Check the candidate through its own root. Compare every reused ID/edition with the actual current and available preserved history: the same ID/edition must retain its full body. A changed body needs its own description edition. This initial current-pair adapter has no qualified archive-backed retirement return: a nonempty retired_methods is held, and removing an active ID without its required retirement return fails transition checking. Hold such a change until that adapter is qualified; do not omit the return to make a candidate pass. State any unavailable older history; a current digest alone does not prove all-time version uniqueness.
4. Record the attempt in its task directory: exact before/after paths and hashes, archive identity, writer/read boundary, candidate check and ordered writes. Before the first current replacement, create `project/artifacts/methodpack-maintenance/pending.json` pointing to that record. This is a recovery marker, not a lock or a transaction.
5. Recheck the actual before token and dependencies. Replace the two current files using available exact file operations; sequential replacement is not atomic as a pair. Do not let another reader use the mixed state. Stop on an unknown write outcome and inspect the same attempt before retrying.
6. Reopen the current bytes, compare them with the recorded after, and perform the same consistency/dependency checks while the read pause remains in force. The checker API's `ignore_pending=True` is for this controlled reconciliation; it is not an ordinary bypass. Clear only the matching pending marker after the checked complete state is established, then run the normal read-only check and update the continuation record.

For an interrupted attempt, compare both actual files with the recorded before and after and the preserved archive. Complete the assigned attempt or restore exact before only where the actual bytes are known members of that attempt. A third-party or otherwise unknown edit holds automatic replacement. Restoring old bytes does not make obsolete advice current or undo external effects. The record identifies what was restored, checked and left open.

## Legacy helper boundary

The helper retains legacy snapshot checking for older environments and their fixed source editions. Its `activate --snapshot` and `recover` writers are unavailable when the current index selects `current-pair`; they return a structured refusal before creating locks or history. Use the ADE/archive procedure above for this installation. This is an explicit profile boundary, not a bypass of a failed material check. Checks reject an unsupported profile.

The clean release includes neither snapshots nor activation history. Development archives and previous Git editions preserve prior sources outside the runtime package. File checks do not establish methodological truth, permission, general effectiveness or production readiness.
