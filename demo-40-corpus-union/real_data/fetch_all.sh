#!/bin/sh
# Re-download the four public corpora used by analyse.py (raw files are not committed).
set -e
cd "$(dirname "$0")"
for s in train test; do python3 fetch.py deepset/prompt-injections $s deepset_$s.jsonl; python3 fetch.py jackhhao/jailbreak-classification $s jackhhao_$s.jsonl; done
for s in train validation test; do python3 fetch.py Lakera/gandalf_ignore_instructions $s lakera_$s.jsonl; done
python3 fetch.py rubend18/ChatGPT-Jailbreak-Prompts train rubend18_train.jsonl
