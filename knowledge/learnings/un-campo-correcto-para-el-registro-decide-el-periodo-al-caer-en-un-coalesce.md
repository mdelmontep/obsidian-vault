---
title: un campo nuevo, correcto en su sitio, decide otra cosa al caer en un COALESCE que ya existía
date: 2026-09-20
source: facturaia
tags: [arquitectura, fiscal, facturaia]
---
Se añadió `fecha_operacion` al abono con la fecha del origen: correcto para lo que se imprime y se
registra ante la AEAT. Pero el motor fiscal periodificaba por `COALESCE(fecha_operacion, fecha)`
**sin mirar el tipo de documento**, así que ese dato, sin que nadie lo decidiera, pasó a arrastrar
el abono al trimestre de la operación original. Y si ese trimestre estaba presentado, a uno cerrado.

El patrón: un campo que antes estaba siempre nulo para un tipo de fila no es inerte, es un
**parámetro apagado**. Al encenderlo hereda todo el significado que otros módulos ya le habían
dado. El typecheck no ve nada: el tipo no cambió, cambió quién lo rellena.

Regla: al empezar a escribir un campo que antes nadie escribía para ese tipo de fila, grep de
TODOS sus lectores antes del PR — no de sus escritores. Aquí eran tres, en TS y en SQL
(`fecha-devengo.ts`, `universo.ts` y el índice de la migración).
Ver [[rectificativa-se-declara-en-el-periodo-de-su-expedicion]].
