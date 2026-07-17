---
title: importar CSV de ERP/tarifa español = cp1252 + ';' + normalizar precio por unidad-múltiple
date: 2026-07-17
source: claude-code-session
tags: [import, csv, erp, telematel, facturaia, obras]
---
Los exports de tarifas de ERPs españoles (Telematel/GO!Catalog "Actualizar
tarifas ERP", y similares) vienen con dos trampas que NO se ven hasta que
parseas de verdad:

1. **Codificación latin1/Windows-1252, no UTF-8.** Separador `;`. Si lo lees
   como UTF-8 salen `�` en ARTÍCULO/DESCRIPCIÓN/CÓDIGO. Decodifica cp1252.
2. **El precio NO es por unidad: es por lote.** Hay una columna `UNIDADES`
   (1, 1000…) y el `P.V.P.` es para ESE lote. Cable a `P.V.P.=2517,00` con
   `UNIDADES=1000` = **2,517 €/m**, no 2.517 €/m. Precio real = `P.V.P. / UNIDADES`.
   Sin dividir cargas precios ×1000.

Regla: capturar un fichero REAL y verificar encoding + columna de unidad-múltiple
ANTES de codificar el importador. El header nominal miente sobre el contenido.
Ver [[transcribir-video-sin-audio-extraer-fotogramas-ffmpeg]].
