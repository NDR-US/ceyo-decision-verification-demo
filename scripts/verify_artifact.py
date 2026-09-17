"""Verify a CEYO decision-verification demo artifact.

The demo delegates verification to the canonical public CEYO reference
implementation so the demonstration cannot drift into a separate protocol.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from ceyo import verify_artifact

ARTIFACT_FILE = "artifacts/example_artifact.json"
PUBLIC_KEY_FILE = "artifacts/example_public_key.pem"


def main() -> None:
    artifact_file = sys.argv[1] if len(sys.argv) > 1 else ARTIFACT_FILE
    public_key_file = sys.argv[2] if len(sys.argv) > 2 else PUBLIC_KEY_FILE

    artifact = json.loads(Path(artifact_file).read_text(encoding="utf-8"))
    public_key_pem = Path(public_key_file).read_bytes()

    result = verify_artifact(artifact, public_key_pem)

    for message in result.passed:
        print("PASS:", message)

    if not result.ok:
        for message in result.failed:
            print("FAIL:", message)
        raise SystemExit(1)

    print("Verification PASSED")


if __name__ == "__main__":
    main()
