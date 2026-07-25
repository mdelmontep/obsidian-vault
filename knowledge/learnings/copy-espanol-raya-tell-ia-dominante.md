---
title: en copy español la raya (—) es el tell de IA dominante; de-slop quirúrgico, no find-replace
date: 2026-07-18
updated: 2026-07-25
source: claude-code-session
tags: [copy, ux-writing, español, ia-slop, facturaia]
---

Al limpiar copy de cara al cliente para que no "grite IA": las frases-plantilla clásicas
("sin esfuerzo", "descubre", "no solo… sino", triples) suelen estar casi ausentes. El tell
real y masivo es el **em-dash (—)**:

1. Como **remate dramático** ("frase normal — golpe final"). Es la firma.
2. Con **espacios a ambos lados (" — ")**: convención inglesa; en español el inciso va pegado
   (`—inciso—`). Ese espaciado es en sí anglicismo de máquina.
3. Por **densidad** (raya en casi cada párrafo).

NO hacer find-replace ciego: la raya es puntuación legítima y hay usos intocables →
placeholder `'—'` de celda vacía, separadores de título/asunto, comentarios de código,
prompts al LLM, docs dev (openapi), manuales internos, joins de dato `${a} — ${b}`, y
**texto legal impreso en documento con efectos fiscales** (citas normativas de una factura:
6 años de retención, el receptor B2B espera el literal → ganancia de estilo nula, riesgo
asimétrico). Romperlos = destructivo.

**Barrer `.ts` además de `.tsx`** (25-jul): labels de opción, catálogos de módulos y
plantillas de mensaje viven en `.ts`; solo-`.tsx` deja la misma pantalla a dos estilos.

Fix quirúrgico (conserva sentido): 2 frases → punto · `término — desc` → dos puntos ·
inciso → coma/paréntesis · contraste → punto y coma. Aislar prosa renderizada del código
con grep antes de tocar. Guardarraíl reusable: `docs/architecture/copy-humano.md` +
inviolable en CLAUDE.md del proyecto. Aplica a TODOS los clientes (copy español).
Verificar sin E2E → [[verificar-refactor-de-copy-sin-e2e-grepeando-el-diff]]. Distinto de [[2-agentes-humanos-paralelos-detectan-jerga-tecnica-en-copy]] (eso es criticar
jerga con agentes-persona; esto es el criterio mecánico anti-slop).
