"""Stable Markdown rendering for roadmap reports."""

from __future__ import annotations

from collections.abc import Iterable

from workflow_agent_studio.domain.recommendation import RecommendationCard
from workflow_agent_studio.domain.roadmap import (
    ProcessInventoryItem,
    RoadmapReport,
    RoadmapWorkflowMap,
)


def render_roadmap_markdown(report: RoadmapReport, *, status: str = "Draft") -> str:
    """Render a RoadmapReport in the contract section order."""
    lines = [
        "# SMB AI Roadmap Report",
        "",
        f"Status: {status}",
        f"Report ID: {report.report_id}",
        f"Schema Version: {report.schema_version}",
        "",
        "## Executive Summary",
        f"Company Context: {report.executive_summary.company_context}",
        "",
        "Top Recommended Initiatives:",
        *_bullet(report.executive_summary.top_recommended_initiatives),
        "",
        "Top Do-Not-Automate-Yet Items:",
        *_bullet(report.executive_summary.top_do_not_automate_yet_items),
        "",
        "30/60/90 Day Roadmap:",
        *_bullet(report.executive_summary.roadmap_30_60_90),
        "",
        "Overall Privacy Mode Recommendation: "
        f"{report.executive_summary.overall_privacy_mode_recommendation}",
        f"Overall Confidence Level: {report.executive_summary.overall_confidence_level}",
        "",
        "Critical Assumptions:",
        *_bullet(report.executive_summary.critical_assumptions),
        "",
        "## What The Agent Will Not Replace",
        *_agent_expectation_check(report),
        "",
        "## Evidence Packet",
        *_evidence_packet(report),
        "",
        "## Workflow Map",
        *_workflow_map(report.workflow_map),
        "",
        "## Process Inventory",
        *_process_inventory(report.process_inventory),
        "",
        "## Readiness And Deployment Fit",
        *_readiness_and_deployment_fit(report),
        "",
        "## AI Opportunity Map",
        *_ai_opportunity_map(report),
        "",
        "## Recommendation Cards",
        *_recommendation_cards(report.recommendations),
        "",
        "## Harness Candidate Cards",
        *_harness_candidate_cards(report),
        "",
        "## Use Case Card Exports",
        *_use_case_card_exports(report),
        "",
        "## Cloud Vs Local/Private Recommendation",
        *_cloud_private_recommendations(report),
        "",
        "## Build Vs Buy",
        *_build_vs_buy(report.recommendations),
        "",
        "## Cost, Time, And Team Plan",
        *_cost_time_team(report.recommendations),
        "",
        "## Rollout Plan",
        *_bullet(report.rollout_plan.stages),
        "",
        "## Evaluation Plan",
        *_evaluation_plan(report),
        "",
        "## Governance And Maintenance",
        f"Owner: {report.governance_plan.owner}",
        f"Review Cadence: {report.governance_plan.review_cadence}",
        "",
        "Approval Rules:",
        *_bullet(report.governance_plan.approval_rules),
        "",
        f"Incident Handling: {report.governance_plan.incident_handling}",
        f"Change Policy: {report.governance_plan.change_policy}",
        f"Data Retention: {report.governance_plan.data_retention}",
        f"Audit Logs: {report.governance_plan.audit_logs}",
        "",
        "## Verification Appendix",
        *_verification_appendix(report),
        "",
    ]
    return "\n".join(lines)


def _agent_expectation_check(report: RoadmapReport) -> list[str]:
    check = report.agent_expectation_check
    return [
        f"Realistic Autonomy Level: {check.realistic_autonomy_level}",
        f"Autonomy Rationale: {check.autonomy_rationale}",
        "",
        "Human-Owned Responsibilities:",
        *_bullet(check.what_agent_will_not_replace),
        "",
        "Workflow-Specific Agent Myths:",
        *_bullet(check.workflow_specific_myths),
        "",
        "Required Human Capabilities:",
        *_bullet(check.required_human_capabilities),
        "",
        "Proof Gates Before Rollout:",
        *_bullet(check.proof_gates_before_rollout),
    ]


def _evidence_packet(report: RoadmapReport) -> list[str]:
    lines: list[str] = []
    for source in report.evidence_packet.source_documents:
        lines.extend(
            [
                f"### Source {source.source_id}",
                f"- Type: {source.source_type}",
                f"- Hash: {source.source_hash}",
                f"- Redaction Status: {source.redaction_status}",
                f"- Source Privacy Class: {source.source_privacy_class}",
                "- Extracted Evidence Snippets:",
                *_bullet(source.extracted_evidence_snippets),
                "- Missing Evidence:",
                *_bullet(source.missing_evidence),
                "",
            ]
        )
    return lines


def _workflow_map(workflows: list[RoadmapWorkflowMap]) -> list[str]:
    lines: list[str] = []
    for workflow in workflows:
        lines.extend(
            [
                f"### {workflow.workflow_id}: {workflow.workflow_name}",
                f"- Business Owner: {workflow.business_owner}",
                f"- Trigger: {workflow.trigger}",
                f"- Frequency/Volume: {workflow.frequency_or_volume}",
                f"- Current Manual Effort: {workflow.current_manual_effort}",
                "- Actors:",
                *_bullet(workflow.actors),
                "- Systems:",
                *_bullet(workflow.systems),
                "- Steps:",
                *_bullet(workflow.steps),
                "- Decisions:",
                *_bullet(workflow.decisions),
                "- Exceptions:",
                *_bullet(workflow.exceptions),
                "- Inputs:",
                *_bullet(workflow.inputs),
                "- Outputs:",
                *_bullet(workflow.outputs),
                "- Pain Points:",
                *_bullet(workflow.pain_points),
                "- Current Tools:",
                *_bullet(workflow.current_tools),
                "- Evidence References:",
                *_bullet(_format_evidence_ref(ref) for ref in workflow.evidence_references),
                "",
            ]
        )
    return lines


def _process_inventory(items: list[ProcessInventoryItem]) -> list[str]:
    lines: list[str] = []
    for item in items:
        lines.extend(
            [
                f"### {item.process_id}: {item.process_name}",
                f"- Automation Feasibility Score: {item.automation_feasibility_score}",
                f"- Business Impact Score: {item.business_impact_score}",
                f"- Privacy Sensitivity Score: {item.privacy_sensitivity_score}",
                f"- Security Risk Score: {item.security_risk_score}",
                f"- Data Readiness Score: {item.data_readiness_score}",
                f"- Implementation Complexity Score: {item.implementation_complexity_score}",
                f"- Evaluation Clarity Score: {item.evaluation_clarity_score}",
                f"- Recommended Solution Type: {item.recommended_solution_type}",
                "",
            ]
        )
    return lines


def _readiness_and_deployment_fit(report: RoadmapReport) -> list[str]:
    lines: list[str] = []
    if report.data_readiness_report is not None:
        data = report.data_readiness_report
        lines.extend(
            [
                "### Data Readiness",
                f"- Status: {data.status}",
                f"- Score: {data.score}",
                "- Ready Sources:",
                *_bullet(data.ready_sources),
                "- Blockers:",
                *_bullet(data.blockers),
                "- Required Next Questions:",
                *_bullet(data.required_next_questions),
                "",
            ]
        )
    if report.eval_readiness_report is not None:
        eval_report = report.eval_readiness_report
        lines.extend(
            [
                "### Eval Readiness",
                f"- Status: {eval_report.status}",
                f"- Score: {eval_report.score}",
                "- Golden Cases:",
                *_bullet(eval_report.golden_cases),
                "- Acceptance Criteria:",
                *_bullet(eval_report.acceptance_criteria),
                "- Blockers:",
                *_bullet(eval_report.blockers),
                "- Required Next Questions:",
                *_bullet(eval_report.required_next_questions),
                "",
            ]
        )
    for score in report.workflow_candidate_scores:
        lines.extend(
            [
                f"### Candidate Score {score.recommendation_id}",
                f"- Feasibility: {score.feasibility}/5",
                f"- Data Readiness: {score.data_readiness}/5",
                f"- Eval Readiness: {score.eval_readiness}/5",
                f"- Risk Level: {score.risk_level}",
                f"- TCO Complexity: {score.tco_complexity}",
                f"- Deployment Fit: {score.deployment_fit}",
                f"- Recommended Autonomy Mode: {score.autonomy_fit.recommended_mode}",
                "- ROI Proxy:",
                f"  - FTE Minutes Saved: {score.roi_proxy.fte_minutes_saved}",
                f"  - Cycle Time Delta: {score.roi_proxy.cycle_time_delta}",
                f"  - Error Rate Delta: {score.roi_proxy.error_rate_delta}",
                f"  - Throughput Delta: {score.roi_proxy.throughput_delta}",
                f"  - Service Delta: {score.roi_proxy.service_delta}",
                "  - Evidence Basis:",
                *_indented_bullet(score.roi_proxy.evidence_basis),
                "- Caveats:",
                *_bullet(score.caveats),
                "",
            ]
        )
    for deployment in report.autonomous_deployment_recommendations:
        lines.extend(
            [
                f"### Deployment Recommendation {deployment.recommendation_id}",
                f"- Fit: {deployment.fit}",
                f"- Runtime Target: {deployment.runtime_target}",
                f"- Trigger Contract: {deployment.trigger_contract}",
                f"- Idempotency Key: {deployment.idempotency_key}",
                f"- Secrets Boundary: {deployment.secrets_boundary}",
                f"- Fallback Policy: {deployment.fallback_policy}",
                f"- Rationale: {deployment.rationale}",
                "- Blockers:",
                *_bullet(deployment.blockers),
                "",
            ]
        )
    return lines or ["- none"]


def _ai_opportunity_map(report: RoadmapReport) -> list[str]:
    pain_points = _flatten(workflow.pain_points for workflow in report.workflow_map)
    lines: list[str] = []
    for card in report.recommendations:
        lines.extend(
            [
                f"### {card.recommendation_id}: {card.recommendation}",
                f"- Workflow Step: {card.target_workflow_step}",
                f"- Pain Point: {', '.join(pain_points) if pain_points else 'not specified'}",
                f"- Automation Pattern: {card.implementation_option}",
                f"- AI Fit: {_ai_fit(card)}",
                f"- Expected Value: {card.expected_value.qualitative}",
                f"- Required Data: {', '.join(card.required_data)}",
                f"- Privacy Class: {card.privacy_class}",
                f"- Confidence: {card.confidence_level}",
                f"- Fallback Option: {card.fallback_option}",
                "",
            ]
        )
    return lines or ["- none"]


def _recommendation_cards(cards: list[RecommendationCard]) -> list[str]:
    lines: list[str] = []
    for card in cards:
        lines.extend(
            [
                f"### {card.recommendation_id}: {card.recommendation}",
                f"- Target Workflow Step: {card.target_workflow_step}",
                f"- Expected Value: {card.expected_value.qualitative}",
                f"- Quantitative Assumption: {card.expected_value.quantitative_assumption}",
                f"- Required Data: {', '.join(card.required_data)}",
                f"- Privacy Class: {card.privacy_class}",
                f"- Implementation Option: {card.implementation_option}",
                f"- Architecture Model: {card.architecture.model}",
                "- Deterministic Components:",
                *_bullet(card.architecture.deterministic_components),
                "- LLM Components:",
                *_bullet(card.architecture.llm_components),
                "- Risks:",
                *_bullet(card.risks),
                "- Validation Method:",
                *_bullet(card.validation_method),
                "- Success Metrics:",
                *_bullet(card.success_metrics),
                f"- Confidence Level: {card.confidence_level}",
                "- Assumptions:",
                *_bullet(card.assumptions),
                "- Evidence:",
                *_bullet(_format_evidence_ref(ref) for ref in card.evidence),
                f"- Fallback Option: {card.fallback_option}",
                "- Human Gate:",
                f"  - Required: {card.human_gate.required}",
                f"  - Reviewer: {card.human_gate.reviewer}",
                f"  - Approval Event: {card.human_gate.approval_event}",
                f"  - Rationale: {card.human_gate.rationale}",
                "",
            ]
        )
    return lines or ["- none"]


def _harness_candidate_cards(report: RoadmapReport) -> list[str]:
    lines: list[str] = []
    for card in report.harness_candidate_cards:
        lines.extend(
            [
                f"### {card.recommendation_id}",
                f"- Harness Boundary: {card.harness_boundary}",
                f"- Memory Policy: {card.memory_policy}",
                f"- Retry/Recovery Policy: {card.retry_recovery_policy}",
                f"- Permission Policy: {card.permission_policy}",
                f"- Human Handoff: {card.human_handoff}",
                "- Tools:",
                *_bullet(card.tools),
                "- Trace Requirements:",
                *_bullet(card.trace_requirements),
                "- Eval Required:",
                *_bullet(card.eval_required),
                "",
            ]
        )
    return lines or ["- none"]


def _use_case_card_exports(report: RoadmapReport) -> list[str]:
    lines: list[str] = []
    for card in report.use_case_card_exports:
        lines.extend(
            [
                f"### {card.use_case_id}: {card.title}",
                f"- Problem: {card.problem}",
                f"- Current Workflow: {card.current_workflow}",
                f"- AI Opportunity: {card.ai_opportunity}",
                f"- Human In Loop: {card.human_in_loop}",
                f"- TCO Complexity: {card.tco_complexity}",
                f"- MVP Scope: {card.mvp_scope}",
                "- Data Required:",
                *_bullet(card.data_required),
                "- Risk/Privacy:",
                *_bullet(card.risk_privacy),
                "- Eval Plan:",
                *_bullet(card.eval_plan),
                "- Production Hardening:",
                *_bullet(card.production_hardening),
                "",
            ]
        )
    return lines or ["- none"]


def _cloud_private_recommendations(report: RoadmapReport) -> list[str]:
    lines = [
        f"- Overall Recommendation: {report.executive_summary.overall_privacy_mode_recommendation}"
    ]
    for card in report.recommendations:
        lines.extend(
            [
                f"- {card.recommendation_id}: {_privacy_mode_label(card.privacy_class)}",
                f"  - Rationale: data class `{card.privacy_class}` with risks "
                f"{', '.join(card.risks)}.",
                f"  - Data Classes Involved: {card.privacy_class}",
                "  - Quality/Cost Tradeoff: stricter privacy modes may increase setup time "
                "and reduce model convenience.",
            ]
        )
    return lines


def _build_vs_buy(cards: list[RecommendationCard]) -> list[str]:
    return [
        f"- {card.recommendation_id}: {_build_buy_label(card.implementation_option)}"
        for card in cards
    ] or ["- none"]


def _cost_time_team(cards: list[RecommendationCard]) -> list[str]:
    lines: list[str] = []
    for card in cards:
        lines.extend(
            [
                f"### {card.recommendation_id}: {card.recommendation}",
                "- One-Time Implementation Cost Range: "
                f"{card.estimated_cost.currency} {card.estimated_cost.one_time_low}-"
                f"{card.estimated_cost.one_time_high}",
                "- Monthly Run Cost Range: not captured in RecommendationCard v1.",
                "- Human Review Cost: depends on reviewer sample size.",
                "- Integration/Subscription Cost: depends on selected tools.",
                "- Maintenance Cost: depends on review cadence and workflow drift.",
                "- Estimated Time: "
                f"{card.estimated_time.low} / {card.estimated_time.medium} / "
                f"{card.estimated_time.high}",
                "- Required People:",
                *_bullet(card.required_people),
                "- Dependencies:",
                *_bullet(card.dependencies),
                "- Assumptions:",
                *_bullet(card.assumptions),
                f"- Confidence: {card.confidence_level}",
                "",
            ]
        )
    return lines or ["- none"]


def _evaluation_plan(report: RoadmapReport) -> list[str]:
    plan = report.evaluation_plan
    return [
        "Golden Test Cases:",
        *_bullet(plan.golden_test_cases),
        "",
        f"Shadow Mode: {plan.shadow_mode}",
        f"Human Review Sample: {plan.human_review_sample}",
        "",
        "Acceptance Criteria:",
        *_bullet(plan.acceptance_criteria),
        "",
        "Regression Tests:",
        *_bullet(plan.regression_tests),
        "",
        "Stop Conditions:",
        *_bullet(plan.stop_conditions),
    ]


def _verification_appendix(report: RoadmapReport) -> list[str]:
    appendix = report.verification_appendix
    receipt = appendix.receipt
    lines = [
        "### Claims Registry",
    ]
    for claim in appendix.claims_registry:
        lines.extend(
            [
                f"- {claim.claim_id}: {claim.claim_text}",
                f"  - Type: {claim.claim_type}",
                f"  - Evidence Level: {claim.evidence_level}",
                f"  - Confidence: {claim.confidence}",
                f"  - Status: {claim.status}",
                f"  - Source Refs: {_format_mapping_refs(claim.source_refs)}",
            ]
        )
    lines.extend(["", "### Assumptions Registry"])
    for assumption in appendix.assumptions_registry:
        lines.extend(
            [
                f"- {assumption.assumption_id}: {assumption.text}",
                f"  - Impact If Wrong: {assumption.impact_if_wrong}",
                f"  - Verification Method: {assumption.verification_method}",
                f"  - Owner: {assumption.owner}",
                f"  - Expires At Stage: {assumption.expires_at_stage}",
                f"  - Status: {assumption.status}",
            ]
        )
    lines.extend(["", "### Evidence Table"])
    for evidence in appendix.evidence_table:
        lines.extend(
            [
                f"- {evidence.evidence_id}: {evidence.evidence_summary}",
                f"  - Source: {evidence.source_id} / {evidence.chunk_id}",
                f"  - Hash: {evidence.source_hash}",
                f"  - Redacted: {evidence.redacted}",
            ]
        )
    lines.extend(["", "### Recommendation Trace"])
    for trace in appendix.recommendation_trace:
        lines.extend(
            [
                f"- {trace.recommendation_id}: {trace.matched_pattern_id}",
                f"  - Target Step ID: {trace.target_step_id}",
                f"  - Supporting Claims: {', '.join(trace.supporting_claims)}",
                f"  - Cost Model Version: {trace.cost_model_version}",
                f"  - Scoring Model Version: {trace.scoring_model_version}",
                f"  - Privacy Model Version: {trace.privacy_model_version}",
                f"  - Decision Log ID: {trace.decision_log_id}",
                f"  - Review Status: {trace.review_status}",
            ]
        )
    lines.extend(
        [
            "",
            "### Decision Log",
            *_bullet(appendix.decision_log),
            "",
            "### Reviewer Notes",
            *_bullet(appendix.reviewer_notes),
            "",
            "### Confidence And Uncertainty Flags",
            *_bullet(appendix.confidence_and_uncertainty_flags),
            "",
            "### Verification Receipt",
            f"- Report Schema Version: {receipt.report_schema_version}",
            f"- Pattern Library Version: {receipt.pattern_library_version}",
            f"- Privacy Model Version: {receipt.privacy_model_version}",
            f"- Cost Model Version: {receipt.cost_model_version}",
            f"- Scoring Model Version: {receipt.scoring_model_version}",
            f"- Claim Count: {receipt.claim_count}",
            f"- Assumption Count: {receipt.assumption_count}",
            f"- Blocking Finding Count: {receipt.blocking_finding_count}",
            f"- Review Status: {receipt.review_status}",
            "- Source Hashes:",
            *_bullet(receipt.source_hashes),
        ]
    )
    return lines


def _bullet(items: Iterable[str]) -> list[str]:
    values = [str(item) for item in items]
    return [f"- {item}" for item in values] if values else ["- none"]


def _indented_bullet(items: Iterable[str]) -> list[str]:
    values = [str(item) for item in items]
    return [f"    - {item}" for item in values] if values else ["    - none"]


def _format_evidence_ref(ref) -> str:
    quote = f": {ref.quote}" if getattr(ref, "quote", None) else ""
    return f"{ref.source_id} / {ref.chunk_id}{quote}"


def _format_mapping_refs(refs: list) -> str:
    return ", ".join(
        f"{_ref_value(ref, 'source_id')} / {_ref_value(ref, 'chunk_id')}" for ref in refs
    )


def _ref_value(ref, key: str) -> str:
    if isinstance(ref, dict):
        return ref.get(key, "unknown")
    return getattr(ref, key, "unknown")


def _flatten(groups: Iterable[Iterable[str]]) -> list[str]:
    return [item for group in groups for item in group]


def _ai_fit(card: RecommendationCard) -> str:
    if card.architecture.llm_components:
        return "AI assists with language-heavy interpretation while deterministic gates bound risk."
    return "AI is not central; deterministic automation should carry the workflow."


def _privacy_mode_label(privacy_class: str) -> str:
    if privacy_class in {"public", "internal"}:
        return "cloud safe"
    if privacy_class in {"confidential", "sensitive"}:
        return "cloud only after redaction"
    return "local/on-prem required"


def _build_buy_label(solution_type: str) -> str:
    if solution_type == "do_not_automate_yet":
        return "do not build yet"
    if solution_type in {"classic_script", "api_integration", "rpa"}:
        return "build small integration"
    if solution_type == "high_autonomy_agent_future_only":
        return "do not build yet"
    return "build custom AI workflow"
