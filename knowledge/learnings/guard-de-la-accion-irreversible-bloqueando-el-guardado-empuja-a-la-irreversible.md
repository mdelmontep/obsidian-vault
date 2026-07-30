---
title: un guard de la acción irreversible bloqueando el guardado empuja al usuario a la irreversible
date: 2026-07-30
source: claude-code-session
tags: [ux, guards, facturaia, stock]
---

Validación que pertenece a la acción irreversible (emitir, publicar, enviar) colocada
en el camino compartido, así que también bloquea el guardado reversible (borrador).

Caso TuFacturaIA (PR #1382): en `/generar`, "Guardar borrador" con 20 uds sobre una
partida de 3 no guardaba NADA y respondía "No hay stock suficiente en la partida
LOTE-B". Un borrador no tiene número, no va a VeriFACTU y no mueve stock: no había
nada que proteger. El otro guard decía "elige la partida **antes de emitir**"
impidiendo un guardado que no emite.

El daño no es el mensaje raro: si no puedes guardar, la única salida visible es
pulsar el botón irreversible. Es como se llegó al bucle del ticket #117 (usuario
dándole a Emitir una y otra vez).

Señal barata: dos ramas de la misma pantalla (crear vs editar) que corren distintos
guards — una de las dos está mal. Fix: el criterio "¿esto emite o solo guarda?" en
una función compartida, y los guards dentro de él. Ver
[[auditar-un-lado-de-par-simetrico-revisar-el-espejo]]
