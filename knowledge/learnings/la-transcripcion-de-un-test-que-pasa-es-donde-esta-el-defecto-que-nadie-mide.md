---
title: la transcripción de un test que pasa esconde el defecto que nadie mide
date: 2026-08-27
source: centro-elphis
tags: [testing, agentes-voz, prompting, metodo]
---
Un test de agente solo comprueba sus `metrics`. Todo lo demás que ocurra en la
conversación pasa en verde aunque sea justo lo que enfada al usuario.

Elphis: 8 de 9 casos en verde. Leyendo las transcripciones apareció que el agente
**no dejaba colgar**: ante "gracias, que tengas un buen día" respondía *"Espera un
momento, antes de que cuelgues…"* y volvía a ofrecer la cita — cuatro veces
seguidas en un caso. No lo pedía ningún prompt; el LLM improvisa retención
comercial si nadie se lo prohíbe. Era literalmente la queja del cliente
("desespera"), y ninguna métrica la habría visto nunca.

**Método: en un agente conversacional, leer 2-3 transcripciones completas de casos
que PASAN, cada tanda.** Las métricas cubren lo que ya sabías que podía fallar.
