"""Deterministic roadmap report assembly for demo domain inputs."""

from __future__ import annotations

import hashlib
from pathlib import Path

from workflow_agent_studio.costing.engine import estimate_pattern_cost
from workflow_agent_studio.domain.recommendation import RecommendationCard
from workflow_agent_studio.domain.roadmap import (
    EvaluationPlan,
    EvidencePacket,
    EvidenceSourceSummary,
    ExecutiveSummary,
    GovernancePlan,
    ProcessInventoryItem,
    RoadmapReport,
    RoadmapWorkflowMap,
    RolloutPlan,
    VerificationAppendix,
)
from workflow_agent_studio.domain.verification import (
    ModelMetadata,
    RecommendationTrace,
    RoadmapAssumption,
    RoadmapClaim,
    RoadmapEvidenceItem,
    RoadmapVerificationReceipt,
)
from workflow_agent_studio.privacy.classifier import classify_privacy
from workflow_agent_studio.roadmap.pattern_matching import match_smb_pattern
from workflow_agent_studio.scoring.priority import compute_priority_score


def generate_roadmap_report(input_path: str | Path) -> RoadmapReport:
    path = Path(input_path)
    text = path.read_text(encoding="utf-8")
    profile = _profile_for_input(path, text)
    source_hash = f"sha256:{hashlib.sha256(text.encode('utf-8')).hexdigest()}"
    privacy = classify_privacy(text)
    source_privacy_class = profile["privacy_class"]
    match = match_smb_pattern(
        workflow_description=profile["workflow_description"],
        pain_point=profile["pain_point"],
        privacy_class=source_privacy_class,
    )
    cost = estimate_pattern_cost(
        pattern_id=match.pattern_id,
        scope=profile["scope"],
        privacy_mode=profile["privacy_mode"],
        monthly_volume=profile["monthly_volume"],
        assumptions=profile["assumptions"],
        confidence=profile["confidence"],
    )
    score = compute_priority_score(
        business_value=profile["business_value"],
        delivery_readiness=profile["delivery_readiness"],
        risk_penalty=profile["risk_penalty"],
        evaluation_clarity=profile["evaluation_clarity"],
        solution_type=match.recommended_solution_type,
        confidence=profile["confidence"],
        uncertainty_notes=profile["uncertainty_notes"],
    )
    recommendation_id = f"REC-{profile['domain_id'].upper()}-001"
    claim_id = f"CLM-{profile['domain_id'].upper()}-001"
    assumption_id = f"ASM-{profile['domain_id'].upper()}-001"

    recommendation = RecommendationCard.model_validate(
        {
            "recommendation_id": recommendation_id,
            "recommendation": profile["recommendation"],
            "target_workflow_step": profile["target_step"],
            "expected_value": {
                "qualitative": profile["expected_value"],
                "quantitative_assumption": profile["quantitative_assumption"],
            },
            "required_data": profile["required_data"],
            "privacy_class": source_privacy_class,
            "implementation_option": match.recommended_solution_type,
            "architecture": {
                "model": profile["architecture_model"],
                "deterministic_components": profile["deterministic_components"],
                "llm_components": profile["llm_components"],
            },
            "estimated_cost": {
                "one_time_low": cost.one_time.low,
                "one_time_medium": cost.one_time.medium,
                "one_time_high": cost.one_time.high,
                "currency": cost.currency,
            },
            "estimated_time": profile["estimated_time"],
            "required_people": profile["required_people"],
            "dependencies": profile["dependencies"],
            "risks": profile["risks"],
            "validation_method": profile["validation_method"],
            "success_metrics": profile["success_metrics"],
            "confidence_level": profile["confidence"],
            "assumptions": profile["assumptions"],
            "evidence": [{"source_id": profile["source_id"], "chunk_id": "CH-001"}],
            "fallback_option": profile["fallback_option"],
            "human_gate": profile["human_gate"],
        }
    )

    claim = RoadmapClaim(
        claim_id=claim_id,
        claim_text=profile["claim_text"],
        claim_type="recommendation",
        source_refs=[{"source_id": profile["source_id"], "chunk_id": "CH-001"}],
        evidence_level="pattern_based",
        confidence=profile["confidence"],
        created_by="roadmap_service:v1",
        status="needs_review",
    )
    assumption = RoadmapAssumption(
        assumption_id=assumption_id,
        text=profile["assumptions"][0],
        impact_if_wrong=profile["assumption_impact"],
        verification_method=profile["assumption_verification"],
        owner=profile["business_owner"],
        expires_at_stage="before_implementation",
        status="unresolved",
    )
    trace = RecommendationTrace(
        recommendation_id=recommendation_id,
        target_step_id=profile["target_step_id"],
        matched_pattern_id=f"{match.pattern_id}:{match.pattern_version}",
        supporting_claims=[claim_id],
        cost_model_version="cost-engine-baseline-v1",
        scoring_model_version=score.scoring_model_version,
        privacy_model_version=privacy.schema_version,
        decision_log_id=f"DEC-{profile['domain_id'].upper()}-001",
        review_status="needs_human_review",
    )

    return RoadmapReport(
        report_id=f"RPT-{profile['domain_id'].upper()}-001",
        executive_summary=ExecutiveSummary(
            company_context=profile["company_context"],
            top_recommended_initiatives=[profile["recommendation"]],
            top_do_not_automate_yet_items=profile["do_not_automate"],
            roadmap_30_60_90=profile["roadmap_30_60_90"],
            overall_privacy_mode_recommendation=profile["privacy_mode_recommendation"],
            overall_confidence_level=profile["confidence"],
            critical_assumptions=profile["assumptions"],
        ),
        evidence_packet=EvidencePacket(
            source_documents=[
                EvidenceSourceSummary(
                    source_id=profile["source_id"],
                    source_type="synthetic_demo_markdown",
                    source_hash=source_hash,
                    extracted_evidence_snippets=profile["evidence_snippets"],
                    missing_evidence=profile["missing_evidence"],
                    redaction_status=privacy.redaction_status,
                    source_privacy_class=source_privacy_class,
                )
            ]
        ),
        workflow_map=[
            RoadmapWorkflowMap(
                workflow_id=profile["workflow_id"],
                workflow_name=profile["workflow_name"],
                business_owner=profile["business_owner"],
                trigger=profile["trigger"],
                actors=profile["actors"],
                systems=profile["systems"],
                steps=profile["steps"],
                decisions=profile["decisions"],
                exceptions=profile["exceptions"],
                inputs=profile["inputs"],
                outputs=profile["outputs"],
                frequency_or_volume=profile["frequency_or_volume"],
                pain_points=profile["pain_points"],
                current_tools=profile["current_tools"],
                current_manual_effort=profile["current_manual_effort"],
                evidence_references=[{"source_id": profile["source_id"], "chunk_id": "CH-001"}],
            )
        ],
        process_inventory=[
            ProcessInventoryItem(
                process_id=f"PROC-{profile['domain_id'].upper()}-001",
                process_name=profile["workflow_name"],
                automation_feasibility_score=profile["delivery_readiness"],
                business_impact_score=profile["business_value"],
                privacy_sensitivity_score=profile["privacy_sensitivity_score"],
                security_risk_score=profile["risk_penalty"],
                data_readiness_score=profile["data_readiness_score"],
                implementation_complexity_score=profile["implementation_complexity_score"],
                evaluation_clarity_score=profile["evaluation_clarity"],
                recommended_solution_type=match.recommended_solution_type,
            )
        ],
        recommendations=[recommendation],
        do_not_automate_rationale=profile["do_not_automate"],
        rollout_plan=RolloutPlan(stages=profile["roadmap_30_60_90"]),
        evaluation_plan=EvaluationPlan(
            golden_test_cases=profile["golden_test_cases"],
            shadow_mode=profile["shadow_mode"],
            human_review_sample=profile["human_review_sample"],
            acceptance_criteria=profile["acceptance_criteria"],
            regression_tests=profile["regression_tests"],
            stop_conditions=profile["stop_conditions"],
        ),
        governance_plan=GovernancePlan(
            owner=profile["business_owner"],
            review_cadence="Weekly during pilot.",
            approval_rules=[profile["human_gate"]["approval_event"]],
            incident_handling="Pause automation and route work manually.",
            change_policy="Review prompt, model, pattern, cost, and privacy changes.",
            data_retention="Retain only redacted planning artifacts for demo use.",
            audit_logs="Record local review notes and verification receipts.",
        ),
        verification_appendix=VerificationAppendix(
            claims_registry=[claim],
            assumptions_registry=[assumption],
            evidence_table=[
                RoadmapEvidenceItem(
                    evidence_id=f"EVD-{profile['domain_id'].upper()}-001",
                    source_id=profile["source_id"],
                    chunk_id="CH-001",
                    source_hash=source_hash,
                    evidence_summary=profile["evidence_snippets"][0],
                    redacted=True,
                )
            ],
            recommendation_trace=[trace],
            decision_log=[f"{trace.decision_log_id}: matched {match.pattern_id}."],
            reviewer_notes=[],
            confidence_and_uncertainty_flags=score.uncertainty_notes,
            receipt=RoadmapVerificationReceipt(
                report_schema_version="roadmap_report:v1",
                source_hashes=[source_hash],
                prompt_versions={"roadmap": "deterministic_service:v1"},
                model_metadata=ModelMetadata(
                    provider="local",
                    model="deterministic-roadmap-service",
                    prompt_version="none",
                    generation_mode="deterministic_demo",
                ),
                pattern_library_version="smb-pattern-v1",
                privacy_model_version=privacy.schema_version,
                cost_model_version="cost-engine-baseline-v1",
                scoring_model_version=score.scoring_model_version,
                claim_count=1,
                assumption_count=1,
                blocking_finding_count=0,
                review_status="draft",
                recommendation_traces=[trace],
            ),
        ),
    )


def _profile_for_input(path: Path, text: str) -> dict:
    name = path.name
    if "hair_salon" in name:
        return _hair_salon_profile()
    if "ecommerce" in name:
        return _ecommerce_profile()
    if "legal" in name:
        return _legal_profile()
    raise ValueError(f"Unsupported roadmap demo input: {path}")


def _hair_salon_profile() -> dict:
    return {
        "domain_id": "salon",
        "source_id": "SRC-SALON",
        "privacy_class": "sensitive",
        "privacy_mode": "lightweight_cloud",
        "privacy_mode_recommendation": "Lightweight cloud only after contact fields are redacted.",
        "company_context": "Beauty salon with four stylists and repeated booking messages.",
        "workflow_description": "Hair salon appointment reminders and booking confirmations.",
        "pain_point": "Front desk manually checks calendar availability.",
        "workflow_name": "Appointment booking and reminders",
        "workflow_id": "WF-SALON",
        "business_owner": "Salon owner",
        "trigger": "Client asks for appointment availability.",
        "actors": ["client", "receptionist", "stylist", "owner"],
        "systems": ["Instagram", "WhatsApp", "Google Calendar"],
        "steps": ["Capture service request", "Check calendar", "Confirm booking", "Send reminder"],
        "decisions": ["Confirm available slot", "Escalate cancellation decision"],
        "exceptions": ["Late cancellation", "stylist-specific request"],
        "inputs": ["client name", "phone number", "service type", "preferred time"],
        "outputs": ["calendar booking", "reminder message"],
        "frequency_or_volume": "70-100 appointments per week.",
        "pain_points": ["missed messages", "no-shows", "manual reminders"],
        "current_tools": ["Instagram", "WhatsApp", "Google Calendar"],
        "current_manual_effort": "Receptionist manually checks and confirms every booking.",
        "recommendation": "Appointment booking and reminder automation",
        "target_step": "Check availability and send reminder",
        "target_step_id": "WF-SALON-STEP-003",
        "expected_value": "Reduce missed messages and no-shows.",
        "quantitative_assumption": "Reduce manual reminder work by 30-50 percent.",
        "required_data": ["service menu", "availability", "booking rules"],
        "architecture_model": "Deterministic calendar checks with optional reply drafting.",
        "deterministic_components": ["availability lookup", "slot hold", "confirmation rule"],
        "llm_components": ["draft customer-friendly reply"],
        "estimated_time": {"low": "2 weeks", "medium": "4 weeks", "high": "5 weeks"},
        "required_people": ["automation engineer", "owner", "front desk reviewer"],
        "dependencies": ["calendar access", "service menu", "booking rules"],
        "risks": ["double booking", "wrong service duration", "contact data exposure"],
        "validation_method": ["golden booking requests", "calendar conflict checks"],
        "success_metrics": ["booking accuracy", "no-show rate", "manual handling time"],
        "human_gate": {
            "required": True,
            "reviewer": "Owner",
            "approval_event": "Approve first live booking workflow.",
            "rationale": "Calendar writes affect customers.",
        },
        "fallback_option": "Manual receptionist booking with canned reminders.",
        "assumptions": ["Calendar availability can be accessed reliably."],
        "assumption_impact": "Automation may double-book or fail to confirm appointments.",
        "assumption_verification": "Test calendar access against sample booking requests.",
        "claim_text": (
            "Appointment booking is repetitive and suitable for deterministic automation."
        ),
        "evidence_snippets": ["Salon workflow lists repeated booking and reminder steps."],
        "missing_evidence": ["Exact no-show baseline"],
        "do_not_automate": ["Cancellation penalty decisions", "medical or skin-condition advice"],
        "roadmap_30_60_90": ["Clean booking rules", "Pilot reminders", "Review channel analytics"],
        "scope": "small",
        "monthly_volume": 400,
        "confidence": "medium",
        "business_value": 70,
        "delivery_readiness": 80,
        "risk_penalty": 20,
        "evaluation_clarity": 85,
        "privacy_sensitivity_score": 55,
        "data_readiness_score": 75,
        "implementation_complexity_score": 35,
        "uncertainty_notes": ["No-show baseline is estimated."],
        "golden_test_cases": ["appointment request", "late cancellation", "stylist preference"],
        "shadow_mode": "Draft replies without writing calendar events.",
        "human_review_sample": "First 50 booking recommendations.",
        "acceptance_criteria": ["No calendar conflicts in golden cases."],
        "regression_tests": ["double-booking prevention", "late cancellation escalation"],
        "stop_conditions": ["Calendar conflict", "medical advice request"],
    }


def _ecommerce_profile() -> dict:
    profile = _hair_salon_profile()
    profile.update(
        {
            "domain_id": "ecom",
            "source_id": "SRC-ECOM",
            "privacy_mode_recommendation": "Private analysis or cloud after PII redaction.",
            "company_context": "Shopify store with repetitive order-status and return questions.",
            "workflow_description": "E-commerce returns workflow checks orders and refund policy.",
            "pain_point": "Support agents manually summarize return requests.",
            "workflow_name": "Returns and support triage",
            "workflow_id": "WF-ECOM",
            "business_owner": "Store owner",
            "trigger": "Customer asks about return, refund, or order status.",
            "actors": ["customer", "support assistant", "owner", "fulfillment partner"],
            "systems": ["Gmail", "Instagram DM", "Shopify", "Google Sheets"],
            "steps": [
                "Classify message",
                "Lookup order",
                "Check return policy",
                "Request approval",
            ],
            "decisions": ["Refund requires owner approval", "Damaged item requires photo"],
            "exceptions": ["Damaged item", "compensation request"],
            "inputs": ["email", "shipping address", "order ID", "return reason"],
            "outputs": ["triage label", "draft response", "approval request"],
            "frequency_or_volume": "500 orders per month.",
            "pain_points": ["repetitive order-status questions", "slow returns", "manual reports"],
            "current_tools": ["Gmail", "Shopify", "Google Doc"],
            "current_manual_effort": "Support assistant searches Shopify manually.",
            "recommendation": "Human-in-the-loop returns assistant",
            "target_step": "Return request classification and policy check",
            "target_step_id": "WF-ECOM-STEP-003",
            "expected_value": "Faster return handling without automatic refunds.",
            "quantitative_assumption": "Reduce manual triage time by 30-50 percent.",
            "required_data": ["return policy", "order metadata", "customer message"],
            "architecture_model": "LLM drafting with deterministic policy and approval gates.",
            "deterministic_components": ["order lookup", "refund approval gate", "policy check"],
            "llm_components": ["summarize return request", "draft response"],
            "estimated_time": {"low": "3 weeks", "medium": "5 weeks", "high": "7 weeks"},
            "dependencies": ["return policy", "Shopify access", "approval rules"],
            "risks": ["automatic refund", "wrong policy answer", "customer data exposure"],
            "validation_method": ["golden return tickets", "owner review"],
            "success_metrics": ["return handling time", "approval accuracy", "first response time"],
            "fallback_option": "Manual policy lookup and owner approval queue.",
            "do_not_automate": ["Automatic refunds", "customer compensation decisions"],
            "roadmap_30_60_90": [
                "Clean policy",
                "Pilot returns assistant",
                "Add support reporting",
            ],
            "monthly_volume": 500,
            "business_value": 85,
            "delivery_readiness": 70,
            "risk_penalty": 45,
            "evaluation_clarity": 75,
            "implementation_complexity_score": 55,
            "golden_test_cases": ["order status", "eligible return", "damaged item"],
            "regression_tests": ["automatic refund blocker", "damaged item photo rule"],
            "stop_conditions": ["refund executed without approval"],
        }
    )
    return profile


def _legal_profile() -> dict:
    profile = _hair_salon_profile()
    profile.update(
        {
            "domain_id": "legal",
            "source_id": "SRC-LEGAL",
            "privacy_class": "restricted",
            "privacy_mode": "local_on_prem",
            "privacy_mode_recommendation": "Local/on-prem or strict private analysis required.",
            "company_context": (
                "Immigration consultancy with restricted identity and legal-status data."
            ),
            "workflow_description": "Legal consultancy checklist for visa document collection.",
            "pain_point": "Staff manually verify required documents.",
            "workflow_name": "Visa document checklist",
            "workflow_id": "WF-LEGAL",
            "business_owner": "Consultant",
            "trigger": "Client asks about missing documents or case status.",
            "actors": ["client", "coordinator", "consultant", "document reviewer"],
            "systems": ["website form", "email", "shared drive", "case tracker"],
            "steps": ["Collect inquiry", "Send checklist", "Check documents", "Escalate strategy"],
            "decisions": ["Consultant controls legal strategy", "Coordinator checks completeness"],
            "exceptions": ["missing passport", "deadline risk", "strategy question"],
            "inputs": ["passport copy", "legal status", "deadline", "checklist status"],
            "outputs": ["missing item list", "consultant review queue"],
            "frequency_or_volume": "Synthetic demo volume not verified.",
            "pain_points": ["missing documents", "repeated status questions", "slow intake"],
            "current_tools": ["email", "shared drive", "case tracker"],
            "current_manual_effort": "Coordinator checks completeness manually.",
            "recommendation": "Private legal checklist assistant",
            "target_step": "Document checklist completeness review",
            "target_step_id": "WF-LEGAL-STEP-006",
            "expected_value": (
                "Reduce missing-document back-and-forth while preserving legal review."
            ),
            "quantitative_assumption": "Reduce coordinator checklist time by 20-40 percent.",
            "required_data": ["approved checklist", "document requirements", "review boundaries"],
            "architecture_model": "Private/local RAG checklist assistant with consultant review.",
            "deterministic_components": ["approved checklist lookup", "restricted mode gate"],
            "llm_components": ["draft missing item questions", "summarize checklist status"],
            "estimated_time": {"low": "5 weeks", "medium": "8 weeks", "high": "12 weeks"},
            "dependencies": [
                "approved checklist",
                "restricted storage",
                "consultant review process",
            ],
            "risks": ["legal advice automation", "restricted data exposure", "outdated checklist"],
            "validation_method": ["golden checklist cases", "consultant review"],
            "success_metrics": ["checklist coverage", "consultant correction rate"],
            "fallback_option": "Manual checklist review by coordinator and consultant.",
            "do_not_automate": ["Legal eligibility decisions", "legal strategy", "final advice"],
            "roadmap_30_60_90": [
                "Define checklist",
                "Pilot private assistant",
                "Review quality tradeoffs",
            ],
            "scope": "medium",
            "monthly_volume": 100,
            "confidence": "low",
            "business_value": 80,
            "delivery_readiness": 45,
            "risk_penalty": 90,
            "evaluation_clarity": 45,
            "privacy_sensitivity_score": 95,
            "data_readiness_score": 50,
            "implementation_complexity_score": 80,
            "uncertainty_notes": ["Local/private model quality is untested."],
            "golden_test_cases": ["missing passport", "deadline question", "strategy escalation"],
            "shadow_mode": "Draft checklist status only; consultant remains final reviewer.",
            "acceptance_criteria": ["No legal advice is generated without consultant review."],
            "regression_tests": ["legal advice blocker", "restricted cloud blocker"],
            "stop_conditions": ["client-facing legal interpretation without consultant review"],
        }
    )
    return profile
