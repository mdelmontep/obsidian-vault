---
title: una piel de tokens solo alcanza lo que no está escrito a mano
date: 2026-08-28
source: facturaia
tags: [diseno, css, tokens, design-system, medicion]
---

La piel `freebie`/Cristal de TuFacturaIA redefine `--radius` y compañía, y aun así solo cambiaba la **forma del 2 % al 16 %** de las cajas pintadas: unas 105 declaraciones escribían `border-radius: 12px` a mano y la piel les pasaba por encima sin tocarlas.

**La métrica útil no es cuántos tokens redefine la piel, sino qué fracción de lo pintado cambia al encenderla.** Se mide en el navegador, no leyendo CSS: recorrer los elementos visibles con `getComputedStyle` con la piel apagada y encendida, y contar cuántos valores de destino se mueven. Contar declaraciones en el CSS da un número bonito y falso; contar tokens definidos, peor.

**Fix:** dar peldaño propio a cada valor que se repetía a mano (`--radius-md: 8px`, `--radius-card: 12px`) y migrar los sitios. Alcance en el dashboard 16 % → 40 %, en conciliación 2 % → 16 %. Lo que queda sin migrar es exactamente la distancia entre ese 40 % y el 100 %: es contable, no una sensación.

Corolario: un componente que **deriva** de un token (`calc(var(--radius-card) + 6px)`) conserva su escalón en las dos pieles; escrito a mano, la piel sube uno de los dos y el diseño pierde la relación que lo definía.

Ver [[un-token-definido-bajo-un-selector-que-nadie-produce-no-existe]] · [[un-fix-en-una-media-query-sobre-un-selector-que-no-existe-ahi-es-codigo-muerto]]
