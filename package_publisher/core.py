import json
import subprocess
from typing import Any


class PackagePublisher:
    def __init__(
        self, registry: str, attestation_bundle_path: str | None = None
    ) -> None:
        (self.organization_slug, self.registry_slug) = registry.split("/")
        self.attestation_bundle_path = attestation_bundle_path

    def upload_package(self, file_path: str) -> Any:
        url = "https://api.buildkite.com/v2/packages/organizations/{}/registries/{}/packages".format(
            self.organization_slug, self.registry_slug
        )

        command: list[str] = ["curl"]
        command += ["--fail-with-body", "--silent"]
        command += [
            "--header",
            "Authorization: Bearer {}".format(self.get_token()),
        ]
        command += ["--form", "file=@{}".format(file_path)]
        command += (
            [
                "--form",
                "attestation_bundle=@{}".format(self.attestation_bundle_path),
            ]
            if self.attestation_bundle_path is not None
            else []
        )
        command += [url]

        try:
            result = subprocess.run(command, capture_output=True, check=True, text=True)
            return json.loads(str(result.stdout))
        except subprocess.CalledProcessError as error:
            print("")
            print("ERROR: PackagePublisher.upload_package failed to execute curl")
            print("returncode: {}".format(error.returncode))
            print("stdout: {}".format(error.stdout))
            print("stderr: {}".format(error.stderr))
            exit(1)

    def get_token(self) -> str:
        audience = "https://packages.buildkite.com/{}/{}".format(
            self.organization_slug, self.registry_slug
        )
        command: list[str] = ["buildkite-agent", "oidc", "request-token"]
        command += ["--audience", audience]
        command += ["--lifetime", "300"]

        response = subprocess.run(
            command,
            capture_output=True,
            check=True,
            text=True,  # important to treat output as text so that .strip() works
        )
        token = str(response.stdout).strip()  # strip() to remove trailing `\n` char
        return token
