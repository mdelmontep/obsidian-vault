---
title: un plan que hereda patrones de un repo hermano da por existente lo que solo existe allí
date: 2026-08-07
source: claude-code-session — TuCRMIA, 3 CVE graves que encontró Borja y no el arnés
tags: [gates, planificacion, deuda-tecnica, tucrmia, facturaia]
---
El plan de TuCRMIA citaba en P8 «patrón ya reusado 3× (inline-style, design-debt,
npm audit)» y en `research/10:221` especificaba `audit-ratchet.mjs` con su baseline.
Las dos frases eran **ciertas sobre TuFacturaIA** (`facturaia/scripts/audit-ratchet.mjs`
y `.audit-baseline.json` existen) y se copiaron al plan del repo nuevo como si lo
describieran a él. Se portaron dos trinquetes y no el tercero, y el documento siguió
contándolos en pasado: 46 días con `npm audit` fuera de los 34 gates, y las tres
vulnerabilidades graves las encontró una persona corriendo `npm` a mano.

La señal: **«ya reusado N veces» describe el repo ORIGEN**, no éste. Un plan heredado
mezcla inventario (lo que hay allí) con propósito (lo que queremos aquí) y la frase se
lee igual en los dos casos.

Fix: al portar de un repo hermano, cada mecanismo dado por existente necesita una
comprobación **ejecutable** en el destino (`ls scripts/`, `npm run <gate>`), no una cita
al documento. Es barato y es lo único que distingue heredado de escrito.

Relacionado: [[trinquete-baseline-bloquea-solo-lo-nuevo-patron-reusable]] ·
[[una-decision-pendiente-sin-issue-no-esta-en-ninguna-cola]]
