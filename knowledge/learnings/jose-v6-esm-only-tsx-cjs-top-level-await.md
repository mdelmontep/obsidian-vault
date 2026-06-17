---
title: jose v6 es esm-only; tsx sin "type":"module" transpila a cjs y rompe top-level await
date: 2026-06-18
source: claude-code-session
tags: [node, esm, tsx, jose, typescript]
---

`jose` v6 es **ESM-only** (`package.json` `type:module`, exports solo `default` → sin build CJS).
Un servicio Node corrido con `tsx` cuyo repo NO tiene `"type":"module"` en el package.json raíz
(p.ej. una app Next) hace que esbuild transpile a **CJS** por defecto → dos fallos:

- Top-level `await` revienta: `Top-level await is currently not supported with the "cjs" output format`.
- `require()` de un paquete ESM-only puede fallar según versión de Node.

Fixes (cualquiera sirve, según el caso):
- Correr el servicio como **ESM**: `tsconfig` con `module:ESNext`/`moduleResolution:bundler` y entry sin
  top-level await, o usar extensión **`.mts`** (tsx la trata como ESM siempre).
- Para scripts puntuales: envolver el cuerpo en `async function main(){...}; main()` en vez de top-level await.

Caso real: servicio MCP de TuFacturaIA (`services/mcp-server/`, patrón `pdf-renderer`) usa jose
para verificar JWT ES256. `mint-token.ts` con top-level await rompía; el server arranca OK como ESM.
El typecheck del repo (moduleResolution `bundler`) resuelve los subpaths del SDK sin problema.
