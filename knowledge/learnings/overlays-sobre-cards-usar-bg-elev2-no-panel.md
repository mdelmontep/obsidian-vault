---
title: overlays sobre cards — usar token elevación superior, no --panel
date: 2026-05-11
source: claude-code-session
tags: [css, frontend, design-tokens, gotcha]
---

Tooltip / popover / dropdown / context menu posicionado sobre una card del mismo color = se ve transparente. Pasa cuando el sistema de tokens tiene varios niveles (`--bg`, `--bg-elev`, `--bg-elev2`, `--panel`) y eliges el mismo que el surface debajo.

**Patrón**:
- Surface base (card normal): `--panel`
- Overlay sobre surface: `--bg-elev2` (o el tier más alto disponible)
- Sombra doble fuerte: `0 16px 48px rgba(0,0,0,0.32), 0 4px 12px rgba(0,0,0,0.20)`
- `isolation: isolate` para evitar que un ancestor con `backdrop-filter`/`transform` lo desvanezca

**Caso real FacturaIA**: tooltip de info en `/admin/system/crons` (componente `InfoTooltip`) usaba `var(--panel)` igual que la card debajo → invisible. Fix con `--bg-elev2` + shadow doble + isolation.

**Generalización**: cualquier overlay flotante sobre una card debe estar **un escalón por encima** en el sistema de tokens. Si tu design system solo tiene `--bg` y `--panel`, añade un `--popover-bg` o usa box-shadow muy marcado para crear separación visual.
