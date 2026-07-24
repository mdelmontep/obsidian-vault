---
title: hook en worktree efímero no debe derivar nombre de basename(cwd)
date: 2026-07-24
source: claude-code-session
tags: [ticket-runner, time-tracking, worktree, dokploy]
---

Un hook de reporting (time-tracking) que corre dentro de un worktree efímero
(`mkdtempSync` → `ticket-<id8>-XXXXXX`) derivaba el "nombre de proyecto" del
`basename` del directorio con `.git` más cercano. En checkouts normales eso da
el nombre del repo; en un worktree con nombre aleatorio (típico de runners
tipo "resolver ticket con Claude" que crean 1 worktree por job) da basura
(`ticket-01c913fb-fqdtav`) y cada job aparece como un "proyecto" distinto en
vez de agruparse bajo el repo real.

**Fix**: priorizar una env var explícita del contexto del runner (`REPO_SLUG`,
"org/repo") sobre el basename del filesystem — el runner ya la conoce y la
pasa al proceso hijo (`claude`) por herencia de entorno.

**Gotcha aparte de despliegue**: el hook vive copiado dentro de la imagen
Docker del runner (build time) — mergear a `main` no aplica el fix solo, hace
falta rebuild + redeploy del servicio (y si Autodeploy está apagado, dispararlo
a mano una vez).

Aplica a cualquier tooling CI/CD que use worktrees temporales por job y derive
identidad de "proyecto" del path en vez de una env var explícita del orquestador.
