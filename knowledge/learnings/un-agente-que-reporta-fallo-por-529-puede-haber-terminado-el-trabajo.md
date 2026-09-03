---
title: un agente que reporta fallo por 529 puede haber terminado el trabajo
date: 2026-09-03
source: centro-elphis
tags: [claude-code, subagentes, harness, gotcha]
---
- Dos subagentes Opus acabaron en «failed» por sobrecarga de la API (529)… y los dos habían hecho el trabajo: uno reparó un deal real en Clientify (ejecución 11818 en n8n), el otro editó `clientify-create-deal` en producción. El error llegó al redactar el informe, no al empezar.
- Relanzar «porque falló» habría repetido la escritura: segundo PATCH, segundo deal, segunda edición encima de la primera.
- Regla: antes de relanzar un agente que escribe en un sistema externo, medir el sistema (ejecuciones nuevas en n8n, `updatedAt` del workflow, GET del objeto), no el estado del agente. El informe es un canal lateral; el efecto es la verdad.
- Caso inverso, mismo principio: [[agente-cortado-a-media-tarea-deja-trabajo-que-parece-terminado]] · [[subagente-reporta-hecho-codigo-que-no-existe-o-no-compila]]
