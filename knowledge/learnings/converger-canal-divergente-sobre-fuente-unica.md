---
title: converger un canal divergente sobre la fuente única sin regresión
date: 2026-06-28
source: claude-code-session
tags: [arquitectura, refactor, facturaia]
---
Un canal que forkeó la lógica core (ej. `voice/generate` reimplementaba creación de
documentos) converge sobre la fuente única SIN regresión así:

- **Los bordes se quedan en el canal**, no se delegan: auth, identidad, cuotas, audit
  con contexto rico (teléfono), TTL de URL propio. Solo se delega el núcleo.
- **Pasar IDs ya resueltos**, no payloads: el canal resuelve cliente+409 en su borde y
  pasa `cliente.id` → evita que el assert del core valide sobre un payload incompleto.
- **Flags opt-in para deltas de comportamiento** (defaults = sin cambio para los otros
  callers): `skipAudit` (el canal audita él), `checkQuota:false` (no bloquear la op por
  una cuota de otro canal), `nifValidation:'lenient'` (no abortar por validación estricta
  en un path que no debe romperse).
- **Traductor de errores en el borde**: el core lanza `ApiError(code)` genérico; el canal
  lo mapea a SUS `error_code` (los que enruta n8n/cliente). Sin esto rompes el contrato.

Ver [[port-devuelve-dato-discriminado-tool-traduce-throw-en-borde]].
