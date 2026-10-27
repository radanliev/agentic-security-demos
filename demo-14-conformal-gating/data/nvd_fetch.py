"""Fetch CVE records from the NVD CVE API 2.0 (public, unauthenticated).
This product uses the NVD API but is not endorsed or certified by the NVD.
Usage: python nvd_fetch.py OUT.json key=value [key=value...]   (e.g. keywordSearch="prompt injection" or cweId=CWE-22)
Pass totals_only=1 to record only totalResults."""
import json, sys, time, urllib.parse, urllib.request, datetime
API = "https://services.nvd.nist.gov/rest/json/cves/2.0"
def get(params):
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(5):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "research-fetch"}), timeout=60) as r:
                return json.load(r)
        except Exception as e:
            time.sleep(8 * (attempt + 1))
    raise SystemExit("NVD fetch failed: " + url)
def main():
    out = sys.argv[1]; params = dict(a.split("=", 1) for a in sys.argv[2:])
    totals_only = params.pop("totals_only", None)
    meta = {"source": API, "params": params, "retrieved_utc": datetime.datetime.utcnow().isoformat(timespec="seconds") + "Z",
            "notice": "This product uses the NVD API but is not endorsed or certified by the NVD."}
    if totals_only:
        d = get({**params, "resultsPerPage": 1}); meta["totalResults"] = d["totalResults"]; json.dump(meta, open(out, "w"), indent=1); return
    vulns, start = [], 0
    while True:
        d = get({**params, "resultsPerPage": 2000, "startIndex": start})
        vulns += d["vulnerabilities"]; start += d["resultsPerPage"]
        if start >= d["totalResults"] or not d["vulnerabilities"]: break
        time.sleep(6)
    meta["totalResults"] = len(vulns); meta["vulnerabilities"] = vulns
    json.dump(meta, open(out, "w"))
if __name__ == "__main__": main()
