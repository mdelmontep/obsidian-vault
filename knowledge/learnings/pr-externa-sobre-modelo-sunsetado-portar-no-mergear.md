---
title: pr externa sobre modelo sunsetado — portar al nuevo antes de mergear
date: 2026-05-26
source: claude-code-session
tags: [colaboracion, pr-review, arquitectura, deuda-tecnica]
---

Cuando main pivota a una arquitectura nueva mientras hay PR ajena abierta sobre el modelo viejo, lo profesional es portar al modelo nuevo **antes** de mergear, no "mergear y refactor luego".

**Por qué**: mergear introduce inmediatamente dos modelos coexistiendo (endpoints paralelos, envs duplicadas, dos paths que escriben el mismo concepto). La promesa de "refactor luego" se diluye con la siguiente prioridad y queda como deuda.

**Patrón aplicado**: cerrar la PR con link explicativo + rama nueva desde main + portar la idea de UX (no el código) al modelo nuevo + tests + docs en el mismo PR. Mantener el nombre del feature, no la arquitectura.

**Caso real 2026-05-26**: PR #76 TuFacturaIA construida sobre `organizations.settings.email` legacy. Mientras Borja rebasaba, main mergeó `9ce3760` (plataforma de integraciones con `integration_connections`). Se cerró PR76 → PR77 nueva (~3h) con iCloud como provider de la plataforma. Reusa cifrado, registry, endpoints `/api/integrations/*`. Cero envs nuevas. Sin esto: `EMAIL_SECRET_KEY` paralela, `/api/auth/icloud/*` paralela al patrón canónico — deuda inmediata.
