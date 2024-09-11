import argparse


class CliArguments:
    def __init__(self, organization_slug: str) -> None:
        self.organization_slug = organization_slug.strip()
        parser = argparse.ArgumentParser(
            prog="python3 main.py",
            description="Publishes files to Packages",
            epilog="Have a nice day!",
        )
        parser.add_argument("--registry", default="")
        parser.add_argument("--artifacts-dir", default="")
        parser.add_argument("--provenance-bundle", default="")

        self.arguments = parser.parse_args()

    def get_registry(self) -> str:
        registry = str(self.arguments.registry).strip()
        if registry.find("/") == -1:
            registry = "{}/{}".format(self.organization_slug, registry)
        return registry

    def get_artifacts_dir(self) -> str:
        return str(self.arguments.artifacts_dir).strip()

    def get_provenance_bundle(self) -> str:
        return str(self.arguments.provenance_bundle).strip()
