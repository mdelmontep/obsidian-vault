---
title: no forzar un componente base en paneles con interacción divergente
date: 2026-06-18
source: claude-code-session
tags: [frontend, arquitectura, componentes]
---

Al extraer un componente base (Drawer/Modal único), NO metas dentro paneles cuya interacción diverge del patrón común:
- header rico (avatar, subtítulo, varias acciones) vs el `title`+cerrar del base
- patrón overlay-contenedor (click en el wrapper cierra) vs backdrop+aside hermanos
- doble-panel lado a lado (p.ej. visor PDF + panel) — no es un panel único
- escape condicional con submodales **hermanos** del panel (un focus-trap del base los dejaría fuera)

**Señal de parada:** si para migrar tienes que pasar flags que NEUTRALIZAN el base (`closeOnEscape={false}`, `trapFocus={false}`), no migres — es abstracción con fugas / regresión por ahorrar ~25 líneas.

El base sirve al patrón común; los bespoke legítimos conviven. Un design system bueno tiene un `<Drawer>` base Y paneles a medida justificados. Caso: TuFacturaIA #374 — base + casilla/cuadre migrados; movimiento-detail/copiloto/notifications/details-panel quedan bespoke por diseño.

Relacionado: [[zindex-capa-overlay-orden-portal]] · [[controles-form-nativos-no-estilables-construir-componente]]
