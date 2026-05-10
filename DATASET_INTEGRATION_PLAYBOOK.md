# Dataset Integration Playbook

## Purpose

This document explains how to combine multiple datasets or source sets into a more complete, trustworthy working dataset.

This is especially useful when:

- no single source is complete
- sources overlap
- sources use slightly different wording or schemas
- provenance matters

---

## 1. Define The Canonical Target Schema First

Before merging anything, define the shape of one final record.

Example fields:

- `id`
- `question`
- `options`
- `answer`
- `explanation`
- `source`
- `source_version`
- `topic`
- `learning_objective`
- `tags`

If you do not define the target schema first, integration becomes ad hoc.

---

## 2. Classify Source Types

Identify what each source contributes:

- authoritative source
- supplementary source
- legacy source
- inferred/generated source

Use that classification to guide conflict resolution.

Authoritative sources should outrank supplementary ones.

---

## 3. Normalize Before You Merge

Each source may need normalization:

- rename fields
- normalize data types
- trim whitespace
- standardize enums or labels
- convert wording into one consistent style
- split combined values into structured fields

Do not merge raw inconsistent records directly.

---

## 4. Preserve Provenance On Every Record

Every merged record should retain source information.

Useful provenance fields:

- source name
- source document or file
- version
- original question identifier
- transformation notes

Without provenance, the combined dataset becomes harder to trust or repair.

---

## 5. Detect Duplicates Intelligently

Duplicates are often not exact string matches.

Look for:

- same logical content with different wording
- same options reordered
- same question with slight punctuation changes
- same item from multiple editions or versions

Good duplicate signals:

- normalized text comparison
- source ids
- option set similarity
- answer consistency

---

## 6. Define Merge Rules Explicitly

Examples:

- if two records are equivalent, keep the higher-authority source
- if one source has better explanation metadata, merge that field in
- if answers conflict, quarantine the record for review
- if one source is older, prefer the newer authoritative version

Do not resolve conflicts implicitly.

---

## 7. Quarantine Ambiguous Records

Some records should not merge automatically.

Examples:

- conflicting correct answers
- mismatched option counts
- missing required fields
- materially different wording that may indicate different questions

Create a review bucket instead of forcing a bad merge.

---

## 8. Validate The Combined Dataset

After merging:

- validate required fields
- validate type consistency
- validate answer exists in options
- validate option count if fixed
- validate source metadata presence
- validate record uniqueness where possible

The merged dataset should go through stronger validation than any single raw source.

---

## 9. Track Transformations

A useful integration process records:

- what source files were used
- what normalization rules were applied
- what duplicates were merged
- what records were dropped
- what records need manual review

This can be:

- a log file
- a markdown summary
- a JSON audit report

---

## 10. Suggested Merge Workflow

1. define canonical schema
2. ingest source A
3. normalize source A
4. ingest source B
5. normalize source B
6. compare for duplicates
7. apply merge rules
8. quarantine conflicts
9. validate merged output
10. write final dataset plus audit metadata

---

## 11. Practical Rules For Trustworthy Combined Sets

- prefer authoritative over convenient
- preserve provenance even after transformation
- never silently overwrite conflicts
- validate after every merge stage
- keep the original raw sources
- keep the merged output reproducible

---

## 12. How This Applies To Future Projects

This approach is useful for:

- exam question banks
- knowledge bases
- inventory catalogs
- content libraries
- product datasets
- requirement repositories
- training corpora

The core problem is the same:

how to turn multiple partial sources into one reliable dataset without losing traceability.
