# Spec (per PR)

**Spec ID**: 20251031  
**Created**: 2025-10-31  

**Feature name**: Spec Ordering System  
**One-line summary**: Enable agents and developers to view specs in chronological order through date-prefixed directories and metadata.  

---

## Problem
Currently, spec directories are unordered and sorted alphabetically by name. There's no way for the agent or developers to understand which specs came first, which are newest, or see the evolution of the project over time. This makes it difficult to:
- Understand project history
- Reference specs in chronological order
- Navigate the specs directory logically

## Goal
Implement a consistent date-based naming system for specs that provides clear chronological ordering both in the filesystem and through metadata.

## Success Criteria
- [ ] All new specs use YYYYMMDD date-prefixed directories (e.g., `20251031-feature-name/`)
- [ ] Spec template includes metadata fields (Spec ID, Created date)
- [ ] Agent automatically uses current date for new spec directories
- [ ] Agent documentation clearly explains the YYYYMMDD naming convention

## User Story
As a developer or AI agent, I want specs to be numbered and ordered chronologically, so that I can easily navigate the project's evolution and reference specs in a logical sequence.

## Flow / States
**Happy Path:**
1. Agent/developer needs to create a new spec
2. Agent uses current date to create directory with YYYYMMDD prefix (e.g., `20251031-new-feature/`)
3. Spec includes metadata in header with matching Spec ID
4. Directory and files created from templates

**Edge Case:**
1. Multiple specs created on same date - append suffix if needed (e.g., `20251031-feature-name`, `20251031-another-feature`)
2. Manual spec creation - developer must use correct YYYYMMDD format

## UX Links
- Designs: N/A (filesystem and template changes)
- Prototype: N/A
- Copy/Content: Template updates below

## Requirements
- Must use YYYYMMDD date format for directory prefixes (e.g., `20251031-feature-name/`)
- Must include metadata in spec header: Spec ID (matching date), Created date
- Must update all templates (spec, impact, TDR) to include new metadata fields
- Must update agent_operating_procedure.md with the date-based naming convention
- Agent must have access to current date to create properly formatted directories
- Must not touch existing unprefixed specs

## Acceptance Criteria
- Given a new spec needs to be created, when the agent uses the current date, then it creates a directory with YYYYMMDD prefix format
- Given the spec template is used, when a new spec is created, then it includes all metadata fields (Spec ID matching the date, Created date)
- Given multiple specs exist, when viewing the specs directory, then they sort chronologically by date prefix
- Given an existing unprefixed spec exists, when referenced, then it continues to work without requiring immediate migration
- Given two specs are created on the same date, when viewing the directory, then both are clearly distinguishable by their feature names

## Non-Goals
- Migration or renaming of existing unprefixed specs
- Enforcement of naming convention through CI/CD (future enhancement)
- Complex dependency tracking between specs
- Integration with external project management tools
- Status tracking within spec metadata

