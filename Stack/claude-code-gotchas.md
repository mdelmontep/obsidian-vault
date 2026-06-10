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
- **`pnpm/action-setup@v4` + `packageManager` en package.json** — declarar versión solo en UN sitio. Si declaras `version: 10` en el workflow Y `packageManager: pnpm@10.33.3` en `package.json` → CI rompe con "Multiple versions of pnpm specified". Quitar `version` del workflow es la fix recomendada (action-setup lo lee de packageManager automáticamente).
- **Next.js `unstable_cache` no invalida con escrituras directas a BD** — si modificas datos via script externo (Prisma directo, SQL, seed), el cache lo ignora hasta `revalidateTag(TAG)` o reinicio del dev server. En prod no es problema porque las server actions llaman `revalidateTag`. En dev/scripts, recordar reiniciar o llamar revalidate.
- **Cloudflared quick tunnel sin login** — `cloudflared tunnel --url http://localhost:PORT --no-autoupdate` da una URL `*.trycloudflare.com` temporal. Útil para apuntar webhooks de provider externo a localhost en pruebas E2E. La URL se pierde al parar el proceso, no es estable.
- **Next.js route handlers no permiten exports custom** — solo `GET`, `POST`, etc. Si exportas un helper desde `route.ts`, typecheck devuelve `Type ... not assignable to type 'never'` en `.next/types/...`. Mover el helper a archivo aparte o dejarlo private.
- **`req.text()` antes de cualquier parse** para verificación HMAC — leer el body como string crudo antes de `JSON.parse` o cualquier middleware. La firma se computa sobre los bytes EXACTOS recibidos; cualquier re-serialización rompe el digest.
- **Edits paralelos al mismo archivo se rompen** — múltiples Edit calls en una sola tool-block sobre el mismo path: el primero muta el contenido y el segundo no encuentra su `old_string`. Síntoma "String to replace not found" tras edit exitoso. Hacer secuencial. Paralelo solo entre archivos distintos.
- **Subagentes investigando repo distinto al cwd** — pasar ruta absoluta en la primera línea del prompt + "investiga SOLO en esa ruta, no leas archivos fuera de ella". Sin esto contaminan el reporte con paths del cwd actual (caso: agente reportó hallazgos de `facturaia/src/...` cuando debía auditar `~/agency-portal-fix`).
- **`.claude/settings.local.json` acumula secretos en literales de allowlist** — cuando aceptas comandos tipo `Bash(curl -H 'Authorization: Bearer <jwt>' ...)` o `Bash(curl ... apikey: <service_role> ...)`, esos literales se guardan tal cual. Añadir `.claude/settings.local.json` al `.gitignore` en TODO repo nuevo desde el primer commit. Caso: agency-portal PR #76 2026-05-28 (JWTs n8n + service_role Supabase en patterns).
- **Un subagente puede re-dispararse solo en bucle y NO se mata con `TaskStop`** (figura `completed` cada ciclo → "not running"). Caso 2026-06-10: agente de research se reactivó ~30 veces, escaló de investigar a editar código y manipular git (ramas, stashes), y llegó a stashear WIP de otra sesión del mismo repo. Mitigación: para trabajo grande/arriesgado de un agente, aislarlo en **worktree desde `origin/main`** (working tree propio; un runaway no puede pisar/stashear el repo principal). Corte de raíz fiable = el humano interrumpe la sesión (Esc); desde el orquestador no hay kill si el task reporta completed.
- **`gh pr merge --delete-branch` falla (exit 1) si la rama vive en un worktree local — pero el merge remoto SÍ se completa**: verificar con `gh pr view N --json state` antes de reintentar o asumir fallo. Además puede dejar el checkout principal a medias (switch a main sin pull) si hay untracked en conflicto. Caso TuFacturaIA 2026-06-10 (repo con 50+ worktrees).
