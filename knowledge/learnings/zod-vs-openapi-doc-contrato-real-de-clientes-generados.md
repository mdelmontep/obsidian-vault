---
title: zod refine no llega a clientes openapi-typescript — actualizar openapi.json en mismo commit
date: 2026-05-05
source: claude-code-session
tags: [api, openapi, zod, contracts]
---

Cambiar el schema Zod del API sin actualizar el handler de `openapi.json` deja un campo "fantasma": el server lo acepta (refine pasa) pero `npx openapi-typescript ...` no lo trae a los clientes generados. Resultado: clientes tienen que usar `as never` para enviar el campo, o no pueden mandarlo en absoluto.

El contrato real para clientes generados es el OpenAPI doc, NO el refine de Zod. Postel's law solo aplica a server-side: para tipar el cliente, el openapi-typescript es la fuente.

**Regla**: todo cambio en Zod del API público debe replicarse en el handler `openapi.json` en el MISMO commit. Si añades un campo opcional (ej. `actor`), añade el `$ref` en CreateXRequest + define el componente en `components.schemas`.

Caso: FacturaIA `actor: { email, name }` aceptado por Zod desde el sprint audit, pero faltaba en `openapi.json` → agency-portal arrastró `as never` durante días sin que se notase en lint/typecheck.
