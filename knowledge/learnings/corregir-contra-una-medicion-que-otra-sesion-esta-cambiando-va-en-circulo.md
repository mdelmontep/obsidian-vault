---
title: corregir contra una medición que otra sesión está cambiando va en círculo
date: 2026-08-15
source: claude-code-session
tags: [metodo, sesiones-paralelas, migraciones]
---

Medí `schema_migrations` en prod, vi el 696 ocupado por otra rama, moví la mía a
697 y mergeé el PR. Veinte minutos después la otra sesión había renumerado la
suya a 697 y reparado el registro: prod decía 696=mía, y mi repo decía lo
contrario. Iba a mergear el revert cuando pidió parar.

Las dos mediciones fueron **correctas al tomarlas**. El error no fue medir mal,
fue tratar una foto como estado estable teniendo otro escritor delante. Medir
mejor no lo arregla: mientras tú corriges, el otro también.

**La salida es coordinación, no precisión**: uno de los dos FIJA el estado
objetivo, lo anuncia, y el otro se adapta sin tocar nada. Gana el que ya tiene
el trabajo en `main` — mueve menos piezas. Y elige el estado que deja `main`
como está, no el que te da la razón.

Después, verificar por **nombre**, no por número: `696` no dice de quién es;
`696 | trial_ending_avisos_claim` sí. Y releer justo después, no solo antes.

Relacionado: [[el-hueco-libre-de-migraciones-puede-estar-ya-ocupado-en-produccion]] · [[un-guard-que-se-apoya-en-una-medicion-externa-no-es-un-guard]] · [[antes-de-tocar-un-ticket-mira-si-otra-sesion-ya-lo-esta-cerrando]]
