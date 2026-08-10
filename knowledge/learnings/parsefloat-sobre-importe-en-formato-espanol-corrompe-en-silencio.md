---
title: parseFloat sobre un importe en formato español lo corrompe en silencio
date: 2026-08-10
source: claude-code-session
tags: [i18n, datos, formularios, validacion]
---
`Number.parseFloat` sobre lo que teclea un usuario español da tres resultados **plausibles y
falsos**, que es lo que los hace invisibles:

    "12,50"    → 12       se come los céntimos
    "1.234,56" → 1.234    divide el importe por mil
    "abc"      → NaN      y `JSON.stringify` lo manda como null: BORRA el campo

Nadie mira dos veces un 12 ni un 1.234. El canal de API validaba con `z.number().finite()`; era el
formulario web el que no — la asimetría entre canales otra vez.

Y **el parser tolerante tampoco vale al guardar**: si degrada a 0 ante basura, guardas 0 €, que es
tan creíble como los otros dos. Hacen falta dos parsers: uno tolerante para calcular mientras se
teclea y uno **estricto que devuelva null** para persistir, y quien llama avisa en vez de guardar.

Exigir además que lo normalizado sea número de punta a punta: `parseFloat` para en el primer
carácter raro, así que «12€» le da 12 — así se convierte una errata en un importe creíble.
Ver [[una-suite-en-verde-no-prueba-el-camino-real]]
