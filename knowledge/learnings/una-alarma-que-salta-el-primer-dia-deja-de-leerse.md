---
title: una alarma que salta el primer día con todo deja de leerse para siempre
date: 2026-07-31
source: claude-code-session
tags: [monitorizacion, metodo, ux, verificacion]
---

Al estrenar una comprobación hay un estado transitorio —arranque en frío, backfill, primer
despliegue— en el que lo comparado **no es comparable todavía**. Si la alarma no lo modela,
dispara con todo el universo el día uno.

Caso (cryptobruj-bot): la conciliación reportó *"el bot abrió 46 operaciones que la
referencia NO haría — la lógica viva no es la que se midió"*. Falso. Al ver cada símbolo por
primera vez el bot está plano y **adopta** el estado en curso; la referencia, recorriendo el
histórico, entró cuando ese estado empezó. No casan por fecha porque uno empezó a mirar más
tarde, no porque nadie se equivocara.

Fix: excluir la **primera** observación de cada clave, contarla aparte (`adopciones`) y, si
solo hay de esas, devolver un estado propio que lo **explique** en vez de acusar.

Lo que está en juego no es la falsa alarma: es que después nadie mira la alarma el día que
sí pasa algo — y este módulo existía precisamente porque tres fallos caros no se vieron a
tiempo. Misma familia: un límite silencioso (top-N, muestreo) debe **decir** que recortó, o
se lee como "revisado todo".
