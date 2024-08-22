# Publish to Packages

A [Buildkite plugin](https://buildkite.com/docs/agent/v3/plugins) that publishes packages to [Buildkite Packages](https://buildkite.com/packages).

This plugin authenticates with Buildkite Packages using an [Agent OIDC token](https://buildkite.com/docs/agent/v3/cli-oidc), so your registry needs to be configured with a suitable [OIDC policy](https://buildkite.com/docs/packages/security/oidc#define-an-oidc-policy-for-a-registry).

## Options

These are all the options available to configure this plugin's behaviour.

### Required

#### `files` (string)

A glob pattern for files to publish to Buildkite Packages from [Build artifacts](https://buildkite.com/docs/pipelines/artifacts).

#### `registry` (string)

Buildkite Packages registry to publish to.

- Full format is `<organization>/<registry_name>` (e.g. `acme-corp/awesome-logger`).
- `<organization>` defaults to your Buildkite organization if omitted (e.g. `awesome-logger`).

## Examples

Show how your plugin is to be used

```yaml
steps:
  - name: "Build Gem"
    command: "gem build awesome-logger.gemspec"
    artifact_paths: "awesome-logger-*.gem"

  - name: "Publish Gem"
    plugins:
      - buildkite-plugin/publish-to-packages#main:
          files: awesome-logger-*.gem
          registry: acme-corp/awesome-logger
```
