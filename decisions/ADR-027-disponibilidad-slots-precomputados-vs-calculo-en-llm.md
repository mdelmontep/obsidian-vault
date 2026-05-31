---
title: ADR-027 — disponibilidad de citas: backend devuelve slots pre-computados, el LLM no calcula
date: 2026-05-31
status: accepted
tags: [adr, simarro, retell, n8n, voz]
---

## Contexto
Agente de voz/chat agenda visitas de 1h con buffer entre viviendas (0 misma / 30 min distinta). El LLM (gpt-4.1-mini) recibía el rango bloqueado en prosa y debía deducir las horas libres → ofrecía horas que invadían el margen (no descontaba su visita de 1h). Además la lógica de buffer vivía solo en el nodo de disponibilidad.

## Opciones consideradas
- **A** — Backend pre-computa la lista de horas válidas (`slots`); el LLM solo elige. Lógica en un sub-workflow único compartido por disponibilidad y reserva.
- **B** — Mantener la prosa y reforzar el prompt para que el LLM reste 1h+buffer. Frágil: depende del razonamiento del modelo cada vez.
- **C** — Calcular el buffer en SQL/RPC Supabase. La ocupación vive en Google Calendar, no en Supabase → obligaría a sincronizar GCal→DB (anti-patrón) o pasar eventos como parámetro.

## Decisión
**A**, porque elimina el cálculo del LLM (causa raíz) y un sub-workflow único (`Calc_Disponibilidad`, modos listar/validar) evita que disponibilidad y reserva diverjan. Recheck fail-open en la reserva como segunda barrera.

## Consecuencias
El prompt queda como "elige slots[0]/slots[1], no calcules". Cualquier cambio de regla de buffer se toca en un solo sitio. La ventana de lectura de GCal debe cubrir el día completo (un evento colindante invade la franja hasta 90 min antes). Patrón reutilizable en otros agentes de voz/chat. Ver [[defensa-en-codigo-vs-prompt-llm-para-invariantes-de-dominio]].
