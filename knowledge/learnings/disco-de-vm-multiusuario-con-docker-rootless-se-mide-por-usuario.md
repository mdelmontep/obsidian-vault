---
title: disco de vm multiusuario con docker rootless se mide por usuario, no en /var/lib/docker
date: 2026-10-15
source: facturaia (VM gates, ssh gates)
tags: [docker, rootless, disco, gates, infra]
---
- **Síntoma**: 60-80 GB ilegibles sin sudo; la hipótesis «Docker de root sobrante» era falsa (daemon parado y desactivado). El hueco estaba en los homes de los otros usuarios, cada uno con su Docker rootless (gh-runner con ~17 contenedores de CI).
- **Medir el tuyo sin sudo**: `nsenter -U --preserve-credentials -m -t $(pgrep -P $(pgrep -u $USER -x rootlesskit)) du -xsh ~/.local/share/docker/*`; `du` normal choca con los ficheros de subuid.
- **El de otro, como root**: `sudo -u U XDG_RUNTIME_DIR=/run/user/$ID DOCKER_HOST=unix:///run/user/$ID/docker.sock docker system df`. Con `sudo -iu U docker` apunta al socket de root y no mide nada.
- **Guardas**: `pgrep -f vitest` sin `-u $USER` caza procesos de otros usuarios (`vitest.config.ts` en los argumentos de eslint). Y en la VM `/tmp` es tmpfs: probar un umbral de `df` con el sandbox en `/home`.
- **Prevención**: sin cron en la VM, el prune periódico va en un timer de systemd por usuario de CI, más `supabase stop --no-backup` con `if: always()` en los workflows.
