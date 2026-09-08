---
title: el filtro que saca el ruido saca también la prueba de que funciona
date: 2026-09-08
source: facturaia
tags: [metodo, sql, medicion, smokes]
---

Regla de la casa al medir prod: «siempre con las `is_test` fuera». Correcta para preguntas de
negocio y **falsa para preguntas de funcionamiento** — los smokes viven justo ahí.

8-sep-2026: pregunté «¿se ha usado el abono parcial?» con `coalesce(o.is_test,false)=false`,
salió **0**, y lo publiqué como «no lo ha estrenado nadie», rematando con que faltaba que lo
usara el cliente. Sin el filtro eran **10 abonos parciales** en la sandbox: dos multi-origen
—el caso exacto del ticket— y uno de recibidas, el último de esa misma madrugada. El
instrumento no falló; mi predicado respondía otra pregunta.

**Antes de publicar un cero, quítale el filtro y vuelve a contar.** Si el número cambia, el cero
no era del mundo, era del `WHERE`. Y son dos preguntas distintas: «¿lo usan clientes?» va con
`is_test` fuera; «¿funciona?» va con `is_test` DENTRO y partido por org.

Hermana de [[el-instrumento-devuelve-cero-sin-decir-que-no-ha-medido]] —allí el instrumento
estaba roto, aquí funcionaba— y de [[ausencia-de-consumidor-no-es-ausencia-de-funcion]].
