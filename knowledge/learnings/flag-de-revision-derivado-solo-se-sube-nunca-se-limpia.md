---
title: un flag derivado que solo se escribe al detectar anomalía deja avisos fantasma
date: 2026-06-16
source: claude-code-session
tags: [arquitectura, estado, ocr, facturaia, anti-patron]
---

Anti-patrón: un flag calculado (`requires_human_review` + `review_reasons`) que
SOLO se escribe cuando hay anomalía y nunca se baja. Tras un reproceso correcto
el item queda con un cartel de revisión obsoleto (caso real: `ocr_trigger_error`
de un fallo previo mostrándose sobre una factura ya bien extraída — ticket Abba).

Fix: el último cálculo es la fuente de verdad → recalcular el flag COMPLETO en
cada pasada, incluida la rama "limpia" que lo baja a false y vacía los motivos.

Trampa al centralizar: si había overrides que forzaban revisión por fuera de la
función de decisión (en facturaia, dos anomalías `medium` —moneda baja confianza,
NIF emisor==receptor— que `ocr-process` marcaba a mano), muévelos DENTRO de la
función (`requiresReview`) antes de añadir la rama de limpieza, o la limpieza los
pisará. Verifica los productores: misma lógica usada por más de un endpoint.

Relacionado: [[recuperacion-ui-gated-por-estado-pierde-items-en-estado-hermano]]
