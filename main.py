import os
from glob import glob
from pathlib import Path

from package_publisher.cli_arguments import CliArguments
from package_publisher.core import PackagePublisher
from package_publisher.helpers import attestations_to_bundle

arguments = CliArguments()

artifacts_dir = arguments.get_artifacts_dir()
if artifacts_dir == "":
    print(
        "Error: Missing --artifacts-dir argument. Example: --artifacts-dir ./artifacts"
    )
    exit(1)

artifacts_glob = glob("{}/**/*".format(artifacts_dir), recursive=True)
file_paths = [path for path in artifacts_glob if os.path.isfile(path)]

attestations_dir = arguments.get_attestations_dir()

if attestations_dir != "":
    attestations_glob = glob("{}/**/*".format(attestations_dir), recursive=True)
    attestation_files = [path for path in attestations_glob if os.path.isfile(path)]
    attestation_bundle_path = attestations_to_bundle(attestation_files)
else:
    attestation_bundle_path = None


publisher = PackagePublisher(
    registry=arguments.get_registry(),
    attestation_bundle_path=attestation_bundle_path,
)

for file_path in file_paths:
    print(
        "Publishing {} → {}".format(
            file_path.replace("{}/".format(artifacts_dir), ""), arguments.get_registry()
        )
    )

    response = publisher.upload_package(
        file_path=file_path,
    )

    print(" ✅ \033]1339;url={}\a".format(response["web_url"]))
    print("")


if attestation_bundle_path is not None:
    print("~~~ 🚚 Preview Attestation Bundle")
    with open(attestation_bundle_path, "r", encoding="utf-8") as f:
        print(f.read())

    Path(attestation_bundle_path).unlink()
