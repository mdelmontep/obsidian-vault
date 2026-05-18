---
title: supabase .maybeSingle() devuelve null sin throw si hay >1 filas
date: 2026-05-18
source: claude-code-session
tags: [supabase, postgrest, gotcha]
---

`.maybeSingle()` tiene tres comportamientos:
- 0 filas → `{ data: null, error: null }`
- 1 fila → `{ data: row, error: null }`
- **>1 filas → `{ data: null, error: PostgrestError }`** (pero suele propagarse como null si no compruebas error)

En consumidores que solo desestructuran `{ data }` ignorando `error`, el caso
">1 filas" se ve indistinguible de "0 filas" → fallback path o 404 silencioso.

Caso real (agency-portal onboarding): resolución por phone hacía `.or(...)
.maybeSingle()` asumiendo 1 sesión activa por teléfono. Con dos sesiones
test activas mismo phone (caso de prueba, no producción) → query devolvió
null → handler 404 → mensajes WhatsApp no procesados.

Reglas:
- `.maybeSingle()` solo es seguro cuando hay constraint UNIQUE que garantiza
  ≤1 filas.
- Si la query puede tener múltiples matches por diseño, usar
  `.limit(1).order('created_at', { ascending: false })` y aceptar la más
  reciente explícitamente.
- Siempre desestructurar `{ data, error }` y loggear el error aunque parezca
  inofensivo.

Aplicable también a `.single()` (que sí throw pero a veces se atrapa sin
distinguir el caso).
