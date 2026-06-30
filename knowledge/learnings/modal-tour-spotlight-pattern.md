---
title: tour spotlight in-modal — tourHighlight necesita fondo propio, no solo outline
date: 2026-06-30
source: claude-code-session
tags: [frontend, ux, onboarding, facturaia]
---

Tutorial guiado tipo spotlight (velo + zona resaltada + tooltip), sin librerías externas.

**Bug real**: `tourHighlight` con solo `outline:2px solid var(--brand)` y sin `background`
propio no se distingue del velo oscuro si el panel detrás es translúcido/glass — el velo
se filtra igual a través de la zona "marcada" y el usuario no percibe nada resaltado.
Fix: la zona activa necesita `background: var(--bg-elev)` (opaco, no heredado del panel)
además del outline/glow.

**Capas** (contenedor `position:relative`): `tourBlocker` (inset:0, z-5, velo oscuro) →
`tourHighlight` (z-10, fondo propio + outline) → `tourTooltip` (z-20, `style` por step).

**Ya no se copia por modal**: extraído a componente compartido
`src/components/ui/{onboarding-tour,use-onboarding-tour}.tsx` — un cambio de diseño se
propaga a todos los tours del proyecto. Skill de referencia: `fia-onboarding-tour`
(proyecto-local, con registro de qué vistas lo usan) y versión genérica para otros
proyectos del equipo en `agentesia-skills/onboarding-tour-spotlight`.
