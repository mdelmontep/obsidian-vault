---
title: formAction con server action secuestra el name del botón, y el test no lo ve
date: 2026-08-09
source: claude-code-session
tags: [react, nextjs, testing, formularios]
---

Un `<button formAction={accionDeServidor} name="via" value="enlace">` **pierde su `name`**: React
lo usa para codificar la acción y sirve `name="$ACTION_ID_…"`. Cualquier mecanismo que dependa
de leer ese `name` del `FormData` deja de funcionar en el navegador.

**Y ninguna prueba lo ve**: el doble de `useFormStatus` fabrica su propio `FormData`, así que el
test comprueba lo que el propio test escribió. Se descubre leyendo el HTML que sirve el servidor.

**Fix**: no pongas `formAction` en el botón. Un solo `action` en el `<form>`, el botón con
`name`/`value` planos, y el reparto en el servidor (`if (fd.get('via') === …)`). HTML de siempre,
funciona sin JS, y el reparto pasa a ser una función con test propio.

Regla general: cuando un framework escribe atributos por ti, **compruébalo en el HTML servido**,
no en jsdom. Ver [[una-afirmacion-repetida-no-es-una-verificacion]].
