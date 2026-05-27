---
title: un gate de rol en un endpoint debe contemplar al superadmin (role=null) o lo bloquea
date: 2026-05-27
source: claude-code-session
tags: [auth, facturaia, withApiAuth, superadmin]
---
Patrón con bypass de superadmin: el middleware/wrapper salta el lookup del rol de org para el superadmin (ya puede operar sobre cualquier org), dejándole `role = null`. Si luego añades un check de rol "extra" en el handler tipo `if (role !== 'propietario' && role !== 'admin') return 403`, **bloqueas justo al superadmin** (null falla ambas comparaciones) — el que más permisos tiene.

Caso TuFacturaIA: el hard-delete del catálogo (`/api/catalogo/productos/[id]`) cortaba al superadmin. `withApiAuth` ya expone `ctx.isSuperadmin`; fix = `if (!isSuperadmin && role !== 'propietario' && role !== 'admin') return 403`.

Regla: cualquier check de rol manual en un handler debe ser `isSuperadmin || role in [...]`. NO uses `role` crudo para autorizar sin contemplar el null del superadmin. Ver [[cifras-derivadas-en-capa-ia-reusan-filtro-canonico]].
