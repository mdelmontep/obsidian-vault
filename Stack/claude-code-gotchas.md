---
title: claude code — gotchas técnicos
date: 2026-04-24
source: claude-md-cleanup
tags: [claude-code, gotchas, github, plugins]
---

# Claude Code — Gotchas técnicos

- **Scheduled triggers** no acceden a repos privados — repo público o GitHub conectado en claude.ai/settings.
- **`gh repo edit --visibility`** requiere `--accept-visibility-change-consequences`.
- **`gh auth switch` para repos multi-cuenta** — `gh auth switch --user <org>` + `gh auth setup-git` antes de push.
- **Plugins settings.json** — nombre debe coincidir con `marketplace.json` del repo fuente.
- **Claude Design handoff bundles son tar** — `tar xf`, no abrir como HTML. Contiene README.md + chats/ + project/. Leer chat transcripts primero para la intención.
- **Zod `.strict()` bloquea campos no listados** — al añadir campos editables desde admin, añadirlos al schema Zod. Si no, PATCH devuelve 400 silenciosamente.
- **Verificación obligatoria antes de commit (Next.js)** — `npm run lint → typecheck → build`. Los tres deben pasar. No silenciar con `@ts-ignore`/`eslint-disable`/`as any`.
