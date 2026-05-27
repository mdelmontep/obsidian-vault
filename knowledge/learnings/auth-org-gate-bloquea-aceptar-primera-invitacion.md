---
title: middleware que exige org activa bloquea el endpoint de aceptar la 1ª invitación
date: 2026-05-27
source: claude-code-session
tags: [auth, multi-tenant, onboarding, facturaia]
---

Un middleware de auth que exige org activa (FacturaIA `withApiAuth` → `getOrgId`)
bloquea el propio endpoint que concede la primera org: el invitado a su 1ª org
tiene membresía `invitado` (no `activo`) → `getOrgId`=null → 401 "no org" antes
del handler → huevo-y-gallina, no puede aceptar nunca. Lo tapaba otro bug que
impedía siquiera llegar a la página.

Fix: bypass explícito del gate org (opción `allowNoOrg`) solo en endpoints de
onboarding pre-org; el handler deriva la org de su propio input (body) y solo
muta lo propio (promueve su membresía). Tras aceptar (`estado='activo'`),
`resolveActiveOrg` ya resuelve la org normal.

2ª vez que el flow de invitación tiene un pre-org chicken-and-egg →
[[rls-org-members-select-debe-incluir-own-memberships]].
