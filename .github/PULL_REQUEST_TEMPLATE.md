# Pull Request Template

## Description

Brief description of changes:

## Type of Change

- [ ] Bug fix
- [ ] New exercise (beginner/standard/extension)
- [ ] Documentation improvement
- [ ] Test improvement
- [ ] Reproducibility enhancement
- [ ] Safety improvement
- [ ] New demo module
- [ ] Refactoring (no functional change)

## Affected Demo(s)

- [ ] demo-01-blind-verification
- [ ] demo-02-supply-chain-aibom
- [ ] demo-03-eval-invariants
- [ ] demo-04-authoritybound
- [ ] demo-05-eviassure
- [ ] demo-06-reconscope
- [ ] demo-07-triagetrap
- [ ] demo-08-inclusiontrap
- [ ] demo-09-interceptbound
- [ ] demo-10-scanbound
- [ ] Root / Shared / CI

## Checklist

- [ ] `make test` passes locally
- [ ] `make verify-safety` passes locally
- [ ] No network access in tests or demos
- [ ] No real credentials or API keys
- [ ] Only synthetic fixtures used
- [ ] Safety notices present in modified demo READMEs
- [ ] Standardized result schema maintained
- [ ] Tests added/updated for changes
- [ ] Documentation updated (README, docstrings, etc.)
- [ ] Beginner/standard/extension exercises included (if adding features)
- [ ] Reproducibility metadata: seed, commit, environment, command

## Testing

Describe how you tested your changes:

```bash
# Commands run
make test
make verify-safety
make demo DEMO=XX
```

## Screenshots / Output (if applicable)

Paste relevant test output or demo results:

## Related Issues

Closes #

## Safety Review

- [ ] No network access added
- [ ] No credentials or API keys added
- [ ] No executable code or malware added
- [ ] All fixtures are synthetic
- [ ] Safety notices present