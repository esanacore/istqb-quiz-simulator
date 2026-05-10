# Merge Checklist

## Before You Merge

- identify all source files
- classify each source as authoritative, supplementary, legacy, or generated
- define the canonical target schema
- define required fields
- define conflict rules
- define duplicate-detection rules

## Normalize Each Source

- rename fields into canonical names
- normalize text formatting
- normalize numeric and boolean types
- standardize enum values
- split compound fields if needed
- attach provenance fields

## Validate Source Records

- ensure each record is an object
- ensure required fields are present
- ensure field types are correct
- ensure answer or key references are valid
- quarantine malformed records

## Merge

- compare normalized records for duplicates
- prefer authoritative records when conflicts exist
- merge supplemental fields where safe
- quarantine ambiguous conflicts
- avoid silent overwrites

## Validate Final Dataset

- run full schema validation
- verify uniqueness constraints
- verify provenance is still present
- verify required relationships still hold
- produce an audit summary

## Output

- save the merged dataset
- save conflict or quarantine output
- save a merge summary or log
- keep raw sources unchanged
