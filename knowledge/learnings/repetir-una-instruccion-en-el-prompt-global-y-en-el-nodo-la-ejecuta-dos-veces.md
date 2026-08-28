---
title: repetir una instrucción en el prompt global y en el nodo la ejecuta dos veces
date: 2026-08-28
source: centro-elphis
tags: [llm, prompting, retell, conversation-flow]
---
En un prompt jerárquico (global + nodo), poner la misma acción en los dos sitios no la
refuerza: **la ejecuta dos veces**. En Elphis la fórmula de consentimiento RGPD estaba en
el `global_prompt` y en el nodo `Consentimiento`, y Laura lo pedía dos veces seguidas en
la misma llamada. Caído dos veces en dos sesiones distintas, las dos "reforzando".

Patrón: la **acción** vive en un solo sitio —su nodo—, y el prompt global solo dice
**dónde** pasa: «ES ALLÍ donde se pide; aquí no formules tú ninguna versión de la
pregunta». Lo mismo para cualquier frase con turno propio.

Corolario de auditoría: cuando quites una instrucción de un nodo, `grep` de la frase en el
prompt global y en los nodos vecinos antes de dar el cambio por hecho — el eco literal
sobrevive donde no lo buscas.
