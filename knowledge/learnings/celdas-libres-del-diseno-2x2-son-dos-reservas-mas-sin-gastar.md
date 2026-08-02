---
title: si partes por dos ejes tienes cuatro celdas, y sobran dos reservas sin gastar
date: 2026-08-02
source: claude-code-session
tags: [metodo, estadistica, validacion, backtest]
---

Al reservar datos ciegos se suele partir por UN eje (mitad de entidades, o el tramo
reciente) y se acaba con búsqueda + reserva. Si partes por **dos** (entidad × tiempo) salen
**cuatro** celdas y la práctica habitual solo usa dos:

    impares + antiguo  -> BÚSQUEDA
    pares   + reciente -> reserva
    impares + reciente -> LIBRE
    pares   + antiguo  -> LIBRE

Las dos libres sirven para probar una hipótesis **ya fijada**, sin elegir nada: cero grados
de libertad gastados, así que el t vale lo que dice. Es la vía para juzgar un candidato
cuando la reserva principal ya se abrió (y una reserva abierta dos veces ya no es ciega).

Caso real (cryptobruj, 217 pares): tras 79 combinaciones, el finalista daba +0,0826R en la
reserva. En las dos celdas libres dio −0,0036 y +0,0184 → no era ventaja. De regalo, esas
mismas celdas **confirmaron** una decisión anterior que se había tomado con t=1,45 flojo,
desde muestras que no habían participado en elegirla.

Ver [[reservar-datos-ciegos-y-preregistrar-parametros-antes-de-buscar]] ·
[[dos-finalistas-empatados-que-divergen-fuera-de-muestra-son-ruido]]
