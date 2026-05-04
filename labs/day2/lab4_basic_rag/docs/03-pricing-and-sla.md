# CloudKaiju — Pricing & SLA

## Tiers

CloudKaiju is offered in three tiers: **Free**, **Pro**, and **Enterprise**. Pricing below is in USD; PHP-equivalent invoicing is available for Philippine customers.

### Free

- Up to **3 users**
- Up to **5 GB of log ingest per month**
- Up to **10 million metric data points per month**
- **7 days** of data retention
- Email support, best-effort response
- No SLA

Cost: **$0/month**.

### Pro

- Unlimited users
- **100 GB** of included log ingest per month, then $0.50/GB
- **500 million** included metric data points per month, then $0.10 per million
- **13 months** of data retention
- SAML / OIDC SSO included
- Standard support (business hours, 1-business-day response)
- **99.9% uptime SLA** with service credits

Cost: starts at **$499/month** for the workspace, plus usage above included quotas.

### Enterprise

- Everything in Pro, plus:
- **Single-tenant deployment** in customer's VPC (AWS PrivateLink / Azure Private Link)
- Customer-managed encryption keys (AWS KMS)
- HIPAA BAA available
- WebAuthn MFA, fine-grained audit logs
- 24×7 support with named TAM, **1-hour response** for P1
- **99.95% uptime SLA** with service credits
- Custom data residency options

Cost: **contact sales** — typically starts at $4,000/month for a small workspace.

## SLA details

| Tier | Uptime | Service Credit |
|---|---|---|
| Free | None | None |
| Pro | 99.9% | 10% credit if monthly uptime < 99.9%, 25% credit if < 99.0% |
| Enterprise | 99.95% | 10% credit if monthly uptime < 99.95%, 30% credit if < 99.0% |

"Uptime" is measured as the percentage of 1-minute intervals during a calendar month in which the customer's workspace was available, excluding scheduled maintenance windows announced at least 7 days in advance.

## Billing

- All tiers are billed monthly. Annual prepayment receives a 15% discount.
- Pro and Enterprise customers can add a **monthly spend cap** to prevent runaway usage.
- Invoices include itemized usage by workspace and by data type.
- Philippine customers can be invoiced in PHP at the prevailing month's BSP exchange rate.

## Trial

A 30-day Pro trial is available with no credit card required. After the trial expires, the workspace downgrades to Free unless billing is configured.
