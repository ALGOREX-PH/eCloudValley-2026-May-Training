# CloudKaiju — Security & Compliance

This document covers authentication, authorization, encryption, and the compliance posture of CloudKaiju's managed SaaS offering.

## Authentication

### Single sign-on (SSO)

CloudKaiju supports the following SSO methods:

- **SAML 2.0** — Available on Pro and Enterprise tiers
- **OIDC** — Available on Pro and Enterprise tiers
- **Google Workspace** — Available on all tiers including Free
- **GitHub OAuth** — Available on all tiers including Free

SAML and OIDC are configured per-workspace by an Owner via **Settings → Authentication**.

### Multi-factor authentication

MFA via TOTP is supported on all tiers and can be enforced workspace-wide on Pro and above. WebAuthn (security keys, Touch ID, Windows Hello) is available on Enterprise.

## API key rotation

API keys are issued at the **service account** level (not at the user level) and grant access scoped to a single workspace.

To rotate a key:

1. Open the workspace and go to **Settings → Service Accounts**.
2. Click the service account whose key you want to rotate.
3. Click **Rotate Key**. CloudKaiju issues a new key and displays it once.
4. Update your application or CI to use the new key.
5. The old key continues to work for **24 hours** (a grace period to avoid downtime).
6. After 24 hours the old key is revoked automatically.

Service account keys can also be revoked immediately from the same page if compromise is suspected.

> Best practice: rotate every 90 days. Use the CloudKaiju Terraform provider to automate.

## Authorization (RBAC)

Permissions are enforced at the workspace level. Within a workspace, roles are: Owner, Editor, Viewer, and Service Account. Role-to-resource mapping follows the principle of least privilege:

| Resource | Owner | Editor | Viewer | Service Account |
|---|---|---|---|---|
| Read metrics/logs/traces | ✓ | ✓ | ✓ | ✓ (configurable) |
| Create/edit dashboards | ✓ | ✓ | – | – |
| Create/edit alerts | ✓ | ✓ | – | ✓ (configurable) |
| Manage integrations | ✓ | ✓ | – | – |
| Manage members | ✓ | – | – | – |
| Manage billing | ✓ | – | – | – |

## Encryption

- **In transit** — TLS 1.2+ everywhere. Customer agents pin our public certificate.
- **At rest** — AES-256 for all stored data. Customer-managed keys (AWS KMS) available on Enterprise.

## Compliance

CloudKaiju is **SOC 2 Type II** certified (audited annually) and **ISO 27001** certified. **HIPAA** support is available for Enterprise customers under a signed BAA. **FedRAMP Moderate** is in the authorization queue.

## Vulnerability disclosure

Report security issues to security@cloudkaiju.example. We acknowledge within 24 hours and aim to triage within 72 hours. A public bug-bounty program is in private beta.
