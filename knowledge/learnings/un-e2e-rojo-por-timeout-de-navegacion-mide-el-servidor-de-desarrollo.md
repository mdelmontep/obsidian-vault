---
title: un e2e rojo por timeout de navegación mide el servidor de desarrollo, no el producto
date: 2026-09-08
source: facturaia
tags: [e2e, playwright, nextjs, medicion]
---
`next dev` compila cada ruta la primera vez que alguien la pide. Con 8 workers de
Playwright encima, una página pública estática puede no llegar antes del timeout
del test — y eso se lee como «la ruta está rota».

El discriminador no es repetir la tanda: es **cambiar solo el servidor** y dejar
el árbol fijo en el mismo commit. Sirve el build (`next build && next start`) y
vuelve a correr los mismos ficheros. Rebasar a main a la vez mueve dos variables
y el resultado deja de discriminar.

Caso real (8-sep, facturaia, 43 rojos): `/privacidad` agotaba los 30.000 ms del
test y contra el build tardó 62 ms; `/verifactu`, 8 ms. Doce rojos eran del
arnés. Y ojo al literal: **«timeout 30.000 ms» no es «tardó 30 s»**, es «el test
se rindió»; no sabes cuánto habría tardado.

Los que sobreviven al build sí son candidatos a fallo real — o a
[[una-base-de-staging-por-detras-deja-un-candado-sin-medir]].
Ver [[e2e-baseline-contra-main-antes-de-culpar-a-tu-rama]].
