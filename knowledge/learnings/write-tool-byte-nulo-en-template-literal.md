---
title: edit no casa una línea "idéntica" → revisar bytes ocultos (byte nulo) con python repr
date: 2026-07-02
source: claude-code-session
tags: [claude-code, harness, gotcha, debugging]
---

Al escribir un template literal `` `${a} ${b}` `` con la tool Write, se coló un **byte nulo**
(`\x00`) en vez del espacio entre las interpolaciones. Síntoma: `Edit` fallaba con "String to
replace not found" sobre una línea que en el Read se ve idéntica, y `perl -0pi` tampoco casaba.

Fix / diagnóstico: cuando un `Edit` no casa una línea que parece exacta, no asumir "está bien" —
inspeccionar los bytes reales:
`python3 -c "print(repr(open('f').read().splitlines()[N]))"` → destapa `\x00`, CRLF, NBSP, etc.
Luego reemplazar con Python (`s.replace(old_con_\x00, new)`) y verificar que el fichero queda
libre de nulos. Raro, pero cuesta minutos si no se sospecha.
