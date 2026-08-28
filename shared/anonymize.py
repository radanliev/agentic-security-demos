"""Offline PII de-identification for the teaching demos.

Three techniques a class can read in a couple of minutes, all deterministic and
network-free (import only ``re`` and ``hashlib``):

* ``pseudonymize`` - replace an identifier with a stable pseudonym
  (``alice`` -> ``USER_7f3a``).  The same input always maps to the same
  pseudonym, so an analyst keeps the ability to *join* records ("USER_7f3a
  appears in frame 1 and frame 4") without learning who the person is.  The
  mapping is held in a local dict, so it is reversible on the machine that owns
  it and nowhere else.  This is the utility-preserving option.

* ``redact_secrets`` - mask values that have no analytic use at all - tokens,
  passwords, API keys - to ``[REDACTED]``.  Deny-by-default over a small set of
  known secret shapes: a secret is destroyed, not pseudonymized, because there
  is nothing to preserve.

* ``deidentify`` - run pseudonymization and redaction over a blob of text and
  return the scrubbed text together with a report of what changed, so the
  control is *observable*: the demo can print "2 usernames, 1 IP, 1 secret" and
  show the before/after.

The point for a lecture is the contrast between the three: you pseudonymize
what still has to be analysed, you redact what must simply disappear, and you
can always say exactly what you removed.

Everything here operates on synthetic fixtures only.  Real de-identification of
production data is harder (free text re-identifies, quasi-identifiers combine);
the demos state that limitation rather than hiding it.
"""

from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from typing import Dict, List, Tuple

# A fixed salt keeps pseudonyms stable across runs (byte-identical output) while
# still depending on the value, so two different names get two different tags.
_SALT = "agentic-security-demos/anonymize/v1"

REDACTION = "[REDACTED]"

# --- identifier patterns (pseudonymized: replaced by a stable tag) -----------
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+\-]+@[A-Za-z0-9.\-]+\.[A-Za-z]{2,}")
IPV4_RE = re.compile(r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b")
# A username in a named field: "user": "alice" / username=alice.  Only these
# named fields are treated as usernames - a bare word is not guessed at.
USER_FIELD_RE = re.compile(r'("(?:user|username|login|account)"\s*:\s*")([^"]{1,64})(")', re.I)
USER_KV_RE = re.compile(r"\b((?:user|username|login|account)\s*=\s*)([A-Za-z0-9._\-]{1,64})", re.I)

# --- secret patterns (redacted: value destroyed) -----------------------------
# Deny-by-default: only these shapes are treated as secrets.  Each rule captures
# the value in group 1 so we can replace just the value, not the whole key.
SECRET_RULES: List[Tuple[str, re.Pattern]] = [
    ("json_secret", re.compile(r'("(?:token|password|passwd|secret|api[_-]?key)"\s*:\s*")([^"]{4,})(")', re.I)),
    ("kv_secret", re.compile(r"\b((?:token|password|passwd|secret|api[_-]?key)\s*=\s*)([^\s,;&]{4,})", re.I)),
    # YAML / bare "key: value" secret (the JSON key is quoted, so this never
    # collides with json_secret); the value group excludes [] so a value already
    # replaced by [REDACTED] is not matched again.
    ("yaml_secret", re.compile(r"\b((?:token|password|passwd|secret|api[_-]?key)\s*:\s*['\"]?)([^'\"\s\]\[]{4,})", re.I)),
    ("bearer", re.compile(r"\b(Bearer\s+)([A-Za-z0-9_\-.]{8,})", re.I)),
    # URL userinfo password only: scheme://user:pass@host.  Scoped to the "@"
    # form so it can never mistake a host:port for a credential.
    ("userinfo_credential", re.compile(r"(://[A-Za-z0-9._\-]{1,64}:)([^\s:@/]{3,})(?=@)")),
]


def pseudonym(value: str, kind: str = "ID") -> str:
    """Return a stable pseudonym for ``value`` under a category ``kind``.

    Deterministic: the same (value, kind) always yields the same tag, so
    records still join.  Different values get different tags.
    """
    digest = hashlib.sha256(f"{_SALT}:{kind}:{value}".encode("utf-8")).hexdigest()[:4]
    return f"{kind}_{digest}"


@dataclass
class DeidReport:
    """Result of ``Anonymizer.deidentify``: the scrubbed text and what changed."""

    text: str
    changes: Dict[str, int] = field(default_factory=dict)

    @property
    def total(self) -> int:
        return sum(self.changes.values())

    def summary(self) -> str:
        if not self.changes:
            return "no identifiers or secrets found"
        parts = []
        labels = {"username": "usernames", "email": "emails", "ipv4": "IPs",
                  "hostname": "hostnames", "secret": "secrets"}
        for key in ("username", "email", "ipv4", "hostname", "secret"):
            if self.changes.get(key):
                parts.append(f"{self.changes[key]} {labels[key]}")
        for key, n in self.changes.items():
            if key not in labels and n:
                parts.append(f"{n} {key}")
        return ", ".join(parts)


class Anonymizer:
    """Holds the pseudonym map so tags stay consistent (and locally reversible)
    across every value it sees.  One Anonymizer per analysis keeps a stable
    view; a fresh one starts a fresh namespace."""

    def __init__(self) -> None:
        self._map: Dict[str, str] = {}      # original -> pseudonym
        self._reverse: Dict[str, str] = {}  # pseudonym -> original

    # -- pseudonymization -----------------------------------------------------
    def pseudonymize(self, value: str, kind: str = "ID") -> str:
        key = f"{kind}:{value}"
        if key not in self._map:
            tag = pseudonym(value, kind)
            self._map[key] = tag
            self._reverse[tag] = value
        return self._map[key]

    def reverse(self, tag: str) -> str:
        """Recover the original for a pseudonym this Anonymizer minted.

        Only works locally - the map never leaves the machine, which is the
        whole point of holding it here rather than in the scrubbed record.
        """
        return self._reverse.get(tag, tag)

    def email(self, addr: str) -> str:
        return self.pseudonymize(addr, "EMAIL")

    def ip(self, addr: str) -> str:
        return self.pseudonymize(addr, "HOST")

    def username(self, name: str) -> str:
        return self.pseudonymize(name, "USER")

    # -- redaction ------------------------------------------------------------
    @staticmethod
    def redact_secrets(text: str) -> Tuple[str, int]:
        """Mask known secret shapes.  Returns (masked_text, count)."""
        n = 0

        def repl(match: "re.Match") -> str:
            nonlocal n
            n += 1
            groups = match.groups()
            if len(groups) == 3:                       # json_secret: key + value + close
                return groups[0] + REDACTION + groups[2]
            return groups[0] + REDACTION               # kv/bearer/colon: prefix + value

        for _name, pattern in SECRET_RULES:
            text = pattern.sub(repl, text)
        return text, n

    # -- combined -------------------------------------------------------------
    def deidentify(self, text: str) -> DeidReport:
        """Redact secrets, then pseudonymize the identifiers that remain.

        Order matters: redact first so a token that happens to look like an
        e-mail local part is destroyed rather than pseudonymized.
        """
        changes: Dict[str, int] = {}
        text, n_secret = self.redact_secrets(text)
        if n_secret:
            changes["secret"] = n_secret

        def sub_user_field(m: "re.Match") -> str:
            changes["username"] = changes.get("username", 0) + 1
            return m.group(1) + self.username(m.group(2)) + m.group(3)

        def sub_user_kv(m: "re.Match") -> str:
            changes["username"] = changes.get("username", 0) + 1
            return m.group(1) + self.username(m.group(2))

        text = USER_FIELD_RE.sub(sub_user_field, text)
        text = USER_KV_RE.sub(sub_user_kv, text)

        def sub_email(m: "re.Match") -> str:
            changes["email"] = changes.get("email", 0) + 1
            return self.email(m.group(0))

        def sub_ip(m: "re.Match") -> str:
            changes["ipv4"] = changes.get("ipv4", 0) + 1
            return self.ip(m.group(0))

        text = EMAIL_RE.sub(sub_email, text)
        text = IPV4_RE.sub(sub_ip, text)
        return DeidReport(text=text, changes=changes)


# ---------------------------------------------------------------------------
# Allowlist redaction - deny-by-default over the FIELDS of a record.
# ---------------------------------------------------------------------------

def redact_record(record: Dict, allow: List[str], mask: str = "[PII-REDACTED]") -> Tuple[Dict, List[str]]:
    """Keep only the allowlisted keys of ``record`` in the clear; replace every
    other key's value with ``mask``.  Returns (redacted_record, removed_keys).

    Deny-by-default: a field is exposed only if it is named in ``allow``, so a
    new metadata field a class has never seen is masked, not leaked.  This is
    the pattern the RAID triage proxy uses on VirusTotal responses.
    """
    allowed = set(allow)
    out: Dict = {}
    removed: List[str] = []
    for key, value in record.items():
        if key in allowed:
            out[key] = value
        else:
            out[key] = mask
            removed.append(key)
    return out, removed
