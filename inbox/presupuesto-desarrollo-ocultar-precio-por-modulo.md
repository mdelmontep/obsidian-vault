---
title: presupuesto-desarrollo — opción para ocultar el precio por módulo
date: 2026-09-24
source: simarro
tags: [inbox, skills, presupuestos]
---
El motor `~/.claude/skills/presupuesto-desarrollo/scripts/presupuesto_desarrollo.py` pinta siempre el precio de cada módulo. Para el P2026-0024 (Simarro) y el P2026-0023 hizo falta sin desglose: se resolvió con una copia parcheada en el scratchpad (`etiqueta_precio` por módulo: vacío o «Incluido»). Propuesta: flag `ocultar_precios_modulos` + `etiqueta_precio` opcional en el JSON.
