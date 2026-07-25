---
title: al cambiar de qué campo sale un importe, borra el viejo del tipo en vez de convivir
date: 2026-07-25
source: claude-code-session facturaia
tags: [typescript, refactor, dinero, migracion-de-datos]
---

Cuando un cálculo pasa a leer otro campo (`total` → `importe_cobrable`), la
tentación es añadir el nuevo y dejar el viejo en el tipo "por compatibilidad".
Eso deja al consumidor olvidado compilando y equivocándose en silencio.

**Borra el campo viejo del tipo/interfaz.** El compilador enumera entonces todos
los consumidores, incluidos los que no salen en tu traza mental ni en el grep.

Caso real TuFacturaIA: quitar `total` de `FacturaElegible`/`RemesaSourceLine`/
`CandidataRow` destapó `api/modules/[id]/metrics/route.ts:432`, que sumaba el
bruto en la métrica "total domiciliable" del panel SEPA. No apareció en ninguna
de las trazas ni lo vieron los agentes que auditaron el flujo.

Corolario: el grep encuentra los usos que sabes nombrar; el tipo encuentra los
que no. Con dinero, la diferencia es un cobro indebido.

Relacionado: [[importe-fiscal-no-es-importe-a-cobrar-retenciones]] · [[campo-huerfano-shape-sin-migracion-paralela]]
