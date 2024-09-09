import os
from glob import glob

from package_publisher.cli_arguments import CliArguments
from package_publisher.core import PackagePublisher
from package_publisher.helpers import fake_env

environment = fake_env() if os.environ.get("FAKE_ENV") == "1" else os.environ

arguments = CliArguments(organization_slug=environment["BUILDKITE_ORGANIZATION_SLUG"])

publisher = PackagePublisher(registry=arguments.get_registry())

files = [
    path
    for path in glob(arguments.get_artifacts_glob(), recursive=True)
    if os.path.isfile(path)
]

for file in files:
    print("Uploading {} to {}".format(file, arguments.get_registry()))

    response = publisher.upload_package(
        file_path=file,
        provenance_bundle_path=arguments.get_provenance_bundle(),
    )

    print(
        "⬆️ Uploaded {} to {}/{}".format(
            file.split("/")[-1],
            response["organization"]["slug"],
            response["registry"]["slug"],
        )
    )
    print("  \033]1339;url={}\a".format(response["web_url"]))
    print("")
