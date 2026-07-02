---
title: "ADR-036 — Export contable gestorías: libro registro CSV/XLSX sin cuentas PGC; A3/Sage nativos diferidos"
date: 2026-07-03
tags: [adr, facturaia, fiscal]
---
**Contexto**: TuFacturaIA necesitaba entregar facturas emitidas/recibidas importables por gestorías (PRs #653/#654).
**Decisión**: libro REGISTRO de facturas normalizado (1 fila por factura × tipo IVA, con IRPF prorrateado, RE, exenciones) en XLSX (3 hojas: Emitidas/Recibidas/Avisos) y CSV (`;` + coma decimal + BOM). SIN columna de cuenta contable y SIN asientos de diario. Datos incompletos degradan por hoja Avisos, nunca exclusión silenciosa. Gating: feature `fiscal` existente (cero migración).
**Alternativas descartadas**:
- A3 enlace / Sage 50 / ContaPlus XDiario nativos: exigen subcuentas PGC por tercero (430x/400x) que no existen en el schema, y specs propietarias sin fichero real capturado para validar (inviolable). Diferido a v1.5 como serializadores sobre el mismo modelo de filas (`aeat-posicional-core` reutilizable).
- Inventar mapeo PGC por defecto (477/472/430/400): sin subcuentas por tercero da más trabajo a la gestoría que dejarla mapear columnas — su software genera los asientos al importar facturas.
**Consecuencias**: cualquier gestoría importa vía mapeo Excel; la derivación base/cuota comparte `mapLinea` con el motor fiscal → cuadre con 303/130 por construcción; cuando llegue A3/Sage habrá que añadir mapeo de cuentas configurable (columna en clientes/proveedores + org_module_config).
