#!/usr/bin/env sh
# Offline pre-publication hygiene check, NOT a complete security scanner.
set -eu
if find . -type f \( -name '*.docx' -o -name '*.pdf' -o -name '*.xlsx' -o -name '.env' \) ! -path './.git/*' | grep -q .; then
  echo 'STOP: office document or .env present in repository tree.' >&2
  exit 1
fi
if grep -R -n -E 'BEGIN (RSA|OPENSSH|EC) PRIVATE KEY|ghp_[A-Za-z0-9]{30}|github_pat_[A-Za-z0-9_]{40}' --exclude-dir=.git --exclude='check_publication.sh' .; then
  echo 'STOP: potential credential detected.' >&2
  exit 1
fi
echo 'Basic publication check passed (not a security audit).'
