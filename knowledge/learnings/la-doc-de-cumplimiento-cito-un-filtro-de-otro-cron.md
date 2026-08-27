---
title: la doc de cumplimiento citó un filtro que vivía en otro cron
date: 2026-08-27
source: agency-portal
tags: [rgpd, documentacion, auditoria]
---

La ficha de subencargado afirmaba, para tranquilizar sobre el alcance: «el filtro es
por cliente y ya existe la forma (`?only=` / `?skip=`)». Cierto — **de otro cron**.
El pipeline que iba a mandar los datos al tercero filtraba solo por `ready_to_judge`
y `updated_at`: honrar la oposición de un cliente exigía pausar la agencia entera.

El patrón: un documento de cumplimiento describe una capacidad del sistema por
familiaridad («eso ya lo tenemos») y nadie lo comprueba en la función concreta que
la ejecutará, porque el revisor del documento es legal y el que conoce el código no
lee el documento. La frase sobrevive porque **suena verificada**.

**Regla**: toda afirmación de capacidad técnica en un documento legal lleva al lado
el símbolo que la implementa (`runFleetJudgeEnqueue`, no «el cron»). Si no se puede
nombrar la función, la capacidad no existe todavía.

Y el default de una cobertura de datos es **cerrado**: sin marca explícita por
cliente, no se procesa. Ver [[single-source-attribution-pitfall]].
