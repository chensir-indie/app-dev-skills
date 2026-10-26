#!/usr/bin/env python3
"""Offline release proposal and artifact hash checks; never contacts a store."""
import argparse
from datetime import datetime, timedelta, timezone
import hashlib
import hmac
import json
from pathlib import Path
import re
import sys


class EvidenceError(ValueError):
    """An evidence input cannot establish the requested local check."""


VERSION = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\Z")
SHA256 = re.compile(r"[0-9a-fA-F]{64}\Z")
REQUIRED = ("bundle_id", "platform", "observed_at", "public_version",
            "latest_uploaded_version", "highest_uploaded_build")


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise EvidenceError("Duplicate JSON keys are ambiguous; provide one value per field.")
        result[key] = value
    return result


def version_tuple(value, field):
    if not isinstance(value, str) or VERSION.fullmatch(value) is None:
        raise EvidenceError(f"{field} must be an exact A.B.C version with no prerelease suffix.")
    return tuple(int(part) for part in value.split("."))


def make_plan(baseline, now=None):
    if not isinstance(baseline, dict):
        raise EvidenceError("Baseline must be a JSON object.")
    missing = [field for field in REQUIRED if field not in baseline]
    if missing:
        raise EvidenceError("Missing baseline fields: " + ", ".join(missing))
    if not isinstance(baseline["bundle_id"], str) or not baseline["bundle_id"].strip():
        raise EvidenceError("bundle_id must be a nonempty string.")
    if baseline["platform"] not in ("ios", "android"):
        raise EvidenceError("platform must be ios or android.")
    observed = baseline["observed_at"]
    if not isinstance(observed, str):
        raise EvidenceError("observed_at must be an ISO 8601 timestamp including its timezone.")
    try:
        parsed = datetime.fromisoformat(observed.replace("Z", "+00:00"))
    except ValueError as exc:
        raise EvidenceError("observed_at must be an ISO 8601 timestamp including its timezone.") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise EvidenceError("observed_at needs a timezone; a local wall-clock time is ambiguous.")
    now = now or datetime.now(timezone.utc)
    age = now - parsed
    if age > timedelta(minutes=30):
        raise EvidenceError("Baseline is older than 30 minutes; obtain a fresh authenticated store read.")
    if age < -timedelta(seconds=60):
        raise EvidenceError("Baseline is in the future by more than 60 seconds; correct its timestamp.")
    public = version_tuple(baseline["public_version"], "public_version")
    uploaded = version_tuple(baseline["latest_uploaded_version"], "latest_uploaded_version")
    highest = baseline["highest_uploaded_build"]
    if type(highest) is not int or highest < 1:
        raise EvidenceError("highest_uploaded_build must be an integer >= 1 across all version trains.")
    if uploaded < public:
        raise EvidenceError("Latest uploaded version is older than public; reconcile the store baseline first.")
    if uploaded == public:
        candidate = (public[0], public[1], public[2] + 1)
        decision = "patch_public"
    else:
        candidate = uploaded
        decision = "reuse_testing"
    return {
        "schema": "app-publish-proposal-v1",
        "status": "PROPOSAL_ONLY",
        "limitations": "Offline calculation only. Not an authenticated store read, authorization, source/artifact validation, or release preflight.",
        "bundle_id": baseline["bundle_id"],
        "platform": baseline["platform"],
        "baseline_observed_at": observed,
        "public_version": baseline["public_version"],
        "latest_uploaded_version": baseline["latest_uploaded_version"],
        "highest_uploaded_build": highest,
        "candidate_version": ".".join(str(part) for part in candidate),
        "candidate_build": highest + 1,
        "decision": decision,
        "created_at": now.astimezone(timezone.utc).isoformat(),
    }


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan", help="Calculate a proposal from a normalized fresh baseline.")
    plan.add_argument("--baseline", type=Path, required=True)
    plan.add_argument("--output", type=Path, required=True)
    plan.add_argument("--overwrite", action="store_true", help="Explicitly replace an existing proposal file.")
    artifact = commands.add_parser("verify-artifact", help="Verify bytes against a previously recorded SHA-256.")
    artifact.add_argument("--artifact", type=Path, required=True)
    artifact.add_argument("--expected-sha256", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "plan":
            if args.baseline.resolve() == args.output.resolve():
                raise EvidenceError("Output must differ from the raw baseline; preserve the evidence input.")
            raw = args.baseline.read_bytes()
            baseline = json.loads(raw, object_pairs_hook=unique_object)
            proposal = make_plan(baseline)
            proposal["baseline_sha256"] = hashlib.sha256(raw).hexdigest()
            with args.output.open("w" if args.overwrite else "x", encoding="utf-8") as output:
                output.write(json.dumps(proposal, ensure_ascii=False, indent=2) + "\n")
            print("PROPOSAL_ONLY: saved offline version/build proposal; project release gates remain required.")
        else:
            if SHA256.fullmatch(args.expected_sha256) is None:
                raise EvidenceError("Expected SHA-256 must contain exactly 64 hexadecimal characters.")
            actual = file_sha256(args.artifact)
            if not hmac.compare_digest(actual, args.expected_sha256.lower()):
                raise EvidenceError("Artifact SHA-256 mismatch; preserve this artifact and reconcile its identity before continuing.")
            print(json.dumps({"status": "HASH_MATCH", "sha256": actual,
                              "limitations": "Byte identity only; package contents, signature and provider state are not checked."}))
    except FileExistsError:
        print("FAIL: proposal output already exists; use a new path or explicitly pass --overwrite.", file=sys.stderr)
        return 1
    except (OSError, UnicodeError, json.JSONDecodeError, EvidenceError) as exc:
        # JSONDecodeError's message can quote untrusted input; do not print it.
        message = "Invalid JSON; provide one normalized baseline object." if isinstance(exc, json.JSONDecodeError) else str(exc)
        print("FAIL: " + message, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    if sys.version_info < (3, 9):
        sys.exit("Python 3.9+ is required; install a supported Python and rerun this helper.")
    sys.exit(main())
