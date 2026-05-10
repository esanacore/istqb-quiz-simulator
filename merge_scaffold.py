"""Reusable scaffold for merging normalized datasets.

Author: Eric Sanacore
Date: 2026-05-10
"""

from __future__ import annotations

import json
import argparse
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class MergeRecord:
    """Canonical record used during merge operations.

    Attributes:
        record_id: Stable canonical identifier.
        content: Primary normalized text or item content.
        source_name: Human-readable name of the source dataset.
        source_record_id: Original source-side identifier.
        authority: Relative trust classification for the source.
        payload: Full normalized record data.
        transformation_notes: Audit trail describing merge decisions.
    """

    record_id: str
    content: str
    source_name: str
    source_record_id: str
    authority: str
    payload: dict
    transformation_notes: list[str] = field(default_factory=list)


def load_json_records(path):
    """Load raw records from a JSON file.

    Args:
        path: Path to a JSON file containing a list of records.

    Returns:
        A list of raw dictionaries.
    """
    with Path(path).open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a JSON list.")

    return data


def normalize_record(raw_record, source_name, authority):
    """Normalize one source record into the canonical merge shape.

    Replace this implementation with project-specific field mapping.

    Args:
        raw_record: Raw source dictionary.
        source_name: Source dataset name.
        authority: Source trust classification.

    Returns:
        A MergeRecord instance.
    """
    record_id = str(raw_record.get("id", ""))
    content = str(raw_record.get("content", raw_record.get("q", ""))).strip()
    source_record_id = str(raw_record.get("source_record_id", record_id))

    payload = {
        "id": record_id,
        "content": content,
        "source": {
            "name": source_name,
            "record_id": source_record_id,
        },
        "quality": {
            "authority": authority,
            "review_status": "normalized",
        },
        "raw": raw_record,
    }

    return MergeRecord(
        record_id=record_id,
        content=content,
        source_name=source_name,
        source_record_id=source_record_id,
        authority=authority,
        payload=payload,
    )


def normalize_source(records, source_name, authority):
    """Normalize all records from a single source.

    Args:
        records: Raw source records.
        source_name: Source dataset name.
        authority: Source trust classification.

    Returns:
        A list of MergeRecord objects.
    """
    return [normalize_record(record, source_name, authority) for record in records]


def dedupe_key(record):
    """Generate a comparison key for duplicate detection.

    Args:
        record: A MergeRecord instance.

    Returns:
        A normalized string key.
    """
    return record.content.casefold().strip()


def choose_preferred_record(existing, candidate):
    """Choose which record to keep when duplicate keys collide.

    Args:
        existing: Existing merged record.
        candidate: New candidate record.

    Returns:
        A tuple of ``(chosen_record, rejected_record, merge_note)``.
    """
    rank = {
        "authoritative": 4,
        "supplementary": 3,
        "legacy": 2,
        "generated": 1,
    }

    existing_rank = rank.get(existing.authority, 0)
    candidate_rank = rank.get(candidate.authority, 0)

    if candidate_rank > existing_rank:
        note = f"Replaced {existing.source_name}:{existing.source_record_id} with higher-authority source."
        candidate.transformation_notes.append(note)
        return candidate, existing, note

    note = f"Kept existing {existing.source_name}:{existing.source_record_id} over {candidate.source_name}:{candidate.source_record_id}."
    existing.transformation_notes.append(note)
    return existing, candidate, note


def merge_records(records):
    """Merge normalized records into one deduplicated set.

    Args:
        records: Iterable of MergeRecord instances.

    Returns:
        A tuple of ``(merged_records, quarantined_records, audit_log)``.
    """
    merged = {}
    quarantined = []
    audit_log = []

    for record in records:
        key = dedupe_key(record)
        if not key:
            record.transformation_notes.append("Quarantined because dedupe key was empty.")
            quarantined.append(record)
            continue

        if key not in merged:
            merged[key] = record
            audit_log.append(f"Inserted {record.source_name}:{record.source_record_id}")
            continue

        chosen, rejected, note = choose_preferred_record(merged[key], record)
        merged[key] = chosen
        audit_log.append(note)
        if rejected is not chosen:
            rejected.transformation_notes.append("Rejected during duplicate resolution.")

    return list(merged.values()), quarantined, audit_log


def export_records(records, output_path):
    """Write merged records to JSON.

    Args:
        records: Iterable of MergeRecord instances.
        output_path: Destination file path.
    """
    payload = [record.payload | {"transformation_notes": record.transformation_notes} for record in records]
    with Path(output_path).open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2)


def load_merge_config(config_path):
    """Load merge configuration from JSON.

    Args:
        config_path: Path to a JSON configuration file.

    Returns:
        Parsed configuration dictionary.
    """
    with Path(config_path).open("r", encoding="utf-8") as handle:
        config = json.load(handle)

    if not isinstance(config, dict):
        raise ValueError("Merge config must be a JSON object.")

    sources = config.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("Merge config must define a non-empty 'sources' list.")

    return config


def run_merge(config):
    """Run a merge operation using a config dictionary.

    Args:
        config: Parsed merge configuration.

    Returns:
        A tuple of ``(merged_records, quarantined_records, audit_log)``.
    """
    normalized_records = []

    for source in config["sources"]:
        path = source["path"]
        source_name = source["name"]
        authority = source.get("authority", "supplementary")
        raw_records = load_json_records(path)
        normalized_records.extend(normalize_source(raw_records, source_name, authority))

    return merge_records(normalized_records)


def export_audit_log(audit_log, output_path):
    """Write an audit log to a text file.

    Args:
        audit_log: Sequence of human-readable audit entries.
        output_path: Destination path for the audit log.
    """
    with Path(output_path).open("w", encoding="utf-8") as handle:
        handle.write("\n".join(audit_log))


def main():
    """Run the generic merge scaffold from a config file."""
    parser = argparse.ArgumentParser(description="Run a generic dataset merge.")
    parser.add_argument("config", help="Path to dataset merge config JSON.")
    args = parser.parse_args()

    config = load_merge_config(args.config)
    merged_records, quarantined_records, audit_log = run_merge(config)

    output_dir = Path(config.get("output_dir", "merge_output"))
    output_dir.mkdir(parents=True, exist_ok=True)

    export_records(merged_records, output_dir / "merged_records.json")
    export_records(quarantined_records, output_dir / "quarantined_records.json")
    export_audit_log(audit_log, output_dir / "merge_audit.log")

    print(f"Merged records: {len(merged_records)}")
    print(f"Quarantined records: {len(quarantined_records)}")
    print(f"Audit log: {output_dir / 'merge_audit.log'}")


if __name__ == "__main__":
    main()
