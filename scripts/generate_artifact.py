import json
import hashlib
import os

INPUT_FILE = "data/sample_decisions.json"
OUTPUT_FILE = "artifacts/example_artifact.json"

def canonicalize(data):
    return json.dumps(data, sort_keys=True).encode()

def generate_hash(data):
    return hashlib.sha256(data).hexdigest()

def main():

    with open(INPUT_FILE) as f:
        decisions = json.load(f)

    artifact = {
        "artifact_version": "1.0",
        "records": decisions
    }

    canonical = canonicalize(artifact)
    digest = generate_hash(canonical)

    sealed_artifact = {
        "artifact": artifact,
        "sha256_digest": digest
    }

    os.makedirs("artifacts", exist_ok=True)

    with open(OUTPUT_FILE, "w") as f:
        json.dump(sealed_artifact, f, indent=2)

    print("Artifact generated")
    print("SHA256:", digest)

if __name__ == "__main__":
    main()
