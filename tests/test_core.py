# Run tests with: python3 -m unittest tests/*.py

import unittest
from subprocess import CompletedProcess
from typing import Any, Dict, List
from unittest.mock import Mock, patch

from package_publisher.core import PackagePublisher


class PackagePublisherTests(unittest.TestCase):

    @patch("package_publisher.core.subprocess")
    def test_get_token_shells_out_correctly(self, mock_subprocess: Mock) -> None:
        mock_subprocess.return_value = Mock(name="subprocess")

        pp = PackagePublisher(registry="acme-corp/awesome-gem")

        pp.get_token()

        mock_subprocess.run.assert_called_with(
            [
                "buildkite-agent",
                "oidc",
                "request-token",
                "--audience",
                "https://packages.buildkite.com/acme-corp/awesome-gem",
                "--lifetime",
                "300",
            ],
            capture_output=True,
            check=True,
            text=True,
        )

    @patch("package_publisher.core.subprocess")
    def test_get_token_strips_stdout(self, mock_subprocess: Mock) -> None:
        mock_subprocess.return_value = Mock(name="subprocess")
        mock_subprocess.run.return_value.stdout = "AN_EXAMPLE_TOKEN_HERE\n"

        pp = PackagePublisher(registry="acme-corp/awesome-gem")

        result = pp.get_token()

        self.assertEqual(result, "AN_EXAMPLE_TOKEN_HERE")

    @patch("package_publisher.core.subprocess")
    def test_upload_package_shells_out_correctly(self, mock_subprocess: Mock) -> None:
        mock_subprocess.return_value = Mock(name="subprocess")

        def mock_run(args: str, **_: List[Any]) -> Any:
            if args[0] == "buildkite-agent":
                return CompletedProcess(args="", returncode=0, stdout="PRETEND_TOKEN")
            elif args[0] == "curl":
                return CompletedProcess(args="", returncode=0, stdout="{}")
            else:
                return CompletedProcess(args="", returncode=0, stdout="")

        mock_subprocess.run.side_effect = mock_run

        pp = PackagePublisher(registry="acme-corp/awesome-gem")

        pp.upload_package(file_path="/example/file.gem", provenance_bundle_path="")

        mock_subprocess.run.assert_called_with(
            [
                "curl",
                "--fail-with-body",
                "--silent",
                "--header",
                "Authorization: Bearer PRETEND_TOKEN",
                "--form",
                "file=@/example/file.gem",
                "https://api.buildkite.com/v2/packages/organizations/acme-corp/registries/awesome-gem/packages",
            ],
            capture_output=True,
            check=True,
            text=True,
        )

    @patch("package_publisher.core.subprocess")
    def test_upload_package_shells_out_correctly_with_provenance_path(
        self, mock_subprocess: Mock
    ) -> None:
        mock_subprocess.return_value = Mock(name="subprocess")

        def mock_run(args: str, **_: List[Any]) -> Any:
            if args[0] == "buildkite-agent":
                return CompletedProcess(args="", returncode=0, stdout="PRETEND_TOKEN")
            elif args[0] == "curl":
                return CompletedProcess(args="", returncode=0, stdout="{}")
            else:
                return CompletedProcess(args="", returncode=0, stdout="")

        mock_subprocess.run.side_effect = mock_run

        pp = PackagePublisher(registry="acme-corp/awesome-gem")

        pp.upload_package(
            file_path="/example/file.gem",
            provenance_bundle_path="/example/provenance.json",
        )

        mock_subprocess.run.assert_called_with(
            [
                "curl",
                "--fail-with-body",
                "--silent",
                "--header",
                "Authorization: Bearer PRETEND_TOKEN",
                "--form",
                "file=@/example/file.gem",
                "--form",
                "provenance_bundle=@/example/provenance.json",
                "https://api.buildkite.com/v2/packages/organizations/acme-corp/registries/awesome-gem/packages",
            ],
            capture_output=True,
            check=True,
            text=True,
        )

    @patch("package_publisher.core.subprocess")
    def test_upload_package_returns_the_response_correctly(
        self, mock_subprocess: Mock
    ) -> None:
        mock_subprocess.return_value = Mock(name="subprocess")

        def mock_run(args: str, **_: List[Any]) -> Any:
            if args[0] == "buildkite-agent":
                return CompletedProcess(args="", returncode=0, stdout="PRETEND_TOKEN")
            elif args[0] == "curl":
                return CompletedProcess(
                    args="",
                    returncode=0,
                    stdout='{"field_1": "value_1", "field_2": "value_2"}',
                )
            else:
                return CompletedProcess(args="", returncode=0, stdout="")

        mock_subprocess.run.side_effect = mock_run

        pp = PackagePublisher(registry="acme-corp/awesome-gem")

        result = pp.upload_package(
            file_path="/example/file.gem", provenance_bundle_path=""
        )

        self.assertEqual(result, dict(field_1="value_1", field_2="value_2"))
