---
title: en un smoke de prod, ?org_id= no abre páginas de un sector que la org activa no tiene
date: 2026-10-04
source: facturaia
tags: [facturaia, smoke, superadmin, impersonation, qa]
---

Superadmin con `?org_id=<sandbox Obras>` en `/obras/*` da **404**: `?org_id=` lo leen los endpoints (`effectiveOrgId`), pero el layout de la página decide por la org activa, que no tiene el sector Obras.
Para QA visual sin `switch-org`: `?impersonate=<org_id>`, que solo pone la cookie `impersonate_org` en ESE navegador (caduca en 1 h; salir con `/api/admin/exit-impersonation`). La org activa de la cuenta compartida no cambia.
Cerrar la sesión de agent-browser al acabar: si el perfil de auth persiste cookies, el siguiente smoke arranca suplantando.
Tema: sembrar `af-theme` (y el legacy `af-tema`) y comprobar `dataset.theme`, ver [[dos-capturas-identicas-byte-a-byte-es-que-el-tema-no-cambio]]. Relacionado: [[endpoints-impersonate-por-query-no-cookie]], [[cookie-impersonate-leak-fuera-de-admin]].
