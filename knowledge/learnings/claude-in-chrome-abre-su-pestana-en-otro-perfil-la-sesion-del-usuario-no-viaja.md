---
title: Claude in Chrome abre su pestaña en otro perfil — la sesión del usuario no viaja
date: 2026-07-31
source: claude-code-session
tags: [claude-code, browser, testing]
---
`tabs_context_mcp` puede devolver una pestaña que vive en un **perfil de Chrome distinto**
del que usa el usuario. Las cookies no cruzan perfiles: el usuario entra en su ventana, ve
el dashboard, y a la pestaña controlada le sigue rebotando al login. Se pierde un buen rato
pidiéndole que "entre otra vez".

Síntoma exacto: el usuario enseña una captura ya autenticado y `navigate` + screenshot desde
la herramienta devuelve `/login?redirect=…` para la misma URL.

Fix: `list_connected_browsers` → preguntar cuál es → `select_browser <deviceId>`. Después
`tabs_context_mcp` ya lista la pestaña real del usuario y se opera sobre su sesión. Hacerlo
**al principio** de cualquier tarea de navegador si hay más de un Chrome/perfil abierto, no
tras dos rebotes.

Corolario del mismo caso: no teclear contraseñas en formularios de login (ni de cuentas de
prueba). Se le pide al usuario ese paso y se sigue desde dentro.
Ver [[agent-browser-navegador-compartido-entre-sesiones-concurrentes]]
