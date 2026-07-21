---
title: sql server — cast(money as varchar) redondea a 2 decimales; exportar con decimal(18,4)
date: 2026-07-21
source: claude-code-session
tags: [sql-server, migracion, precision]
---
`CAST(un_money AS varchar)` formatea a **2 decimales** aunque `money` guarde 4 internamente.
Al extraer precios unitarios para migrar, esto pierde los decimales 3º/4º y el sumatorio
(unitario × cantidad, sobre miles de líneas) deriva euros. Costó horas de diagnóstico:
los totales por-presupuesto bailaban aunque la aritmética SQL era correcta.

Fix: convertir a `decimal(18,4)` antes de volcar a texto: `CAST(CONVERT(decimal(18,4), x) AS varchar)`.
Relacionado: si concatenas columnas con `+` y alguna es NULL, la fila entera sale NULL
(usar `ISNULL(...)`); y una función escalar (UDF) por fila va lentísima con `FOR JSON`+padding
`-y 8000` pero rápida con salida pipe (`-W -s"|"`). Ver [[migrar-precios-erp-congelar-neto-con-aritmetica-del-origen]].
