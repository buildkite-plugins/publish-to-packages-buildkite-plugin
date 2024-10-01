# Publish to Packages [![Build status](https://badge.buildkite.com/8dff045aea2a2227a4387e77941af1177230066dc459982c67.svg)](https://buildkite.com/buildkite/plugins-publish-to-packages)

A [Buildkite plugin](https://buildkite.com/docs/agent/v3/plugins) that publishes [build artifacts](https://buildkite.com/docs/pipelines/artifacts) and attestations to [Buildkite Packages](https://buildkite.com/packages).

This plugin authenticates with Buildkite Packages using an [Agent OIDC token](https://buildkite.com/docs/agent/v3/cli-oidc), so your registry needs to be configured with a suitable [OIDC policy](https://buildkite.com/docs/packages/security/oidc#define-an-oidc-policy-for-a-registry).

## Quick Start

### Minimal

```yaml
steps:
  - label: "Publish Gem"
    plugins:
      - publish-to-packages#v2.2.0:
          artifacts: "awesome-logger-*.gem"
          registry: "acme-corp/awesome-logger"
```

### The Works

```yaml
steps:
  - label: "Publish Gem"
    plugins:
      - publish-to-packages#v2.2.0:
          artifacts: "awesome-logger-*.gem"
          registry: "acme-corp/awesome-logger"
          attestations: # optional
            - "gem-build.attestation.json"
            - "gem-package.attestation.json"
          artifact_build_id: "${BUILDKITE_TRIGGERED_FROM_BUILD_ID}" # optional
```

## Options

#### `artifacts` (string, required)

A glob pattern for artifacts to publish to Buildkite Packages from [Build artifacts](https://buildkite.com/docs/pipelines/artifacts).

#### `registry` (string, required)

Buildkite Packages registry to publish to.

- Full format is `<organization>/<registry_name>` (e.g. `acme-corp/awesome-logger`).
- `<organization>` defaults to your Buildkite organization if omitted (e.g. `awesome-logger`).

#### `attestations` (string or array of strings, optional)

One or more attestations from artifact storage to publish along with each package created from `artifacts`.

Each attestation file must be a valid JSON object. You can use [Generate Provenance Attestation](https://github.com/buildkite-plugins/generate-provenance-attestation-buildkite-plugin) plugin to generate a valid SLSA Provenance attestation in your Buildkite pipeline.

If `artifact_build_id` is specified, attestations will be downloaded from the relevant build artifact storage.

#### `artifact_build_id` (string, optional)

Configures the plugin to download artifacts from a different build, referenced by its UUID.

When this option is not specified, the plugin defaults to downloading artifacts from the build that it is running in.

This is typically used when package building and package publishing are split across two different pipelines and the former triggers the latter. See _Building and publishing from different pipelines_ example below.

## Usage

### Building and publishing from the same pipeline

_Build Gem_ step builds and uploads `awesome-logger-*.gem` package to the build artifact storage.

_Publish Gem_ step uses Publish to Packages to publish the package from the build artifact storage to **acme-corp/awesome-logger** Packages registry.

Globbing (`awesome-logger-*.gem`) is a good way to accommodate version changes/increments (e.g. `awesome-logger-1.0.5.gem`).

```yaml
steps:
  - label: "Build Gem"
    key: "build-gem"
    command: "gem build awesome-logger.gemspec"
    artifact_paths: "awesome-logger-*.gem" # upload to build artifact storage

  - label: "Publish Gem"
    depends_on: "build-gem"
    plugins:
      - publish-to-packages#v2.2.0:
          artifacts: "awesome-logger-*.gem" # publish from build artifact storage
          registry: "acme-corp/awesome-logger"
```

### Building and publishing from different pipelines

There are two pipelines in this example:

1. _Build Package_ pipeline
2. _Publish Package_ pipeline

_Build Package_ pipeline builds a gem, uploads it to its artifact storage and triggers the _Publish Package_ pipeline to publish the package.

In _Publish Packages_ pipeline, the `artifact_build_id` option is specified to reference [the build that triggered it](https://buildkite.com/docs/pipelines/environment-variables#BUILDKITE_TRIGGERED_FROM_BUILD_ID). This configures the plugin to download artifacts from the _Build Package_ build that triggered it.

```yaml
# build.pipeline.yml

steps:
  - label: "Build Gem"
    key: "build-gem"
    command: "gem build awesome-logger.gemspec"
    artifact_paths: "awesome-logger-*.gem" # upload to build artifact storage

  - label: "Trigger Publish pipeline"
    depends_on: "build-gem"
    trigger: "publish-package-pipeline"
    branches: "${BUILDKITE_BRANCH}"
    build:
      commit: "${BUILDKITE_COMMIT}"
      branch: "${BUILDKITE_BRANCH}"
```

```yaml
# publish.pipeline.yml

steps:
  - label: "Publish Gem"
    plugins:
      - publish-to-packages#v2.2.0:
          artifacts: "awesome-logger-*.gem"
          registry: "acme-corp/awesome-logger"
          artifact_build_id: "${BUILDKITE_TRIGGERED_FROM_BUILD_ID}"
```

### Building and publishing with a provenance attestation

```yaml
steps:
  - label: "Build Gem"
    key: "build-gem"
    command: "gem build awesome-logger.gemspec"
    artifact_paths: "awesome-logger-*.gem" # upload to build artifact storage
    plugins:
      - generate-provenance-attestation#v1.0.0:
          artifacts: "awesome-logger-*.gem" # publish from build artifact storage
          attestation_name: "gem-build.attestation.json"

  - label: "Publish Gem"
    depends_on: "build-gem"
    plugins:
      - publish-to-packages#v2.2.0:
          artifacts: "awesome-logger-*.gem" # publish from build artifact storage
          registry: "acme-corp/awesome-logger"
          attestations: "gem-build.attestation.json"
```
