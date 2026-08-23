# Security Policy

## Reporting Vulnerabilities

If you discover a security issue in these teaching materials:

1. **Do not** open a public issue
2. Email the maintainers at `security@agentic-security-demos.example` (placeholder)
3. Include steps to reproduce and potential impact
4. Allow time for assessment before disclosure

## Scope

This policy covers:
- The teaching repository code and fixtures
- Generated demo keys (which are explicitly non-production)
- Student exercise solutions

This policy does **not** cover:
- Private research repositories
- External systems students might incorrectly target
- Production deployments of patterns taught here

## Safety by Design

These demos are built with safety guarantees:
- No network I/O in any test or demo
- No persistent credentials — keys generated per-run
- No executable payloads — only synthetic metadata
- Fail-closed defaults in all policy gates

## Disclosure Timeline

- Acknowledgment: within 48 hours
- Assessment: within 7 days
- Fix and coordinated disclosure: case-by-case basis