# Results: keyword screening of 60 public model cards

Command: `python3 fetch_and_code.py`. Outputs: `cards_coded.json`, `results.json`.

| Obligation | Cards with a matching keyword (n = 60) |
|---|---|
| threats | 17 |
| evals | 56 |
| agentic | 40 |
| third_party | 6 (weakest) |
| mitigations | 11 |
| all five | 3 |

Reading. On real, widely downloaded model cards the ordering seen in the synthetic toy holds for the weakest obligation: third-party evaluation is mentioned least often. Evaluation language is near universal, but this is mostly benchmark tables. These are keyword hits, not coded claims. A hit for "agent" can be a chat-template note, and a hit for "third-party" can refer to software rather than evaluation. The FAccT study still needs the present/absent/vague codebook, double coding and a reliability figure; this pass only shows the corpus is reachable and gives a first screening.

Note: Hugging Face model cards are not the same artefact as frontier-lab system cards. They are a complementary public corpus, not a substitute for the planned sample.
