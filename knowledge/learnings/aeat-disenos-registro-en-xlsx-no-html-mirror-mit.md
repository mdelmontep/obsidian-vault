---
name: aeat-disenos-registro-en-xlsx-no-html-mirror-mit
description: Formato posicional TXT modelos AEAT viene en XLSX (no HTML público). Mirror MIT en GitHub con YAML normalizado.
date: 2026-05-22
source: claude-code-session
tags: [aeat, fiscal, txt-posicional, integracion]
---

**Problema**: las instrucciones AEAT publicadas en HTML (`sede.agenciatributaria.gob.es/.../instrucciones-2026.html`) describen casillas funcionalmente pero NO el diseño posicional del TXT para presentar telemáticamente. Sin ese formato no se puede emitir el fichero que sube el cliente a la sede.

**Fuente correcta**: `sede.agenciatributaria.gob.es/Sede/ayuda/disenos-registro/modelos.html` publica Excel oficial por modelo (`DR303e26v101.xlsx` v1.01 fechado 2026-01-28 para 303 ejercicio 2026, etc).

**Mirror MIT con YAML normalizado** (`generated_2026.1.yaml` 2.426 líneas, todos los campos con posición/longitud/tipo): `github.com/hokus15/ArrendaToolsModelo303/specs/2026`. Util para evitar parsear XLSX a mano.

**Estructura confirmada 303-2026**: encoding ISO-8859-1, salto CRLF, importes céntimos enteros con padding `0` izquierda + signo `N` líder para negativos, alfanuméricos padding espacio derecha. 8 páginas: registro_apertura, dp30300 (AUX), dp30301, dp30303 (IVA dev/ded), dp30304 (resultados 110/78/108/109/110/112), dp30305, dp303did, registro_cierre.

**Patrón aplicable a TODOS los modelos AEAT** (303, 130, 347, 349, 390, 111, 115, 180, 190). Antes de implementar cualquier exporter TXT: buscar el XLSX oficial, no perder tiempo en instrucciones HTML.
