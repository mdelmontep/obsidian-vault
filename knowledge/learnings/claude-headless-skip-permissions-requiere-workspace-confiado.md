---
title: claude headless con --dangerously-skip-permissions requiere workspace confiado
date: 2026-07-23
source: claude-code-session
tags: [claude-code, headless, runner, ci, docker]
---

CLIs recientes de Claude Code (≥~2.1.x) rechazan `--dangerously-skip-permissions`
en un workspace sin trust aceptado → exit 1 con stderr de solo-warnings
("Ignoring N permissions.allow entries… this workspace has not been trusted").
El warning solo (sin bypass) es no-fatal. NO está en la doc oficial.

Fix en runners/containers headless: sembrar en el entrypoint
`projects["<repo>"].hasTrustDialogAccepted: true` en `~/.claude.json`
(merge idempotente con node, no pisar oauth/onboarding). Un worktree en /tmp
resuelve su trust key al repo principal, con eso basta.

Gotchas asociados: (1) al reportar fallo de un subproceso, incluir stderr Y
stdout — `stderr || stdout` oculta el error fatal si stderr trae solo warnings;
(2) `spawn` con stdin pipe abierto → claude espera 3s ("no stdin data received");
usar `stdio: ['ignore', 'pipe', 'pipe']`. Riesgo latente: Dockerfile con
`npm i -g @anthropic-ai/claude-code` (latest) → cada rebuild puede traer un CLI
con checks nuevos. Caso real: ticket-runner TuFacturaIA (PR #1182).
