---
title: las frases entrecomilladas de un prompt son un guion que el modelo recita
date: 2026-08-28
source: centro-elphis
tags: [llm, prompting, voz, retell, prompt-engineering]
---
Una frase de ejemplo escrita entre comillas dentro de un prompt **deja de ser ejemplo**:
el modelo la reproduce literal, llamada tras llamada. El síntoma que ve el cliente no es
"suena mal", es «no da conversación»: *hola-problema-etiqueta-cita-fin*, siempre igual.

Medido en el agente de voz de Elphis sobre 21 llamadas simuladas por configuración,
contando turnos que reproducen una frase del prompt palabra por palabra: **32,6 % con las
comillas → 18,2 % sin ellas**. Bajar el guion pesó más que cualquier ajuste de modelo o
temperatura ([[subir-la-temperatura-de-un-agente-de-voz-le-rompe-el-enrutado]]).

Patrón: quitar las comillas y decir en cabecera que **son cosas que hay que transmitir, no
un texto que recitar** («si te sale la misma construcción dos veces, no la estás
construyendo, la estás copiando»). Y declarar la lista corta de excepciones que SÍ van
literales — aviso legal de IA, frases de crisis, fórmula de consentimiento — o el modelo
también improvisa esas.
