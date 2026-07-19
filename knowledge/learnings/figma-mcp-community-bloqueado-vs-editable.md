---
title: figma mcp — el community bloqueado solo da raster; el editable es otro fichero
date: 2026-07-20
source: claude-code-session
tags: [figma, mcp, design-to-code, tooling]
---
Al replicar un diseño de Figma Community vía Figma MCP (`mcp.figma.com`, auth OAuth):

- El fichero **community gratis bloqueado** ("Buy me a coffee $2 to unlock") solo expone la versión **aplanada a raster**: `get_variable_defs` → `{}` y cada capa vuelve como `<img>`. Imposible sacar specs exactos.
- El "$2 unlock" **NO desbloquea ese fichero**: entrega uno **editable distinto** (otro `fileKey`) por email/Gumroad. Hay que abrir ESE y duplicarlo a Drafts.
- Con el editable: `get_design_context` sobre el nodo del componente da fill/stroke/sombras/tipo exactos; `download_assets` con `defaultFormat: svg` da el **path vectorial real + el filtro SVG** (que es el stack de box-shadow). El Dev Mode redondea (0.075→0.08); el export crudo trae el valor fino.
- Un `<Icon>` monocromo compartido usado en N sitios NO se toca para un cambio local: componente/asset local (p.ej. `<img>` del SVG en /public, aísla ids de clipPath al repetirse).

Caso real FacturaIA: botón «Ask» Glass Button 2.0 → topbar + Copiloto, PR #1054. Ver [[facturaia]].
