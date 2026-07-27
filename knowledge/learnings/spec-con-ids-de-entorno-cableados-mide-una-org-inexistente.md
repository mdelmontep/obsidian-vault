---
title: spec con IDs de entorno cableados mide una org que no existe
date: 2026-07-27
source: claude-code-session
tags: [e2e, playwright, testing, sandbox, facturaia]
---

`cierre-cuenta.spec.ts` llevaba `const ORG = 'b5f86e8f-…'` y `const USER = '70346169-…'`, UUIDs de
otra máquina. En el sandbox actual esas filas no existen, así que:
- `facturasCount()` contaba las facturas de una org inexistente → devolvía **0**.
- El `update` que elevaba el usuario a propietario **no tocaba ninguna fila**, en silencio.

O sea que el test no probaba el cierre de cuenta de nadie. Solo se cayó porque había un
`expect(facturasAntes).toBeGreaterThan(0)`; sin ese assert habría pasado en verde. La ruta de
salida de capturas también era absoluta de otro equipo (`/private/tmp/claude-502/…`).

Reglas:
- **Resolver del entorno, nunca cablear**: org por `E2E_ORG_NAME`, usuario por `E2E_EMAIL`, y
  fallar con mensaje claro si no aparecen (`No existe la org "X" en este proyecto Supabase`).
- Rutas temporales con `os.tmpdir()`, jamás absolutas de una máquina.
- Un `update`/`delete` que no afecta filas es un fallo silencioso: si el test depende de que haya
  surtido efecto, comprobar el conteo.
- Verificar los nombres reales de columnas antes de escribir SQL: `profiles` se identifica por
  `user_id`, no por `id`; `billing_accounts` no tiene `org_id` (se une por
  `organizations.billing_account_id`).

Ver [[e2e-smoke-skip-honesto]] · [[locator-de-test-atado-a-la-implementacion-caduca-y-da-falso-verde]]
