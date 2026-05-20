---
name: signOut-solo-invalida-refresh-no-access-token
description: Supabase Auth Admin signOut() invalida refresh tokens pero el access_token JWT sigue vivo hasta su expiración natural (~1h). Lleva a loops /login↔/dashboard.
date: 2026-05-20
source: claude-code-session
tags: [supabase, auth, jwt]
---

`admin.auth.admin.signOut(userId)` y `admin.auth.admin.signOut(userId, 'global')` (ambos por default ya son 'global', verificado en `@supabase/auth-js/dist/module/GoTrueAdminApi.js`) solo revocan los refresh tokens. El access_token JWT actual del user sigue válido hasta su expiración natural (~1h).

**Síntoma**: tras revocar membresía del único equipo (DELETE soft) o expirar invitación (cron), el user con JWT vivo entra a loop: middleware ve `user` truthy → no redirige a login. Layout-server llama `getOrgId()` → null → `redirect('/login')`. Middleware ve `user && isAuthPage` → `redirect('/dashboard')`. Loop hasta JWT expire.

**Fix**: página `/sin-acceso` para autenticados sin org operable. Middleware exempt (no redirige authenticated users desde aquí). Layout-server redirige ahí en lugar de `/login`. Botón "Cerrar sesión" client-side limpia la cookie Supabase. Ver [[ADR-007-sin-acceso-fallback-vs-loop-redirect]] y [[matriz-permisos-rol-aware-bd-mas-espejo-ts]].
