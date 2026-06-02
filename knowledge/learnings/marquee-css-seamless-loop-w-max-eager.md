---
title: marquee css seamless loop: w-max + loading eager en wrapper único
date: 2026-06-02
source: claude-code-session
tags: [css, frontend, marquee, performance]
---

Marquee infinito sin salto visible:
- Animar UN solo div wrapper (no dos `<ul>` independientes — cada una calcula su propio -50%)
- `width: max-content` (`w-max`) en el wrapper para que `translateX(-50%)` = ancho real de un set
- Sin `w-max`: el browser colapsa al ancho del viewport → el % se calcula mal → logos salen de pantalla
- `loading="eager"` en todas las imgs del marquee — con `lazy`, el intersection observer descarga las imgs cuando el contenedor animado se sale del viewport → desaparecen y reaparecen
- `will-change: transform` para compositing GPU
- Estructura: `<div.marquee overflow-hidden> → <div.marquee-inner flex w-max animate> → <ul>×2`
- keyframe: `from translateX(0) to translateX(-50%)`; con `infinite linear` el loop es invisible si ambas listas son idénticas
