import os
from glob import glob

from package_publisher.cli_arguments import CliArguments
from package_publisher.core import PackagePublisher

arguments = CliArguments()

publisher = PackagePublisher(registry=arguments.get_registry())

artifacts_dir = arguments.get_artifacts_dir()
artifacts_glob = glob("{}/**/*".format(artifacts_dir), recursive=True)
files = [path for path in artifacts_glob if os.path.isfile(path)]

for file in files:
    print(
        "Publishing {} → {}".format(
            file.replace("{}/".format(artifacts_dir), ""), arguments.get_registry()
        )
    )

    response = publisher.upload_package(
        file_path=file,
        provenance_bundle_path=arguments.get_provenance_bundle(),
    )

    print(" ✅ \033]1339;url={}\a".format(response["web_url"]))
    print("")
