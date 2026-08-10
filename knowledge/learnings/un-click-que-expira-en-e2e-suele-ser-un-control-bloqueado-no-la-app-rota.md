---
title: un click que expira en e2e suele ser un control bloqueado, no la app rota
date: 2026-08-10
source: claude-code-session
tags: [e2e, testing, precondiciones, metodo]
---
FacturaIA 10-ago: 4 casos fallaban con `locator.click: Timeout 15000ms` y `waitForResponse` a 8 s.
Parecían bugs de la app y eran una **precondición que nadie establecía**: los campos dependían de
un interruptor maestro apagado, y su wrapper lleva `pointer-events: none` → el click nunca llega.

Dos cosas que lo hacen difícil de ver:
- el bloqueo se calcula con la config **GUARDADA**, no con el borrador local: encender el
  interruptor no desbloquea hasta que vuelve el PATCH **y** se relee la config;
- el caso anterior deja su PATCH de restauración en vuelo; si su respuesta llega después, la vista
  pinta la config vieja y el `expect` cae con el producto sano.

**Patrón**: (1) el helper de precondición pulsa el gesto REAL (la etiqueta, no el input oculto);
(2) espera **al efecto** con aserción web-first, no a un `waitForTimeout`; (3) si en pocos segundos
no desbloquea, **recarga** — releer del servidor quita la carrera en vez de taparla con más espera;
(4) `afterAll` devuelve el interruptor: dejarlo encendido activa la función de verdad en la org.
