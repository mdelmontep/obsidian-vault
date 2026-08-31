---
title: un repo coherente consigo mismo no prueba el nombre que vive fuera
date: 2026-08-31
source: elphis-psicologia
tags: [guardianes, prompts, retell, agentes, arnes]
---
El prompt de un agente de voz ordenaba «cuelgas con `end_call`». `end_call` es el
**`type`** de la herramienta en Retell; el modelo solo ve su **`name`**, que era
`colgar`. Y el mismo prompt decía «tienes dos herramientas y solo esas dos»
habiendo **tres** cableadas: negaba justo la de despedirse.

Nada lo veía, y no por descuido:

- El generador comparaba el artefacto con **sus fuentes**, todas del repo.
- El test afirmaba `/Tienes dos herramientas y solo esas dos/` — un número
  **escrito a mano**, así que el test **clavaba el defecto en su sitio**.
- Los dos son coherentes entre sí y con el fichero. **El nombre real solo existe
  en el servicio externo.**

Regla: cuando un artefacto del repo *invoca* algo que vive en otro sistema
(herramienta, cola, tabla, endpoint), el guardián que vale es el que trae la lista
del sistema y la cruza — en los dos sentidos: cableado sin nombrar, y nombrado sin
cablear. Y un número esperado escrito a mano en un test es sospechoso por
definición: **deriva del recuento real o no lo afirmes.**

Familia de [[el-arnes-se-mide-a-si-mismo]] ·
[[un-consumidor-del-shape-puede-vivir-fuera-del-repo]] ·
[[comparar-por-tamano-no-ve-un-artefacto-servido-desde-otra-version]]
