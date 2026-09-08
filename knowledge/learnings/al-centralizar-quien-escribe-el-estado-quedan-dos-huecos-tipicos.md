---
title: al centralizar quién escribe el estado del lead quedan dos huecos típicos
date: 2026-09-09
source: clinica-zen
tags: [kommo, n8n, crm, diseño]
---
Aplicar [[el-nodo-que-envia-el-mensaje-no-debe-escribir-la-etapa-del-lead]] —un solo nodo escribe la
etapa, con lista de etapas intocables— deja dos agujeros que hay que buscar a propósito:

1. **La lista se escribe pensando en el camino feliz.** La de Clínica Zen protegía «ganado» y no
   «Perdido»: un paciente CANCELA, otro workflow marca Perdido, y el siguiente mensaje del bot
   resucita el lead a Contestados 37 s después. Al escribir la lista, enumerar los cierres
   NEGATIVOS primero — son los que no vienen a la cabeza.
2. **El otro workflow.** Centralizar dentro de un workflow no impide que OTRO escriba el mismo campo
   en el mismo evento de negocio. Aquí el sub-workflow de reserva escribía «Contestados» mientras el
   guard escribía «Pendiente de asignar»: salía bien solo por orden de llegada. `grep` del id de
   estado en TODOS los workflows, no solo en el que estás tocando.

Y para fechar quién escribió qué, leer el `workflowData` incrustado en la EJECUCIÓN, no el workflow
vivo: el vivo es de hoy y el evento es de ayer. Ver [[clinica-zen]]
