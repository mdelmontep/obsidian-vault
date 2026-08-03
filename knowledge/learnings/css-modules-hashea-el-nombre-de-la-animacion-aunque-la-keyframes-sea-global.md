---
title: css modules hashea el nombre de la animación aunque la keyframes sea global
date: 2026-08-03
source: claude-code-session
tags: [css-modules, nextjs, lightningcss, refactor, deuda]
---
Un barrido contó **20 copias** de `@keyframes {to{transform:rotate(360deg)}}` en 20 ficheros y pedía a
gritos unificarlas. **No se puede**, y comprobarlo con dos builds reales evitó romper todos los
spinners de la app en silencio (un spinner que no gira sigue pintándose).

Definiendo `fia-spin` en un CSS global y usándolo desde un `.module.css`, la salida es:

```
@keyframes fia-spin{to{transform:rotate(360deg)}}          /* global, sin hash */
animation:.7s linear infinite button-module__HjQxJG__fia-spin   /* módulo, CON hash */
```

lightningcss hashea **todo** `animation-name` dentro de un módulo, defina o no la keyframes ahí. No
coinciden. Y el escape `animation-name: :global(fia-spin)` sale literal al CSS
(`animation-name::global(fia-spin)`), que es un valor inválido: el navegador lo descarta y la animación
desaparece del todo — peor que el hash, que al menos es un nombre válido.

Conclusión: esas 20 copias **no son deuda técnica, son el scoping funcionando**. Cada módulo tiene que
declarar la suya. Antes de proponer «unificar los N keyframes duplicados» en cualquier repo con CSS
Modules, mira la salida del build; el conteo por grep parece deuda y no lo es.

Ver [[css-module-camelcase-turbopack]] · [[llave-css-faltante-invalida-todo-el-css-posterior]]
