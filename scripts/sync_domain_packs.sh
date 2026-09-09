#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
set -euo pipefail
platform="${1:?usage: sync_domain_packs.sh /path/to/recordlane}"
ecosystem_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$ecosystem_root/domain-packs"
cp -R "$platform/domains/." "$ecosystem_root/domain-packs/"
printf 'Synchronized domain packs from platform contract at %s\n' "$(git -C "$platform" rev-parse HEAD 2>/dev/null || printf uncommitted)"
