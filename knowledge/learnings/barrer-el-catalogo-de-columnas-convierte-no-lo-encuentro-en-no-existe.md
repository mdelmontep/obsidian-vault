---
title: Barrer el catálogo de columnas convierte «no lo encuentro» en «no existe»
date: 2026-08-07
source: TuFacturaIA · buscar el coste-empresa en el ERP WAPI de IET
tags: [learning, metodo, datos, erp, cliente]
---

El cliente preguntó de dónde salían los 16 €/h y si eran coste-empresa o bruto.
Habíamos mirado las pantallas y las tablas evidentes y la respuesta era «no lo
aclara en ningún sitio», que en una conversación con el cliente no vale nada:
suena a que no supimos buscar.

Un barrido de `sys.columns` sobre las 1.100 tablas buscando `segur`, `cotiz`,
`nomina`, `salario`, `bruto`, `ss` tarda un segundo y devolvió **cero campos
reales** (solo falsos positivos: `denominacion`, `passwd`). Eso ya no es «no lo
encontramos», es **el ERP no guarda ese dato**, y cambia la conversación: deja de
ser una duda nuestra y pasa a ser un número que solo puede dar el cliente.

**La regla**: antes de decirle a alguien que un dato no aparece, o de estimarlo,
barre el catálogo del sistema por nombre de columna. Es la diferencia entre una
duda y un hecho, y cuesta una query.

Vale igual en Postgres (`information_schema.columns`) y en un repo (`grep` por el
nombre del concepto, no por el del campo que esperabas).

Relacionado: [[precio-unitario-1-00-marca-una-cantidad-que-son-euros]] ·
[[un-gate-sobre-el-resultado-no-valida-la-transformacion]]
