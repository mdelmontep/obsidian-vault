---
title: dos series de ADR con el mismo prefijo — la cita resuelve a un documento coherente que habla de otra cosa
date: 2026-08-30
source: facturaia
tags: [adr, documentacion, facturaia, obsidian, candados]
---

`facturaia/docs/decisions/` y `obsidian-vault/decisions/` numeran igual —
`ADR-NNN` — y el código cita las dos. Seis comentarios de `services/mcp-server/`
decían «ADR-032» apuntando al del vault (AS OAuth partido, jun-2026); dos meses
después nació un `ADR-032` en el repo (albarán valorado) y esas citas pasaron a
resolver a otra decisión. **No es un enlace roto**: el lector abre un documento
válido, bien escrito, sobre otra cosa, y no tiene motivo para dudar. Un enlace
roto se ve; este no. Ya había mordido antes: `gotchas.md:349` lleva la cicatriz
del `ADR-024` de multidivisa (PR #2118).

**Libre aquí no es libre.** El primer arreglo movió el duplicado al 034 y el
candado dio verde, porque medía una sola carpeta — y el `ADR-034` del vault es
también de este proyecto. Se cambió un choque por otro, a un sitio donde nadie
mira. Acabó en 062 (31-ago). Corolario: **un candado que solo ve tu mitad del
espacio de nombres certifica lo que no puede saber.**

Y por eso el «no lee el vault porque no existe en CI» que escribí ayer era la
excusa, no el diseño: aquí NO HAY CI, así que la única máquina donde importa
correr es ésta, y en ésta el vault está. Ahora lo lee; si no lo encuentra,
degrada a comprobar que la regla escrita sigue en su sitio — y esa rama
degradada tiene su propio caso que muerde, porque es la que más se ejecuta y la
que nadie mira.

Regla: contador ÚNICO entre las series que comparten prefijo (el mayor de las dos
más uno). Una serie con prefijo propio (`ADR-obras-NNN`) no entra en el contador;
su riesgo es que se cite por elipsis.

PR #2311 · [[facturaia]] · `docs/decisions/NUMERACION.md` ·
[[el-limite-silencioso-una-respuesta-que-llega-al-tope-parece-completa]]
