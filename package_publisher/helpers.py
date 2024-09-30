import json

from tempfile import NamedTemporaryFile
from typing import Optional


def attestations_to_bundle(file_paths: list[str]) -> Optional[str]:
    if len(file_paths) <= 0:
        return None

    bundle_file = NamedTemporaryFile(delete=False)

    for file_path in file_paths:
        with open(file_path, "r", encoding="utf-8") as file:
            try:
                content = json.loads(file.read())
            except json.decoder.JSONDecodeError as error:
                print("Error parsing JSON in attestation: {}".format(file_path))
                print("  {}".format(error))
                exit(1)
            bundle_file.write(bytearray(json.dumps(content), encoding="utf-8"))
            bundle_file.write(bytearray("\n", encoding="utf-8"))

    bundle_file.close()
    return bundle_file.name
