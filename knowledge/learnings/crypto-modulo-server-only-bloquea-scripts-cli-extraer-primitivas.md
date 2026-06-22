---
title: módulo de cifrado con `import 'server-only'` bloquea scripts cli — extraer primitivas
date: 2026-05-26
source: claude-code-session
tags: [nextjs, scripts, crypto, server-only, tsx]
---

Si un módulo de cifrado en Next.js usa `import 'server-only'` y un script CLI (`tsx --env-file=.env.local scripts/foo.ts`) lo importa, peta con:
```
Error: Cannot find module 'server-only'
```
`server-only` es un paquete fantasma que solo el bundler de Next.js sabe resolver — `tsx` puro no lo conoce.

Fix limpio (DRY, sin duplicar código):
1. `src/lib/<mod>/crypto-primitives.ts` — primitivas puras (`encryptX`, `decryptX`) SIN guard. Importable por scripts.
2. `src/lib/<mod>/encryption.ts` — `import 'server-only'` + `export { encryptX, decryptX } from './crypto-primitives'`. Importable por runtime de Next.js.

El bundler bloquea `encryption.ts` en componentes cliente. Los scripts importan de `crypto-primitives.ts`. Misma implementación, mismo formato de blob.

Caso real 2026-05-26 TuFacturaIA: backfill OAuth `scripts/backfill-google-ocr-to-integrations.ts` necesitaba `encryptIntegrationSecret` (AES-256-GCM kid versionado). Fix con split — sin duplicar la lógica de cifrado.

**Atajo para scripts desechables** (no quieres refactorizar un módulo grande): shim no-op `node_modules/server-only/{package.json,index.js}` con `module.exports = {}`. tsx lo resuelve; Next provee el suyo. BORRARLO tras el test — si queda, debilita el guard server/client en `build`. Caso 2026-06-22 TuFacturaIA: test del email unificado de stock importaba `@/lib/email/send` (cadena profunda con `server-only`).
