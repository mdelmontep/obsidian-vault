---
title: kommo webhook status_lead dispara en todos los cambios de estado
date: 2026-04-20
source: claude-code-session
tags: [kommo, webhook, n8n]
---

El webhook `status_lead` de Kommo dispara en TODOS los cambios de estado del lead, no solo el estado objetivo. Si un lead pasa de "Pendiente" a "Especialista asignado", el webhook dispara. Pero si después alguien lo mueve de vuelta a "Pendiente" y luego otra vez a "Especialista asignado", dispara de nuevo — generando ejecuciones duplicadas.

**Fix obligatorio**: añadir un nodo IF inmediatamente después del webhook filtrando por `status_id == X` (el status objetivo). Sin esto, cualquier movimiento de status genera ejecución y posibles emails/tareas duplicadas.

Descubierto en Clínica Zen: mover lead ida y vuelta generó 2 emails de confirmación + 2 eventos Calendar.
