---
title: un candado que empareja dos señales se esquiva renombrando una de ellas
date: 2026-09-15
source: agh-iberica
tags: [guards, tests, prompts, refactor]
---
Un guard exigía evidencia de evals a todo fichero que llevara el marcador `SYSTEM_PROMPT`.
Su criterio real, leído en el test, era otro: emparejaba «fichero con marcador» con
«fichero que emite `role: "system"`». Un extractor nuevo llevaba el texto del prompt pero
delegaba el turno en un cliente de gateway, así que rompía el candado sin ser culpable.

El rename a `INSTRUCCIONES_*` deja el candado coherente y NO es esquivarlo — pero abre el
agujero de verdad: el texto que el modelo lee vive en un fichero y el marcador en otro,
así que cambiar el prompt no pide evidencia y tocar un `timeout` del cliente sí.

Regla: antes de renombrar para satisfacer un guard, leer **qué empareja**, no cómo se
llama. Si las dos señales pueden vivir en ficheros distintos, el guard vigila la señal
equivocada → issue, no rename silencioso.

Ver [[un-candado-que-el-issue-pide-puede-cegar-a-otro-consumidor]].
