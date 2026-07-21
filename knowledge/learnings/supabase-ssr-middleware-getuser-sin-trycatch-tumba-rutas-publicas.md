---
title: middleware Next.js con @supabase/ssr sin try-catch en getUser() tumba también rutas públicas
date: 2026-07-21
source: claude-code-session
tags: [nextjs, supabase, middleware, auth, resiliencia]
---
El patrón estándar de `@supabase/ssr` en middleware llama
`supabase.auth.getUser()` ANTES de comprobar si la ruta es pública o
protegida (para poder resolver la sesión de una sola vez). Si esa llamada
lanza (timeout/error de red a GoTrue), la excepción sube sin control y
tumba con 500 no manejado TODA request que pase por el middleware —
landing pública, legales, todo — no solo el login, porque el fallo ocurre
antes del branch público/protegido.

Fix barato: envolver en try-catch y, si falla, tratar como "sin sesión"
(`user = null`). Esto reutiliza gratis la lógica existente de rutas
públicas/protegidas: fail-open en públicas (siguen sirviendo), fail-closed
en protegidas (redirect a login) — sin necesitar categorización de errores
ni retry (GoTrue ya reintenta internamente, y la siguiente request del
usuario lo resuelve en segundos).

Detectado auditando el proyecto contra un post genérico de terceros sobre
error-handling en middleware de Supabase — el único gap real de 4 temas
auditados (RLS recursión/silent-failures y N+1 ya estaban resueltos).
