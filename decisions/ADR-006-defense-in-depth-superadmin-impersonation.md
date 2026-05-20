---
title: ADR-006 — Override vs union semantics en impersonación de superadmin
date: 2026-05-20
status: accepted
tags: [adr, facturaia, auth, multi-tenant]
---

## Contexto
FacturaIA permite a superadmins impersonar otra org vía cookie `impersonate_org` (set por `?impersonate=`, TTL 1h). 4 sitios consumen esta cookie y la semántica correcta no es la misma en todos.

## Opciones consideradas
- **Override en todo** — la cookie reemplaza siempre la org propia. Simple, pero superadmin pierde acceso a sus propios recursos hasta que la cookie expire (causa del Forbidden 2026-05-20).
- **Union en todo** — la cookie añade. Seguro, pero rompe el "ver lo que ven ellos" del dashboard (verías datos mezclados de ambas orgs).
- **Mixta por capa** — override en contexto de visualización, union en autorización pura.

## Decisión
**Mixta por capa**, porque cada sitio tiene un propósito distinto:
- `with-api-auth.ts`, `(dashboard)/layout-server.tsx`, `render-pdf/route.ts` → **override** (intención: ver/operar como ellos).
- `/api/documents/file` → **union** (intención: autorizar lectura del bucket; no hay contexto que sustituir).

## Consecuencias
- Nunca un superadmin pierde acceso a sus propios PDFs por cookie pegada.
- Cualquier endpoint nuevo que consuma `impersonate_org` debe declarar explícitamente qué semántica usa (comentario o helper compartido).
- Pendiente: helper `resolveAccessContext({ ownership: 'strict-override' | 'union' })` para forzar la decisión consciente.
