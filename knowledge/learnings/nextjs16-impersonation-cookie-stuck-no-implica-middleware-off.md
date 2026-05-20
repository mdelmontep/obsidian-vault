---
title: cookie de impersonación pegada no implica middleware caído
date: 2026-05-20
source: claude-code-session
tags: [nextjs, auth, impersonation, debugging, supabase]
---

## Síntoma
Superadmin ve `Forbidden` en endpoint con cookie `impersonate_org` activa.

## Falsa hipótesis
"El middleware no se está ejecutando, por eso la cookie no se limpia."

## Causa típica real
1. La función que resuelve orgs permitidas tiene **override semantics**: si hay cookie → devuelve SOLO la org impersonada. El superadmin pierde acceso a sus propias orgs.
2. La cookie tiene `maxAge: 3600s` (1h). Tras impersonar legítimamente y volver a otra ruta, el middleware la borra al cabo de la siguiente navegación — pero hasta entonces hay 0-3600s donde el endpoint la ve.

## Cómo discriminar antes de tocar middleware
- Query `org_members` y `profiles.is_superadmin` para el user → si es superadmin con cookie set, **siempre** sospechar override semantics primero.
- Grep `resolveAllowedOrgIds` / `effectiveOrgId` / `cookieStore.get('impersonate_org')` → ver si hay `new Set([impersonate])` (override) vs `ids.add(impersonate)` (union).
- Si el middleware existe y `proxy.ts`/`middleware.ts` están en el sitio correcto, asumir que se ejecuta.

## Fix
En endpoints de autorización pura (lectura bucket, etc.) → union. En endpoints de contexto de visualización → override. Ver [[ADR-006-defense-in-depth-superadmin-impersonation]].
