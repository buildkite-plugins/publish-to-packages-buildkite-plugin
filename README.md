# Publish Package

```yaml
steps:
  - label: ":pipeline:"
    plugins:
    - sj26/publish-package:
        package: *.rpm
        registry: agent-rpm-experimental
```
