---
title: un guard enumera la clase entera; la regla escrita solo documenta el caso que te mordió
date: 2026-08-03
source: claude-code-session
tags: [gates, guards, auditoria, metodo]
---
Al arreglar un fallo, escribir la regla en el gotcha documenta **ese** caso. Poner
un guard que la compruebe **cuenta cuántos más hay**, y suele haber más.

Caso TuFacturaIA (mismo día, dos PRs): `resolve-ia:job_fallido` se emitía sin que
nadie lo resolviera. Lo arreglé y lo dejé escrito en `gotchas.md` («todo emisor
necesita un dueño»). Horas después, el guard que comprueba esa misma regla
destapó **8 emisores más** en idéntica situación, que la regla escrita no había
encontrado en todo el día porque nadie la vuelve a leer contra el repo entero.

Dos cosas para que el guard valga:
- **El detector se prueba contra las evasiones que YA existen en el repo**, no
  contra las que imaginas. Aquí eran dos y estaban las dos: un comentario que
  dice `emitSystemAlert (OCR 502…)` casa con `/emitSystemAlert\s*\(/` sin ser
  código, y un fichero que emite por inyección (`deps.alert ?? emitSystemAlert`)
  no casa con la llamada. Mirar el **import** cubre las dos.
- **Lista de excepciones con motivo escrito, y que rompa si la excepción muere.**
  Sin la segunda mitad, la lista se vuelve el cajón donde va lo que no quieres
  arreglar hoy.

Y no arreglar los 8 fue deliberado: ninguno había disparado nunca, y un `resolve`
sin un caso real que lo pruebe parece cubierto sin estarlo. La deuda nombrada
vale más que el código especulativo. Ver
[[alerta-que-se-resuelve-al-volver-a-funcionar-queda-huerfana-si-su-sujeto-desaparece]] ·
[[un-guard-que-grepea-el-texto-del-fichero-no-distingue-uso-de-asercion]] ·
[[una-metrica-por-regex-sin-test-del-parser-cuenta-ruido-y-se-vuelve-ignorable]]
