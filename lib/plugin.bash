#!/usr/bin/env bash
set -euo pipefail

# Copied partially from https://github.com/buildkite-plugins/template-buildkite-plugin/blob/16a1d1ebc840cf929fdb4f8955607d49709ee9da/lib/plugin.bash

PLUGIN_PREFIX="PUBLISH_TO_PACKAGES"

# Reads a single value
function plugin_read_config() {
  local var="BUILDKITE_PLUGIN_${PLUGIN_PREFIX}_${1}"
  local default="${2:-}"
  echo "${!var:-$default}"
}
