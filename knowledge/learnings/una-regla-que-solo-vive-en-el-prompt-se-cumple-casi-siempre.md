---
title: una regla que solo vive en el prompt se cumple casi siempre, y «casi» es el problema
date: 2026-08-18
source: learn-agentesia
tags: [llm, prompts, gates, metodo, agentes]
---

El prompt declaraba, como **«la regla que manda sobre todas las demás»**, que ninguna palabra técnica podía aparecer antes de explicarla. Se publicó una lección titulada *«Cuándo grep deja de buscar»* para alguien que no sabe qué es grep.

**Y el modelo no desobedeció.** Obedeció a otra entrada: el temario, cuyos títulos ya traían la jerga puesta —11 de 19—. Un prompt compite con el resto del contexto; el dato sucio gana.

**Las dos capas que faltaban, y por qué las dos:**
1. **Validar la salida** — rechazar el resultado si incumple. Aquí, el título con jerga hace fallar el parseo y el trabajo se reintenta.
2. **Validar la ENTRADA** — si lo que se le da al modelo ya viene sucio, la salida sale sucia por obediencia. Esta es la que casi nadie pone y es la que falló.

**Regla.** Si una instrucción del prompt importa de verdad, tiene que existir un comprobador determinista que la mida. Lo que solo está escrito se cumple el 90 % de las veces, y el 10 % restante se publica.

**Al escribir el comprobador**, cuidado con el falso positivo: comparar por palabra completa (no por subcadena: «api» marcaba *rápido*) y dejar pasar el caso legítimo —«Qué es una API REST, explicada como…» **presenta** el término—. Un guard que denuncia lo bueno se acaba desactivando.

Ver [[una-obligacion-legal-no-puede-colgar-del-prompt-del-llm]] · [[un-guard-que-decide-por-mencion-bloquea-lo-que-solo-nombra-el-comando-caro]]
