---
title: el test que prueba el bug es la traza real, no el golden que propone el issue
date: 2026-07-30
source: claude-code-session
tags: [testing, proceso, agentes-conversacionales, agh]
---
Un issue bien escrito suele traer su caso de prueba propuesto. Ese caso está **limpio**: es la secuencia mínima que ilustra el síntoma. La traza que produjo el bug tiene ruido en medio — un turno fallido, una acción intercalada, un reintento — y **ese ruido es a veces la causa**.

Caso real (AGH #672): el golden del issue era «propone 5 → "no" → "crea los 5" debe re-proponer los 5». Mi primera implementación (un puntero único al último lote) lo pasaba. Pero en la conversación real, entre el lote muerto y la retoma la usuaria había creado una **nota**, que sobrescribía el puntero. O sea: el fix habría pasado el golden del issue y **fallado la conversación que motivó el issue**. Rehecho a una lista de lotes con desambiguación por cardinal.

Patrón: escribir el test contra la **transcripción real turno a turno** (con su basura), no contra el resumen del issue. Si la traza ya no existe, reconstruirla desde el análisis y decirlo. El golden del issue vale como no-regresión, no como prueba de que el fix sirve.

Corolario del mismo día: cuando un test pasa **a la primera**, desactivar el fix y comprobar que se pone rojo. Si no se pone, el test estaba afirmando sobre otra cosa. Ver [[verificar-que-un-test-tiene-dientes-con-una-mutacion]].

Relacionado: [[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]] · [[cada-fix-de-agente-medido-contra-el-modelo-real-destapa-el-siguiente-hueco]] · [[agh-iberica]].
