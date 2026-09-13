---
title: cache components: searchParams solo dentro de suspense, y el swap del fallback necesita js
date: 2026-08-20
source: facturaia
tags: [nextjs, cache-components, ppr, streaming]
---

Con Cache Components (Next 16), leer `searchParams` en una página revienta el **build**
(«Uncached data was accessed outside of <Suspense>») aunque en dev funcione. El patrón:
pasar la **promesa** de `searchParams` a un server component hijo que la awaitea dentro
de `<Suspense>`; la ruta queda ◐ Partial Prerender y el contenido real llega **en el
mismo stream HTML** de la respuesta (no tras hidratar, como `useSearchParams` de cliente).

Letra pequeña: el swap fallback→contenido lo hace un script inline, así que un cliente
con JavaScript deshabilitado ve el **fallback**. Si el dato es crítico (un gclid en un
CTA), el fallback debe degradar con sentido y la decisión quedar registrada.

Medido contra el build (13-sep): React retiene el swap, que llega **36-507 ms** después de pintarse
lo de fuera del Suspense. Un E2E que lee el atributo nada más ver el titular lee el fallback: usar
una aserción que espera (`toHaveAttribute`), y comprobar el HTML servido aparte con una petición.

Caso real: landing del apex de TuFacturaIA (FB-10, ADR-020) — el gate cazó que el CTA
perdía el gclid hasta hidratar; el fix fue exactamente este patrón.
