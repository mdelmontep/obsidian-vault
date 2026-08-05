---
title: la reparación conversacional tiene nombre canónico y los frameworks la traen de serie
date: 2026-08-06
source: claude-code-session
tags: [agentes, voz, dialogo, pragmatica, arquitectura]
---
Cuatro defectos de dos llamadas reales resultaron ser **tres categorías canónicas** de un problema que
la industria trata como resuelto: **digresión · corrección · cancelación**. Rasa las envía **por
defecto** bajo el nombre *Conversation Repair*; **ISO 24617-2** (*SemAF: Dialogue acts*) estandariza los
actos de diálogo y su concepto central es la **multifuncionalidad** (un enunciado ejerce varias
funciones a la vez); y la teoría del «vuelvo a lo que decía» es **Grosz & Sidner 1986**: pila de
espacios de foco, *push* al abrirse un propósito subordinado y *pop* al satisfacerse.

Los síntomas y su nombre: «Sí, añade Pablo…» perdiendo las dos cosas = multifuncionalidad · «y ahora lo
de la reunión» = digresión y reanudación · «no, sí, sí que estaba bien» = reparación en tercera posición
· «no, está bien» ejecutado como cancelar = **acto indirecto** (forma negativa, fuerza afirmativa).

**El tell estructural, y es el que sirve para diagnosticar rápido: un slot no es una pila.** Si el
estado guarda «lo pendiente» como UN lote (`pending: ProposedWrite[]`), una intención retenida **no
tiene dónde ir** — así que cada forma de reanudación hay que enumerarla a mano, y se acumulan reglas
(nos pasó cinco veces: #411, #586, #647, #535-G1, #937-#939). Con pila, «retener → resolver → reanudar»
es el comportamiento por defecto.

Corolario de redacción: **no formular preguntas polares en negativo** («si algo NO es correcto, dime…»)
— induce respuestas que empiezan por «no» y luego las malinterpretas. Es *organización de preferencia*
en análisis conversacional y *sesgo de aquiescencia* en encuestas.
