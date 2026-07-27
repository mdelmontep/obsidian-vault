---
title: un camino crítico sin smoke se pudre durante meses aunque tenga miles de tests unitarios alrededor
date: 2026-07-27
source: claude-code-session
tags: [testing, arquitectura, qa, pdf]
---

TuFacturaIA tiene 7.541 tests unitarios y **ninguno arranca Chromium**. En el camino que
genera todas las facturas convivieron dos podredumbres independientes, cada una de ~2 meses:

- el microservicio `pdf-renderer` devolvía 500 en todos los renders desde que un refactor
  metió un `import` de CSS Module en una plantilla (tsx intenta parsear el `.css` como JS);
- la vista previa enseñaba 150 px del PDF y el resto en blanco.

Las dos se encontraron por accidente el mismo día, una construyendo la imagen a mano y la
otra abriendo la pantalla en el navegador.

Lo que sí se prueba (helpers, cálculos, plantillas como componentes React) no toca el
motor ni el visor. El smoke que faltaba es barato y determinista: llamar a la función de
render con el payload de ejemplo y afirmar cabecera `%PDF`, nº de páginas y que el texto
extraído contiene número y total. Para el visor, un paso de Playwright que compruebe
geometría (el iframe mide > N px), sin comparación de imágenes.

Regla general: **si un camino produce el artefacto que ve el cliente y no hay un test que
lo produzca de verdad, ese camino está sin cubrir por mucho porcentaje que diga la suite.**
Corolario del mismo día: el microservicio llevaba meses desplegándose sin que lo llamara
nadie — código muerto pero en producción, ver [[defensa-cableada-vs-codigo-muerto]].

Ver [[iframe-con-flex-1-en-contenedor-no-flex-cae-a-150px]] · [[validar-cambio-de-motor-de-render-con-ab-de-misma-imagen]]
