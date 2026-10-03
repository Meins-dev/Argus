# Security

**Language:** **English** · [Português (Brasil)](SECURITY.pt-BR.md)

**Operational template. Review and complete the contact details and response
process before offering commercial support.**

## Reporting a vulnerability

Use **Report a vulnerability** / GitHub Security Advisories in the repository
where Argus is published. If this feature is disabled, contact the repository
maintainer privately; do not include exploitable details in a public issue.
This project has no official response email address or response time.

Include the affected version or commit, operating system, minimal reproduction
steps, observed impact, and a possible mitigation. Remove tokens, keys, personal
data, and private content from logs and screenshots. Do not test against
third-party services or accounts without authorization.

## Secure configuration

- In production, set your own `JWT_SECRET`, `ARGUS_ENCRYPTION_KEY`,
  `DATABASE_URL`, `REDIS_URL`, and `CORS_ORIGINS`. The API rejects the example
  JWT secret, a missing encryption key, and a database other than PostgreSQL in
  production (`api/config.py`).
- Do not publish `.env`, OAuth credential files, databases, dumps, or local
  data. Restrict access to the database and provider logs.
- Update dependencies and review microphone, screen, camera, filesystem, and
  external integration permissions.
- The current data expiration policy and its limitations are described in
  `PRIVACY.md`; it does not delete accounts, persisted memory, or secrets.

## Response

Maintainers should acknowledge reports through a private channel, reproduce the
issue, assess its impact, prepare a fix, and coordinate disclosure with the
reporter. This repository does not yet define an SLA, response team, or credit
process; complete these details before promising support.

---

**Language:** **English** · [Português (Brasil)](SECURITY.pt-BR.md)
