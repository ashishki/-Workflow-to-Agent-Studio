# Data Classification

Purpose: classify source text, workflow fields, and recommendation data
requirements before architecture decisions are made.

## Classes

| Class | Meaning | Examples | Default Mode |
|-------|---------|----------|--------------|
| Public | intended for public use | public FAQ, public pricing page | lightweight cloud |
| Internal | operational but not sensitive | process steps, team roles, system names | lightweight cloud or private |
| Confidential | business-sensitive | private SOP, margins, vendor contracts | private analysis |
| Sensitive | personal or regulated-adjacent data | names, phones, addresses, order history | private analysis or cloud after redaction |
| Restricted | high-risk regulated or identity data | passports, health data, legal status, tax docs, payment card data | local/on-prem or private with strict controls |

## Field Flags

The classifier should detect:

- email;
- phone;
- address;
- name-like values in context;
- passport/ID-like values;
- payment card-like values;
- API keys and credentials;
- health keywords;
- legal/immigration keywords;
- tax/accounting keywords;
- HR/candidate keywords;
- minors/student data hints.

## Source Classification

Source privacy class is the highest class detected across:

- raw content;
- field inventory;
- domain;
- uploaded file type;
- operator-selected domain;
- known workflow category.

## Recommendation Impact

Privacy class affects:

- allowed model mode;
- redaction requirement;
- human review requirement;
- storage retention;
- export warnings;
- cost/security overhead;
- implementation complexity score.

## Blocking Examples

- Passport copies in a legal consultancy workflow -> restricted.
- Patient diagnosis notes -> restricted.
- Credit card numbers -> restricted and should not be accepted as source data.
- Customer emails and addresses in e-commerce support -> sensitive.
- Salon appointment preferences -> sensitive but usually not restricted.
