---
title: Self-fetch entre API routes falla en Docker prod — extraer a lib
date: 2026-06-15
source: FacturaIA — importación inventario (commit 0f34e135)
tags: [nextjs, docker, dokploy, api, antipattern, facturaia]
---

Un API route que hace `fetch(\`${process.env.APP_URL}/api/otra-ruta\`)` a sí mismo
**falla dentro del contenedor Docker** (hairpin NAT / DNS interno): la petición sale
al dominio público y no vuelve. Síntoma: el endpoint "no hace nada" (en la importación
de inventario daba `0 importados / N errores`), sin error claro.

Trampa: en local puede fallar por `APP_URL` sin setear y parecer un problema de
entorno → asumes que "en prod funciona". **NO. En prod (Docker) está igual de roto.**

Fix: extraer la lógica compartida a una **lib** y llamarla directa (sin HTTP). El
gate de auth/rol que daba el endpoint interno hay que replicarlo en el caller
(`requireWrite` + guard de miembro activo si la lib usa admin client / bypass RLS).

Regla: **siempre smoke en PROD, no solo local** — un fallo "local" puede ser un bug
de prod disfrazado. Ver inviolable CLAUDE.md "no fetch a sí mismo entre API routes".
