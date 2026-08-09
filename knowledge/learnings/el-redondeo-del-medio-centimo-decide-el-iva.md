---
title: dos redondeos "equivalentes" divergen en el medio céntimo y mueven el IVA
date: 2026-08-09
source: claude-code-session
tags: [dinero, fiscal, refactor, facturaia]
---

Un agente propuso «unificar `round2`, está duplicado 42 veces». Antes de aplicarlo, medir:

    n        Math.round((n+EPSILON)*100)/100    Math.round(n*100)/100
    1.005    1.01                               1.00
    1.015    1.02                               1.01

No son la misma función. `1.005` en binario es 1.00499…, así que sin el `EPSILON` el medio céntimo BAJA, al revés de lo que escribió quien factura. Un DRY mecánico ahí mueve cuotas de IVA y retenciones en producción.

Método para unificar aritmética duplicada, en este orden:
1. **Clasifica las copias por variante** antes de tocar nada: pueden ser dos funciones distintas con el mismo nombre.
2. **Línea base de tests de importes** (`npx vitest run <módulos de dinero>`) y guarda el número.
3. Unifica y vuelve a correr. **Si algún test cambia de resultado, no lo adaptes**: es un importe moviéndose en producción, y eso se decide, no se ajusta.
4. Respeta las precisiones distintas (4 decimales para precios unitarios, 3 para stock): `roundN(n, dec)`, no aplastar todo a 2.

En TuFacturaIA: 55 copias → 1, decisión en [[ADR-051-el-redondeo-de-importes-sube-el-medio-centimo]], 3.019 tests antes y después sin un solo cambio. Corolario del tripwire: un comentario que dice «divergencia DELIBERADA» puede tapar tanto una decisión buena como una que nadie ha revisado en un año — valida el RESULTADO de negocio, no el comentario.
