---
title: GCal q-search eventual-consistency — usar event_id determinista
date: 2026-05-25
source: claude-code-session
tags: [google-calendar, idempotency, eventual-consistency]
---

`Calendar.events.list?q=...` no garantiza encontrar eventos recién creados. Hay ventana de eventual consistency (segundos a minutos) entre Create event y aparición en q-search.

Pattern robusto cuando necesitas cancelar/modificar tu propio evento:

1. **Reservar**: generar `event_id` determinista de `(phone, slot)`:
```js
const event_id = ('pre' + fnv32(phone+slot, seed)).substring(0,30);
events.create({ id: event_id, summary, start, end });
// Si ya existe → 409, no duplica (idempotency natural)
```

2. **Buscar**: q-search sí funciona para eventos antiguos. Usar para listar próximas citas del cliente:
```js
events.list({ q: phone, timeMin: now, singleEvents: true })
```
Devuelve el `event.id` real (que coincide con el determinista). Pasar ese ID al delete.

3. **Cancelar**: `events.delete(eventId)` directo. No buscar de nuevo.

Caso real: EcoBox 2026-05-25 — Cancelar_cita inicial buscaba por q-phone y devolvía 0 items para eventos creados en la misma sesión. Refactor: Buscar_reserva devuelve `event_id` → Cancelar_cita lo recibe y borra by id. Cancela SOLO esa cita, no toca el resto del histórico.
