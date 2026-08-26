---
title: subir ancestros buscando el texto de una fila clica la de al lado
date: 2026-08-26
source: facturaia
tags: [qa, agent-browser, playwright, smoke, dom]
---

Para pulsar el botón de UNA fila concreta en un smoke, el patrón «coge todos los
botones y quédate con el que tenga mi texto en algún ancestro» está roto:

```js
let n = boton; for (let i=0;i<6;i++){ n=n.parentElement; if (/ionos/.test(n.innerText)) return true }
```

A pocos niveles ya estás en el contenedor de la LISTA, cuyo `innerText` contiene
**todas** las filas: el filtro dice sí para el primer botón y borras la fila
equivocada. Y como la acción es legítima, responde `DELETE 200`: no hay ninguna
señal de error, solo un dato que ya no está.

Filtrar por algo **propio de la fila**: el `id` que ya viene en el payload del
endpoint, un `data-*`, o el `closest('li'/'tr'/'[data-id]')` exacto. Nunca el
texto de un ancestro cuyo nivel no controlas.

Mismo error de fondo que [[arnes-con-asserts-de-eco-y-falso-verde-no-detecta-nada]]:
el instrumento afirmó algo que no había comprobado.
