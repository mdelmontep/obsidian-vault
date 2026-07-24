---
title: para deduplicar items de 1Password agrupar por título+usuario+password, nunca solo por título
date: 2026-07-24
source: claude-code-session
tags: [1password, seguridad, dedup]
---
Un vault reimportado dos veces (ej. export de navegador cargado en dic-2024 y otra vez en mar-2026) genera duplicados con el MISMO título de item pero pueden esconder cuentas reales distintas bajo ese título (ej. "www.instagram.com" con 6 copias: tu cuenta personal + la de un negocio, cada una con user/password distintos).

Agrupar por título solo y "quedarse con el más reciente" borraría cuentas reales. Fix: agrupar por (título, usuario) y, antes de borrar, comparar también la contraseña real de cada par — no asumir por las fechas de import que son idénticos. En una limpieza real (98 items), ~8% de los pares con mismo user tenían password DISTINTO (rotación de contraseña no sincronizada entre las dos copias) — sin la verificación se habría podido perder la contraseña vigente.

Caso límite real: un item con password vacío tenía fecha de modificación más reciente que su "duplicado" con password real — la regla ciega "quedarse con el más nuevo" hubiera borrado la contraseña buena.
