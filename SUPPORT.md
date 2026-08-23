# Support

## Getting Help

### Documentation
- **Root README**: Overview, quick start, repository structure
- **Demo READMEs**: Each demo has detailed learning objectives and explanations
- **docs/**: Additional documentation
- **Makefile help**: Run `make help` for available commands

### Community Support
- **GitHub Discussions**: Ask questions, share ideas, get help
- **GitHub Issues**: Report bugs, request features

## Reporting Issues

### Bug Reports
Use the [Bug Report template](.github/ISSUE_TEMPLATE/bug_report.yml):
- Clear description of the problem
- Steps to reproduce
- Environment details (Python version, OS)
- Error output/logs
- Safety check confirmation

### Feature Requests
Use the [Feature Request template](.github/ISSUE_TEMPLATE/feature_request.yml):
- Clear description of the proposed feature
- Educational motivation/value
- Safety considerations

### Documentation Issues
Use the [Documentation template](.github/ISSUE_TEMPLATE/documentation.yml):
- Location of the issue
- What's unclear/missing/incorrect
- Suggested improvement

## Security Vulnerabilities

**Do NOT open public issues for security vulnerabilities.**

See [SECURITY.md](SECURITY.md) for responsible disclosure process.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Code style guidelines
- Pull request process
- Safety requirements
- Adding new demos

## Response Times

- **Bug reports**: Initial response within 48 hours
- **Feature requests**: Initial response within 1 week
- **Security issues**: Acknowledgment within 48 hours
- **Documentation**: Initial response within 1 week

## Community Guidelines

- Be respectful and constructive
- Follow the [Code of Conduct](CODE_OF_CONDUCT.md)
- Assume good intent
- Focus on educational value and safety
- Credit sources appropriately

## Commercial Support

This project is maintained by volunteers for educational purposes.
For commercial support or custom training materials, contact:
maintainers@agentic-security-demos.example (placeholder)

## FAQ

**Q: Can I use these demos in my course?**
A: Yes! These are designed for educational use. Please cite appropriately.

**Q: Are these demos safe to run?**
A: Yes. All demos use synthetic fixtures only — no network access, no real credentials, no malware.

**Q: Can I add a new demo?**
A: Yes! Follow the pattern in CONTRIBUTING.md and maintain safety guarantees.

**Q: Why do tests fail with "network access"?**
A: Our CI blocks any test that imports network libraries. Check for accidental imports.

**Q: How do I cite this work?**
A: See CITATION.cff for citation metadata in multiple formats.