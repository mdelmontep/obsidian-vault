---
title: tests que caen por contención de CPU: verifícalos aislados antes de diagnosticar
date: 2026-07-29
source: claude-code-session
tags: [vitest, testing, verificacion, metodo]
---

Suite completa con 3 ficheros en rojo y ninguno relacionado con el cambio. La
firma de que es contención y no código:

- los tiempos se clavan **en el límite por defecto** (5000-5100 ms en Vitest),
  no en valores dispersos;
- los ficheros caídos no tienen nada que ver entre sí ni con el diff;
- la tanda entera tarda un múltiplo de lo normal (277 s frente a 77 s).

Antes de tocar nada, corre solo esos ficheros: si pasan, era ahogo de CPU
(otro build en paralelo, varias sesiones en la misma máquina), no un fallo.

```bash
npx vitest run <los tres ficheros caídos>
```

No lo des por flaky sin la comprobación aislada: la misma pinta la tiene un test
que depende del orden de ejecución, y ese sí es un fallo real. Lo que distingue
a uno de otro es que el de contención pasa aislado Y la tanda entera vuelve a
pasar cuando la máquina está libre — comprueba las dos.
