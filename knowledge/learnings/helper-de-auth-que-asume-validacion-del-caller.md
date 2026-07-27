---
title: un helper de auth que asume "el caller ya validó X" es una fuga esperando a ocurrir
date: 2026-07-27
source: claude-code-session
tags: [auth, multi-tenant, security, rls, refactor]
---

`effectiveOrgId()` (facturaia) devolvía el `?org_id=` recibido **sin validar nada**, y su docstring lo justificaba: "uso típico: endpoints bajo `/api/admin/*` que YA validaron `requireAdmin()`". El helper no tenía consumidores; su único consumidor natural, `/api/render-pdf`, se había escrito una copia local que SÍ comprobaba `isSuperadmin()`.

El mapa de dependencias recomendaba "unificar: que render-pdf importe el canónico y borre la copia". Hacerlo habría abierto una **fuga cross-org**: el GET de `render-pdf` solo exige sesión, y luego filtra con `createAdminClient()`, que salta RLS → cualquier usuario autenticado leería facturas de otra org pasando su UUID.

Reglas:
- El gate va **dentro** del helper, no en la disciplina del que llama. Un docstring no es un control de acceso.
- Cuando dos implementaciones divergen, **la más restrictiva suele ser la correcta**. No unifiques hacia la canónica por ser la canónica: compara semántica línea a línea antes.
- Un helper con **cero consumidores** es el mejor momento para arreglarle el contrato: no hay nada que regresionar.
- Señal de alarma: helper de auth + `createAdminClient()` aguas abajo. Ver [[defense-in-depth-estado-activo-cuando-admin-client-bypasa-rls]] y [[gate-en-wrapper-web-no-cubre-canales-con-otro-auth]].
