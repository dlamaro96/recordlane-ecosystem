# Recordlane ecosystem

The open connector authoring kit, isolated connector template, six versioned domain packs, and integration recipes for Recordlane. Recipe status is deliberately explicit: none of the vendor recipes in this alpha was live-vendor validated because customer credentials were not available. The tiny JSONL connector is conformance-tested.

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e '.[test]'
pytest
./scripts/sync_domain_packs.sh ../recordlane
```

Third-party connectors run outside the core API process with scoped credentials and destination allowlists. Passing conformance proves contract behavior; it does not make code safe or certify a vendor integration.
