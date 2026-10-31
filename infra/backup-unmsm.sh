#!/usr/bin/env bash
set -euo pipefail
umask 077
dest=/var/backups/unmsm
install -d -m 700 "$dest"
name="unmsm-$(date +%Y%m%d-%H%M%S).tar.gz"
tar -czpf "$dest/$name" --acls -C / var/www/unmsm etc/nginx/sites-available/unmsm
(cd "$dest" && sha256sum "$name" > "$name.sha256")
echo "Copia creada: $dest/$name"
