---
name: signOut-solo-invalida-refresh-no-access-token
description: Supabase Auth Admin signOut() recibe el JWT de una sesión, NO un userId (con un id devuelve error y no cierra nada); y aun con JWT solo revoca refresh tokens, el access token vive hasta expirar (~1h).
date: 2026-05-20
updated: 2026-09-24
source: facturaia
tags: [supabase, auth, jwt]
---

**Corregido el 24-sep-2026.** Esta nota decía que `admin.auth.admin.signOut(userId)` revocaba los refresh tokens del usuario. Es falso. El primer argumento es el **JWT de una sesión**. Con un id **devuelve** `{ error }` sin lanzar, así que no cierra nada y un `try/catch` no se entera. Así estuvo roto el «No fui yo» de facturaia hasta el #2910 (PR #2916): prometía echar al intruso y lo dejaba dentro.

- **Cerrar las sesiones de un usuario por su id, sin tener su JWT** (por ejemplo, un enlace abierto desde un correo): borrar sus filas de `auth.sessions`. Los refresh tokens caen por la cascada `refresh_tokens_session_id_fkey`. En facturaia lo hace la RPC `auth_cerrar_sesiones_usuario` (mig 935, SECURITY DEFINER, solo service_role).
- **Con el JWT de la petición**: `signOut(jwt, 'others' | 'global')`. Hay que comprobar el `error` devuelto.
- Candado en facturaia: `src/lib/auth/__tests__/signout-admin-recibe-un-jwt.test.ts`.

**Lo que sigue siendo cierto:** incluso bien llamado, solo se revocan los refresh tokens. El access token JWT sigue válido hasta que caduca (~1h). Síntoma: tras revocar la membresía, un usuario con el JWT vivo entra en bucle `/login` ↔ `/dashboard`. Arreglo: la página `/sin-acceso` para autenticados sin org operable. Ver [[ADR-007-sin-acceso-fallback-vs-loop-redirect]] y [[matriz-permisos-rol-aware-bd-mas-espejo-ts]].
