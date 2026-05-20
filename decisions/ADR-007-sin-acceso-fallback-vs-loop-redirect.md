---
title: ADR-007 — Página `/sin-acceso` para JWT vivo sin org operable
date: 2026-05-20
status: accepted
tags: [adr, facturaia, auth]
---

## Contexto
User revocado del único equipo o invitación expirada por cron → su access_token Supabase sigue válido hasta ~1h (signOut solo invalida refresh tokens). Layout-server con `if (!realOrgId) redirect('/login')` causa loop con middleware que redirige authenticated users a `/dashboard`.

## Opciones consideradas
- **A** — Loop hasta que JWT expire (status quo). Cero código pero UX rota durante 1h, ataques posibles ya que el user revocado mantiene shell vacío sin escape limpio.
- **B** — Forzar signOut server-side antes de redirect (sin página dedicated). Limpia cookie pero genera flash y pierde mensaje contextual.
- **C** — Nueva página `/sin-acceso` (authenticated allowed) con mensaje claro + botón logout. Middleware exempt, layout redirige ahí.

## Decisión
**C**, porque comunica claramente al user qué pasó (eliminado del equipo / invitación expirada) y le da agencia para cerrar sesión. Coste: 1 página + 2 líneas en middleware.

## Consecuencias
Patrón reusable para cualquier futuro escenario "JWT vivo sin contexto operable". También cron `team-expire-invites` ahora hace `signOut('global')` a users huérfanos para acelerar el ciclo. Ver [[signOut-solo-invalida-refresh-no-access-token]].
