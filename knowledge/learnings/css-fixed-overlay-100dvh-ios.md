---
title: overlay fixed en ios: usar 100dvh no inset-0
date: 2026-06-02
source: claude-code-session
tags: [ios, safari, css, mobile]
---

`position: fixed; inset: 0` no siempre cubre el viewport completo en iOS Safari al hacer scroll.
El browser chrome (barra URL) interfiere con el cálculo de altura.

Fix: `inset-x-0 top-0 h-[100dvh]` — `dvh` = dynamic viewport height, ajusta al chrome real del browser.
`100vh` también falla (usa el viewport sin chrome). `100dvh` es el correcto desde iOS 15.4+.

Combinar siempre con [[ios-safari-body-scroll-lock-position-fixed]] para bloqueo completo.
