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
2. **El precio NO es por unidad: es por lote.** Precio real = `precio_tarifa / divisor`.
   Sin dividir cargas precios ×1000. **OJO: el nombre de la columna divisora
   varía entre exports Telematel** — no asumir:
   - Export "Actualizar tarifas ERP" (GO!Catalog): divisor = columna `UNIDADES` (1, 1000…).
   - Export WAPI (MARCA/REFERENCIA/SERIE/FAMILIA/UNIDADES/UD. PRECIO): ahí
     `UNIDADES` es el **código** de unidad (PZ/MT/JU/KI), y el divisor numérico
     es la columna **`UD. PRECIO`** ("unidad de precio"). Invertirlas = precios
     mal + `UNIDADES inválidas PZ` (caso real obras-076, 20-jul: la tabla-resumen
     del doc las tenía cruzadas; el vídeo/transcript WAPI fue la fuente de verdad).
3. **Decimales de ese formato:** un punto con 1-2 dígitos detrás es decimal US
   (`22.70`→22,70; `1.00`→1), con 3 = miles ES (`1.000`→1000); con coma presente
   → siempre ES. No asumir un único locale (ver [[csv-import-precio-decimal-es-us-desambiguar-no-asumir]]).

Regla: capturar un fichero REAL y verificar encoding + qué columna es el divisor
ANTES de codificar el importador. El header nominal (y hasta la tabla-resumen del
proveedor) miente sobre el contenido. Ver [[transcribir-video-sin-audio-extraer-fotogramas-ffmpeg]].
