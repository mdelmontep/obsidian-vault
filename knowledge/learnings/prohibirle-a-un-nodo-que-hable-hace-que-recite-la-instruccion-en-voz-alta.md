---
title: prohibirle a un nodo que hable hace que recite la instrucción en voz alta
date: 2026-08-29
source: centro-elphis
tags: [retell, prompting, agentes-de-voz]
---
Para quitar la doble despedida (el nodo `cierre` se despedía y `despedida` volvía a despedirse) le
puse a `cierre`: «NO te despidas tú, no digas adiós». El modelo, que en ese nodo tiene que producir
turno sí o sí, en vez de callar **narró su razonamiento al paciente**:

> «(El registro salió bien. Ya he dicho que el equipo la llamará. Marta acaba de decir "Gracias por
> llamar", que es una despedida clara. Según las instrucciones: "Si el usuario dice que no necesita
> nada más o se despide: NO te despidas…»

- Una prohibición no le da nada que decir. Si el nodo habla por diseño, hay que darle **contenido
  alternativo**, no una negación.
- Y si lo que sobra es el turno entero, el arreglo es **estructural** (arista que salte el nodo),
  nunca una instrucción: el prompt no puede hacer que un nodo hablante se calle.
- Medido además: la doble despedida no la causaba ese nodo (control 3/45, con el parche 2/27). El
  parche atacaba un defecto que no estaba donde yo creía, y de paso introdujo este.

Ver [[dato-en-bloque-de-contexto-se-lee-en-voz-alta-aunque-no-este-en-el-guion]] y
[[las-frases-entrecomilladas-de-un-prompt-son-un-guion-que-el-modelo-recita]].
