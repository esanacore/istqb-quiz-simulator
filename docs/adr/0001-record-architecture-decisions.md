# ADR: Record Architecture Decisions

Status: Accepted

Date: 2026-06-08

## Context

The project now follows the shared Engineering Constitution. The constitution requires major architecture, data, infrastructure, framework, and security decisions to be documented as Architecture Decision Records.

This repository already has strong architecture and SQA documentation, but it did not have a dedicated ADR location for decision history.

## Decision

Use Markdown ADRs in `docs/adr/` for major technical decisions.

Keep ADRs focused on decisions and link to detailed design or SQA documents when more context is needed.

## Consequences

Future agents and maintainers have a stable place to find why major decisions were made.

This adds a small documentation maintenance cost, but reduces the risk of losing architectural reasoning in chat history, commit messages, or issue comments.

## Alternatives Considered

- Keep decision history only in `ARCHITECTURE.md`. This was rejected because architecture docs describe current structure better than decision history.
- Keep decision history only in pull requests or commits. This was rejected because those records are harder for future agents to discover quickly.
