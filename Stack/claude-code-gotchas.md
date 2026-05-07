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
