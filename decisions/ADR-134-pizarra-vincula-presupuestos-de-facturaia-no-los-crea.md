---
title: ADR-134 — Pizarra vincula presupuestos de FacturaIA, no los crea
date: 2026-10-15
status: accepted
tags: [adr, agency-portal, pizarra, facturaia]
---

## Contexto
Desde el 9-jun el portal no crea presupuestos: los 13 desde junio se hicieron a mano en TuFacturaIA. El PDF de la skill presupuesto-desarrollo numera a mano y choca (P2026-0019 de ORCONSA es de Alba Orgaz en FacturaIA).

## Opciones consideradas
- **A** — Pizarra crea el presupuesto (`quote.draft`) desde la sesión: duplica numeración y flujo; pocas veces se pide.
- **B** — Subir líneas y PDF de la skill a FacturaIA: complejo, y el número seguiría naciendo fuera del ERP.
- **C** — Presupuesto a mano en TuFacturaIA; Pizarra solo lo identifica y vincula (`quote.link`).

## Decisión
**C**, porque el flujo orgánico ya funciona y FacturaIA manda en la numeración. Además: alta de lead nuevo desde un agente = propuesta que confirma una persona; ops sobre leads existentes = automáticas; ganar el trato, siempre humano.

## Consecuencias
El guard del plugin deniega `quote.draft`. `quote.link` exige que el cliente de FacturaIA case con nombre/empresa del prospect; si no, se vincula a mano desde la ficha. Portal #802/#803, plugin #23/#24.
