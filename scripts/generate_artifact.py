import json
import hashlib
import os
import sys
import base64

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding

INPUT_FILE = "data/sample_decisions.json"
OUTPUT_ARTIFACT = "artifacts/example_artifact.json"
OUTPUT_SIGNATURE = "artifacts/example_signature.json"


def canonicalize(data):
    return json.dumps(data, sort_keys=True, separators=(",", ":")).encode()


def generate_hash(data):
    return hashlib.sha256(data).hexdigest()


def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    return private_key, private_key.public_key()


def sign_digest(private_key, digest_hex):
    signature = private_key.sign(
        digest_hex.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH,
        ),
        hashes.SHA256(),
    )
    return base64.b64encode(signature).decode()


def export_public_key(public_key):
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode()


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else INPUT_FILE

    with open(input_file) as f:
        decisions = json.load(f)

    artifact = {
        "artifact_version": "1.0",
        "records": decisions,
    }

    canonical = canonicalize(artifact)
    digest = generate_hash(canonical)

    private_key, public_key = generate_key_pair()
    signature_b64 = sign_digest(private_key, digest)
    public_key_pem = export_public_key(public_key)

    sealed_artifact = {
        "artifact": artifact,
        "sha256_digest": digest,
        "public_key_pem": public_key_pem,
    }

    signature_record = {
        "sha256_digest": digest,
        "signature_algorithm": "RSA-PSS-SHA256",
        "signature_b64": signature_b64,
    }

    os.makedirs("artifacts", exist_ok=True)

    with open(OUTPUT_ARTIFACT, "w") as f:
        json.dump(sealed_artifact, f, indent=2)

    with open(OUTPUT_SIGNATURE, "w") as f:
        json.dump(signature_record, f, indent=2)

    print("Artifact generated:", OUTPUT_ARTIFACT)
    print("Signature written:", OUTPUT_SIGNATURE)
    print("SHA256:", digest)


if __name__ == "__main__":
    main()
