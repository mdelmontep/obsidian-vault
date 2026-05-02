---
title: openapi.json mantenido a mano deriva silenciosamente del handler
date: 2026-05-02
source: claude-code-session
tags: [api-design, openapi, sdk, drift]
---

Cuando el `openapi.json` de tu API se escribe a mano (no autogenerado del runtime), los handlers pueden divergir del contrato sin que nada lo detecte.

Síntoma: un consumidor que genera SDK desde la spec (`openapi-typescript`) ve `data.cliente?.id = undefined` aunque la spec lo declare como objeto. Ningún error, solo campos que llegan null.

Caso real (FacturaIA): `GET /v1/facturas/{id}` declaraba `cliente: { id, nombre }` en spec pero el handler devolvía solo `cliente_id: string`. El portal sincronizaba sombras sin nombre de cliente. Fix: JOIN en el handler para alinear con la spec (commit `debd55e`).

Reglas:
- Cuando añadas/cambies un endpoint, abre el `openapi.json` lado a lado y compáralo línea por línea con el response real.
- Cualquier cambio de schema = revisión obligada del handler correspondiente.
- A medio plazo: tests de contrato (response real ↔ spec) o autogenerar la spec desde el runtime con tipos compartidos.
