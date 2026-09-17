---
title: mapear la nomenclatura de un cliente no es casar campos, es casar qué se comparte y cuándo existe
date: 2026-09-17
source: facturaia
tags: [modelado, migracion-erp, identificadores, obras]
---
Al portar el código de documento de un ERP viejo (IET, `25I-RE-0127/01A` de wapi),
troceé el string y busqué cada pieza en mi modelo. Las seis casaban. El plan aun así
no valía, porque un identificador no son sus piezas: son sus **relaciones**.

Tres comprobaciones que el troceo por campos NO hace:

- **Qué piezas COMPARTEN valor.** En IET `/01A` y `/01B` comparten el `0127`. En
  FacturaIA el subpresupuesto nace como otra familia con su propio `numero`, así que
  la `B` saldría con otro número. Mismo campo, cardinalidad distinta, otro sistema.
- **CUÁNDO existe cada pieza.** La letra se imprime en la propuesta que el cliente
  envía; las columnas de las que pensaba derivarla (`obra_id`, `rol`) son NULL hasta
  que se acepta. Una pieza que nace tarde no puede sostener un código que se imprime
  antes.
- **Si la pieza puede CAMBIAR.** Un código compuesto en tiempo de render desde un dato
  vivo (la sigla de la empresa) se repinta retroactivamente en todo lo ya impreso:
  hay que congelarlo en el documento o decidir explícitamente que no.

Y el contador: mientras no sepas su clave (¿por empresa o por departamento?), déjalo
agnóstico (`ambito TEXT DEFAULT ''` en la PK) en vez de aplazarlo. Cuesta lo mismo hoy
y evita una segunda migración.
