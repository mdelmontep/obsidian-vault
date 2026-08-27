---
title: prohibir una frase dentro de un nodo no cubre lo que se dice al transicionar
date: 2026-08-27
source: centro-elphis
tags: [retell, voz, conversation-flow, prompting]
---
La frase con la que un agente **entra** en un nodo la genera el nodo de ORIGEN, no
el de destino. Una prohibición escrita en la instrucción del nodo destino llega
tarde: el agente ya la ha dicho.

Caso: la versión nueva de Elphis no transfiere llamadas, avisa al equipo. El
"no digas que vas a pasar la llamada" estaba en `recepcion_aviso` y el agente
seguía diciendo *"Te paso ahora mismo con nuestro equipo"* justo antes de entrar.
Igual con "nunca pidas el teléfono", que vivía en un solo nodo y se violaba en otro.

**Las prohibiciones absolutas van al `global_prompt`, nunca a un nodo.** El nodo es
para lo que cambia según dónde estés; lo que no se puede decir NUNCA no depende del
nodo. Y con excepción explícita si la hay (aquí, la frase literal de crisis).
