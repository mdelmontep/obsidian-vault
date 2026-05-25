---
title: ADR-021 — HTML strings tipados para 6 templates email FacturaIA (vs React Email / MJML)
date: 2026-05-25
status: accepted
tags: [adr, facturaia, email, arquitectura]
---

## Contexto

Sprint 2026-05-25 Nivel 1+2 refactoriza 6 templates email transaccional (factura, presupuesto, OTP, team-invite, colleague-invite, change-email) actualmente con HTML hardcoded en cada callsite (`send-factura.ts:188-203`, etc.). Necesitamos: layouts compartidos, type-safety, snapshots, cross-client (Outlook MSO + dark mode + Gmail iOS), zero security regressions (XSS, open redirect).

## Opciones consideradas

- **A** React Email — Tree React + `@react-email/render` con `react-dom/server`. Componentes JSX abstraídos. ~250 KB deps. Editor mental cómodo. Stack ya tiene React 19.
- **B** MJML — Sintaxis declarativa específica de email. Parser/compilador en runtime o build-step. Abstracción primitives sólida.
- **C** HTML strings con helpers tipados — funciones puras `(data) => string` + escape helpers + `TemplateData<K>` discriminated union + snapshots vitest.

## Decisión

**C**, porque:

1. Solo 6 templates, simples (header + body + CTA + footer). Abstracción (A/B) no amortiza.
2. Stack FacturaIA con Dokploy/Alpine/Puppeteer ya tiene fricción Docker — menos deps = menos surface area de fallo en build.
3. Hacks email obligatorios (MSO conditional `<v:roundrect>`, VML buttons, dark-mode `[data-ogsc]` Gmail iOS, tablas Outlook, inline CSS forzado) son más fáciles directo en string que peleando con abstracción.
4. Snapshots vitest diffan output crudo legible en PR review.
5. Helpers `escapeHtml/escapeAttr/escapeUrl` + `buildAppUrl` con host pinning aplican universalmente, no dependientes de framework.

## Consecuencias

- Estructura: `src/lib/email/templates/{types,theme,index,layout/{base,header,footer,button,info-block},emails/<kind>.ts}`.
- Cada email kind: `render<Kind>(data): RenderedEmail = { subject, html, text, preheader, list_unsubscribe? }`.
- **Umbral de cambio**: si llegamos a 30+ templates o admin demanda editor visual → reconsiderar React Email (reduce mantenimiento ~30% en ese rango). MJML descartado siempre — runtime parser frágil.
- Ver [[html-email-strings-tipados-vs-react-email-mjml]].
