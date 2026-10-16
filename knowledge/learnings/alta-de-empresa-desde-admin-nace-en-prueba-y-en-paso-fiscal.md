---
title: una empresa creada desde /admin nace en prueba de 14 días y en el paso fiscal
date: 2026-10-16
source: facturaia (alta de las empresas de Gonzalo)
tags: [facturaia, admin, billing, onboarding, operativa]
---
`POST /api/admin/orgs` crea la org con `billing_status='trial'` (14 días), `complimentary=false` y `onboarding_current_step='fiscal'`, y solo guarda nombre, NIF y teléfono: **la dirección no entra** (tampoco por el PATCH admin, que es `.strict()`).

Para un cliente de cortesía, la receta completa:
1. `POST /api/admin/orgs` con el email del usuario: si la cuenta ya existe, entra como miembro `activo` sin correo.
2. `PATCH /api/admin/orgs/[id]` `{complimentary:true, complimentary_reason:'beta'}` y `PUT .../billing` `{new_status:'active'}`. Sin esto, la empresa se bloquea al vencer la prueba.
3. Dirección: Ajustes → Empresa como miembro, nunca impersonando (ver punto 5 de [[impersonacion-superadmin-no-sirve-para-qa-de-ui-org-scoped]]). El 16-oct se hizo con PostgREST y service role, fusionando `template_config.emisor` y la columna `direccion`.
4. Dar acceso a una org que ya existe: `POST .../members` con `mode:'create'` reutiliza la cuenta y da `activo` sin correo; `invite` deja `invitado` y manda correo.

El propietario verá el paso fiscal (NIF, IRPF, «Configurar después») la primera vez que entre. Es a propósito: confirma el NIF.
Gotcha: un `fetch` desde agent-browser recién logueado puede devolver un 403 de Cloudflare («Just a moment»). Basta con abrir una página del panel antes.
