import json
import hashlib

ARTIFACT_FILE = "artifacts/example_artifact.json"

def canonicalize(data):
    return json.dumps(data, sort_keys=True).encode()

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def main():

    with open(ARTIFACT_FILE) as f:
        artifact = json.load(f)

    original_digest = artifact["sha256_digest"]

    canonical = canonicalize(artifact["artifact"])
    recalculated_digest = sha256(canonical)

    if recalculated_digest == original_digest:
        print("PASS: artifact integrity verified")
    else:
        print("FAIL: artifact was modified")

if __name__ == "__main__":
    main()
