# Data sources (retrieved 2026-10-26)

All data below is real public data. Nothing here is simulated. The existing fixtures/ remain synthetic teaching fixtures and are labelled as such in the demo README.

| Source | URL | Licence | Local file |
|---|---|---|---|
| NVD CVE API 2.0, query keywordSearch="prompt injection" | https://services.nvd.nist.gov/rest/json/cves/2.0 | Public domain US Government data; NVD notice: "This product uses the NVD API but is not endorsed or certified by the NVD." | raw/nvd_prompt_injection.json |

Re-fetch with `bash data/fetch_data.sh`. NVD queries are rate-limited (unauthenticated, 6 s spacing). Snapshots may differ from a later re-fetch as the feeds are live.
