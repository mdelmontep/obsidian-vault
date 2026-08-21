---
title: un candado puesto tras un incidente puede quedar del revés de lo lógico
date: 2026-08-21
source: facturaia
tags: [diseño, permisos, fiscal]
---
El editor de facturas recibidas cerraba los campos fiscales en cuanto la factura
se aprobaba. La razón era buena y medida: reabrirlo entero dejó 412 recibidas
sin líneas.

El efecto colateral tardó un año en verse y es del revés: **se podía corregir
mientras la factura no declaraba nada, y dejaba de poder corregirse justo cuando
empezaba a contar para Hacienda**. Si el OCR leía mal una retención y se veía
tras aprobar, la única salida era borrar y volver a subir el documento.

Al revisar un candado, la pregunta no es «¿qué protege?» sino **«¿en qué estado
queda el usuario atrapado?»**. Si la respuesta es «en el estado que más importa»,
el candado está mal puesto aunque su motivo siga siendo cierto.

El arreglo no fue levantarlo: fue abrir un camino ESTRECHO y auditado para el
único campo que hacía falta (endpoint propio + RPC transaccional + bloqueo si ya
está en una declaración presentada), dejando el editor ancho cerrado.
