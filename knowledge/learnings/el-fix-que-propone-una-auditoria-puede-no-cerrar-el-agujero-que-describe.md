---
title: el fix que propone una auditoría puede no cerrar el agujero que describe
date: 2026-09-03
source: facturaia
tags: [auditoria, testing, metodo, subagentes, verificacion]
---
Un hallazgo trae **diagnóstico** y **fix**, y se aceptan por separado: quien lo escribe razona sobre
el código que lee, no sobre el que ejecuta.

FacturaIA 3-sep, gate de cierre: «una regresión que se rindiera al mínimo donde aún cabe pasaría en
verde. Fix: `if (px > MINIMO) expect(tope <= limite)`». Diagnóstico exacto, fix inservible: un `px`
rendido vale **exactamente** el mínimo, así que su propia rama ni entra. Aplicado tal cual queda un
candado que parece cubrir el caso y no lo toca — peor que el hueco, porque cierra el asunto.

Método: **reproduce el fallo descrito contra el fix propuesto** antes de aplicarlo (mutar el código
para que se rinda de más y ver si el test se pone rojo). El mismo gesto que se exige a un test
nuevo, aplicado a la sugerencia de otro.

Corolario que costó dos intentos: si la decisión usa un umbral **con margen**, el test que la juzga
usa ese umbral, no el nominal — medir contra el del contrato declaraba «se rindió sin motivo» un
caso correcto. Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]] (modo decimoséptimo).
