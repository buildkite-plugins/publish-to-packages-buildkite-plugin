# Publish to Packages

A [Buildkite plugin](https://buildkite.com/docs/agent/v3/plugins) that publishes [build artifacts](https://buildkite.com/docs/pipelines/artifacts) to [Buildkite Packages](https://buildkite.com/packages).

This plugin authenticates with Buildkite Packages using an [Agent OIDC token](https://buildkite.com/docs/agent/v3/cli-oidc), so your registry needs to be configured with a suitable [OIDC policy](https://buildkite.com/docs/packages/security/oidc#define-an-oidc-policy-for-a-registry).

## Options

#### `artifacts` (string, required)

A glob pattern for artifacts to publish to Buildkite Packages from [Build artifacts](https://buildkite.com/docs/pipelines/artifacts).

#### `registry` (string, required)

Buildkite Packages registry to publish to.

- Full format is `<organization>/<registry_name>` (e.g. `acme-corp/awesome-logger`).
- `<organization>` defaults to your Buildkite organization if omitted (e.g. `awesome-logger`).

#### `artifact_build_id` (string, optional)

Configures the plugin to download artifacts from the build referenced by the UUID specified here.
By default, the plugin downloads artifacts from the build that it is running in.

This option is typically used when a "Publish Package" pipeline is triggered by a "Build Package" pipeline where the artifacts are built and stored.
Specifying `"${BUILDKITE_TRIGGERED_FROM_BUILD_ID}"` here configures the plugin to reference the artifact storage of the _triggering_ "Build Package" build.

```yaml
- buildkite-plugins/publish-to-packages#main:
    artifacts: "other-logger-*.gem"
    registry: "acme-corp/other-logger"
    artifact_build_id: "${BUILDKITE_TRIGGERED_FROM_BUILD_ID}"
```

## Example

In the example below, _Build Gem_ step builds and uploads `awesome-logger-*.gem` package to the build artifact storage.

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
      - buildkite-plugins/publish-to-packages#main:
          artifacts: "awesome-logger-*.gem" # publish from build artifact storage
          registry: "acme-corp/awesome-logger"

  - label: "Publish Gem from a triggering pipeline build"
    depends_on: "build-gem"
    plugins:
      - buildkite-plugins/publish-to-packages#main:
          artifacts: "other-logger-*.gem"
          registry: "acme-corp/other-logger"
          artifact_build_id: "${BUILDKITE_TRIGGERED_FROM_BUILD_ID}" # publish from triggering build's artifact storage
```
