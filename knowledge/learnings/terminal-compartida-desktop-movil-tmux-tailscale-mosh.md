---
title: terminal/claude compartida desktop+móvil — tmux grouped + tailscale ssh + mosh
date: 2026-06-19
source: claude-code-session
tags: [tmux, tailscale, mosh, mobile, infra]
---
Sesión de terminal (con `claude` dentro) espejada Mac+móvil:
- tmux persistente en host always-on (systemd la recrea al reboot; tmux la mantiene entre desconexiones).
- Tailscale en los 3, misma cuenta → malla privada, 0 exposición. `tailscale up --ssh` = SSH por identidad de tailnet, sin gestionar claves.
- mosh para móvil (sobrevive cambios de red/bloqueo de pantalla); ssh pelado se cae al rotar red.
- Agrupado (`tmux new-session -A -s <disp> -t base` + `set -g aggressive-resize on`) → cada dispositivo a su tamaño compartiendo ventanas; sin grupo tmux encoge al cliente más pequeño.

Gotchas:
- mosh desde macOS: el Mac exporta `LC_CTYPE=UTF-8` (pseudo-locale) → "mosh-server needs a UTF-8 native locale". Fix: `locale-gen en_US.UTF-8` en el host + conectar con `LC_ALL=en_US.UTF-8 mosh …`.
- ssh no-interactivo (sin TTY, p.ej. prefijo `!` de Claude Code) → "Host key verification failed" cuando hay que aceptar la clave del host; acéptala una vez en terminal real.
- Editar ficheros del usuario remoto: hacerlo desde dentro de la sesión (ya eres ese usuario), no por ssh root no-interactivo.
