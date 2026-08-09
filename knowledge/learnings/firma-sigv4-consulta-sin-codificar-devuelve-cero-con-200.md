---
title: una consulta S3 sin codificar en la firma devuelve cero resultados con un 200 limpio
date: 2026-08-09
source: claude-code-session
tags: [s3, wasabi, aws, firma, gotcha]
---
Implementando SigV4 a mano contra Wasabi, `?prefix=carpeta/` devolvía **una lista vacía con
HTTP 200**. No 403, no error: vacío. Parece «no hay nada ahí» cuando en realidad los objetos
estaban.

Causa: la forma canónica de SigV4 exige la query **percent-encoded y ordenada por clave**. Al
pasarla tal cual, la firma se calcula sobre otra cadena y el servicio responde como si el
filtro no casara con nada.

Es la peor clase de fallo porque **el éxito y el fallo son indistinguibles**: si no hubiera
mirado el bucket entero sin filtro, habría concluido que la subida no funcionaba.

Regla: construir la query dentro del firmador (objeto → `encodeURIComponent` → `sort`), nunca
aceptar una cadena ya montada. Y al depurar un listado vacío en S3, listar sin filtro antes de
tocar nada más.
