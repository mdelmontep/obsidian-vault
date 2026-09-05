---
title: un agente que trae documentación transcribe el marcador como si fuera un valor
date: 2026-09-05
source: mandadm
tags: [subagentes, documentacion, fixtures, verificacion]
---

Tres agentes Haiku trajeron 18 páginas oficiales de Meta con la instrucción «contenido útil literal,
sin interpretar». Aun así, en el payload de ejemplo del callback de borrado escribieron `0`, `0` y
`<app-scoped ID>` donde la página trae valores literales. Nadie lo miró: los fixtures se construyeron
encima, y sobre el `issued_at: 0` inventado se diseñó una ventana de frescura que la fuente **no pide**.

El fallo no es del modelo barato: transcribir es justo su carril. El fallo es que **un documento
traído por un agente entra al repo con el mismo estatus que uno verificado**, y a partir de ahí todo
lo que se apoye en él hereda el error sin trazas.

Qué hacer:
- El fichero traído lleva **URL + fecha + quién lo trajo**, y una línea que diga si algún valor viene
  de una captura real o solo de la página.
- **Verificar dos veces contra la URL** cualquier valor que vaya a convertirse en fixture, constante o
  regla de validación. Los demás párrafos pueden esperar.
- Cuando el documento se corrija, **releer lo que se apoyaba en él**: aquí la corrección movió la cita
  y dejó una constante citando una línea que decía lo contrario.

Ver [[una-asercion-deja-de-medir-cuando-cambia-su-fuente]] · [[una-pieza-con-su-suite-en-verde-que-el-sistema-no-llama]]
