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
