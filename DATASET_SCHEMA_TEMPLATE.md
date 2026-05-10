# Dataset Schema Template

## Purpose

Use this template as a starting point when defining a canonical schema for a merged dataset.

## Core Fields

```json
{
  "id": "string",
  "title": "string",
  "content": "string",
  "options": ["string"],
  "answer": "string",
  "explanation": "string",
  "topic": "string",
  "learning_objective": "string",
  "tags": ["string"],
  "source": {
    "name": "string",
    "document": "string",
    "version": "string",
    "record_id": "string"
  },
  "quality": {
    "authority": "authoritative|supplementary|legacy|generated",
    "review_status": "raw|normalized|merged|quarantined|approved"
  },
  "transformation_notes": ["string"]
}
```

## Field Guidance

### Identity

- `id`
  Stable canonical identifier in the merged dataset.

### Primary Content

- `title`
  Short label or prompt title.
- `content`
  Main body text or item body.

### Structured Answer Content

- `options`
  Array of choices where applicable.
- `answer`
  Canonical correct answer or key value.
- `explanation`
  Supporting rationale.

### Classification

- `topic`
  Broad subject grouping.
- `learning_objective`
  Specific skill or concept tested.
- `tags`
  Flexible filtering metadata.

### Provenance

- `source.name`
  Source provider or origin.
- `source.document`
  File, document, or dataset name.
- `source.version`
  Version or release identifier.
- `source.record_id`
  Original record identifier if available.

### Quality / Workflow

- `quality.authority`
  Relative trust level of the source.
- `quality.review_status`
  Workflow state of the merged item.

### Auditability

- `transformation_notes`
  Freeform notes explaining edits, merges, or conflict decisions.

## Adaptation Notes

This template is intentionally broad. Remove fields that do not fit the project, but keep:

- canonical identity
- content fields
- provenance
- workflow state

Those are the minimum useful foundations for a trustworthy merged dataset.
