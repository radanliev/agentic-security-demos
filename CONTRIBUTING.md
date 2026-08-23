# Contributing to Agentic Security Demos

Thank you for improving these teaching materials! This project follows a standard GitHub workflow.

## Ways to Contribute

- **Fix bugs** in starter code, tests, or fixtures
- **Improve explanations** in READMEs or docstrings
- **Add exercises** at beginner/standard/extension levels
- **Enhance reproducibility** (better seeds, environment capture)
- **Add new demos** following the established pattern
- **Fix typos** and formatting

## Pull Request Process

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b improve-demo-03-readme`
3. **Make your changes** following the style guide below
4. **Run tests locally**: `make test` (must pass)
5. **Ensure safety compliance**: `make verify-safety` (must pass)
6. **Submit a PR** with a clear description

## Code Style

- **Python**: Follow PEP 8, use type hints (`mypy` clean)
- **Keep functions small** and focused (single responsibility)
- **Document public APIs** with docstrings (Google style)
- **Use `snake_case`** for functions/variables, `PascalCase` for classes
- **No global state** — prefer dependency injection

## Safety Requirements

Every contribution must maintain:
- **Zero network access** in tests and demos
- **No real credentials** — only generated demo keys
- **No executable malware** — synthetic fixtures only
- **Clear safety notices** in each demo README
- **Standardized result schema** for all demos

## Adding a New Demo

1. Create `demo-XX-name/` following the standard structure:
   ```
   demo-XX-name/
   ├── README.md          # Learning objectives, explanation, safety notice
   ├── fixtures/          # Synthetic input data (JSON/YAML)
   ├── student/           # Starter code with TODO comments
   ├── tests/             # Visible correctness tests (pytest)
   ├── results/           # Generated output (gitignored)
   ├── solutions/         # Instructor-only (excluded from public repo)
   ├── Makefile           # setup, test, demo, clean
   └── pyproject.toml     # Optional demo-specific deps
   ```
2. Add to root `Makefile` demo targets
3. Add CI test entry in `.github/workflows/ci.yml`
4. Update root `README.md` demo table
5. Ensure `make verify-safety` passes

## Demo Structure Checklist

- [ ] `README.md` with learning objectives, conceptual explanation, safety notice, reproducibility metadata
- [ ] `fixtures/` with synthetic data only (no real data)
- [ ] `student/` with starter code + exercise TODOs
- [ ] `tests/` with beginner/standard/extension exercises
- [ ] `results/` directory (created at runtime)
- [ ] `Makefile` with `setup`, `test`, `demo`, `clean`
- [ ] Beginner, standard, and extension exercises
- [ ] Clear safety notice
- [ ] Reproducibility metadata (seed, commit, environment, command)

## Code Review Criteria

PRs are evaluated on:
- Educational clarity and correctness
- Safety compliance (zero network, no credentials, synthetic only)
- Test coverage and determinism
- Reproducibility metadata completeness
- Consistency with existing demos
- Code quality and style

## Reporting Issues

- **Bug reports**: Use the bug report template
- **Feature requests**: Use the feature request template
- **Security issues**: See [SECURITY.md](SECURITY.md) — do not open public issues

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.