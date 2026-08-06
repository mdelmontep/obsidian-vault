---
title: un modal de edición que reenvía el snapshot completo revalida de balde valores sin tocar
date: 2026-08-06
source: claude-code-session
tags: [validacion, formularios, delta, ux, react]
---
Un modal que precarga N campos y en "Guardar" manda TODOS los valores mostrados (no solo
los tocados) rompe en cuanto el backend valida por delta: cualquier validador que trate
"clave presente en el payload" como "esta clave se está escribiendo de nuevo" (patrón
común: opción de un select que se archivó pero el valor viejo sigue siendo válido EN
LECTURA, no como valor nuevo) rechaza el guardado aunque el usuario solo tocara OTRO
campo del mismo formulario.

Caso real (TuCRMIA, issue 021): modal de "campos personalizados" reenviaba el snapshot
completo; reabrir la ficha de un lead con un valor bajo una opción ya archivada y pulsar
Guardar sin cambiar nada lo rechazaba, bloqueando también el resto del formulario.

Fix: guardar `valoresIniciales` junto a `valores` en el estado del modal, y en Guardar
calcular el delta real (`JSON.stringify` por clave basta para strings/números/booleans/
arrays de código) contra los iniciales. Si el delta está vacío, ni se llama a la acción.
Se detecta solo verificando en el navegador con datos reales que ya tienen ese estado
"legacy" (opción archivada) — no aparece leyendo el código de la validación en aislado.
