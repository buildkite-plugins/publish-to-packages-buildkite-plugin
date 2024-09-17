# Run tests with: python3 -m unittest tests/*.py

import json
import unittest
from tempfile import NamedTemporaryFile
from unittest.mock import Mock, patch

from package_publisher.helpers import attestations_to_bundle


class AttestationsToBundleTests(unittest.TestCase):
    def test_it_returns_none_if_file_paths_is_empty(self) -> None:
        result = attestations_to_bundle([])
        self.assertIsNone(result)

    def test_it_bundles_up_single_valid_json_correctly(self) -> None:
        payload = json.dumps(
            dict(a=1, b="two", c=dict(d="buckle my", e="shoe")), indent=2
        )

        attestation_file = NamedTemporaryFile(delete=False)
        attestation_file.write(bytearray(payload, encoding="utf-8"))
        attestation_file.close()

        bundle_file_path = str(attestations_to_bundle([attestation_file.name]))

        with open(bundle_file_path, "r", encoding="utf-8") as f:
            result = f.read()
            self.assertEqual(
                result, '{"a": 1, "b": "two", "c": {"d": "buckle my", "e": "shoe"}}\n'
            )

    def test_it_bundles_up_multiple_valid_json_correctly(self) -> None:
        payloads = [
            json.dumps(dict(a=1, b="two", c=dict(d="buckle my", e="shoe")), indent=2),
            json.dumps(
                dict(a=3, b="four", c=dict(d="knock at", e="the door")), indent=2
            ),
            json.dumps(dict(a=5, b="six", c=dict(d="pick up", e="sticks")), indent=2),
        ]

        def payloads_to_files(payload: str) -> str:
            file = NamedTemporaryFile(delete=False)
            file.write(bytearray(payload, encoding="utf-8"))
            file.close()
            return file.name

        filenames = list(map(payloads_to_files, payloads))

        bundle_file_path = str(attestations_to_bundle(filenames))

        with open(bundle_file_path, "r", encoding="utf-8") as f:
            result = f.read()
            self.assertEqual(
                result,
                '{"a": 1, "b": "two", "c": {"d": "buckle my", "e": "shoe"}}\n'
                '{"a": 3, "b": "four", "c": {"d": "knock at", "e": "the door"}}\n'
                '{"a": 5, "b": "six", "c": {"d": "pick up", "e": "sticks"}}\n',
            )

    @patch("builtins.print")  # mock_print
    @patch("builtins.exit")  # mock_exit
    def test_it_exits_if_json_is_invalid(
        self,
        mock_exit: Mock,
        mock_print: Mock,  # mainly to suppress print output in unittest
    ) -> None:

        class ExitException(Exception):
            pass

        # Pop the call stack when `exit` is called
        def mock_exit_fn(_: int) -> None:
            raise ExitException

        mock_exit.side_effect = mock_exit_fn

        payload = "INVALID JSON"

        attestation_file = NamedTemporaryFile(delete=False)
        attestation_file.write(bytearray(payload, encoding="utf-8"))
        attestation_file.close()

        with self.assertRaises(ExitException):
            attestations_to_bundle([attestation_file.name])

        mock_exit.assert_called_with(1)
        self.assertEqual(len(mock_print.call_args_list), 2)
