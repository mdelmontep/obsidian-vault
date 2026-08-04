---
title: al extraer un subconjunto de un design system, cruza var(--x) usadas vs definidas — no a ojo
date: 2026-08-04
source: claude-code-session
tags: [css, design-system, frontend, qa]
---
Copiar 5 componentes reales (`.tsx`+`.module.css`) a un starter y decidir a ojo qué tokens
"hacen falta" se queda corto: una `var(--x)` no definida no da error de build ni de lint, el
navegador simplemente ignora la declaración o usa el valor inicial/heredado. El componente
se renderiza, solo que sin ese color/sombra/lo-que-sea — se lee como "raro", no como "roto".

Pasó extrayendo un starter de TuFacturaIA: exclude "a propósito" el morado IA/admin y la
familia pomegranate por parecer "de negocio", y resulta que `Button` (`tone="ai"`) y
`EstadoPill` (familia `pomegranate`) sí las usan de verdad — no eran opcionales.

**Fix mecánico, no revisión manual**:
```
grep -ohE '\-\-[a-z0-9-]+' components/*.css | sort -u > usadas.txt
grep -oE '^\s*--[a-z0-9-]+' tokens.css | tr -d ' ' | sort -u > definidas.txt
comm -23 usadas.txt definidas.txt   # usadas sin definir
```
Filtra los falsos positivos: custom properties que el propio componente declara localmente
(`--banner-tint: var(--brand)`) y coincidencias de substring en nombres de clase BEM
(`.billing-banner--info` contiene `--info`, no es un `var(--info)`).
