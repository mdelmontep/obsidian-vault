---
title: antes de mergear una validación que bloquea, cuenta en prod a quién bloquea
date: 2026-08-01
source: claude-code-session facturaia
tags: [migraciones, producto, prod, metodo]
---
Un gate correcto puede ser inaceptable de enviar. Se añadió que no se pueda emitir factura sin domicilio fiscal del emisor (lo exige el reglamento). Medido en producción antes de mergear: bloqueaba a **4 organizaciones reales**, una con facturas ya emitidas, y a una sandbox con **1340**. Ya estaba rompiendo dos tests sin que nadie relacionara el rojo con el gate.

Lo que enseña: la validación tenía razón y **el dato es el que falta**. Cuando el arreglo correcto deja a clientes reales sin poder trabajar, la decisión ya no es técnica, es de producto, y hay que subirla con la cifra delante en vez de mergear y ver qué pasa.

Método, una query antes de mergear: `select ... where <la condición del gate no se cumple>`, separando orgs reales de `is_test` y contando **cuántas ya usan** el flujo que vas a bloquear (una org con 0 documentos emitidos no es lo mismo que una que factura). Esa segunda columna es la que cambia la decisión.

Salida elegida aquí: aviso recurrente en vez de bloqueo. Con su coste, dicho en voz alta: un aviso que se cierra se puede ignorar, así que el incumplimiento sigue. No es la opción «segura», es un riesgo aceptado a conciencia.

Y si eliges avisar, que el aviso diga **por qué importa**, no solo qué falta: hazlo obligatorio en el tipo. Un aviso recurrente sin consecuencia se aprende a ignorar en dos días y entonces no sirve para nada.

Ver [[medir-alcance-en-multi-tenant-sin-agrupar-por-org-mezcla-la-sandbox]] · [[el-gate-verde-no-sustituye-una-revision-adversarial-antes-de-mergear]]
