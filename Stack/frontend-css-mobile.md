---
title: frontend — CSS mobile y overflow
date: 2026-04-20
source: claude-md-migration
tags: [frontend, css, mobile, overflow]
---

# Frontend / CSS Mobile

## Flex-direction: column en mobile

- **`flex-basis` pensado para ancho pasa a medir ALTO** si el breakpoint mobile cambia el contenedor a `flex-direction: column` — el eje principal rota con la dirección. Un input con `flex: 1 1 240px` se infla a 240px de alto en vez de mantener 240px de ancho. Resetear explícito en el media query: `flex: none; width: 100%;`. Ver [[flexbasis-en-flex-direction-column-se-interpreta-como-alto]]

## Overflow horizontal — causas y fixes

- **`flex` container tiene `min-width: max-content` por defecto** — un `div` o `p` con `display: flex` dentro de un CSS Grid sin `min-w-0` puede expandir el grid track y hacer la página más ancha que el viewport. Fix: `min-w-0` en el grid item + `min-w-0` en el flex container + `truncate` en los spans de texto largo.

- **`inline-flex` sin ancho explícito = riesgo de overflow en mobile** — un elemento con `inline-flex` que contiene texto largo se expande hasta su `max-content` y desborda. Siempre usar `flex w-full sm:w-auto sm:max-w-X` o al menos `max-w-full` cuando el contenedor es mobile.

- **`overflow-x: hidden` en ancestros no resuelve el overflow si no se elimina en el origen** — si un elemento es más ancho que el viewport, `mx-auto` centra dentro del layout width (más ancho), y el `overflow:hidden` recorta el lado derecho. La solución es añadir `min-w-0`/`overflow-hidden` en el elemento infractor, no en los ancestros.

- **`tracking-[N]` uppercase en flex container puede desbordar en pantallas < 375px** — textos con letter-spacing alto miden más de lo esperado. Siempre añadir `min-w-0` + `truncate` a spans dentro de flex containers con letter-spacing alto.

- **`grid-column: span N` en un grid colapsado a 1 col (mobile) crea una columna implícita** y ensancha el grid fuera del viewport. Fix: `grid-column: 1 / -1` (ancho completo en 1 y 2 cols, sin track implícito). Caso facturaia `/generar` (PR #161).

- **Un `overflow-x:auto` cuyo contenido excede su scroll-box expande el LAYOUT VIEWPORT móvil** (`innerWidth` crece, todo "encoge para caber"); `overflow:clip`/`hidden` en ancestros NO lo arregla. Fix: `contain: layout` en el contenedor scrollable (aísla el subárbol; el scroll interno sigue; overlays por `createPortal`). Caso facturaia tablas `has-vf`/`has-origen`. Ver [[mobile-overflow-layout-viewport-contain-y-grid-span]]

## Sticky headers y contenido en scenes móvil

- **Padding-top extra obligatorio cuando hay barra sticky flotante** — si una sección tiene una pill/nav sticky (ej: indicador de paso) que flota sobre el contenido, el primer scene necesita al menos 36-40px de padding-top en móvil. 18px no es suficiente y el título se solapa con la pill.
- **Números grandes + símbolo en móvil necesitan `whitespace-nowrap`** — "78%" se parte en "78" y "%" si el contenedor flex no tiene `whitespace-nowrap`. Aplica a cualquier stat card con número + sufijo (%, +, s, x).

## Checklist al depurar overflow en mobile

1. Buscar `inline-flex` sin `max-width` o `w-full` → cambiar a `flex` o añadir `max-w-full`
2. Buscar `flex items-center` sin `min-w-0` dentro de grid items → añadir `min-w-0` al grid item Y al flex container
3. Buscar texto con `tracking-[N]` o `uppercase` dentro de flex → añadir `truncate`
4. Añadir `overflow-x-hidden` a la sección que contiene el overflow, no solo al body/html
5. Medir en browser `window.innerWidth` vs `body.scrollWidth` vs `window.scrollX`, no fiarse del ojo ni de screenshots `fullPage`: si `pageScrollX=0` pero `innerWidth>vw`, es el viewport de layout expandido (scroll container interno) → `contain:layout`, no overflow de página

## Modales y popovers

- **Popover dentro de modal con `overflow: hidden` se corta** — el ancestro clipa al popover absoluto. Soluciones: portal con `position: fixed` + `getBoundingClientRect`, o disclosure inline (el popover es un `<div>` siguiente que empuja contenido). Inline es más simple y mejor en móvil. Ver [[popover-en-modal-con-overflow-hidden-se-corta-usar-inline-disclosure]]
- **Popover/menú anclado a un trigger** → `@floating-ui/react` (hook `useAnchoredMenu` en FacturaIA), no `getBoundingClientRect` + flip manual (frágil). Posicionar con `top/left`, no `transform`. Ver [[react-hooks-refs-falso-positivo-floating-ui]] · ADR-033

## `dvh` y viewports dinámicos iOS

- **Cascada doble declaración `vh` → `dvh`, NUNCA `min(vh, dvh)` atómico**. Safari <15.4 no soporta `dvh`; si va dentro de `min()` la función entera se descarta y la propiedad queda sin valor. Patrón seguro:
  ```css
  max-height: calc(100vh - 240px);     /* fallback */
  max-height: calc(100dvh - 240px);    /* gana donde haya soporte */
  ```
  Si el valor vive en `style={{...}}` inline (React) no se puede declarar dos veces → mover a clase CSS. Caso real: `voz-variables-form.tsx` con `min(calc(100vh-240px), calc(100dvh-240px))` → rompía el modal entero en Safari 15.0-15.3. Ver [[mobile-vh-dvh-cascade-vs-min-atomic-safari-15]].

## Drawer mobile a11y — `inert` + `aria-hidden` + restore-focus

- **`inert` + `aria-hidden` complementarios**. `inert` (Safari 15.5+, Chrome 102+) bloquea Tab + interacción puntero, pero iOS 15.0-15.4 lo ignora. Añadir `aria-hidden={open || undefined}` en paralelo cubre VoiceOver en esa franja:
  ```jsx
  <main inert={open || undefined} aria-hidden={open || undefined}>
  ```
- **Restore-focus tras `inert` debe ir en `requestAnimationFrame`**. WebKit descarta silenciosamente `.focus()` sobre un elemento aún `inert`. Si haces `setOpen(false)` + `trigger.focus()` en el mismo tick, React aún no ha re-renderizado → focus se pierde. Patrón: `useRef` previo + `useEffect` con `requestAnimationFrame` para focusear tras el re-render. Ver [[mobile-restore-focus-after-inert-needs-raf]].
- **Focus trap real**: al abrir drawer, focus al primer interactivo (X de cerrar). Listener `keydown` en el aside que cicla Tab/Shift+Tab entre primer y último focusable (`querySelectorAll('a[href], button:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])')`). Sin trap el foco escapa al body cuando llega al último link.

## Tablas con scroll horizontal y WCAG 2.1.1

- **Wrapper `<div role="region" tabIndex={0} aria-label="...">`** alrededor de `<table>` con `overflow-x: auto`. Sin `tabIndex={0}` el usuario de teclado no puede hacer scroll horizontal — falla WCAG 2.1.1 (Keyboard). El `<table>` mantiene su role implícito intacto. Patrón:
  ```jsx
  <div className="set-table-wrap" role="region" tabIndex={0} aria-label="Tabla de usuarios">
    <table style={{ minWidth: 600 }}>...</table>
  </div>
  ```
  CSS: `.set-table-wrap { overflow-x: auto; border-radius: inherit; } .set-table-wrap:focus-visible { outline: 2px solid var(--brand); outline-offset: 2px; }`. Una clase reusable evita el patrón de 5 inline-styles duplicados. Ver [[mobile-table-scroll-x-needs-region-tabindex-wcag-2-1-1]].
- **`WebkitOverflowScrolling: 'touch'`** es legacy (iOS 13+ default). No daña pero contamina — eliminar.

## Tabla densa → tarjeta en móvil

- **Al colapsar una `<table>` a tarjetas en móvil, prefiere disclosure inline a scroll horizontal**: chevron que despliega los campos ocultos en una línea extra; el tap-fila sigue abriendo el detalle. Reutiliza una celda con `display:none` en desktop → `colSpan` no cambia. Ojo: `display:flex` en un `<td>` lo saca del layout de tabla y **rompe el `colSpan`** en desktop → acótalo al `@media` móvil (donde el `<tr>` ya es `block`); para alinear sumas usa `margin-left:auto`, no `float:right`. Y `text-overflow:ellipsis` heredado en un `td`/`th` estrecho pinta "…" sobre hijos no-texto (checkbox/badge) → `overflow:visible; text-overflow:clip` en esas columnas. Caso facturaia `fact-table` (2026-06-26). Ver [[tabla-densa-a-tarjeta-en-movil-ellipsis-y-colspan]].

## Mobile Auth — Inputs y touch targets

- **iOS zoom = `font-size < 16px` en inputs** — Safari auto-hace zoom cuando el input enfocado tiene font-size < 16px. Fix definitivo: `font-size: 16px` en todos los `input`, `select`, `textarea` en la hoja global.
- **Touch targets: `min-height: 44px` + `min-width: 44px`** — aplica a botones, password-eye toggles y cualquier elemento interactivo pequeño.
- **Password-eye con padding en vez de size** — `padding: 12px` en el botón + `min-width/height: 44px`. Ajustar `padding-right` del input al nuevo tamaño del botón.
- **`env(safe-area-inset-*)` en pantallas auth mobile** — `padding-bottom: env(safe-area-inset-bottom, 16px)` en el scroll container. Sin esto el contenido queda cortado bajo el home bar de iOS.
- **`inputMode="tel"` en campos de teléfono** — abre teclado numérico en iOS/Android directamente, sin depender del `type="tel"`.
- **Un icono con `opacity: 0` sigue ocupando ancho** — la flecha de ordenar reservaba 12 px + 4 de `gap` en TODAS las cabeceras, también donde nunca se ve, y por eso una columna estrecha recortaba el rótulo con "…" dejando un hueco que parecía libre (medido: 41 px útiles para un rótulo de 46). Icono a `position: absolute` + `padding-right` equivalente solo donde es permanente (columna activa) o el texto va pegado al borde (numéricas). Mide el NODO DEL TEXTO (`scrollWidth > clientWidth`), no la celda. Caso TuFacturaIA #1341. Ver [[icono-invisible-en-linea-sigue-robando-ancho-al-rotulo]]
- **`table-layout: fixed` reparte los px declarados salvo que la tabla mida `width: 0`** — si el ancho de la tabla no coincide con la suma de sus columnas, el navegador reparte la diferencia EN PROPORCIÓN a los px, así que dejan de ser anchos y pasan a ser pesos: con `width:100%` reparte el del contenedor y con `max-content` el del CONTENIDO (peor: arrastrar una columna a 81px la dejaba en 232). Firma: todas las columnas escaladas por el mismo factor. `width: 0` + un `<th aria-hidden>` spacer sin ancho al final (se come el sobrante cuando `min-width:100%` estira). Caso TuFacturaIA materiales (PR #1328 lo introdujo, #1335 lo corrige). Ver [[table-layout-fixed-con-width-100-reparte-los-px-en-vez-de-respetarlos]]
- **`max-width:Npx` y `min-width:Npx` con el MISMO N se solapan exactamente en N** — a 768px ambas queries aplican; si una oculta un panel (`display:none`) y la otra ya cambió la rejilla a 2 columnas, la mitad queda en blanco. Usar límites asimétricos: mobile `max-width:767px`, tablet `min-width:768px`. Caso TuFacturaIA login (PR #704).
- **Dos breakpoints DISTINTOS para una misma transición (ej. 767px móvil-compacto vs 1100px sidebar-fijo) dejan una franja tablet sin tratar** — si el layout completo (columna fija) solo cae a 1 columna en 1100px pero el modo compacto (barra de chips) solo activa en 767px, todo lo que hay entre 767-1100px (iPad portrait típico) pierde la columna fija SIN ganar el modo compacto: queda la lista completa desplegada tapando el contenido. Al auditar un sidebar/nav con 2+ media queries, comprobar el rango ENTRE ellas, no solo cada breakpoint aislado. Fix: unificar ambos al mismo número. Caso TuFacturaIA `/settings` (PR #754, ticket iPad).

## CSS Grid · trampas de layout en cards móvil

- **2+ items con el mismo `grid-area` se solapan en la misma celda** — si tienes 2 `<td>` o `<div>` apuntando a `grid-area: footer`, el segundo se renderiza encima del primero, no debajo. Solución: usar `grid-column: 1 / -1` en cada uno y dejar que `grid-auto-flow: row` (default) los coloque en filas implícitas sucesivas. Caso real NotCaído mobile: `down-since` + `error chip` ambos con `grid-area: footer` → solapados invisibles. Fix: `grid-column: 1 / -1` en ambos.

- **Columna `auto` toma el ancho del item más ancho de CUALQUIER fila** — `grid-template-columns: auto 1fr auto` con un dot 14px (col 1 row 1) y un toggle 48px (col 1 row 3) hace que la col 1 mida 48px en TODAS las filas. Resultado: el dot de la fila 1 queda con un hueco enorme a su derecha. Solución: usar más columnas + `grid-template-areas` con span (`"dot name name" / "dot probes probes" / "tog tog acts"`) para que la col del dot no comparta tamaño con la col del toggle.

- **Cache-bust manual de CSS en Jinja/HTMX/Flask** — incrementar `?v=N` en `<link rel="stylesheet" href="/static/styles.css?v=N">` cada vez que cambias el CSS. Sin esto, deploys con caché agresivo (Cloudflare, Dokploy + Traefik con `Cache-Control: public, max-age=...`) no se ven en clientes que tengan la versión vieja. Caso real NotCaído: bumps `v=11→12→13→14` durante iteración móvil.

- **Next 16 + lightningcss: NUNCA escribir `-webkit-backdrop-filter` a mano** junto al `backdrop-filter` estándar. El minificador colapsa el par y deja SOLO el `-webkit-`; Chrome moderno lo IGNORA (usa el sin prefijo) → `backdrop-filter` computa `none` → cero blur en TODA superficie glass/scrim, sin error de build/lint. Regla: escribir **solo `backdrop-filter`**, el build añade el prefijo. Corolario: tokens de blur (`--glass-blur`/`--scrim-blur`) en `:root` base, NO en `[data-theme=light]` (selectores hermanos no heredan → en dark indefinidos → `blur(var(--undef))` inválido → none). Diagnóstico: `curl` el chunk CSS servido (`/_next/static/chunks/src_*._.css`) y mira la regla compilada — headless NO renderiza/reporta backdrop-filter fiable; un `<div>` con `backdrop-filter` inline SÍ (descarta que sea GPU). Caso TuFacturaIA 2026-06-10, costó horas.
- **Cascada de clases glass decorativas**: shorthand `background:` posterior pisa el `background-image` de una clase compuesta (usar `background-color:`); guards de fallback (`@supports not`/`prefers-reduced-transparency`) al FINAL del archivo o quedan muertos a igual especificidad. Ver [[css-clase-decorativa-compartida-trampas-cascada]]
- **Selector multi-toggle ≠ `filter-pill.active`** (TuFacturaIA) — `.filter-pill.active` es azul sólido (pensado para selección única, tipo segmented); con N opciones activas a la vez = muro de azul feo. Para multi-select clonar el popover del **Select** del sistema (`composes glass-strong+glass-sheen from global` + `useAnchoredMenu` portado a `<body>` + filas `.option` con punto de color + check), no pills. Caso: selector de "Capas" del calendario (#382).

## Punteros recolocados desde hot.md (2026-07-27)

_Salieron del índice caliente al reservarlo a método/riesgo transversal; el learning está íntegro en `knowledge/learnings/`._

- **Tooltip sobre botón `disabled`** — ver [[tooltip-en-boton-disabled-necesita-pointer-events-none-y-tabindex-wrapper]]
- **Auditar "0 consumidores" de una clase CSS antes de borrarla: grep `\bclase\b` sin anclar, no solo `className="clase"`** — ver [[grep-classname-plano-subestima-template-literals]]
- **Grab-to-scroll (arrastrar con ratón): NO `setPointerCapture` en contenedor con links/botones** — ver [[drag-scroll-no-setpointercapture-en-contenedor-con-links]]
- **Botón de design-system con `overflow:hidden`: borde/halo animado va en PSEUDOS del botón, no en un `<span>` hijo** — ver [[boton-design-system-overflow-hidden-halo-y-linea-en-pseudos-del-boton]]
- **Centrar número+sufijo dentro de un input como unidad** — ver [[centrar-numero-mas-sufijo-en-input-field-sizing-fallback-ch]]
- **Iframe con `flex:1` en un padre que no es flex → 150px (su alto por defecto), parece contenido recortado** — y `min-height` en el ancestro no habilita `height:100%` en el hijo. Ver [[iframe-con-flex-1-en-contenedor-no-flex-cae-a-150px]]
- **Escape cierra el modal de más: el culpable no suele ser el popover** — antes de tocar `floating-ui`, mira quién más escucha la tecla. Ver [[escape-en-modal-el-culpable-no-es-el-popover-de-floating-ui]]
- **`'use cache'` keyado por org ignora la impersonación** — cabecera y filas de la misma pantalla discrepan. Ver [[use-cache-keyado-por-org-sirve-datos-de-la-org-anterior-al-impersonar]]
- **El CLS medido contra `next dev` es ficción** — StrictMode corre los efectos dos veces, y un componente que hace `setLoading(true)` en su cargador y devuelve `null` se DESMONTA tras haberse pintado: la atribución sale como un salto enorme "hacia arriba" que en producción no existe. El dev server señala al culpable por `sources`; la cifra sale de `build`+`start`. Ver [[no-medir-cls-contra-next-dev-strictmode-desmonta-lo-ya-pintado]]
- **El suelo de una fila de tabla es su elemento más alto, no el padding** — un tap target de 44px en el botón compartido hace la fila densa imposible; sepáralo por `pointer: fine`. Ver [[el-tap-target-del-boton-compartido-es-el-suelo-de-la-altura-de-fila]]
- **Y al separarlo por puntero, la COLUMNA que aloja ese botón tampoco puede tener un ancho** — dimensionada al caso ratón, en táctil los dos botones se desbordan sobre la columna de al lado. Ancho a variable con el TÁCTIL por defecto, total con `calc()`, y el test leyendo el tamaño del botón de su propio fichero (con literales, subirlo deja el test verde). Ver [[columna-que-aloja-un-control-necesita-un-ancho-por-tipo-de-puntero]]
- **El cero de "aún no lo sé" no es el de "está vacío"** — si un contador en su valor neutro decide tamaño o presencia de un elemento, hay CLS garantizado; el estado de carga es un tercer valor. Ver [[cero-mientras-carga-no-es-cero-vacio-y-provoca-cls]]
- **Un contenedor `grid`/`flex` no lleva texto suelto entre sus hijos** — cada corrida de texto se vuelve ítem anónimo de rejilla. Un `<li>` con `display:grid` y `<strong>Título.</strong> resto…` manda el "resto" a la columna de 8px del bullet: una palabra por línea, sin ningún warning. Ver [[grid-en-el-li-manda-el-texto-suelto-a-la-columna-del-bullet]]
- **Una celda `sticky` no tapa por estar fijada: tiene que medir toda la fila Y ganar al `z-index` del primitivo que pasa por debajo** — si la fila centra sus celdas, la fijada mide su contenido y deja dos bandas; y el `<input>` `opacity:0` de un Checkbox (`z-index:2`) le roba el clic desde el contexto del contenedor. `align-self: stretch` + `isolation: isolate` en la fila. Se ve con `elementFromPoint`, no con una captura. Ver [[columna-congelada-se-tapa-con-altura-y-con-apilado]]
- **En un control con riel + opciones, el objetivo táctil es la OPCIÓN, no el riel** — el riel cumplía 28px y la opción medía 20. Se extiende el área pulsable con un pseudo del hijo, SOLO en vertical (a lo ancho se pisarían las opciones adyacentes) y sin salirse de la caja del control (fuera le roba el toque al vecino). Y el guard debe resolver el alto desde lo que la talla DECLARA, no desde el token que se supone que usa. Ver [[el-objetivo-tactil-de-un-control-compuesto-es-su-hijo]]
- **`:root{--x}` (0,1,0) pierde contra `:root[data-theme=…]` (0,2,0)** — un token inyectado en `:root` no pisa al del tema: el valor llega al DOM, se ve en el inspector y no pinta. Solo lo caza el valor COMPUTADO en un navegador de verdad; los unitarios validan la cadena de CSS y siguen verdes. Ver [[style-inyectado-con-root-pierde-contra-root-data-theme]]

## Ancho y desbordamiento (11-ago)

- **`word-break: break-word` NO evita que la página se dibuje más ancha que el teléfono.** No reduce
  el *ancho mínimo intrínseco*, que es con lo que el navegador decide el ancho de layout. Hace falta
  `overflow-wrap: anywhere`, en todo lo que lleve rutas, identificadores o URLs.
- El síntoma no es scroll lateral: es **todo el texto encogido**, sin barra que lo delate. A ojo
  parece "letra pequeña". Ver [[overflow-wrap-anywhere-no-break-word-o-el-movil-encoge-el-texto]]
- Se mide con el ancho de layout de `<html>` contra el del dispositivo — **nunca**
  `window.innerWidth`, que en emulación reporta el área desplazable y da falso positivo con
  cualquier bloque que tenga scroll propio.
- Culpable difícil de ver → bisección del DOM: ocultar elementos uno a uno y mirar el `scrollWidth`.
- **Migrar CSS a un `.module.css` pierde estilos SIN error**, y un empate de especificidad contra
  `globals.css` lo decide el orden de los chunks: haz LOCAL el modificador (el rival desaparece, no
  le ganas) y verifica con estilos computados indexados por RUTA de DOM.
  Ver [[empate-de-especificidad-entre-globals-y-un-module-lo-decide-el-orden-de-inyeccion]] ·
  [[baseline-de-estilos-computados-por-ruta-de-dom-para-migrar-css-sin-e2e]]

## Movido desde `hot.md` (poda del 14-ago)

Estaban en el índice de arranque, que se paga en TODA sesión sin disparador claro, y la regla del propio `hot.md` dice que un gotcha de un stack concreto no entra ahí: su casa es este fichero, que ya se carga cuando tocas lo suyo.

- **Preferencia por tenant restaurada de un `localStorage` global se filtra entre organizaciones** — el switch de empresa recarga y aplica la clave del tenant anterior. Sembrar en servidor. Encender una restauración muerta es cambio de comportamiento, no arreglo. Ver [[localstorage-global-en-app-multitenant-filtra-entre-organizaciones]]
