"""Generate a CEYO decision-verification demo artifact.

This demo intentionally consumes the canonical public CEYO reference
implementation instead of defining a separate cryptographic profile.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

from ceyo import seal_body
from ceyo.keys import InMemoryKeyProvider

INPUT_FILE = "data/sample_decisions.json"
OUTPUT_ARTIFACT = "artifacts/example_artifact.json"
OUTPUT_PUBLIC_KEY = "artifacts/example_public_key.pem"


def main() -> None:
    input_file = sys.argv[1] if len(sys.argv) > 1 else INPUT_FILE

    with open(input_file, encoding="utf-8") as f:
        decisions = json.load(f)

    body = {
        "event": {
            "event_id": "demo_batch_001",
            "type": "decision_batch",
            "occurred_at": "2026-03-06T18:12:00Z",
        },
        "policy": {
            "id": "demo.capture.minimum",
            "version": "1.0",
        },
        "disclosure_tier": "public-demo",
        "capture": {
            "records": decisions,
        },
    }

    key_provider = InMemoryKeyProvider()
    envelope = seal_body(body, key_provider=key_provider, validate=True)
    public_key_pem = key_provider.get_public_key_pem()

    os.makedirs("artifacts", exist_ok=True)
    Path(OUTPUT_ARTIFACT).write_text(
        json.dumps(envelope, indent=2) + "\n",
        encoding="utf-8",
    )
    Path(OUTPUT_PUBLIC_KEY).write_bytes(public_key_pem)

    print("CEYO artifact generated:", OUTPUT_ARTIFACT)
    print("Public verification key written:", OUTPUT_PUBLIC_KEY)
    print("Artifact ID:", envelope["artifact_id"])
    print("Suite:", envelope["integrity"]["sig"]["alg"])
    print("Canonicalization:", envelope["canonicalization"]["scheme"])


if __name__ == "__main__":
    main()
