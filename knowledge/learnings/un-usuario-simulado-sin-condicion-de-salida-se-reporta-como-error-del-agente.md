---
title: un usuario simulado sin condición de salida se reporta como error del agente
date: 2026-08-27
source: centro-elphis
tags: [retell, testing, simulacion, falsos-positivos]
---
En los tests de simulación de Retell, el `user_prompt` que dice "insiste hasta que
lo consigas" no termina nunca: el usuario simulado repite su frase, el arnés lo
corta con **`ERROR: Ending the conversation early as there might be a loop`** y en
el informe eso parece un fallo del agente.

Tres casos de Elphis lo dieron durante tres tandas seguidas. Leer la transcripción
demostró lo contrario: el agente respondía bien y hasta intentaba cerrar la llamada.

Al escribir el caso, dale al usuario simulado un **contador y una salida**:
"insiste dos veces más, cada vez con palabras distintas; a la tercera negativa
acepta, da las gracias y despídete". Y "no repitas nunca la misma frase" — repetir
literal es lo que dispara el detector.

Corolario: `ERROR` en un batch de Retell no es `FAIL`; antes de tocar el agente,
mira si el guion del usuario tenía forma de acabar.
