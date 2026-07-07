---
title: verificación adversarial de N lentes — triar cada hallazgo por QUÉ lente lo refuta
date: 2026-07-07
source: AGH auditoría Tier 3 agente Carlos
tags: [meta, audit, multi-agent]
---

Segunda fase que mejora la criba manual del ~50% de [[audit-3-agentes-paralelos-detecta-vulnerabilidades-cross-sprint]]: tras los finders paralelos, pasa CADA hallazgo por 3 verificadores adversariales con lentes distintas — (1) ¿reproduce en el código/esquema real?, (2) ¿un guard/test/constraint/RLS/issue ya lo cubre?, (3) ¿impacto real para el producto? Sobrevive si <2/3 lo refutan. Cada verificador lee el código, escéptico por defecto.

Triaje por QUÉ lente refuta (el patrón que emergió, limpio):
- **0 refutan** → fuerte, filar issue individual. Suelen ser los medium/high.
- **Refutado SOLO por la lente de impacto** (hechos de código correctos, pero código muerto/path inalcanzable/teórico para el producto actual) → NO es urgente. Bundlea por tema + encuadre honesto "latente/defense-in-depth", nunca como bug urgente.
- **Refutado por reproduce/cobertura** → falso positivo, descartar.

Reglas duras: NO filar contra comportamiento **documentado como intencional** (un comentario en el código que asume el tradeoff = decisión tomada, no bug). Verificar tú mismo los 1-2 de mayor severidad antes de filar (evidencia > confianza en el agente). Da el falso-positivo descartado con su razón — es señal de que la verificación funciona.
