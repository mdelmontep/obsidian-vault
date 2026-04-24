---
title: test manual tanda 2 y 3 — facturaia
date: 2026-04-21
source: test manual en localhost
tags:
  - facturaia
  - borja
  - test
  - design-system
---

# Test manual — Tanda 2 + Tanda 3

PRs mergeados a main el 21/04/2026: #2 (Tanda 2 — tokens, focus ring, fuentes PDF) y #3 (Tanda 3 — empty states, skeletons, tablas móvil, a11y).

## Aprobados

- **EstadoPill**: colores correctos con tokens semánticos (pendiente azul, cobrada verde, incobrable pomegranate, borrador/rectificada neutral)
- **Drop-zone ingesta**: icono, título, hint "PDF, JPG, PNG, WebP o HEIC · máximo 10 MB", borde dashed
- **ProgressBar ingesta**: barra visual verde "12 de 22 aprobadas" reemplaza el counter textual
- **Empty state presupuestos**: "Aún no tienes presupuestos" con descripción e icono
- **Empty state filtros sin match**: "Sin resultados con estos filtros" con hint. Distingue bien de "no hay datos"
- **Focus ring**: outline azul visible en tab-navigation
- **Disabled styles**: opacity 0.5, cursor not-allowed
- **Formulario generar**: correcto, empieza con 1 línea

## Issues encontrados

1. ~~**Mobile responsive (< 767px)**~~: RESUELTO (2026-04-25) — filtros apilados, cards 1 columna, pills con scroll horizontal, tabla scroll optimizada, preview fullscreen en móvil.
2. **Preview PDF en Generar**: algunos campos aparecen fuera de posición y apilados. La tipografía parece Filson pero el layout del PDF tiene problemas de maquetación.
3. **PDF descargado**: falta verificar descargando el PDF real y comprobando fuentes embebidas y layout.
4. **autoFocus modal edición**: no se pudo verificar.

## Próximos pasos sugeridos

- Tanda 4 (dominio fiscal) según roadmap
- Tanda dedicada a mobile responsive
- Fix del layout de la preview/PDF en Generar (campos apilados/fuera de posición)
