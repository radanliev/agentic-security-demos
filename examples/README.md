# Cross-Demo Examples

This directory contains examples that span multiple demos.

## Example: Full Pipeline

Combining blind verification (01) with evidence assurance (05):

```python
# Pseudocode for integrated workflow
agent = VerifiedAgent(scenarios)
commitments = agent.commit_all()
evidence = EvidencePipeline().record(commitments)
ReleaseGate().verify(evidence)
```

See individual demo `student/` directories for starter code.