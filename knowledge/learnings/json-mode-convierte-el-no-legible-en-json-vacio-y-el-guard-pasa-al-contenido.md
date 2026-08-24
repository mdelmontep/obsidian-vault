---
title: json mode convierte el «no legible» en json vacío, y el guard pasa del parse al contenido
date: 2026-08-25
source: facturaia
tags: [llm, ocr, openai, evals, guards]
---
Una extracción con `response_format: json_object` deja de narrar («no veo ninguna factura») y devuelve
JSON válido y vacío (`{"doc_type":"desconocido"}`). Si tu rama de «documento no legible» vivía en el
`catch` del `JSON.parse`, activar JSON mode la apaga sin ningún test en rojo: el JSON vacío pasa Zod y
sigue por el camino feliz (en facturaia: bandeja `listo` con el trío `missing_*` y un WhatsApp equivocado).
Medido con una foto de DNI ficticio ×3: sin flag 2/3 narración + 1/3 JSON vacío; con flag 3/3 JSON vacío.

Patrón: el «no legible» se decide por CONTENIDO (`esLecturaSinDatos`: los seis campos núcleo vacíos y
`doc_type` fuera de los tipos que legítimamente no los traen), y va DESPUÉS del bucle de auto-orientación
(un escaneo girado también da vacío la primera vez). El eval reporta siempre por qué rama pasó
(`parse` / `zod` / `vacia`): un verde sin rama es un verde que no sabes leer. Y `it.fails` no vale para un
gap conocido contra un modelo no determinista: se pone rojo el día que acierta.

Ver [[evals-de-modelo-real-oscilan-agregar-corridas-y-baseline-con-margen]] · repo: `ocr-process/__evals__/README.md` (#2180).
