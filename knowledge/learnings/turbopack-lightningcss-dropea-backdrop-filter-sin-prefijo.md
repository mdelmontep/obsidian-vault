---
title: turbopack/lightningcss dropea backdrop-filter sin prefijo si declaras -webkit- idéntico a mano
date: 2026-07-15
source: claude-code-session
tags: [css, turbopack, nextjs, glassmorphism, gotcha]
---

Síntoma: `.mhead { backdrop-filter: blur(...); -webkit-backdrop-filter: blur(...) }` (mismos valores) → en Chrome `getComputedStyle().backdropFilter` computa `none`, el glass no se ve. El resto de la regla (background/sheen) SÍ aplica.

Causa: lightningcss (el transformador CSS de Turbopack, Next 16) colapsa el par prefijado/sin-prefijo y sirve **solo `-webkit-backdrop-filter`**, dropando el sin prefijo. Chrome moderno lee el sin prefijo → sin él, `none`.

Fix: declarar **solo `backdrop-filter`** (sin prefijo) y dejar que el pipeline añada `-webkit-` si el browserslist lo pide. Es lo que hace el sistema glass del repo (`.glass`, `.sidebar` freebie) — por eso esas sí funcionan.

Diagnóstico: fetch same-origin del CSS servido y grep del bloque; o comparar computed de un `.glass` control vs tu clase. No fiarse de "compila" — el build/typecheck no lo detecta.
