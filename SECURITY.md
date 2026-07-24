# Security Policy

## Scope

This repository contains only sample code, synthetic data, and production-inspired reference implementations.

No production credentials, customer information, or confidential datasets should ever be committed.

---

## Never Commit

- passwords
- API keys
- storage account keys
- SAS tokens
- OAuth secrets
- client secrets
- connection strings
- certificates
- tenant identifiers
- production URLs
- customer data

---

## Authentication

Production environments should use:

- Managed Identity
- Microsoft Entra ID
- Service Principals
- Azure Key Vault
- Unity Catalog Storage Credentials

Never store credentials in source code.

---

## Secret Management

Secrets belong in:

- Azure Key Vault
- GitHub Secrets
- Databricks Secret Scopes (only when justified)

---

## Responsible Disclosure

Security issues should be privately reported before public disclosure.
