---
title: un 200 no prueba que la página citada exista
date: 2026-09-06
source: mandadm
tags: [verificacion, documentacion, agentes, metodo]
---
Dos ficheros de `docs/meta/` traídos por un agente resultaron ser **reconstrucción**, no transcripción,
y las citas venían con URL que devolvía 200. Lo midió la sesión `mandadm-5c` el 6-sep:

- En `developers.facebook.com`, `/docs/<basura>` da **404** pero `/documentation/<basura>` da **200
  siempre**: hay un comodín bajo ese prefijo. Una cita con `/documentation/` no prueba nada. La prueba
  que discrimina es pedir una ruta que sabes falsa **bajo el mismo prefijo**; si también da 200, el
  200 no es evidencia.
- La otra cita apuntaba a una página real, pero de 909 KB quedaban **35 caracteres** de texto visible
  al quitar los scripts, y el título volvía en español: se renderiza en cliente. De ahí no sale un
  párrafo literal en inglés.

**Fix, dos comprobaciones baratas:** un 200 solo cuenta bajo un prefijo donde una ruta inventada dé
404; y si lo descargado casi no tiene texto, no has leído la página — no cites lo que no has visto.
Corolario para el que revisa a un agente: pídele la cita **literal** y búscala en el HTML bajado.
Ver [[un-agente-que-trae-documentacion-transcribe-el-marcador-como-valor]] · [[una-busqueda-cortada-por-timeout-no-prueba-una-ausencia]]
