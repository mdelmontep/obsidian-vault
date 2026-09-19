---
title: un test de paridad por muestreo no discrimina una copia divergente
date: 2026-09-19
source: agh-iberica
tags: [tests, mutacion, duplicacion]
---
Copiar un validador a otro runtime (agente → dashboard, que no puede importar `src/`) con un «test de paridad» da falsa seguridad si el test MUESTREA. Caso #1701: la paridad de `validarNif` probaba 5 de los 23 restos de la letra de control; intercambiar `W`↔`A` en la copia dejó el test en verde, y `00000002W` era válido en un lado e inválido en el otro.
Fix:
- recorrer el dominio completo (los 23 restos) o comparar la constante directamente;
- contrastar también contra las otras copias: el CHECK de SQL es una tercera.
Comprobarlo SIEMPRE con una mutación de la copia (`mutate`): si no hay víctima, el candado no existe.
