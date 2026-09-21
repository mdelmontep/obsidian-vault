---
title: un flag encendido contra el defecto del código se busca antes de llamarlo fallo
date: 2026-09-21
source: agh-iberica
tags: [metodo, prod, flags, premisas-falsas, rgpd]
---
AGH 21-sep. Una sonda sobre prod dio `LANGFUSE_TRACE_CONTENT=true`, y el código lo documenta como «OFF by default». Lo publiqué en Slack como **fuga** («el contenido sale del perímetro»). Era falso por partida doble. Langfuse es self-hosted en el mismo host. Y el flag **se encendió a propósito el 11-jul**, con la decisión anotada. **Tercera vez** que alguien re-descubre ese flag como problema: la memoria del host ya contaba dos auditorías desviadas igual.

**Patrón:** un valor de prod distinto del defecto del código es un **hallazgo sin clasificar**, no un fallo. Antes de publicarlo:
1. `vault-find` y `grep` en la memoria del proyecto del nombre del flag;
2. `git log -S` del nombre en el repo y en el runbook de despliegue;
3. mira dónde va el dato (¿tercero o infraestructura propia?).

Si hubo decisión, la pregunta útil casi nunca es «¿por qué está encendido?». Es «**¿siguen valiendo los supuestos con los que se decidió?**». Aquí no valían: se decidió para conversación comercial, y con RRHH entran CVs (#1940). La medición era correcta; el marco era el falso.

Espejo: el CLAUDE.md global manda buscar un flag **antes de encenderlo**. Esto es lo mismo **antes de denunciarlo**. Ver [[una-medida-compatible-con-la-hipotesis-no-es-una-medida-de-la-hipotesis]].
