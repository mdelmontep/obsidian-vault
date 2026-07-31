---
title: un paso defensivo de test no es candado de un default
date: 2026-07-31
source: claude-code-session
tags: [testing, e2e, falso-verde]
---
Los pasos de preparación escritos a prueba de balas —`if (await x.isChecked())
await x.uncheck()`— **normalizan el estado**, y por tanto pasan con el default
puesto y con el contrario. No vigilan nada: cambiar el valor por defecto no pone
nada en rojo.

Caso FacturaIA (issue #1409): el smoke E2E de emitir desmarcaba «Enviar al
cliente por email al emitir» de forma defensiva. Ese paso es CORRECTO —lo que
prueba es emitir-sin-enviar, y no debe asumir de qué estado parte— pero deja el
default sin red. Que el `useState(true)` volviera mañana no rompería el E2E.

Regla: si un default es una decisión (aquí, de producto: enviar es irreversible y
de cara afuera), necesita **su propio candado**, aparte del test de flujo. Cuando
montar el componente no compensa para afirmar una constante, vale un test que lea
el fuente y capture la declaración por regex — con mensaje explícito si no la
encuentra, para que un renombrado falle en vez de callarse.

Y al revés: ver un paso defensivo en un test **no** autoriza a concluir que el
comportamiento está cubierto. Ver
[[la-aguja-de-una-asercion-sobre-el-documento-entero-debe-ser-unica-de-la-feature]] ·
[[verificar-que-un-test-tiene-dientes-con-una-mutacion]]
