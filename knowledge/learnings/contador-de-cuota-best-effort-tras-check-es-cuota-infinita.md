---
title: un contador de cuota best-effort tras el check es cuota infinita si el increment falla
date: 2026-06-26
source: claude-code-session
tags: [billing, cuotas, observabilidad]
---

Patrón de cuota: check ANTES de la acción, increment DESPUÉS. Si el increment es
best-effort (`if (err) console.error(...)` y devolver 200 igual), un fallo
persistente del RPC de incremento deja el contador congelado → el check siempre
ve `used < limit` → cuota infinita de facto, detectada semanas después al mirar
logs efímeros (si alguien los mira).

Caso real FacturaIA: `copiloto_usage_increment` fallaba en silencio → tokens del
copiloto sin tope real.

Fix: el fallo del incremento debe ser OBSERVABLE — emitir alerta (system_alert /
email a operaciones, dedup por org) o registrar en tabla con `status`/`last_error`,
no solo `console.error`. Mismo principio que [[integracion-en-jsonb-tabla-generica-pierde-observabilidad]].
Si el coste lo justifica, hacer check+increment atómico (RPC) para cerrar también
el TOCTOU (org en cap-1 gasta un turno entero).
