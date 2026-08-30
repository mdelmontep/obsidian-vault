---
title: un mutante que no muerde puede no haber mutado nada
date: 2026-08-30
source: centro-elphis
tags: [testing, mutacion, gates, metodo]
---
Verificando por mutación el gate del agente de voz, «precio alterado» no mordió. Diagnóstico
automático: gate ciego → añadir checks. Falso las dos veces que pasó: la cifra mutada **no existía en
el texto que se mutaba** (los precios viven en el `global_prompt`, no en el nodo; y «60» no aparece en
ninguno). El mutante era **equivalente**: no cambió nada, así que ningún gate podía morderlo.

- Antes de tocar el gate, comprueba que el mutante **cambió algo**: comparar el objeto serializado
  antes/después es una línea, y distingue «no muerde» de «no mutó».
- El arnés debe reportar los tres estados —`MUERDE` / `NO MUERDE` / `MUTANTE EQUIVALENTE`—, no dos.
  Con dos, un equivalente se lee como agujero y te hace añadir checks que no vigilan nada.
- No es simétrico: la primera vez que me pasó, investigar el equivalente sí destapó un hueco real
  (las tarifas sin cubrir). El error no es investigar, es **concluir «gate ciego» sin mirar**.

Ver [[barrer-el-diff-en-vez-de-mutar-a-mano]] · [[verificar-que-un-test-tiene-dientes-con-una-mutacion]]
