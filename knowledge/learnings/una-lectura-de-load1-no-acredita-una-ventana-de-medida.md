---
title: una lectura de load1 no acredita una ventana de medida
date: 2026-09-23
source: facturaia
tags: [harness, medicion, fia-gate, claude-code]
---

Una tanda A/B nocturna sobre el arnés (facturaia, 05:21-06:38) midió tres palancas y
**ninguna salió publicable**, no por ser malas ideas: por la carga de la máquina.
`load1` a cada intento: 32,4 (02:13) · 17,3 (03:17) · 7,35 (04:19) · 2,36 (05:21, se
midió) · y de vuelta a 10-15 a las 06:12, cuando otras dos sesiones arrancaron un
`e2e:smoke` y un `tsc`. De 6 filas de un A/B, 5 se midieron con load1 entre 9,8 y 24,6.

**Patrón:** una lectura puntual de `load1` dice cómo está la máquina AHORA, no cómo
estará durante los 20 min de la medida. Con sesiones en paralelo hay que corroborar con
`ps aux` que nadie tiene vivo un `tsc`, un `next build` o un Playwright, igual que
`0/3` en [[fia-gate]] no significa máquina libre. Y si el A/B no es a carga simétrica,
el Δ no vale: el único par simétrico de aquella noche invirtió el signo del resultado.

**Corolario:** publicar «Δ = 49 s» de una muestra asimétrica es peor que no medir, porque
parece un dato. Mejor decir «no decidible» y guardar la receta.
Ver [[un-ensayo-en-seco-que-sustituye-el-gate-no-prueba-la-medida]].
