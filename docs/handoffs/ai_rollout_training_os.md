# AI Rollout Training OS Handoff

Status: draft input format for future training scenarios.

Workflow-to-Agent Studio design candidates now expose a permission/runtime
boundary block that can feed rollout exercises without granting runtime
authority.

Scenario fields:

- candidate variant
- runtime tier
- runtime justification: mutability, privilege level, blast radius, rationale
- tool surfaces: read surfaces, write surfaces, destructive surfaces
- risky-action controls: confirmation required or sandbox recommended
- human approval points
- evidence Context-Refs

Training use:

- ask operators to identify whether a proposed tool surface is read, write, or
  destructive
- require confirmation or sandbox recommendations for write/destructive actions
- compare runtime tier justification against mutability, privilege, and blast
  radius
- keep all generated scenarios as convenience training material, not approval
  authority

