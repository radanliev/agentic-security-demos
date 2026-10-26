#!/usr/bin/env bash
# Re-fetch the real public data used by analysis/analyse.py. Run from the demo folder.
set -euo pipefail; mkdir -p data/raw; cd data/raw
curl -sL -o kev.json https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json
for s in train test; do
 curl -sL -o pi_$s.parquet https://huggingface.co/api/datasets/deepset/prompt-injections/parquet/default/$s/0.parquet
 curl -sL -o jb_$s.parquet https://huggingface.co/api/datasets/jackhhao/jailbreak-classification/parquet/default/$s/0.parquet
done
P=../nvd_fetch.py
python3 $P nvd_prompt_injection.json 'keywordSearch=prompt injection'; sleep 6
python3 $P nvd_vuln_scanner.json 'keywordSearch=vulnerability scanner'; sleep 6
python3 $P nvd_calendar_injection.json 'keywordSearch=calendar injection'; sleep 6
for c in CWE-22 CWE-98 CWE-295 CWE-300 CWE-1427 CWE-77; do python3 $P nvd_tot_$c.json cweId=$c totals_only=1; sleep 6; done
