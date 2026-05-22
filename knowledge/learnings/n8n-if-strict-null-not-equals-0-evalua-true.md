---
title: n8n If strict — null != 0 evalúa TRUE y rompe detección de existencia
date: 2026-05-22
source: claude-code-session
tags: [n8n, if-node, gotcha]
---

`If` v2 con `typeValidation:"strict"` interpreta `null != 0` como TRUE. Si tienes un campo `existing_X_id` que vale `null` cuando no hay match, y usas `notEquals 0` para detectar "existe", el If toma la rama positiva incorrectamente.

Patrón seguro: en el Code node anterior, emite un flag booleano explícito `_has_X = !!X` y configura el If como `boolean.true` sobre ese flag. Más claro y nunca falla.

Aplica a cualquier If que pueda recibir `null` en el campo evaluado: detección de contact existente, conv abierta, deal cacheado, etc.

Caso real Elphis 2026-05-22: `wa-inbound-bridge` creaba contact + conv duplicados porque `If contact exists` con `existing_contact_id != 0` daba TRUE incluso con `null`.
