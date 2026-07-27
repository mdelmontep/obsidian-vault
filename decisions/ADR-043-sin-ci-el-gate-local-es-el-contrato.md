---
title: ADR-043 — sin CI, el gate local es el contrato y los workflows dejan de arrancar solos
date: 2026-07-28
status: accepted
tags: [adr, facturaia, ci, proceso]
---

## Contexto

GitHub Actions no ejecuta nada en el repo de TuFacturaIA: los jobs mueren en
segundos con "recent account payments have failed". No se va a desbloquear. El
efecto medido: **235 PRs y 265 commits** entraron a `main` en 8 días con cuatro
checks en rojo por PR, ninguno significativo. Además, dos mitigaciones de
incidentes pasados viven DENTRO de Actions (`deploy-mcp.yml` y el cron del
watchdog) y por tanto tampoco corrían — el desfase del MCP volvió a producirse.

## Opciones consideradas

- **A. Dejarlo como está** — cero trabajo, pero el rojo permanente entrena al
  equipo a ignorar el rojo, y el día que uno sea real nadie lo mirará.
- **B. Runner self-hosted en el VPS** — devolvería el CI sin consumir minutos,
  pero no está verificado que el bloqueo sea por gasto y no una suspensión de
  cuenta; y añade una pieza de infra que mantener.
- **C. Asumir que no hay CI y hacer del gate local el contrato** — retirar los
  disparadores automáticos, mover a scripts lo que dependía de Actions y reforzar
  los hooks.

## Decisión

**C.** Los workflows se conservan enteros pero pasan a `workflow_dispatch` con su
disparador original comentado dentro; el deploy del MCP se convierte en
`ops/deploy-mcp.sh`; el `pre-push` gana el check de deriva del grafo de
dependencias; y se añade `npm run gate` (lint + typecheck + tests + build) como
paso previo a mergear. Todo documentado en `gotchas.md` §Repo y deploy.

## Consecuencias

- El único gate real son los hooks: `--no-verify` pasa a ser saltarse TODA la
  verificación, y hay que comprobar `git config --get core.hooksPath`.
- Se queda **sin cubrir a sabiendas**: CodeQL (análisis estático de seguridad) y
  la regresión visual del design-system.
- Tras tocar el MCP hay que desplegarlo a mano; si no, prod sirve la imagen vieja
  sin avisar.
- Reversible: restaurar el CI es descomentar los bloques `on:` de cada workflow.
- No sustituye a B. Si algún día se prueba el runner self-hosted, este ADR se
  revisa.

Ver [[actions-sin-billing-hooks-locales-unico-gate]] ·
[[dokploy-autodeploy-false-desfase-silencioso]]
