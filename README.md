# CEYO Decision Verification Demo

**Minimal demonstration of the canonical CEYO evidentiary workflow**

**Created and led by Brian Covarrubias**  
**Copyright © 2026 Brian Covarrubias. All rights reserved.**

This repository demonstrates how structured AI-assisted decision records can be transformed into deterministic, cryptographically verifiable CEYO artifacts and later checked independently of the originating system.

It is a **demonstration layer**, not a separate CEYO protocol implementation.

The canonical protocol, schemas, cryptographic profile, and reference verifier are maintained in:

- `NDR-US/ceyo-protocol`

## Why this repository exists

The demo answers one narrow question:

> How can a structured decision record be sealed into a tamper-evident artifact that a later reviewer can independently verify without access to model weights or proprietary system internals?

The demonstration is intentionally small so the evidence lifecycle remains understandable.

## Canonical profile used by the demo

The demo consumes the current public CEYO reference implementation rather than defining its own cryptography.

Current profile:

```text
policy-scoped structured record
        ↓
RFC 8785 canonicalization
        ↓
SHA-256 digest
        ↓
ECDSA P-256 / SHA-256 signature
        ↓
CEYO artifact envelope
        ↓
independent verification
```

This avoids cryptographic drift between the demo and the protocol repository.

## What the demo demonstrates

- structured event capture;
- declared policy context;
- canonical CEYO artifact generation;
- deterministic hashing;
- digital signing;
- public-key fingerprint binding;
- independent schema/hash/signature verification;
- detection of post-sealing modification.

## What the demo does not claim

The demo does not determine:

- whether an AI decision is correct;
- whether it is fair or unbiased;
- whether source data was truthful or complete before capture;
- whether an organization is legally compliant;
- whether a local timestamp is independently trusted time;
- whether an artifact is legally admissible or sufficient in a particular proceeding.

CEYO verifies explicitly defined evidence properties; it does not replace adjudication or institutional judgment.

## Example decision data

The sample dataset contains simplified operational records such as:

- decision identifier;
- event timestamp;
- source system;
- decision output;
- confidence score;
- recommended action.

The generated CEYO body also declares a demonstration capture policy and disclosure tier.

## Repository structure

```text
ceyo-decision-verification-demo/
├── README.md
├── data/
│   └── sample_decisions.json
├── scripts/
│   ├── generate_artifact.py
│   └── verify_artifact.py
├── artifacts/
│   ├── example_artifact.json
│   └── example_public_key.pem
├── requirements.txt
└── license
```

## Quick start

Install the canonical CEYO reference implementation and dependencies:

```bash
pip install -r requirements.txt
```

Generate a CEYO artifact:

```bash
python scripts/generate_artifact.py data/sample_decisions.json
```

Verify it independently using the public key:

```bash
python scripts/verify_artifact.py \
  artifacts/example_artifact.json \
  artifacts/example_public_key.pem
```

Expected verification covers the artifact schema, canonical digest, ECDSA P-256 signature, and public-key fingerprint.

## Architecture boundary

This repository must not introduce its own:

- artifact schema;
- canonicalization algorithm;
- digest algorithm;
- signature suite;
- verification semantics.

If the canonical CEYO profile changes, the demo should consume the updated versioned profile rather than creating an independent fork.

## Current vs target CEYO architecture

This demo represents the current public reference profile only.

The broader CEYO target architecture includes planned work around protected policy/schema context, authenticated trust registries, trusted-time evidence, hardware-backed key custody, revocation, transparency witnesses, conformance suites, custody, and constrained disclosure.

Those future capabilities are defined and tracked in the canonical protocol and private R&D repositories; they are not implied by this minimal demonstration unless explicitly implemented.

## Authorship and intellectual property

CEYO was conceived and is directed by **Brian Covarrubias**. This demonstration is published through the NDR-US GitHub identity.

See `license` for repository terms.
