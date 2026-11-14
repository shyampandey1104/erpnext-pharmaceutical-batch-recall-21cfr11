# ERPNext Pharmaceutical Batch Recall & FDA 21 CFR Part 11 Engine

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![FDA](https://img.shields.io/badge/Compliance-FDA%2021%20CFR%20Part%2011-red.svg)](https://www.fda.gov)

Enterprise pharmaceutical manufacturing compliance engine providing SHA-256 electronic signatures, dual-custody Quality Assurance release, and instant mock/mandatory forward-backward drug recall trace audit.

## Key Capabilities
- **21 CFR Part 11 E-Signatures:** Immutable digital signature hashes verifying signer identity, timestamp, and QA verdict.
- **Forward & Backward Batch Recall:** Instantaneous trace linking warehouse quarantined stock to dispatched hospital/pharmacy invoices.
- **Genealogy & Audit Trail:** End-to-end reconciliation proving 100% containment of affected finished vials.

## Tests
```bash
python3 -m unittest discover tests
```
