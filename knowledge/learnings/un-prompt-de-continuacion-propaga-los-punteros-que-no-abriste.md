---
title: un prompt de continuación propaga los punteros que no abriste
date: 2026-08-26
source: facturaia
tags: [metodo, handoff, prompts, documentacion, contexto]
---
Escribí un prompt de continuación con «esto depende del paso 3 →
`PROMPT-aprendizaje-ocr-paso3.md`». Ese fichero lleva **SUPERSEDED** en su primera
línea, el área se cerró cinco días antes con dos ADR y él mismo dice «no lo
ejecutes otra vez». No lo abrí: cité de memoria un nombre que sonaba correcto.

El daño es asimétrico: en un doc de consulta el puntero caducado se detecta al
leerlo; en un prompt de arranque es lo **primero** que ejecuta la sesión nueva, y
la manda a rehacer trabajo terminado con el aval de mi firma.

Regla: **cada ruta de un handoff se abre antes de escribirla** (`head -12` basta,
la cabecera de supersede vive arriba). Y si el prompt afirma que algo sigue
pendiente, la fuente es el código: aquí el doc se contradecía —«pendiente» en una
línea, «hecho, mig 731» en otra— y el código daba razón a la segunda. Corolario:
aplica al subsistema el diagnóstico que el prompt manda usar a otros; sacó cuatro
agujeros donde acababa de dar el área por cerrada.

**Segundo mecanismo, medido el 7-sep**: no hace falta un puntero malo — el prompt
caduca por dentro. El del ticket 171 seguía listando tres bloques como pendientes
tres días después de mergearlos y aplicarlos a prod. Arreglo: al cerrar un bloque,
el prompt se corona con una cabecera de estado («quedan CERO tareas de código») y se
tacha lo hecho **conservando su texto como método**, que sigue valiendo como registro
de cómo se hizo. Un handoff se poda al cerrar, no al reabrir.
Ver [[smoke-insert-directo-no-ejerce-el-motor-real]] ·
[[una-verificacion-corrida-antes-del-cambio-destructivo-prueba-el-esquema-que-vas-a-borrar]].
