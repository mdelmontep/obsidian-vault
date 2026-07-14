---
title: feature construida en la hoja pero sin cablear por el composition root = código muerto que el gate verde no caza
date: 2026-07-14
source: claude-code-session
tags: [subagentes, arquitectura, testing, composition-root]
---
Al delegar una implementación (a un subagente, o a otro dev) con **deps opcionales**, revisar el diff **no basta con leer la hoja** (el executor/brain donde vive la lógica): hay que seguir el **camino de composición** hasta `app.ts`/composition root.

- **Gate verde ≠ feature viva.** Una feature con dep OPCIONAL compila, pasa typecheck y pasa TODOS los tests aunque no esté cableada — los tests inyectan la dep a mano, así ejercitan la lógica de la hoja sin el wiring real. El código muerto no rompe nada.
- Caso real AGH #482: el paso `awaiting_email` + su transición estaban en `onboarding-brain.ts` con deps opcionales `getUserEmail`/`setUserEmail`, pero `module.ts`/`app.ts` nunca las inyectaban → dormido en prod (fail-safe: deps ausentes = comportamiento previo).
- **Fix / check**: por CADA dep o capability nueva, verificar la cadena interfaz → hoja → `module.ts`/factory → `capabilities.ts`/`persistence.ts` → `app.ts` (donde se construye el valor REAL, no el default noop/in-memory). Si el diff toca la hoja pero no `src/composition/*` ni `app.ts`, es señal de código dormido.
- Complementa el gate con un test/smoke que ejercite el camino **wireado** (p. ej. el pg-real que asserta el efecto a través del executor cableado, no del fake). Ver [[audit-log-multi-escritor-procedencia-en-after-before-sin-carrera]].
