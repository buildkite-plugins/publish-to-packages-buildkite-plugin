from typing import Dict


def fake_env() -> Dict[str, str]:
    return {
        "BUILDKITE_ORGANIZATION_SLUG": "acme-corp",
    }
