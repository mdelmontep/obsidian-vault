---
title: busca una capacidad por su llamada, no por el módulo donde crees que vive
date: 2026-08-17
source: claude-code-session
tags: [metodo, busqueda, evidencia]
---

Afirmé dos veces en un día, en tres documentos, que «no existe ninguna ruta de borrado de
objetos». Sí existía, en otro módulo. Busqué `grep` dentro de `src/core/files/` —donde yo
esperaba que estuviera— en vez de `grep -rn "\.storage\.from" src`, que es **la llamada que
esa capacidad tiene que hacer sí o sí**.

El sesgo es fino: buscar por módulo confirma tu mapa mental del código; buscar por la llamada
lo contradice cuando toca. Y un «no existe» es una afirmación universal — no se demuestra
mirando un directorio.

Regla: para «¿existe X?», busca **el verbo del SDK / la API / la sentencia** en todo el árbol
(`.storage.from`, `.remove(`, `createSignedUrl`, `grant `, `create policy`), nunca la carpeta
donde debería estar. Si el módulo esperado no la tiene, eso responde otra pregunta —«¿está
donde yo creo?»— que no era la que hacías.

Y el daño no fue perder tiempo: fue **escribirlo en tres sitios como hecho comprobado**, lo que
convierte un mapa mental en documentación que otro cita. Ver
[[un-no-se-puede-heredado-caduca-como-cualquier-otra-frase]] y
[[el-instrumento-devuelve-cero-sin-decir-que-no-ha-medido]] — misma familia: el instrumento
contestó, contestó cero, y el cero significaba «aquí no», no «en ningún sitio».
