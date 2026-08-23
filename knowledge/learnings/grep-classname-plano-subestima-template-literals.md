---
title: al auditar "0 consumidores" de una clase CSS, grep className="X" plano subestima — falta el patrón interpolado
date: 2026-07-16
source: claude-code-session
tags: [css, refactor, grep, react]
---
El grep anclado `className="btn-*"` solo ve la forma plana: en React lo normal es
`` className={`btn-* ${extra}`} `` o un ternario, y ninguno matchea. Caso real: "6 `<a>` +
21 `<Link>`" resultó ser ~30 ficheros más tras barrer con `\bbtn-[a-z]+\b` sin anclar.
Fix: para declarar "0 consumidores" y borrar el CSS, palabra completa sobre TODO el string
del fichero, y repetir el grep tras cada tanda antes de cerrar el frente.

**Y falla en las dos direcciones: el laxo sobrecuenta** (23-ago, facturaia #2131).
Contando lectores del campo `detail` de una respuesta: `\.detail` a secas dio 93 —
metía `detail.error_kind`, `detail: aiJob.error`, `detail?.thread.titulo`, homónimos
que no son el campo. Una regex que exigía el token siguiente (`\.detail *(\|\||\?\?) *\.?error`)
dio 17 — se dejaba fuera `body.detail ?? labelForError(...)` y el prefijo `retry.json?.`.
La buena era 48/39, y salió de acotar el **objeto** (`(j|json|data|body|errBody)\??\.detail`)
y contar aparte los que llevan fallback. Método: dos regex, una laxa y una estricta, y
mirar la **diferencia** una a una; si no coinciden, ninguna de las dos es la medida.
