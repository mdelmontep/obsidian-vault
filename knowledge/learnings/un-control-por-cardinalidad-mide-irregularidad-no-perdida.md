---
title: un control por cardinalidad mide irregularidad, no pérdida
date: 2026-08-02
source: claude-code-session
tags: [llm, ocr, validacion, prompts, facturaia]
---
Para detectar que un LLM se dejaba una columna de códigos al leer líneas de
factura, el primer control comparaba la cardinalidad entre líneas: si unas traen
3 códigos y otras 2, algo se perdió. **Estaba invertido.** Sobre 8 pasadas dio
4 falsos positivos y 4 falsos negativos:
- un hueco legítimo (celda vacía) desiguala una fila y **dispara** la alarma;
- perder la columna entera iguala todas las filas otra vez y la **apaga**.
La cardinalidad mide irregularidad; la pérdida uniforme es regular.

Fix: cruzar **dos lecturas independientes** del propio documento — cuántas
columnas de código declara la CABECERA (campo nuevo, con instrucción explícita
de no ajustarlo a lo leído) contra el máximo de códigos por línea. 16/16 sin
falsos. Es el patrón de `num_factura` + `num_cliente`: si un dato se puede
confundir, pide los dos y crúzalos.

Dos trampas del método, no del control: en la 1ª medición el control parecía
acertar 8/8 **por casualidad** (esas pasadas perdían además un código suelto), y
se midió sobre el JSON crudo cuando producción evalúa las líneas ya saneadas.
Medir sobre el artefacto que usa prod, y con un caso donde el hueco sea legítimo.
Ver [[defensa-en-codigo-vs-prompt-llm-para-invariantes-de-dominio]].

**Confirmado en prod (02-ago)**: una pasada real que perdió una columna dejó
`refs_columna_perdida — «la cabecera declara 3 columnas y ninguna línea trae más
de 2»` en `ocr_extraction_audit`; la pasada anterior con el prompt viejo no la
tiene. Al emitirse `low` **no llega al usuario**: `review_reasons` solo se
escribe si algo fuerza revisión, así que la etiqueta de UI únicamente se pinta
cuando concurre con otra anomalía seria. Un control que solo deja rastro en el
audit es un control **para nosotros**, no para quien mira la factura.
