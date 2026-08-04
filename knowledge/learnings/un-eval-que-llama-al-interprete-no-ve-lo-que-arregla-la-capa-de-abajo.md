---
title: un eval que llama al intérprete no ve lo que arregla la capa de abajo — lee el instrumento antes de prometer su número
date: 2026-08-04
source: claude-code-session
tags: [evals, agentes, instrumentacion, agh]
---
Prometí que un arreglo dejaría un caso «en 25/25». Salió **0/25**, y no porque el arreglo fallara: el
fichero de eval construye el intérprete y llama a `interpret()` **directamente**, sin pasar por el
brain. Mide la FORMA de la interpretación; mi arreglo vivía en la capa siguiente, así que le era
invisible **por construcción**.

Regla: antes de afirmar qué número moverá un cambio, **abre el fichero de eval y mira qué llama**. Un
eval de agente puede medir cualquiera de tres cosas y no son intercambiables:
1. la INTERPRETACIÓN (intérprete suelto) — barato, determinista, ciego a todo lo de abajo;
2. el TURNO (brain completo) — ve recuperaciones, guards y ruteo;
3. la RESPUESTA (texto final) — ve además presentación y voz.

Consecuencia práctica: un arreglo en el brain se prueba con un test de la costura del brain, y el eje
del eval **seguirá rojo** — no es una regresión ni un arreglo a medias, es que miden capas distintas.
Decirlo en la PR evita que el siguiente lo lea como un fallo.

Relacionado: [[el-verde-de-evals-check-no-significa-que-nada-se-movio]] · [[agh-iberica]].
