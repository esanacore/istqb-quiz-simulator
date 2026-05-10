# Merge CLI Guide

## Purpose

This guide explains how to use the generic merge scaffold with a JSON config file so you can combine multiple datasets without rewriting orchestration code each time.

## Files

- [merge_scaffold.py](C:/Projects/practiceISTQB/merge_scaffold.py:1)
- [dataset_merge_config.template.json](C:/Projects/practiceISTQB/dataset_merge_config.template.json:1)

## Basic Flow

1. Copy the template config.
2. Point each source entry at a source JSON file.
3. Assign an authority level to each source.
4. Run the merge CLI.
5. Inspect merged output, quarantined output, and audit log.

## Config Shape

```json
{
  "output_dir": "merge_output",
  "sources": [
    {
      "name": "authoritative_source",
      "path": "data/source_a.json",
      "authority": "authoritative"
    },
    {
      "name": "supplementary_source",
      "path": "data/source_b.json",
      "authority": "supplementary"
    }
  ]
}
```

## Run Command

```powershell
python merge_scaffold.py dataset_merge_config.template.json
```

## Output

The CLI writes:

- `merged_records.json`
- `quarantined_records.json`
- `merge_audit.log`

into the configured output directory.

## What You Still Customize

The CLI handles orchestration, but you still adapt the project-specific logic in:

- `normalize_record(...)`
- `dedupe_key(...)`
- `choose_preferred_record(...)`

Those functions define how records are interpreted and how conflicts are resolved.

## Recommended Usage Pattern

- start with a small sample of source data
- verify normalization output first
- verify dedupe behavior second
- run a full merge only after conflict rules make sense
- review quarantined records manually
