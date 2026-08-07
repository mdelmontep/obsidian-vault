---
title: Dos piezas en la misma unidad equivocada dan el resultado correcto
date: 2026-08-07
source: TuFacturaIA · módulo Obras · IET (migración desde el ERP WAPI)
tags: [learning, datos, migracion, unidades, facturaia, obras]
---

Un campo migrado desde otro sistema puede estar en la unidad de ORIGEN y no
fallar nunca, porque el otro factor de la multiplicación vino en la misma unidad
equivocada y se compensan. El resultado sale bien y nadie tiene motivo para
mirar. Es peor que un error visible: no hay síntoma hasta que alguien toca UNA de
las dos piezas creyéndose el nombre del campo.

**El caso.** `obras_materiales.tiempo_mo_horas` se llama «horas» y no lo son:
viene de WAPI, que expresa el tiempo de mano de obra en una unidad propia donde
**1 hora = 1,4918**. El precio de venta salía correcto porque
`obras_settings.precio_hora_mo` (34 €) también estaba en unidades WAPI:
1,492 × 34 = 50,73 €/h, igual que el ERP hacía 1,4918 × 33 = 49,23 €/h.

**Lo que casi cuesta dinero.** Al ir a rellenar `coste_hora_mo`, el backup daba
el coste real del instalador: 16,35 €/h. Escribirlo tal cual habría inflado el
coste previsto de cada partida un **49 %**, y con el coste inflado se descartan
obras que sí eran rentables. El valor correcto en la unidad vigente era 10,96.

**Cómo se detecta, y es barato.** Busca en el propio catálogo la fila que se
autodescribe y comprueba que vale lo que dice. Aquí la tabla de tipos tenía una
fila literalmente llamada `TIEMPO 1 HORA`: valía **1,4920**. Una consulta.

La regla operativa: **antes de escribir una constante que multiplica a un campo
migrado, verifica la unidad del campo con un caso cuyo valor esperado conozcas**.
No basta con que el resultado actual sea correcto — puede serlo por compensación.
Y la corrección, si la hay, es de negocio: normalizar el catálogo mueve el precio
que se factura a clientes reales, así que se propone, no se aplica.

Relacionado: [[campo-numerico-opcional-omitido-suma-cero-y-parece-dato]] ·
[[agregar-sobre-todas-las-orgs-mezcla-datos-sembrados-con-datos-de-cliente]] ·
[[la-confianza-autodeclarada-de-un-llm-no-predice-su-acierto]]
