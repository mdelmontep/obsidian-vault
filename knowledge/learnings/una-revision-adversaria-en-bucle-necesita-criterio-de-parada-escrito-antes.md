---
title: una revisión adversaria en bucle necesita criterio de parada escrito antes
date: 2026-09-14
source: agh-iberica
tags: [metodo, revision, subagentes, alcance]
---
Un revisor al que se le pide **atacar** siempre encuentra algo. «Hasta que no encuentre nada» no es criterio de parada: el bucle no converge, solo baja la gravedad de lo que encuentra.

Caso real (agh-iberica #1697, 13–14 sep): subir/listar/descargar originales de RRHH, media jornada de alcance. Salieron **nueve rondas con Opus, 70 commits y 11.300 líneas**. Las rondas 8 y 9 ya no hallaban fugas, caídas ni bloqueos, sino tests que no discriminaban, frases del ADR y detalles de la UI.

Dos causas, las dos evitables:
- **Alcance autoinfligido**: un lector propio de PDF/DOCX decidía la visibilidad sobre ficheros hostiles, en el proceso de la voz. Cada arreglo abría superficie nueva: cuadráticas, worker, OOM, Node 22.
- **No recortar al cambiar la premisa**: en la ronda 6 se decidió que la detección nunca concede acceso. Ese día el lector dejó de hacer falta en la PR, y se siguió puliendo tres rondas más.

Fix:
- Antes de la 1.ª ronda, escribir qué bloquea: fuga, caída, pérdida de datos, bloqueo y **regresión de la función principal**. Lo demás va a issues.
- Tras cada decisión de diseño, preguntar qué componente ha perdido su motivo y sacarlo de la PR.

Ver [[el-gate-verde-no-sustituye-una-revision-adversarial-antes-de-mergear]].
