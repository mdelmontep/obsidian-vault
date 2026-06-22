---
title: intl.numberformat agrupa distinto en node (icu) vs browser — no aseverar el string en tests
date: 2026-06-22
source: claude-code-session
tags: [testing, vitest, intl, i18n]
---
`new Intl.NumberFormat('es-ES', {style:'currency'}).format(1250)` da "1.250 €" en
el browser pero "1250 €" en Vitest/Node (ICU sin full-icu / build sin grouping
es-ES). Un test que aseveraba `toContain('1.250')` falla solo en CI/Node aunque
el código es correcto.
Fix: en tests no aseverar el string formateado completo. Aseverar el dato crudo
(`expect(item.count).toBe(1250)`) y, como mucho, la presencia del símbolo
(`expect(item.display).toMatch(/€/)`). Igual para fechas con `Intl.DateTimeFormat`.
