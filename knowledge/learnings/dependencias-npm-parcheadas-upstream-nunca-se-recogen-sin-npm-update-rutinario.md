---
title: dependencias ya parcheadas por su fabricante nunca se recogen sin npm update rutinario
date: 2026-07-22
source: claude-code-session
tags: [npm, seguridad, dependencias, dependabot, facturaia]
---
Auditoría real: 12 vulnerabilidades acumuladas en `npm audit`. De 6 marcadas
por Dependabot, **4 ya tenían parche del fabricante dentro del rango `^` que
el propio `package.json` ya permitía** (hono, fast-uri, linkify-it,
dompurify) — no hacía falta tocar una sola línea de `package.json`, solo
regenerar el lockfile con `npm update <paquete>`.

Causa: el lockfile solo se toca cuando alguien AÑADE una dependencia nueva.
El mantenimiento rutinario (`npm update`/`npm outdated`) no lo corre nadie
por defecto, así que un parche publicado por el fabricante se queda sin
recoger indefinidamente aunque el rango ya lo permita.

Señal para detectar esto rápido: `npm outdated <paquete>` — si "Wanted" >
"Current", el parche YA cabe en el rango declarado, es un `npm update` de
1 minuto, no requiere tocar `package.json` ni evaluar breaking changes.

Fix estructural (no solo puntual): `.github/dependabot.yml` con
`schedule: weekly` — abre el PR solo, no requiere que nadie recuerde mirar
la pestaña Security. Ver [[dependabot-solo-alerta-no-abre-pr-sin-config-explicita]].
