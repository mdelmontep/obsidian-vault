---
title: un editor inline que compara contra el valor mostrado encalla al reescribir lo mismo
date: 2026-07-27
source: claude-code-session
tags: [frontend, react, ux, datos]
---

Casi todo editor inline confirma así:

```
if (draft.trim() !== (valorMostrado ?? '')) onChange(campo, draft)
```

Es correcto **solo si el valor mostrado sale de la misma fuente que persiste**. Si se muestra
un valor de otro sitio (un buffer de staging, una caché, un override local) y el destino real
está vacío, el usuario queda encallado: teclea el valor correcto, no hay cambio respecto a lo
mostrado, no se dispara nada, y el destino sigue vacío. Reintentar no ayuda **nunca**, y desde
fuera parece el mismo bug de siempre.

Delator: "ya pone la fecha en pantalla, pero en la BD/factura/API es null".
Salida manual mientras no esté arreglado: vaciar el campo y volver a escribirlo (dos cambios).

Arreglo por orden de preferencia:
1. Mostrar el valor de la fuente que persiste (arregla también la mentira visual).
2. Si no se puede, disparar siempre en confirm y hacer el destino idempotente (no-op si igual).

Nace del mismo caso que [[staging-deja-de-ser-fuente-de-verdad-tras-el-commit-y-editarlo-no-cambia-nada]].
