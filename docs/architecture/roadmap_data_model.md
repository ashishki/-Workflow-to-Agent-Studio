# Roadmap Data Model

Purpose: define the main structured entities for `RoadmapReport v1`.

## Entities

### CompanyProject

- project_id;
- company_name or alias;
- industry/domain;
- size band;
- region;
- selected privacy mode;
- goals;
- created_at.

### BusinessContext

- company type;
- channels;
- systems;
- current pains;
- workflow list;
- constraints;
- evidence refs.

### WorkflowMap

- workflow_id;
- name;
- trigger;
- actors;
- systems;
- steps;
- decisions;
- exceptions;
- inputs;
- outputs;
- volume/frequency;
- evidence refs.

### WorkflowStep

- step_id;
- description;
- actor;
- system;
- input fields;
- output fields;
- decision/approval flag;
- evidence refs;
- assumptions.

### DataFieldInventory

- field_id;
- field_name;
- description;
- source workflow step;
- privacy class;
- detected flags;
- required for recommendation IDs;
- redaction status.

### AutomationOpportunity

- opportunity_id;
- workflow step;
- pain point;
- candidate solution type;
- pattern matches;
- expected value;
- required data;
- risks;
- confidence.

### Recommendation

- recommendation_id;
- target workflow step;
- solution type;
- architecture;
- required data;
- privacy class;
- cost estimate;
- time estimate;
- required people;
- dependencies;
- risks;
- validation plan;
- success metrics;
- evidence refs;
- assumptions;
- fallback.

### CostEstimate

- one-time low/medium/high;
- monthly low/medium/high;
- currency;
- assumptions;
- confidence;
- price card versions;
- maintenance cost;
- human review cost.

### PriorityScore

- business value band;
- delivery readiness band;
- risk penalty band;
- final priority band;
- confidence;
- rationale;
- uncertainty notes.

### VerificationReceipt

- report_id;
- schema version;
- source hashes;
- prompt versions;
- model/provider metadata;
- pattern library version;
- cost model version;
- scoring model version;
- privacy model version;
- claim count;
- assumption count;
- blocking finding count;
- reviewer status.

## Storage Direction

MVP can store roadmap artifacts as JSON blobs plus append-only audit events.
Normalized tables become useful when review workflows, search, and comparison are
needed.

Candidate SQLite tables:

- claims;
- assumptions;
- evidence_items;
- recommendation_traces;
- decision_logs;
- verification_receipts;
- reviewer_notes.
