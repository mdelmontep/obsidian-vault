---
title: cambiar la ruta de una máquina de estados deja varadas las filas que ya pasaron
date: 2026-08-15
source: claude-code-session
tags: [maquina-estados, deploy, backfill, migraciones]
---
Un PR mete un productor nuevo y con él cambia la RUTA: lo que antes encadenaba
`guion → producido → revision` ahora se queda esperando en `guion`. El código
nuevo es correcto para lo que venga después; el problema son las filas que
cruzaron por la ruta vieja y quedaron en un estado del que **ningún agente las
saca** — el repartidor solo mira `guion`, ellas están en `revision`, y nadie
vuelve a mirarlas nunca. No dan error: se quedan calladas.

Caso real (TuFacturaIA, 14-ago): el guionista aplicó dos carruseles a las 10:49
y el PR del productor de imagen entró a las 10:59. Diez minutos de ventana, dos
piezas muertas hasta que alguien miró el panel y preguntó «¿por qué no se ve
nada aquí?».

Regla: **cambiar una transición obliga a un backfill de las filas atrapadas en
la ruta anterior, en el MISMO PR**. Escribirlo por invariante («las que están en
X sin el artefacto Y y con el artefacto Z vuelven a W»), no por lista de ids: la
ventana sigue abierta mientras el deploy no termine. Ver
[[reparar-datos-con-la-rpc-de-dominio-arrastra-sus-efectos-de-negocio]] para
cómo hacer ese backfill sin ensuciar el dominio.
