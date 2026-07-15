---
title: dokploy compose.deploy del mismo commit es no-op (no recrea el contenedor); cambiar el SHA fuerza la recreación
date: 2026-07-15
source: claude-code-session
tags: [dokploy, deploy, facturaia, debugging]
---
Perseguí un "deploy que no aplica el código" durante ~1h. Realidad:
- `deployments[]=done` NO garantiza que el contenedor corra ese código
  (gotcha ya conocido: verificar por comportamiento, no por `deployments[]`).
- Un `compose.deploy` manual del **mismo commit** que ya está desplegado es un
  **no-op**: no reconstruye ni recrea el contenedor (`docker ps` seguía mostrando
  el contenedor viejo, misma antigüedad). Perdí tiempo esperando un swap que
  nunca iba a pasar.
- Lo que SÍ fuerza recreación: un **commit nuevo** (SHA distinto) → el auto-deploy
  reconstruye y recrea. Un fix trivial extra basta.

Para diagnosticar "¿mi código está vivo?" sin adivinar: `ssh` + `docker ps`
(antigüedad del contenedor) y `docker exec … grep <literal-de-string>` en
`/app/.next/server/chunks` (los nombres de función se minifican, los string
literales no). Y si el código SÍ está pero falla → reproduce la query por el
mismo cliente contra prod, no asumas que es el deploy. Ver
[[reference-dokploy-facturaia]] · [[column-list-drift-clientes-proveedores-select-inexistente-42703]].
