---
title: una medida limpia que no llega al umbral es el resultado, no un fallo
date: 2026-09-24
source: facturaia
tags: [medicion, harness, decisiones]
---

El A/B de la palanca L2-1 salió limpio: Δ = 7,55 s (mediana A 7.597 ms vs B 51 ms,
`load1` 3,1-4,3). Pasaba con la fracción optimista (f=24,67 % → 35,6 s/sesión) y
rozaba con la revisada (f=21 % → 30,3 s frente a un umbral de 30). Tentación clara:
publicar el f que la salva. **Se descartó**, porque el criterio escrito ANTES exigía
pasar también con f=15 % (21,6 s) y que la mediana de A fuese ≥ 8 s (dio 7,60).

**Patrón:** el criterio de adopción se fija antes de ver el número; después solo se
aplica. Elegir la f, el percentil o la muestra a la vista del resultado es elegir la
conclusión, y encima parece un dato. Un «no llega» medido vale más que un «pasa»
negociado, porque cierra la pregunta.

Lo que sobrevive a la palanca descartada es el dato: esas dos etapas del `pre-push`
cuestan 7,5 s, no los ~17 s que afirmaba el comentario del propio hook.
Ver [[una-lectura-de-load1-no-acredita-una-ventana-de-medida]].
