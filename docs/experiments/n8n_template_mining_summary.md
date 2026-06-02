# n8n Template Mining Summary

Status: public-source metadata mining; not buyer proof

## Claim Boundary

This artifact summarizes extracted metadata from local clones of public
n8n template repositories. It does not commit raw third-party workflow JSON
and does not prove ROI, customer demand, or implementation safety.

## Run Summary

- source roots: .data/n8n_sources
- scanned JSON files: 8854
- parsed n8n workflows: 8824
- skipped JSON files: 30
- duplicate workflows collapsed: 3861
- deduplicated candidates: 4963
- candidates with AI nodes: 1875
- candidates with risky action signals: 2069
- candidates with data sensitivity signals: 3616

## Archetype Counts

| Archetype | Candidates |
|---|---:|
| `internal_notification_or_approval_workflow` | 1717 |
| `automation_workflow_candidate` | 1385 |
| `backoffice_data_sync_or_reporting` | 599 |
| `ai_assisted_workflow` | 498 |
| `crm_lead_enrichment_or_routing` | 237 |
| `ai_email_assistant` | 168 |
| `finance_or_invoice_processing` | 165 |
| `customer_support_triage` | 111 |
| `appointment_or_meeting_coordination` | 83 |

## Top Integrations

| Integration | Candidates |
|---|---:|
| `set` | 2898 |
| `httprequest` | 2169 |
| `slack` | 1694 |
| `webhook` | 1693 |
| `stickynote` | 1187 |
| `openai` | 722 |
| `manual` | 688 |
| `openaiapi` | 631 |
| `googlesheets` | 619 |
| `if` | 607 |
| `schedule` | 604 |
| `gmail` | 580 |
| `cron` | 515 |
| `code` | 473 |
| `googlecalendar` | 455 |
| `agent` | 356 |
| `lmchatopenai` | 353 |
| `function` | 313 |
| `merge` | 288 |
| `splitout` | 263 |

## Top Candidate Clusters

| Archetype | Business integrations | Candidates |
|---|---|---:|
| `internal_notification_or_approval_workflow` | `openaiapi`, `slack` | 628 |
| `internal_notification_or_approval_workflow` | `slack` | 312 |
| `automation_workflow_candidate` | - | 83 |
| `backoffice_data_sync_or_reporting` | `googlesheets` | 43 |
| `internal_notification_or_approval_workflow` | `googlesheets`, `slack` | 33 |
| `backoffice_data_sync_or_reporting` | `googlesheets`, `openai` | 23 |
| `ai_assisted_workflow` | `agent`, `chat`, `lmchatopenai` | 22 |
| `automation_workflow_candidate` | `respondtowebhook` | 15 |
| `crm_lead_enrichment_or_routing` | `hubspot`, `slack` | 14 |
| `internal_notification_or_approval_workflow` | `telegram` | 14 |
| `automation_workflow_candidate` | `wait` | 13 |
| `internal_notification_or_approval_workflow` | `googlecalendar`, `slack` | 13 |
| `automation_workflow_candidate` | `github` | 13 |
| `backoffice_data_sync_or_reporting` | `notion` | 13 |
| `backoffice_data_sync_or_reporting` | `agent`, `embeddingscohere`, `googlesheets` | 12 |
| `automation_workflow_candidate` | `googlecalendar` | 12 |
| `ai_assisted_workflow` | `agent`, `aggregate`, `chat` | 12 |
| `internal_notification_or_approval_workflow` | `googlesheets`, `openai`, `slack` | 12 |
| `internal_notification_or_approval_workflow` | `openai`, `slack` | 12 |
| `backoffice_data_sync_or_reporting` | `agent`, `embeddingshuggingface`, `googlesheets` | 12 |
| `automation_workflow_candidate` | `readwritefile` | 11 |
| `backoffice_data_sync_or_reporting` | `agent`, `embeddingsopenai`, `googlesheets` | 11 |
| `ai_assisted_workflow` | `agent`, `chat`, `documentdefaultdataloader` | 11 |
| `automation_workflow_candidate` | `executeworkflow` | 10 |
| `backoffice_data_sync_or_reporting` | `gmail`, `googlesheets` | 10 |
| `automation_workflow_candidate` | `gmail` | 10 |
| `ai_assisted_workflow` | `agent`, `chat`, `executeworkflow` | 10 |
| `backoffice_data_sync_or_reporting` | `airtable` | 10 |
| `crm_lead_enrichment_or_routing` | `hubspot`, `openai`, `slack` | 10 |
| `internal_notification_or_approval_workflow` | `slack`, `smtp` | 9 |

## Review Queue Sample

| Archetype | Workflow | AI nodes | Risk signals | Sensitivity | Sources |
|---|---|---:|---|---|---:|
| `ai_assisted_workflow` | RAG & GenAI App With WordPress Content | 14 | `filter:action`, `httprequest:action`, `memorypostgreschat:action` | `database_business_data` | 3 |
| `ai_assisted_workflow` | RAG & GenAI App With WordPress Content | 14 | `filter:action`, `httprequest:action`, `memorypostgreschat:action` | `database_business_data` | 2 |
| `ai_assisted_workflow` | Untitled n8n workflow | 8 | `set:action`, `splitout:action`, `switch:action` | `personal_or_customer_messages` | 5 |
| `ai_assisted_workflow` | Untitled n8n workflow | 5 | `redis:get`, `redis:push`, `set:action` | - | 5 |
| `ai_assisted_workflow` | Business WhatsApp AI RAG Chatbot | 11 | `httprequest:action`, `if:action`, `whatsapp:send` | `document_or_workspace_data`, `personal_or_customer_messages` | 2 |
| `ai_assisted_workflow` | Business WhatsApp AI RAG Chatbot | 7 | `httprequest:action`, `if:action`, `whatsapp:send` | `document_or_workspace_data`, `personal_or_customer_messages` | 3 |
| `ai_assisted_workflow` | Email AI Auto-responder. Summerize and send email | 14 | `emailsend:action`, `httprequest:action` | `document_or_workspace_data` | 5 |
| `ai_email_assistant` | ✨🩷Automated Social Media Content Publishing Factory + System Prompt Composition | 17 | `facebookgraphapi:action`, `gmail:sendAndWait`, `googledrive:createFromText` | `document_or_workspace_data`, `personal_or_customer_messages` | 2 |
| `ai_email_assistant` | ✨🔪 Advanced AI Powered Document Parsing & Text Extraction with Llama Parse | 8 | `gmail:get`, `googledrive:createFromText`, `googlesheets:appendOrUpdate` | `document_or_workspace_data`, `personal_or_customer_messages`, `spreadsheet_business_data` | 2 |
| `ai_email_assistant` | Untitled n8n workflow | 5 | `airtable:update`, `airtable:upsert`, `code:action` | `personal_or_customer_messages`, `workspace_or_internal_notes` | 7 |
| `ai_email_assistant` | ✨🩷Automated Social Media Content Publishing Factory + System Prompt Composition | 14 | `facebookgraphapi:action`, `gmail:sendAndWait`, `httprequest:action` | `personal_or_customer_messages` | 2 |
| `ai_email_assistant` | 🦜✨Use OpenAI to Transcribe Audio + Summarize with AI + Save to Google Drive | 5 | `gmail:action`, `gmail:sendAndWait`, `googledrive:createFromText` | `document_or_workspace_data`, `personal_or_customer_messages` | 2 |
| `ai_email_assistant` | Analyze Reddit Posts with AI to Identify Business Opportunities | 7 | `chainsummarization:action`, `gmail:action`, `if:action` | `personal_or_customer_messages`, `spreadsheet_business_data` | 2 |
| `ai_email_assistant` | Effortless Email Management with AI | 12 | `emailsend:action`, `gmail:sendAndWait`, `httprequest:action` | `document_or_workspace_data`, `personal_or_customer_messages` | 5 |
| `appointment_or_meeting_coordination` | Untitled n8n workflow | 35 | `emailsendtool:action`, `memorypostgreschat:action`, `postgrestool:action` | `calendar_or_scheduling_data`, `document_or_workspace_data`, `personal_or_customer_messages` | 2 |
| `appointment_or_meeting_coordination` | Untitled n8n workflow | 5 | `gmail:sendAndWait`, `set:action` | `calendar_or_scheduling_data`, `personal_or_customer_messages` | 2 |
| `appointment_or_meeting_coordination` | Untitled n8n workflow | 4 | `gmail:action`, `gmail:sendAndWait`, `googlecalendar:action` | `calendar_or_scheduling_data`, `personal_or_customer_messages` | 5 |
| `appointment_or_meeting_coordination` | Untitled n8n workflow | 8 | `gmail:get`, `whatsapp:send` | `calendar_or_scheduling_data`, `personal_or_customer_messages` | 5 |
| `appointment_or_meeting_coordination` | Calendar_scheduling | 6 | `gmail:reply` | `calendar_or_scheduling_data`, `personal_or_customer_messages` | 3 |
| `appointment_or_meeting_coordination` | Untitled n8n workflow | 3 | `chainllm:action`, `gmail:action` | `calendar_or_scheduling_data`, `personal_or_customer_messages` | 2 |
| `appointment_or_meeting_coordination` | Template 1150 | 2 | - | `calendar_or_scheduling_data`, `personal_or_customer_messages` | 1 |
| `automation_workflow_candidate` | Untitled n8n workflow | 0 | `gmail:action`, `rssfeedread:action`, `trello:action` | `personal_or_customer_messages` | 2 |
| `automation_workflow_candidate` | 🎥 Analyze YouTube Video for Summaries, Transcripts & Content + Google Gemini AI | 0 | `code:action`, `gmail:action`, `googledrive:createFromText` | `document_or_workspace_data`, `personal_or_customer_messages` | 2 |
| `automation_workflow_candidate` | Log errors and avoid sending too many emails | 0 | `emailsend:action`, `postgres:action`, `postgres:deleteTable` | `database_business_data` | 2 |
| `automation_workflow_candidate` | Monitor_security_advisories | 0 | `if:action`, `jira:action` | `internal_workflow_or_issue_data`, `personal_or_customer_messages` | 2 |
| `automation_workflow_candidate` | PG&E Daily Cost Tracker | 0 | `airtop:action`, `gmail:action` | `personal_or_customer_messages` | 2 |
| `automation_workflow_candidate` | Untitled n8n workflow | 0 | `gmail:action` | `personal_or_customer_messages` | 2 |
| `automation_workflow_candidate` | Untitled n8n workflow | 0 | `gmail:action`, `harvest:create` | `personal_or_customer_messages` | 2 |
| `backoffice_data_sync_or_reporting` | HDW Lead Geländewagen | 11 | `googlesheets:appendOrUpdate`, `googlesheets:update`, `hdwlinkedin:getCompanyPosts` | `spreadsheet_business_data` | 2 |
| `backoffice_data_sync_or_reporting` | AI Social Media Publisher from WordPress | 5 | `facebookgraphapi:action`, `googlesheets:update`, `httprequest:action` | `spreadsheet_business_data` | 2 |
| `backoffice_data_sync_or_reporting` | Resume Screening & Behavioral Interviews with Gemini, Elevenlabs, & Notion ATS copy | 9 | `notion:action`, `notion:update` | `document_or_workspace_data`, `spreadsheet_business_data`, `workspace_or_internal_notes` | 2 |
| `backoffice_data_sync_or_reporting` | Untitled n8n workflow | 9 | `chainllm:action`, `facebookgraphapi:action`, `googlesheets:action` | `spreadsheet_business_data` | 2 |
| `backoffice_data_sync_or_reporting` | HR Job Posting and Evaluation with AI | 7 | `airtable:create`, `airtable:update`, `airtabletool:search` | `document_or_workspace_data`, `workspace_or_internal_notes` | 5 |
| `backoffice_data_sync_or_reporting` | SHEETS RAG | 5 | `code:action`, `postgres:executeQuery`, `toolworkflow:action` | `database_business_data`, `document_or_workspace_data`, `spreadsheet_business_data` | 2 |
| `backoffice_data_sync_or_reporting` | Untitled n8n workflow | 14 | `googledrive:createFromText`, `googlesheets:update` | `document_or_workspace_data`, `spreadsheet_business_data` | 5 |
| `crm_lead_enrichment_or_routing` | Untitled n8n workflow | 6 | `agent:action`, `gmail:action`, `googlecalendartool:action` | `crm_or_lead_data`, `personal_or_customer_messages` | 2 |
| `crm_lead_enrichment_or_routing` | Untitled n8n workflow | 4 | `gmail:action` | `crm_or_lead_data`, `personal_or_customer_messages` | 2 |
| `crm_lead_enrichment_or_routing` | piepdrive-test | 2 | `openai:action`, `pipedrive:action` | `crm_or_lead_data`, `internal_messages` | 5 |
| `crm_lead_enrichment_or_routing` | Untitled n8n workflow | 3 | `hubspot:action` | `crm_or_lead_data` | 2 |
| `crm_lead_enrichment_or_routing` | create-automated-win-loss-analysis-reports | 1 | `notion:create` | `crm_or_lead_data`, `internal_messages`, `spreadsheet_business_data` | 1 |
| `crm_lead_enrichment_or_routing` | Template 1678 | 2 | - | `calendar_or_scheduling_data`, `crm_or_lead_data`, `internal_messages` | 1 |
| `crm_lead_enrichment_or_routing` | Untitled n8n workflow | 3 | - | `crm_or_lead_data` | 2 |
| `customer_support_triage` | Untitled n8n workflow | 15 | `zendesk:update` | `customer_support_data`, `document_or_workspace_data` | 5 |
| `customer_support_triage` | Template 477 | 2 | - | `customer_support_data`, `internal_messages`, `personal_or_customer_messages` | 1 |
| `customer_support_triage` | Template 1173 | 2 | - | `personal_or_customer_messages` | 1 |
| `customer_support_triage` | Template 1191 | 2 | - | `customer_support_data`, `personal_or_customer_messages` | 1 |
| `customer_support_triage` | Template 1143 | 2 | - | `personal_or_customer_messages` | 1 |
| `customer_support_triage` | Template 1163 | 2 | - | `personal_or_customer_messages` | 1 |
| `customer_support_triage` | Template 1413 | 2 | - | `personal_or_customer_messages` | 1 |
| `finance_or_invoice_processing` | Template 429 | 2 | - | `internal_messages`, `payment_or_financial_data`, `personal_or_customer_messages` | 1 |
| `finance_or_invoice_processing` | Streamline Your Zoom Meetings with Secure, Automated Stripe Payments | 0 | `gmail:action`, `googlesheets:create`, `httprequest:action` | `payment_or_financial_data`, `personal_or_customer_messages`, `spreadsheet_business_data` | 2 |
| `finance_or_invoice_processing` | Template 1563 | 2 | - | `payment_or_financial_data`, `personal_or_customer_messages` | 1 |
| `finance_or_invoice_processing` | Template 1641 | 2 | - | `payment_or_financial_data`, `personal_or_customer_messages` | 1 |
| `finance_or_invoice_processing` | Template 1167 | 2 | - | `payment_or_financial_data`, `personal_or_customer_messages` | 1 |
| `finance_or_invoice_processing` | Template 624 | 2 | - | `payment_or_financial_data`, `personal_or_customer_messages` | 1 |
| `finance_or_invoice_processing` | Template 1584 | 1 | - | `internal_messages`, `payment_or_financial_data`, `workspace_or_internal_notes` | 1 |
| `internal_notification_or_approval_workflow` | Test Webhooks in n8n Without Changing WEBHOOK_URL (PostBin & BambooHR Example) | 5 | `bamboohr:action`, `debughelper:action`, `httprequest:action` | `internal_messages` | 2 |
| `internal_notification_or_approval_workflow` | 🤖 AI Powered RAG Chatbot for Your Docs + Google Drive + Gemini + Qdrant | 15 | `code:action`, `googledocs:update`, `googledrive:createFromText` | `document_or_workspace_data`, `personal_or_customer_messages` | 2 |
| `internal_notification_or_approval_workflow` | Pyragogy AI Village - Orchestrazione Master (Architettura Profonda V2) | 12 | `emailsend:action`, `github:createUpdate`, `postgres:executeQuery` | `database_business_data`, `internal_messages` | 1 |
| `internal_notification_or_approval_workflow` | Untitled n8n workflow | 6 | `code:action`, `executeworkflow:action`, `noop:action` | `internal_messages` | 2 |
| `internal_notification_or_approval_workflow` | Untitled n8n workflow | 7 | `googlesheets:appendOrUpdate`, `httprequest:action`, `redis:get` | `personal_or_customer_messages`, `spreadsheet_business_data` | 2 |
| `internal_notification_or_approval_workflow` | ✍️🌄 Your First Wordpress Content Creator - Quick Start | 10 | `agent:action`, `googledrive:createFromText`, `httprequest:action` | `document_or_workspace_data`, `personal_or_customer_messages` | 2 |
| `internal_notification_or_approval_workflow` | 💥AI Social Video Generator with GPT-4, Kling & Blotato —Auto-Post to Instagram, Facebook,, TikTok, Twitter & Pinterest - vide | 6 | `httprequest:action`, `telegram:action`, `telegram:sendVideo` | `personal_or_customer_messages`, `spreadsheet_business_data` | 2 |

## Next Review Step

1. Cluster candidates by archetype and integration set.
2. Reject unsafe high-autonomy candidates before pattern generation.
3. Ask the frontier model for missed opportunities and risks using
   `docs/prompts/frontier_opportunity_discovery.md`.
4. Convert accepted candidates into draft SMB pattern JSON only after
   human review.
