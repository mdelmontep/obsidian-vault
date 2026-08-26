---
title: un gate cuyo denominador es la zona que sus propios candados vetan nunca abre
date: 2026-08-26
source: facturaia
tags: [agentes, gates, harness, medicion, ocr]
---
El gate agéntico abre `shadow→activo` con **≥50 decisiones de zona verde resueltas y acierto ≥95%**. Medido en prod sobre el dominio `ocr`: **328 decisiones, 241 ámbar + 87 rojo, 0 verdes**. Nunca ha habido una. Con 0 verdes el acierto es `null`, `evaluarGate` devuelve `mantener / sin_volumen_medido` y el panel dice lo mismo que diría una org que empezó ayer: "aprendiendo".

La causa no es el modelo: son los candados del propio evaluador. Sobre esas 328, y cualquiera de ellos fuerza ámbar por sí solo:

- `proveedor_no_confianza` **320** (97,6 %)
- `requiere_confirmacion_stock` **296** (90 %)
- `es_intracom` **90**

Contraste en el mismo sistema: `categorias` acumuló 112 verdes de 131 y su gate abrió solo.

Regla: en cualquier gate de promoción, medir la **distribución de motivos de bloqueo**, no el contador. "0 de N en la zona que habilita" no es aprendizaje lento, es un bloqueo estructural, y su telemetría es idéntica a la del aprendizaje lento. Ver [[gate-de-automatizacion-n50-al-95-no-sostiene-el-95-usa-cota-wilson]] (el mismo gate, por el lado del muestreo) y [[dos-castigos-por-el-mismo-evento-hacen-inalcanzable-el-estado-bueno]] (uno de los candados).
