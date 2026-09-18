---
title: el mismo tipo de documento llega en dos familias según quién lo generó — enruta por valores, no por texto
date: 2026-09-18
source: agh-iberica
tags: [pdf, extraccion, ocr, enrutado, medicion]
---
Dos contratos laborales del mismo cliente, del mismo mes y con la misma plantilla legal **se leen de forma opuesta** según el `Producer` del PDF. Medido (AGH, piloto RRHH):

| | «Microsoft: Print To PDF» | **Docusign DMv10** |
|---|---|---|
| capa de texto | solo rótulos fijos | **421 líneas / 14.091 caracteres** |
| importes · fechas · NIF | 0 · 0 · 0 | **2 · 2 · 2** |

O sea: el primero exige visión, el segundo se lee con `pdftotext`. **Un solo ejemplar no define el tipo de documento**, define la familia de quien lo firmó.

- **Enruta preguntando por los VALORES que buscas** («¿hay candidatos a importe/fecha?»), no por «¿hay capa de texto?»: la hay en los dos, y en uno no sirve de nada.
- Antes de declarar «esto necesita OCR/visión para todos», cuenta **cuántos de cada familia** manda el cliente. Puede convertir un bloqueante universal en un caso minoritario.
- Y ojo al salto: *«el grep no encuentra el salario en el contrato»* es una **medición correcta**; *«el salario vive en el anexo»* es una **inferencia** que resultó falsa — estaba delante, vectorizado. Ver [[pdf-escaneado-sin-capa-de-texto-renderizar-paginas-con-pdftoppm]] y [[una-premisa-heredada-se-remide-antes-de-filiarla]].
