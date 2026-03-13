import json
import hashlib
import sys
import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

ARTIFACT_FILE = "artifacts/example_artifact.json"
SIGNATURE_FILE = "artifacts/example_signature.json"


def canonicalize(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode()


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def main():
    artifact_file = sys.argv[1] if len(sys.argv) > 1 else ARTIFACT_FILE
    signature_file = sys.argv[2] if len(sys.argv) > 2 else SIGNATURE_FILE

    with open(artifact_file) as f:
        sealed = json.load(f)

    with open(signature_file) as f:
        sig_record = json.load(f)

    original_digest = sealed["sha256_digest"]
    public_key_pem = sealed["public_key_pem"]

    canonical = canonicalize(sealed["artifact"])
    recalculated_digest = sha256(canonical)

    if recalculated_digest != original_digest:
        print("FAIL: artifact content was modified")
        sys.exit(1)

    if sig_record["sha256_digest"] != original_digest:
        print("FAIL: signature digest does not match artifact digest")
        sys.exit(1)

    public_key = serialization.load_pem_public_key(public_key_pem.encode())
    signature = base64.b64decode(sig_record["signature_b64"])

    try:
        public_key.verify(
            signature,
            original_digest.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH,
            ),
            hashes.SHA256(),
        )
        print("PASS: artifact integrity and signature verified")
    except InvalidSignature:
        print("FAIL: signature is invalid")
        sys.exit(1)


if __name__ == "__main__":
    main()
