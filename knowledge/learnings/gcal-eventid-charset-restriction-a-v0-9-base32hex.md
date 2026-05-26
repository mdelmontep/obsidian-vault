---
title: Google Calendar eventId charset restringido a [a-v0-9] (base32hex), 5-1024 chars
date: 2026-05-25
source: claude-code-session
tags: [google-calendar, idempotency, charset]
---

Google Calendar API rechaza event IDs custom con caracteres fuera de `[a-v0-9]` con error 400 "Invalid resource id value". Subset de base32hex (no incluye `w-z`).

Para hashes deterministas idempotentes (anti doble-booking):

```js
// fnv32 → toString(32) emite exactamente [0-9a-v]
function fnv32(s, seed) {
  let h = seed >>> 0;
  for (let i = 0; i < s.length; i++) {
    h ^= s.charCodeAt(i);
    h = Math.imul(h, 0x01000193);
  }
  return (h >>> 0).toString(32).padStart(7, '0'); // valid charset
}
const eventId = ('ec' + fnv32(input, seed1) + fnv32(input, seed2)).substring(0, 30);
```

Si necesitas un hash criptográfico (SHA-256), convertirlo a base32 hex-only via `Buffer.from(hash, 'hex').toString(...)` no funciona directo — el alfabeto difiere. Más fácil tomar substring del hex (0-9 a-f) que también es válido.

NO usar `crypto.randomUUID()`: incluye `-` que tampoco está permitido.

Caso real: EcoBox `Reservar_cita > Gen GCal event ID` 2026-05-25 — `toString(32)` directo desde FNV cumple sin transformación adicional.
