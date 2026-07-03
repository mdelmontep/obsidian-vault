---
title: un campo opcional ya declarado en el tipo compartido puede seguir vacío en N puntos distintos que hacen su propio SELECT
date: 2026-07-03
source: claude-code-session
tags: [supabase, select, propagacion, campo-compartido]
---

`Cliente.empresa`/`Proveedor.empresa` (razón social vs persona de contacto)
llevaba meses en el tipo TS y las plantillas de PDF ya sabían preferirlo sobre
`nombre` — pero seguía sin mostrarse nunca porque 5 sitios independientes
hacían su propio `SELECT ... clientes(nombre, nif, ...)` sin pedir `empresa`,
así que el dato nunca llegaba a esos consumidores aunque existiera en BD.

El bug NO estaba en la lógica de negocio (ya era correcta) sino en la capa de
lectura, repetida sin helper compartido: hook de lista, modal de detalle,
selector de reasignación, y 2 paths de generación de PDF (borrador vs factura
ya emitida).

Fix: al añadir un campo opcional a un tipo compartido, no basta con
`grep <campo>` en el tipo — hay que `grep 'from(.tabla.)'`/`.select(` sobre la
tabla origen para encontrar TODOS los SELECTs que la tocan, no solo el que se
estaba editando.
