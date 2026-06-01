# Redaction Policy

Purpose: remove or mask data that is unnecessary for roadmap planning while
preserving workflow meaning.

## Redaction Goals

- Prevent secrets from entering prompts, logs, exports, or reports.
- Replace personal values with stable placeholders.
- Preserve field names and workflow structure.
- Make redaction visible in evidence packets.

## Placeholder Format

Use stable placeholders:

- `[EMAIL_1]`;
- `[PHONE_1]`;
- `[PERSON_1]`;
- `[ADDRESS_1]`;
- `[ORDER_ID_1]`;
- `[PASSPORT_ID_1]`;
- `[API_KEY_REDACTED]`;
- `[PAYMENT_CARD_REDACTED]`.

## Always Redact

- passwords;
- API keys;
- tokens;
- private keys;
- session cookies;
- payment card values;
- passport/ID numbers;
- medical record identifiers;
- tax identifiers.

## Usually Redact

- customer names;
- emails;
- phone numbers;
- addresses;
- order IDs;
- employee names;
- candidate names.

## Preserve When Safe

- field labels;
- system names;
- workflow step descriptions;
- policy names;
- synthetic examples;
- aggregate volumes;
- non-sensitive business rules.

## Redaction Preview

Before LLM analysis or export, the operator should see:

- detected class;
- redacted fields count;
- high-risk snippets;
- blocked secrets;
- source-level privacy class;
- whether the redacted version is safe for selected mode.

## Validation

Tests must include:

- email;
- phone;
- address;
- passport/ID-like values;
- payment-like values;
- API keys;
- health/legal/accounting context;
- mixed synthetic and real examples;
- false-positive examples.
