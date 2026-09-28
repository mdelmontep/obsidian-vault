---
title: escribir en un lead por api cambia updated_at y falsea a quien mide inactividad
date: 2026-09-28
source: simarro
tags: [kommo, crm, n8n, efectos-secundarios]
---
En Kommo (y en casi cualquier CRM) cualquier PATCH a un lead mueve su `updated_at`, aunque solo copie un dato técnico.
Si algún workflow usa `updated_at` como "última actividad" (alertas de inactividad, rellamadas de reactivación), un relleno masivo
hace que todos los leads parezcan tocados hoy: se silencian alertas y se retrasan rellamadas durante semanas.

- Antes de escribir en bloque en leads: `grep updated_at` en los workflows del cliente y ver quién lo lee.
- Si hay consumidores, o se acepta el efecto explícitamente o se cambian para medir actividad real (mensaje, nota, cambio de etapa).
- Los espejos periódicos solo deben escribir si el valor difiere, para no "tocar" el lead en cada pasada.

Caso real (28-sep-2026, Simarro): espejo contacto→lead de Nombre/Teléfono/Email; `Alertas_inactividad` y `Llamadas_outbound` leen `updated_at`.
Manuel aceptó el efecto y se rellenaron 57 leads. Ver [[simarro]].
